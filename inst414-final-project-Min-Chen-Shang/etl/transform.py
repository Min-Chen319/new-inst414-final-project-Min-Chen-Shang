# etl/transform.py

import pandas as pd
import numpy as np

def transform_data(data_dict):
    """
    Clean and transform raw data.
    Args:
        data_dict (dict): Dictionary containing raw dataframes with keys 'appointments' and 'cms'
    Returns:
        dict: Processed dataframes
    """
    print("Transforming datasets...")

    if "appointments" not in data_dict or "cms" not in data_dict:
        print("❌ transform_data: Missing required datasets.")
        return {}

    df_appointments = data_dict["appointments"].copy()
    df_cms = data_dict["cms"].copy()

    if df_appointments.empty:
        print("⚠️ Appointments dataset is empty.")
    if df_cms.empty:
        print("⚠️ CMS dataset is empty.")

    # --- Normalize column names ---
    df_appointments.columns = (
        df_appointments.columns
        .str.strip()
        .str.lower()
        .str.replace('-', '_')
        .str.replace(' ', '_')
    )

    # Debug: print available columns
    print("📋 Appointments columns:", list(df_appointments.columns))

    # --- Identify possible date columns for lead_time ---
    if "scheduledday" in df_appointments.columns and "appointmentday" in df_appointments.columns:
        start_col = "scheduledday"
        end_col = "appointmentday"
    elif "entry_service_date" in df_appointments.columns and "appointment_date" in df_appointments.columns:
        start_col = "entry_service_date"
        end_col = "appointment_date"
    else:
        start_col = None
        end_col = None

    # --- Calculate lead_time if possible ---
    if start_col and end_col:
        df_appointments[start_col] = pd.to_datetime(df_appointments[start_col], errors="coerce")
        df_appointments[end_col] = pd.to_datetime(df_appointments[end_col], errors="coerce")
        df_appointments["lead_time"] = (df_appointments[end_col] - df_appointments[start_col]).dt.days
    else:
        print("⚠️ Could not find date columns to calculate lead_time.")
        df_appointments["lead_time"] = pd.NA  # keep column for consistency

    # --- Map no_show column ---
    if "no_show" in df_appointments.columns:
        print("🔍 Unique values in no_show before mapping:", df_appointments["no_show"].unique())
        df_appointments["no_show"] = (
            df_appointments["no_show"]
            .astype(str)
            .str.strip()
            .str.lower()
            .map({"yes": 1, "no": 0})
        )
    else:
        print("⚠️ Missing 'no_show' column in appointments data.")
        df_appointments["no_show"] = pd.NA

    # --- Drop rows with missing no_show only ---
    missing_noshow = df_appointments["no_show"].isna().sum()
    if missing_noshow == len(df_appointments):
        print("❌ All rows have missing or invalid 'no_show' values. Stopping transformation.")
        return {}
    elif missing_noshow > 0:
        print(f"⚠️ Dropping {missing_noshow} rows due to missing 'no_show' values.")
        df_appointments.dropna(subset=["no_show"], inplace=True)

    # --- Fill missing values in features ---
    for col in df_appointments.columns:
        if col == "no_show":  # target variable 不補值
            continue
        if pd.api.types.is_numeric_dtype(df_appointments[col]):
            median_value = df_appointments[col].median()
            df_appointments[col].fillna(median_value, inplace=True)
        else:
            df_appointments[col].fillna("Unknown", inplace=True)

    print(f"✅ Transform complete. Remaining rows: {len(df_appointments)}")

    return {
        "appointments": df_appointments,
        "cms": df_cms
    }
