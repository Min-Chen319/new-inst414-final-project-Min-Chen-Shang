# etl/transform.py

def transform_data(data_dict):
    """
    Clean and transform raw data.
    Args:
        data_dict (dict): Dictionary containing raw dataframes with keys 'appointments' and 'cms'
    Returns:
        dict: Processed dataframes
    """
    import pandas as pd

    print("Transforming datasets...")

    df_appointments = data_dict["appointments"].copy()
    df_cms = data_dict["cms"].copy()

    # --- Appointments Cleaning ---
    df_appointments.columns = df_appointments.columns.str.strip().str.lower().str.replace('-', '_')

    df_appointments['scheduledday'] = pd.to_datetime(df_appointments['scheduledday'], errors='coerce')
    df_appointments['appointmentday'] = pd.to_datetime(df_appointments['appointmentday'], errors='coerce')
    df_appointments['lead_time'] = (df_appointments['appointmentday'] - df_appointments['scheduledday']).dt.days

    df_appointments['no_show'] = df_appointments['no_show'].map({'Yes': 1, 'No': 0})

    # Optional: drop or fill missing values
    df_appointments.dropna(subset=['lead_time', 'no_show'], inplace=True)

    print("Transform complete.")

    return {
        "appointments": df_appointments,
        "cms": df_cms
    }
#