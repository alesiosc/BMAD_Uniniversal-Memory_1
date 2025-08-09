import duckdb
import pandas as pd

# The path to your Parquet file
# Using a raw string (r"...") to handle backslashes in Windows paths correctly
parquet_file_path = r"D:\MyPythonProjects\nq_data_2010_2025\New folder\enhanced_nq_data_full_BACKUP2_(Seconds Removed).parquet"

try:
    # Connect to an in-memory DuckDB database
    con = duckdb.connect(database=':memory:', read_only=False)
    
    # Query the Parquet file schema directly
    schema_query = f"DESCRIBE SELECT * FROM '{parquet_file_path}';"
    
    print(f"Reading schema from: {parquet_file_path}")
    
    # Execute the describe query and fetch the result as a Pandas DataFrame
    schema_df = con.execute(schema_query).fetchdf()
    
    print("\nParquet File Schema:")
    print(schema_df)
    
    # Optional: Print the first 5 rows to inspect the data
    print("\nFirst 5 rows of data:")
    sample_df = con.execute(f"SELECT * FROM '{parquet_file_path}' LIMIT 5;").fetchdf()
    print(sample_df)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the database connection
    if 'con' in locals():
        con.close()
