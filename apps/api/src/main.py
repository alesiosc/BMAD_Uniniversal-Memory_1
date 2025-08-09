import os
import duckdb
import pandas as pd
import numpy as np
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .core.config import settings

# --- Configuration ---
app = FastAPI()
PARQUET_FILE_PATH = r"enhanced_nq_data_corrected.parquet"

if settings.GOOGLE_API_KEY:
    genai.configure(api_key=settings.GOOGLE_API_KEY)
else:
    print("Error: GOOGLE_API_KEY not found in .env file.")

# --- Data Schema ---
def get_schema():
    """Reads the Parquet file and returns a string description of its schema."""
    try:
        con = duckdb.connect(database=':memory:', read_only=False)
        schema_df = con.execute(f"DESCRIBE SELECT * FROM read_parquet('{PARQUET_FILE_PATH}');").fetchdf()
        con.close()
        return "\n".join([f"- {row['column_name']} ({row['column_type']})" for _, row in schema_df.iterrows()])
    except Exception as e:
        print(f"Error getting schema: {e}")
        return None

SCHEMA_DESCRIPTION = get_schema()

# --- AI Prompting ---
def construct_prompt(user_query, schema):
    """Constructs a detailed, few-shot prompt for the Gemini API."""
    return f"""
You are a world-class data analyst who can write expert-level, efficient DuckDB-compatible SQL queries.
Your task is to translate a user's natural language question into a precise SQL query.

**Parquet File Schema:**
{schema}

**Important Notes:**
- The table name is `read_parquet('{PARQUET_FILE_PATH}')`.
- Column names with special characters (e.g., '/') must be in double quotes (e.g., `"RTH/ETH"`).
- "Points" or "points move" refers to the difference between two price columns (e.g., `(High - Low)` or `(Close - Open)`). This should be calculated directly in the SQL query; do not assume a 'points_move' column exists.
- For queries about the "nth" bar of a session, use the `ROW_NUMBER()` window function and filter with the `QUALIFY` clause for maximum efficiency.

**Golden Standard Examples:**

User Question: "How many times between March 2022 and September 2022 does the 2nd bar in RTH exceed 8 points?"
SQL Query:
SELECT COUNT(*)
FROM read_parquet('{PARQUET_FILE_PATH}')
WHERE "RTH/ETH" = 'RTH'
  AND "Date" >= '2022-03-01'
  AND "Date" <= '2022-09-30'
QUALIFY ROW_NUMBER() OVER (PARTITION BY "Date" ORDER BY "Time") = 2
  AND (High - Low) > 8;

User Question: "What is the average points move of the fourth RTH bar when the 1st bar is more than 12 points and the 3rd bar is less than 3 points?"
SQL Query:
WITH DailyBars AS (
    SELECT
        "Date",
        (High - Low) AS points_move,
        ROW_NUMBER() OVER (PARTITION BY "Date" ORDER BY "Time") AS bar_num
    FROM read_parquet('{PARQUET_FILE_PATH}')
    WHERE "RTH/ETH" = 'RTH'
),
FilteredDays AS (
    SELECT "Date"
    FROM DailyBars
    WHERE (bar_num = 1 AND points_move > 12) OR (bar_num = 3 AND points_move < 3)
    GROUP BY "Date"
    HAVING COUNT(*) = 2
)
SELECT AVG(db.points_move)
FROM DailyBars db
JOIN FilteredDays fd ON db."Date" = fd."Date"
WHERE db.bar_num = 4;

**User's Question:**
{user_query}

**SQL Query:**
"""

# --- API Endpoints ---
class AIQueryRequest(BaseModel):
    question: str

@app.post("/ai-query/")
async def ai_query(request: AIQueryRequest):
    """
    Takes a natural language question, translates it to SQL using Gemini,
    executes it with DuckDB, and returns the result.
    """
    if not settings.GOOGLE_API_KEY:
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY is not configured on the server.")
    if not SCHEMA_DESCRIPTION:
        raise HTTPException(status_code=500, detail="Could not retrieve data schema.")

    prompt = construct_prompt(request.question, SCHEMA_DESCRIPTION)
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = await model.generate_content_async(prompt)
        sql_query = response.text.strip().replace("```sql", "").replace("```", "")

        print(f"Generated SQL: {sql_query}")

        con = duckdb.connect(database=':memory:', read_only=False)
        result_df = con.execute(sql_query).fetchdf()
        con.close()
        
        # Replace NaN/inf with None for JSON compatibility
        result_df.replace([np.inf, -np.inf], np.nan, inplace=True)
        
        # Check for empty or all-NaN results
        if result_df.empty or result_df.isnull().all().all():
            return {"result": "No data found for this query."}
            
        result_df = result_df.where(pd.notna(result_df), None)
        
        return result_df.to_dict(orient="records")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/validate-query/")
def validate_query(request: AIQueryRequest):
    """
    Independently validates a query using pure pandas logic.
    """
    try:
        df = pd.read_parquet(PARQUET_FILE_PATH)
        
        if "2nd bar in RTH exceed 8 points" in request.question:
            df['Date'] = pd.to_datetime(df['Date'])
            start_date = pd.to_datetime('2022-03-01')
            end_date = pd.to_datetime('2022-09-30')
            
            filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date) & (df['RTH/ETH'] == 'RTH')].copy()
            second_bars = filtered_df.groupby('Date').nth(1)
            exceeds_8_points = second_bars[(second_bars['High'] - second_bars['Low']) > 8]
            count = len(exceeds_8_points)
            
            return {"manual_validation_count": count}
        else:
            return {"error": "This query is not supported by the manual validator yet."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during validation: {str(e)}")

@app.get("/")
def read_root():
    return {"status": "API is running", "data_schema_loaded": SCHEMA_DESCRIPTION is not None}
