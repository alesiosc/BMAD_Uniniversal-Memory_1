import duckdb
import pandas as pd

# The path to your Parquet file
PARQUET_FILE_PATH = r"D:\MyPythonProjects\nq_data_2010_2025\New folder\enhanced_nq_data_full_BACKUP2_(Seconds Removed).parquet"
OUTPUT_CSV_PATH = "rth_sample_2023-01-03.csv"

def extract_rth_sample():
    """
    Extracts a single RTH session to a CSV file for manual verification.
    """
    try:
        con = duckdb.connect(database=':memory:', read_only=False)
        
        # Isolate the specific RTH session
        sample_query = f"SELECT Date, Time, Open, High, Low, Close, Volume FROM read_parquet('{PARQUET_FILE_PATH}') WHERE Date = '2023-01-03' AND \"RTH/ETH\" = 'RTH'"
        
        df = con.execute(sample_query).fetchdf()

        if df.empty:
            print("No data found for the sample RTH session.")
            return

        # Save the sample to a CSV file
        df.to_csv(OUTPUT_CSV_PATH, index=False)
        
        print(f"\nSuccessfully extracted {len(df)} rows for the RTH session of 2023-01-03.")
        print(f"Sample data saved to: {OUTPUT_CSV_PATH}")
        print("\nYou can now use this CSV file with an independent, third-party Volume Profile calculator to establish a trusted baseline.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if 'con' in locals():
            con.close()

if __name__ == "__main__":
    extract_rth_sample()