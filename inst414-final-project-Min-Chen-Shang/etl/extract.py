# etl/extract.py – Extract datasets from source locations

import pandas as pd
import os

def clean_column_names(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df

def extract_data():
    print("Extracting datasets...")

    extracted_dir = os.path.join("data", "extracted")
    processed_dir = os.path.join("data", "processed")
    os.makedirs(extracted_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)

    appointments_path = os.path.join(extracted_dir, "appointments.csv")
    cms_path = os.path.join(extracted_dir, "cms_data.csv")

    if not os.path.exists(appointments_path):
        print(f"appointments.csv not found, please put it in {extracted_dir}")
        return None
    if not os.path.exists(cms_path):
        print(f"cms_data.csv not found, please put it in {extracted_dir}")
        return None

    # Read appointments data
    df_appointments = pd.read_csv(appointments_path)
    df_appointments = clean_column_names(df_appointments)

    # Process CMS data in chunks
    print("Processing CMS data (filtering Maryland data in batches)...")
    chunksize = 100000
    cms_filtered_chunks = []

    # Field Mapping: Actual Name -> Analysis Criteria Name
    rename_map = {
        'rndrng_npi': 'npi',
        'rndrng_prvdr_state_abrvtn': 'state',
        'rndrng_prvdr_type': 'provider_type',
        'tot_srvcs': 'total_claim_count'
    }

    # The actual field name to use (from the source file)
    columns_needed = list(rename_map.keys())

    try:
        for chunk in pd.read_csv(cms_path, chunksize=chunksize, usecols=columns_needed, low_memory=False):
            chunk = clean_column_names(chunk)
            if not all(col in chunk.columns for col in columns_needed):
                print("Error: Some fields are missing, please check if cms_data.csv is correct")
                print(f"Actual field: {chunk.columns.tolist()}")
                return None

            # Filter Maryland data
            filtered = chunk[chunk['rndrng_prvdr_state_abrvtn'] == 'MD']
            filtered.rename(columns=rename_map, inplace=True)
            cms_filtered_chunks.append(filtered)

        df_cms_md = pd.concat(cms_filtered_chunks, ignore_index=True)

        cms_md_path = os.path.join(processed_dir, "cms_md_filtered.csv")
        df_cms_md.to_csv(cms_md_path, index=False)

        print(f"Extract completed, CMS (MD only) has been saved to {cms_md_path}")
        return {
            "appointments": df_appointments,
            "cms": df_cms_md
        }

    except Exception as e:
        print(f"Extract error: {e}")
        return None
#