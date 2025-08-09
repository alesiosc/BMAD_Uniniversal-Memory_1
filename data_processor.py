import duckdb
import pandas as pd
import numpy as np
from tqdm import tqdm

# Configure tqdm to work well with pandas apply
tqdm.pandas()

# Input and Output file paths
INPUT_PARQUET_PATH = r"D:\MyPythonProjects\nq_data_2010_2025\New folder\enhanced_nq_data_full_BACKUP2_(Seconds Removed).parquet"
OUTPUT_PARQUET_PATH = "enhanced_nq_data_corrected.parquet"

# --- From-Scratch Technical Indicator Calculations (Validated Logic) ---

def calculate_volume_profile(session_df, n_bins=50, pct=0.7):
    """Calculates POC, VAH, and VAL from scratch for a given single-session DataFrame."""
    if session_df.empty or session_df['Volume'].sum() == 0:
        return pd.Series({'POC': np.nan, 'VAH': np.nan, 'VAL': np.nan})

    price_min = session_df['Low'].min()
    price_max = session_df['High'].max()
    
    if price_min == price_max:
        return pd.Series({'POC': price_min, 'VAH': price_min, 'VAL': price_min})

    price_range = np.linspace(price_min, price_max, n_bins + 1)
    
    session_df['price_bin'] = pd.cut(session_df['Close'], bins=price_range, labels=False, include_lowest=True)
    volume_by_bin = session_df.groupby('price_bin')['Volume'].sum()
    
    if volume_by_bin.empty:
        return pd.Series({'POC': np.nan, 'VAH': np.nan, 'VAL': np.nan})

    poc_bin_index = volume_by_bin.idxmax()
    poc = price_range[int(poc_bin_index)] + (price_range - price_range) / 2

    total_volume = session_df['Volume'].sum()
    target_va_volume = total_volume * pct
    
    sorted_by_price = volume_by_bin.sort_index()
    poc_bin_series_index = sorted_by_price.index.get_loc(poc_bin_index)
    
    lower_bound_idx = poc_bin_series_index
    upper_bound_idx = poc_bin_series_index
    current_volume = sorted_by_price.iloc[poc_bin_series_index]

    while current_volume < target_va_volume:
        vol_below = sorted_by_price.iloc[lower_bound_idx - 1] if lower_bound_idx > 0 else 0
        vol_above = sorted_by_price.iloc[upper_bound_idx + 1] if upper_bound_idx < len(sorted_by_price) - 1 else 0

        if vol_below == 0 and vol_above == 0: break
        if vol_below > vol_above:
            lower_bound_idx -= 1
            current_volume += vol_below
        else:
            upper_bound_idx += 1
            current_volume += vol_above

    val = price_range[int(sorted_by_price.index[lower_bound_idx])]
    vah = price_range[int(sorted_by_price.index[upper_bound_idx]) + 1]
    
    return pd.Series({'POC': poc, 'VAH': vah, 'VAL': val})

def calculate_static_volume_profile(df, window_days, session_type):
    """Calculates a rolling, multi-day volume profile."""
    session_df = df[df['RTH/ETH'] == session_type].copy()
    session_df['Date'] = pd.to_datetime(session_df['Date'])
    
    # This is a complex operation, so we will process it day by day
    all_dates = sorted(session_df['Date'].unique())
    profile_results = []

    for i in tqdm(range(len(all_dates)), desc=f"Calculating {window_days}-day {session_type} Profile"):
        current_date = all_dates[i]
        # Get the window of data for the calculation
        start_date = current_date - pd.Timedelta(days=window_days - 1)
        window_df = session_df[(session_df['Date'] >= start_date) & (session_df['Date'] <= current_date)]
        
        # Calculate the profile for this window
        profile = calculate_volume_profile(window_df)
        
        # Assign the calculated profile to all rows of the current date
        date_rows = session_df[session_df['Date'] == current_date]
        for idx in date_rows.index:
            profile_results.append({'Index': idx, 'POC': profile['POC'], 'VAH': profile['VAH'], 'VAL': profile['VAL']})

    return pd.DataFrame(profile_results).set_index('Index')


def reprocess_data():
    """
    Reads the existing Parquet file, drops and recalculates ALL Volume Profile columns,
    and saves a new, corrected Parquet file.
    """
    try:
        print(f"Reading data from: {INPUT_PARQUET_PATH}")
        df = pd.read_parquet(INPUT_PARQUET_PATH)
        print(f"Loaded {len(df)} rows.")

        # --- Drop all incorrect profile columns ---
        cols_to_drop = [col for col in df.columns if 'POC' in col or 'VAH' in col or 'VAL' in col]
        if cols_to_drop:
            df.drop(columns=cols_to_drop, inplace=True)
            print(f"Dropped the following columns: {cols_to_drop}")

        # --- Recalculate RTH Profile ---
        print("Recalculating 1-day RTH Volume Profiles...")
        rth_profiles = df[df['RTH/ETH'] == 'RTH'].groupby('Date').progress_apply(calculate_volume_profile)
        rth_profiles.rename(columns={'POC': 'POC_1_RTH', 'VAH': 'VAH_1_RTH', 'VAL': 'VAL_1_RTH'}, inplace=True)
        df = df.merge(rth_profiles, on='Date', how='left')
        print("RTH profiles recalculated.")

        # --- Recalculate ETH Profiles ---
        eth5_profiles = calculate_static_volume_profile(df, 5, 'ETH')
        eth5_profiles.rename(columns={'POC': 'POC_5_ETH', 'VAH': 'VAH_5_ETH', 'VAL': 'VAL_5_ETH'}, inplace=True)
        df = df.merge(eth5_profiles, left_index=True, right_index=True, how='left')
        print("5-day ETH profiles recalculated.")

        eth21_profiles = calculate_static_volume_profile(df, 21, 'ETH')
        eth21_profiles.rename(columns={'POC': 'POC_21_ETH', 'VAH': 'VAH_21_ETH', 'VAL': 'VAL_21_ETH'}, inplace=True)
        df = df.merge(eth21_profiles, left_index=True, right_index=True, how='left')
        print("21-day ETH profiles recalculated.")

        # Forward-fill the profile values within each session
        profile_cols = [col for col in df.columns if 'POC' in col or 'VAH' in col or 'VAL' in col]
        df[profile_cols] = df.groupby('Date')[profile_cols].ffill().bfill()

        # --- Save the corrected data ---
        print(f"\nSaving corrected data to: {OUTPUT_PARQUET_PATH}")
        df.to_parquet(OUTPUT_PARQUET_PATH, index=False)
        print("Successfully saved the corrected Parquet file.")
        
        # --- Final Verification ---
        print("\nPerforming a final spot-check on the new file...")
        con = duckdb.connect(database=':memory:', read_only=False)
        corrected_df = con.execute(f"SELECT POC_1_RTH, VAH_1_RTH, VAL_1_RTH, POC_5_ETH, VAH_5_ETH, VAL_5_ETH FROM read_parquet('{OUTPUT_PARQUET_PATH}') WHERE Date = '2023-01-03' AND \"RTH/ETH\" = 'RTH' LIMIT 1").fetchdf()
        
        print("\nSpot check for 2023-01-03 in the new file:")
        print(corrected_df)
        con.close()

    except Exception as e:
        print(f"An error occurred during data reprocessing: {e}")

if __name__ == "__main__":
    reprocess_data()
