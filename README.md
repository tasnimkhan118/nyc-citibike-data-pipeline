# NYC Citi Bike: Real-Time Data Engineering Pipeline

[![NYC Citi Bike Dashboard](./dashboard_preview.png)](https://datastudio.google.com/reporting/7de0a043-f3fc-4002-b47e-0c79e998d294)
*Note: Click the image above to view the interactive dashboard. Data is currently updated via manual backend execution.*

## Project Overview

This project is an end-to-end data pipeline designed to monitor the live status of the NYC Citi Bike system. It transforms JSON data from the **General Bikeshare Feed Specification (GBFS)** into an interactive dashboard.

---

## Stack

* **Language:** Python (Extraction & ETL)
* **Data Warehouse:** Google BigQuery
* **Visualization:** Looker Studio (Data Studio)
* **SQL Logic:** Advanced Window Functions (`ROW_NUMBER()`, `PARTITION BY`)

---

## Data Architecture

1.  **Extraction:** A Python script polls the Citi Bike GBFS API to capture real-time station status, including bike availability, e-bike counts, and dock capacity.
2.  **Load:** Data is appended to a "Live Status" table in **BigQuery**, preserving historical records for future time-series analysis.
3.  **Transformation (Deduplication):** To ensure the dashboard only shows the current state of the city, I created a **BigQuery SQL View**. This view uses ranking logic to isolate the single most recent record for every individual station:
    ```sql
    SELECT *
    FROM (
      SELECT *,
             ROW_NUMBER() OVER (PARTITION BY name ORDER BY last_reported DESC) as row_num
      FROM `citi-bike-pipeline.citi_bike_data.live_status`
    )
    WHERE row_num = 1
    ```
4.  **Visualization:** The deduplicated snapshot is put into **Looker Studio**, to create a geospatial bubble map and real-time scorecards displaying current E-Bike counts at any given station(s) selected.

---

## Key Insights

* **Identification of New High Volume Stations:** Identified high-traffic bike stations such as **E 40 St & 5 Ave**, which features **85+ docks**, significantly surpassing the 79-dock superstation records established in 2019.
* **Operational Monitoring:** Integrated `is_renting` status to distinguish between active stations and those currently out of service for maintenance.

---

## Future Plan

* **Full Automation:** Transitioning the Python ETL to **Google Cloud Functions** and **Cloud Scheduler** for 24/7 automated updates.
* **Geospatial Expansion:** Adapting the pipeline to include **Chicago Divvy** data to compare urban mobility patterns between New York and Chicago.
* **Predictive Analysis:** Utilizing the accumulated historical data in BigQuery to build a machine learning model that forecasts station "fullness" trends.

---

## How to Run

1. Execute the `citi_bike_pipeline.py` script to fetch current API data and push to BigQuery.
2. The BigQuery View `latest_snapshot` automatically updates to include the new records.
3. Refresh the **Looker Studio** report to visualize the latest system status.
