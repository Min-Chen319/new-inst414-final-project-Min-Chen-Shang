# etl/load.py

import os

def load_data(data_dict):
    """
    Save the cleaned data to data/processed/.
    Args:
        data_dict (dict): Dictionary with keys 'appointments' and 'cms', each a cleaned DataFrame.
    """
    processed_dir = os.path.join("data", "processed")
    os.makedirs(processed_dir, exist_ok=True)

    appointments_path = os.path.join(processed_dir, "appointments_clean.csv")
    cms_path = os.path.join(processed_dir, "cms_md_filtered.csv")

    data_dict["appointments"].to_csv(appointments_path, index=False)
    data_dict["cms"].to_csv(cms_path, index=False)

    print("Clean data saved to data/processed/")
#