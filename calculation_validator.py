import duckdb
import pandas as pd
import numpy as np

# The path to your Parquet file
PARQUET_FILE_PATH = r"D:\MyPythonProjects\nq_data_2010_2025\New folder\enhanced_nq_data_full_BACKUP2_(Seconds Removed).parquet"

def weighted_moving_average(series, window):
    weights = np.arange(1, window + 1)
    return series.rolling(window).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)

def hull_moving_average(series, window):
    half = int(window / 2)
    sqrt_win = int(np.sqrt(window))
    wma_half = weighted_moving_average(series, half)
    wma_full = weighted_moving_average(series, window)
    hull = 2 * wma_half - wma_full
    return weighted_moving_average(hull, sqrt_win)

def calculate_rsi(series, window):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.ewm(alpha=1/window, min_periods=window).mean()
    avg_loss = loss.ewm(alpha=1/window, min_periods=window).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def validate_calculations():
    """
    Validates a subset of technical indicator calculations in the Parquet file.
    """
    try:
        con = duckdb.connect(database=':memory:', read_only=False)
        
        # Let's sample a specific day for our validation, e.g., '2023-01-03'
        # This makes the validation deterministic and focused.
        sample_day_query = f"SELECT * FROM read_parquet('{PARQUET_FILE_PATH}') WHERE Date = '2023-01-03'"
        
        df = con.execute(sample_day_query).fetchdf()

        if df.empty:
            print("No data found for the sample day. Please choose a different day for validation.")
            return

        print(f"Loaded {len(df)} rows for validation on 2023-01-03.")

        # --- Recalculate a few key indicators ---

        # 1. SMA_20
        df['SMA_20_recalc'] = df['Close'].rolling(window=20).mean()
        
        # 2. RSI_14
        df['RSI_14_recalc'] = calculate_rsi(df['Close'], window=14)

        # 3. HMA_7
        df['HMA_7_recalc'] = hull_moving_average(df['Close'], 7)

        # --- Compare the results ---
        
        # Select columns for comparison
        comparison_df = df[[
            'Time', 'Close', 
            'SMA_20', 'SMA_20_recalc',
            'RSI_14', 'RSI_14_recalc',
            'HMA_7', 'HMA_7_recalc'
        ]].copy()

        # Calculate the absolute difference
        comparison_df['SMA_20_diff'] = (comparison_df['SMA_20'] - comparison_df['SMA_20_recalc']).abs()
        comparison_df['RSI_14_diff'] = (comparison_df['RSI_14'] - comparison_df['RSI_14_recalc']).abs()
        comparison_df['HMA_7_diff'] = (comparison_df['HMA_7'] - comparison_df['HMA_7_recalc']).abs()

        print("\n--- Validation Results ---")
        print("Comparing original values with fresh calculations for 2023-01-03.")
        print("A small difference (e.g., < 0.01) is acceptable due to floating point nuances.")
        
        # Display a sample of the comparison, focusing on the differences
        # We'll show rows where the difference is notable, or just a sample if all is good.
        significant_diff_sma = comparison_df[comparison_df['SMA_20_diff'] > 0.01]
        significant_diff_rsi = comparison_df[comparison_df['RSI_14_diff'] > 0.01]
        significant_diff_hma = comparison_df[comparison_df['HMA_7_diff'] > 0.01]

        if not significant_diff_sma.empty:
            print("\nFound significant differences in SMA_20 calculation:")
            print(significant_diff_sma)
        else:
            print("\nSMA_20 calculations look consistent.")

        if not significant_diff_rsi.empty:
            print("\nFound significant differences in RSI_14 calculation:")
            print(significant_diff_rsi)
        else:
            print("\nRSI_14 calculations look consistent.")

        if not significant_diff_hma.empty:
            print("\nFound significant differences in HMA_7 calculation:")
            print(significant_diff_hma)
        else:
            print("\nHMA_7 calculations look consistent.")

        print("\n--- Sample Comparison Data ---")
        # Show the last 10 rows of the comparison dataframe to give a feel for the numbers
        print(comparison_df.tail(10))


    except Exception as e:
        print(f"An error occurred during validation: {e}")

    finally:
        if 'con' in locals():
            con.close()

if __name__ == "__main__":
    validate_calculations()
