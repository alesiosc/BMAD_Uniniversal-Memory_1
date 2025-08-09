import duckdb
import pandas as pd
import numpy as np
from tqdm import tqdm

# The path to your Parquet file
PARQUET_FILE_PATH = r"D:\MyPythonProjects\nq_data_2010_2025\New folder\enhanced_nq_data_full_BACKUP2_(Seconds Removed).parquet"

# --- Independent, From-Scratch Technical Indicator Calculations ---

def calculate_vwap_independent(df, period='1D'):
    """Calculates VWAP using only pandas, for a given period."""
    df = df.copy()
    df['TypicalPrice_x_Volume'] = ((df['High'] + df['Low'] + df['Close']) / 3) * df['Volume']
    
    if period == '1D':
        grouper = pd.to_datetime(df['Date']).dt.date
    else:
        raise ValueError("This independent validator currently supports '1D' VWAP.")
        
    df['CumulativeVolume'] = df.groupby(grouper)['Volume'].cumsum()
    df['Cumulative_TPxV'] = df.groupby(grouper)['TypicalPrice_x_Volume'].cumsum()
    
    vwap = df['Cumulative_TPxV'] / df['CumulativeVolume']
    return vwap.ffill()

def calculate_volume_profile_independent(session_df, n_bins=50, pct=0.7):
    """Calculates POC, VAH, and VAL from scratch for a given session DataFrame."""
    if session_df.empty or session_df['Volume'].sum() == 0:
        return np.nan, np.nan, np.nan

    # 1. Determine the price range and create bins
    price_min = session_df['Low'].min()
    price_max = session_df['High'].max()
    price_range = np.linspace(price_min, price_max, n_bins + 1)
    
    # 2. Assign each row's close price to a bin
    session_df['price_bin'] = pd.cut(session_df['Close'], bins=price_range, labels=False, include_lowest=True)
    
    # 3. Aggregate volume for each price bin
    volume_by_bin = session_df.groupby('price_bin')['Volume'].sum()
    
    # 4. Find the Point of Control (POC)
    poc_bin_index = volume_by_bin.idxmax()
    # Corrected POC calculation to find the midpoint of the bin
    poc = price_range[int(poc_bin_index)] + (price_range[1] - price_range[0]) / 2

    # 5. Calculate the Value Area (VAH and VAL)
    total_volume = session_df['Volume'].sum()
    target_va_volume = total_volume * pct
    
    # Start from the POC and expand outwards
    sorted_by_price = volume_by_bin.sort_index()
    
    # Find the bin with the POC
    poc_bin_series_index = sorted_by_price.index.get_loc(poc_bin_index)
    
    # Expand outwards from the POC to find the Value Area
    lower_bound_idx = poc_bin_series_index
    upper_bound_idx = poc_bin_series_index
    current_volume = sorted_by_price.iloc[poc_bin_series_index]

    while current_volume < target_va_volume:
        # Check which side to expand to next
        vol_below = sorted_by_price.iloc[lower_bound_idx - 1] if lower_bound_idx > 0 else 0
        vol_above = sorted_by_price.iloc[upper_bound_idx + 1] if upper_bound_idx < len(sorted_by_price) - 1 else 0

        if vol_below > vol_above:
            lower_bound_idx -= 1
            current_volume += vol_below
        elif vol_above > 0:
            upper_bound_idx += 1
            current_volume += vol_above
        else: # Break if we can't expand further
            break

    val = price_range[int(sorted_by_price.index[lower_bound_idx])]
    vah = price_range[int(sorted_by_price.index[upper_bound_idx]) + 1]
    
    return poc, vah, val

def run_independent_validation():
    """
    Runs a full, independent validation of VWAP and Volume Profile indicators.
    """
    try:
        con = duckdb.connect(database=':memory:', read_only=False)
        
        # Load a 200-day sample
        sample_query = f"SELECT * FROM read_parquet('{PARQUET_FILE_PATH}') WHERE Date >= '2023-01-01' AND Date <= '2023-07-20'"
        df = con.execute(sample_query).fetchdf()

        if df.empty:
            print("No data found for the sample date range.")
            return

        print(f"Loaded {len(df)} rows for validation.")

        # --- Independent VWAP Validation ---
        df['VWAP_1D_recalc'] = calculate_vwap_independent(df, '1D')
        df['VWAP_1D_diff'] = (df['VWAP_1D'].fillna(0) - df['VWAP_1D_recalc'].fillna(0)).abs()
        
        print("\n--- VWAP Validation ---")
        if (df['VWAP_1D_diff'] > 0.01).any():
            print("[WARNING] VWAP_1D calculations show discrepancies.")
        else:
            print("[OK] VWAP_1D calculations are consistent.")

        # --- Independent Volume Profile Validation ---
        print("\n--- Volume Profile Validation (Spot Check on 2023-01-03 RTH) ---")
        
        # Isolate a single session for a clean test
        session_to_test = df[(df['Date'] == '2023-01-03') & (df['RTH/ETH'] == 'RTH')].copy()
        
        if not session_to_test.empty:
            # Get original values - CORRECTED aS PER INSTRUCTIONS
            original_poc = session_to_test['POC_1_RTH'].iloc[0]
            original_vah = session_to_test['VAH_1_RTH'].iloc[0]
            original_val = session_to_test['VAL_1_RTH'].iloc[0]

            # Recalculate from scratch
            poc_recalc, vah_recalc, val_recalc = calculate_volume_profile_independent(session_to_test)
            
            print(f"Original POC: {original_poc:.2f}, VAH: {original_vah:.2f}, VAL: {original_val:.2f}")
            print(f"Recalculated POC: {poc_recalc:.2f}, VAH: {vah_recalc:.2f}, VAL: {val_recalc:.2f}")

            poc_diff = abs(original_poc - poc_recalc)
            vah_diff = abs(original_vah - vah_recalc)
            val_diff = abs(original_val - val_recalc)

            # Using a tolerance of 1 point for these complex calculations
            if poc_diff > 1.0 or vah_diff > 1.0 or val_diff > 1.0:
                 print("[WARNING] Volume Profile calculations show significant differences.")
            else:
                 print("[OK] Volume Profile calculations appear consistent.")
        else:
            print("[INFO] No RTH data for 2023-01-03 to perform spot check.")

    except Exception as e:
        print(f"An error occurred during validation: {e}")

    finally:
        if 'con' in locals():
            con.close()

if __name__ == "__main__":
    run_independent_validation()