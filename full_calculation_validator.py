import duckdb
import pandas as pd
import numpy as np

# The path to your Parquet file
PARQUET_FILE_PATH = r"D:\MyPythonProjects\nq_data_2010_2025\New folder\enhanced_nq_data_full_BACKUP2_(Seconds Removed).parquet"

# --- Re-implementation of Technical Indicator Calculations ---

def calculate_sma(series, window):
    return series.rolling(window=window).mean()

def calculate_bbands(series, window=20):
    sma = series.rolling(window=window).mean()
    std = series.rolling(window=window).std()
    upper = sma + (std * 2)
    lower = sma - (std * 2)
    return sma, upper, lower

def calculate_rsi(series, window=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.ewm(com=window - 1, min_periods=window).mean()
    avg_loss = loss.ewm(com=window - 1, min_periods=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(series, span1=12, span2=26, signal=9):
    ema1 = series.ewm(span=span1, adjust=False).mean()
    ema2 = series.ewm(span=span2, adjust=False).mean()
    macd = ema1 - ema2
    macd_signal = macd.ewm(span=signal, adjust=False).mean()
    return macd, macd_signal

def calculate_obv(close, volume):
    signed_volume = volume * np.sign(close.diff())
    return signed_volume.cumsum()

def validate_all_calculations():
    """
    Validates all major technical indicator calculations in the Parquet file.
    """
    try:
        con = duckdb.connect(database=':memory:', read_only=False)
        
        # Load a larger sample of data (e.g., one week) to handle look-back periods
        sample_query = f"SELECT * FROM read_parquet('{PARQUET_FILE_PATH}') WHERE Date >= '2023-01-01' AND Date <= '2023-07-20'"
        
        df = con.execute(sample_query).fetchdf()

        if df.empty:
            print("No data found for the sample date range. Please choose a different range.")
            return

        print(f"Loaded {len(df)} rows for validation from 2023-01-01 to 2023-01-07.")

        # --- Recalculate all major indicators ---
        df['SMA_20_recalc'] = calculate_sma(df['Close'], 20)
        df['BB_Mid_recalc'], df['BB_Upper_recalc'], df['BB_Lower_recalc'] = calculate_bbands(df['Close'])
        df['RSI_14_recalc'] = calculate_rsi(df['Close'], 14)
        df['MACD_recalc'], df['MACD_Signal_recalc'] = calculate_macd(df['Close'])
        df['OBV_recalc'] = calculate_obv(df['Close'], df['Volume'])
        df['O-C_Diff_recalc'] = df['Close'] - df['Open']
        df['C-C_Diff_recalc'] = df['Close'].diff()

        # --- Compare and Report ---
        indicators_to_check = {
            "SMA_20": "SMA_20_recalc",
            "BB_Mid": "BB_Mid_recalc",
            "BB_Upper": "BB_Upper_recalc",
            "BB_Lower": "BB_Lower_recalc",
            "RSI_14": "RSI_14_recalc",
            "MACD": "MACD_recalc",
            "MACD_Signal": "MACD_Signal_recalc",
            "OBV": "OBV_recalc",
            "O-C_Diff": "O-C_Diff_recalc",
            "C-C_Diff": "C-C_Diff_recalc"
        }

        print("\n--- Full Validation Results ---")
        all_consistent = True
        for original, recalc in indicators_to_check.items():
            # Use a fillna approach to handle NaNs consistently before comparison
            diff = (df[original].fillna(0) - df[recalc].fillna(0)).abs()
            
            if (diff > 0.01).any():
                all_consistent = False
                print(f"\n[WARNING] Found significant differences in '{original}' calculation.")
                comparison_df = df[[original, recalc]].copy()
                comparison_df['diff'] = diff
                print(comparison_df[comparison_df['diff'] > 0.01].tail())
            else:
                print(f"\n[OK] '{original}' calculations look consistent.")
        
        if all_consistent:
            print("\nConclusion: All validated indicator calculations appear to be correct.")
        else:
            print("\nConclusion: Some indicator calculations show discrepancies. Please review the warnings above.")


    except Exception as e:
        print(f"An error occurred during validation: {e}")

    finally:
        if 'con' in locals():
            con.close()

if __name__ == "__main__":
    validate_all_calculations()
