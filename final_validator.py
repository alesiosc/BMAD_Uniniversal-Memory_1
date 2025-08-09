import duckdb
import pandas as pd
import numpy as np
from tqdm import tqdm

# The path to your Parquet file
PARQUET_FILE_PATH = r"D:\MyPythonProjects\nq_data_2010_2025\New folder\enhanced_nq_data_full_BACKUP2_(Seconds Removed).parquet"

# --- In-House Technical Indicator Calculations ---

def calculate_vwap(df, period='1D'):
    """Calculates VWAP for a given period (1D, 1W, 1M)."""
    df = df.copy()
    df['TypicalPrice_x_Volume'] = ((df['High'] + df['Low'] + df['Close']) / 3) * df['Volume']
    
    if period == '1D':
        grouper = df['Date']
    elif period == '2D':
        # Create a grouper for 2-day periods
        date_series = pd.to_datetime(df['Date']).dt.to_period('D').astype(int)
        grouper = date_series // 2
    elif period == '1W':
        grouper = pd.to_datetime(df['Date']).dt.to_period('W')
    elif period == '1M':
        grouper = pd.to_datetime(df['Date']).dt.to_period('M')
    else:
        raise ValueError("Period must be one of '1D', '2D', '1W', '1M'")
        
    df['CumulativeVolume'] = df.groupby(grouper)['Volume'].cumsum()
    df['Cumulative_TPxV'] = df.groupby(grouper)['TypicalPrice_x_Volume'].cumsum()
    
    vwap = df['Cumulative_TPxV'] / df['CumulativeVolume']
    return vwap.ffill()

def calculate_volume_profile(df, n_bins=50, pct=0.7):
    """Calculates POC, VAH, and VAL for a given DataFrame."""
    if df.empty:
        return np.nan, np.nan, np.nan
    price_range = np.linspace(df['Low'].min(), df['High'].max(), n_bins + 1)
    df['price_bin'] = pd.cut(df['Close'], bins=price_range, labels=False, include_lowest=True)
    
    volume_by_bin = df.groupby('price_bin')['Volume'].sum()
    
    if volume_by_bin.empty:
        return np.nan, np.nan, np.nan

    poc_bin_index = volume_by_bin.idxmax()
    # Correctly calculate the midpoint of the POC bin
    poc = price_range[int(poc_bin_index)] + (price_range[1] - price_range[0]) / 2

    total_volume = df['Volume'].sum()
    
    sorted_bins = volume_by_bin.sort_values(ascending=False)
    
    value_area_volume = 0
    value_area_bins = []
    
    for bin_idx, volume in sorted_bins.items():
        if value_area_volume >= total_volume * pct:
            break
        value_area_bins.append(bin_idx)
        value_area_volume += volume
        
    if not value_area_bins:
        return poc, np.nan, np.nan

    min_bin = min(value_area_bins)
    max_bin = max(value_area_bins)
    
    val = price_range[int(min_bin)]
    vah = price_range[int(max_bin) + 1]
    
    return poc, vah, val

def validate_final_indicators():
    """
    Validates VWAP and Volume Profile indicators.
    """
    try:
        con = duckdb.connect(database=':memory:', read_only=False)
        
        sample_query = f"SELECT * FROM read_parquet('{PARQUET_FILE_PATH}') WHERE Date >= '2023-01-03' AND Date <= '2023-01-10'"
        df = con.execute(sample_query).fetchdf()

        if df.empty:
            print("No data found for the sample date range.")
            return

        print(f"Loaded {len(df)} rows for validation.")

        # --- Recalculate VWAP ---
        df['VWAP_1D_recalc'] = calculate_vwap(df, '1D')
        
        # --- Recalculate Volume Profile (for a single session to test logic) ---
        rth_df = df[(df['RTH/ETH'] == 'RTH') & (df['Date'] == '2023-01-03')].copy()
        poc_recalc, vah_recalc, val_recalc = calculate_volume_profile(rth_df)
        
        # --- Compare and Report ---
        print("\n--- Final Validation Results ---")
        
        # VWAP Comparison
        df['VWAP_1D_diff'] = (df['VWAP_1D'].fillna(0) - df['VWAP_1D_recalc'].fillna(0)).abs()
        if (df['VWAP_1D_diff'] > 0.01).any():
            print("\n[WARNING] Found significant differences in 'VWAP_1D' calculation.")
            print(df[['Date', 'Time', 'VWAP_1D', 'VWAP_1D_recalc', 'VWAP_1D_diff']][df['VWAP_1D_diff'] > 0.01].tail())
        else:
            print("\n[OK] 'VWAP_1D' calculations look consistent.")
            
        # Volume Profile Comparison
        print("\n--- Volume Profile Spot Check (2023-01-03 RTH) ---")
        
        spot_check_df = df[(df['Date'] == '2023-01-03') & (df['RTH/ETH'] == 'RTH')]

        if not spot_check_df.empty:
            # CORRECTED: Use .iloc[0] to get the first scalar value from the Series
            original_poc = spot_check_df['POC_1_RTH'].iloc[0]
            original_vah = spot_check_df['VAH_1_RTH'].iloc[0]
            original_val = spot_check_df['VAL_1_RTH'].iloc[0]

            print(f"Original POC: {original_poc:.2f}, VAH: {original_vah:.2f}, VAL: {original_val:.2f}")
            print(f"Recalculated POC: {poc_recalc:.2f}, VAH: {vah_recalc:.2f}, VAL: {val_recalc:.2f}")

            # A small tolerance for comparison
            poc_diff = abs(original_poc - poc_recalc)
            vah_diff = abs(original_vah - vah_recalc)
            val_diff = abs(original_val - val_recalc)

            if poc_diff > 1.0 or vah_diff > 1.0 or val_diff > 1.0:
                 print("\n[WARNING] Volume Profile calculations show significant differences.")
            else:
                 print("\n[OK] Volume Profile calculations appear consistent.")
        else:
            print("\n[INFO] No RTH data found for 2023-01-03 to perform Volume Profile spot check.")

    except Exception as e:
        print(f"An error occurred during validation: {e}")

    finally:
        if 'con' in locals():
            con.close()

if __name__ == "__main__":
    validate_final_indicators()