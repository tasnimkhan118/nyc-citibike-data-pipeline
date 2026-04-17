import requests
import pandas as pd
from google.colab import auth
import pandas_gbq

# --- CONFIGURATION ---
PROJECT_ID = 'citi-bike-pipeline'
DATASET_ID = 'citi_bike_data'
TABLE_ID = f"{DATASET_ID}.live_status"

def run_pipeline():
    # 1. EXTRACTION
    status_url = "https://gbfs.citibikenyc.com/gbfs/en/station_status.json"
    info_url = "https://gbfs.citibikenyc.com/gbfs/en/station_information.json"
    
    status_data = requests.get(status_url).json()['data']['stations']
    info_data = requests.get(info_url).json()['data']['stations']
    
    # 2. TRANSFORMATION (Cleaning & Merging)
    df_status = pd.DataFrame(status_data)[['station_id', 'num_bikes_available', 'num_ebikes_available', 'num_docks_available', 'last_reported']]
    df_info = pd.DataFrame(info_data)[['station_id', 'name', 'lat', 'lon']]
    
    # Merge & Convert Time
    df = pd.merge(df_status, df_info, on='station_id')
    df['last_reported'] = pd.to_datetime(df['last_reported'], unit='s')
    
    # 3. LOADING (To BigQuery)
    auth.authenticate_user()
    pandas_gbq.to_gbq(df, TABLE_ID, project_id=PROJECT_ID, if_exists='append')
    print(f"Successfully appended {len(df)} rows to {TABLE_ID}")

if __name__ == "__main__":
    run_pipeline()
