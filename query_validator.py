import pandas as pd

# Path to the corrected Parquet file
PARQUET_FILE_PATH = "enhanced_nq_data_corrected.parquet"

def validate_query_manually():
    """
    Independently validates the AI's query using pure pandas logic.
    """
    try:
        print("Starting manual validation...")
        df = pd.read_parquet(PARQUET_FILE_PATH)
        print(f"Loaded {len(df)} rows.")

        # --- Re-implement the query logic in pandas ---

        # 1. Filter for the date range and RTH
        df['Date'] = pd.to_datetime(df['Date'])
        start_date = pd.to_datetime('2022-03-01')
        end_date = pd.to_datetime('2022-09-30')
        
        filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date) & (df['RTH/ETH'] == 'RTH')].copy()
        print(f"Found {len(filtered_df)} RTH bars in the date range.")

        # 2. Find the 2nd bar of each day
        # We group by date and then take the second element of each group
        second_bars = filtered_df.groupby('Date').nth(1) # nth(1) gets the 2nd row (0-indexed)
        
        print(f"Found {len(second_bars)} days with at least 2 RTH bars.")

        # 3. Check if the 2nd bar's range exceeds 8 points
        exceeds_8_points = second_bars[(second_bars['High'] - second_bars['Low']) > 8]
        
        count = len(exceeds_8_points)

        print("\n--- Manual Validation Result ---")
        print(f"The number of times the 2nd RTH bar exceeded 8 points is: {count}")

    except Exception as e:
        print(f"An error occurred during manual validation: {e}")

if __name__ == "__main__":
    validate_query_manually()