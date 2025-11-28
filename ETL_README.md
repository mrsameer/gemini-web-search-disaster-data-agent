# Disaster Data Agent - ETL Integration Guide

This guide explains how to ingest data from the Disaster Data Agent into your ETL pipeline.

## API Endpoint

The agent provides a REST API endpoint to export structured disaster data as JSON.

**Endpoint:** `POST /api/export`
**URL:** `http://localhost:8000/api/export` (or your deployed host)
**Content-Type:** `application/json`

### Request Body

```json
{
  "query": "recent floods in India"
}
```

- `query`: The search query to find disaster events. Be specific for better results (e.g., include location and time).

### Response

The API returns a JSON file (`disaster_data.json`) containing a list of event objects.

**Structure:**

```json
{
  "events": [
    {
      "location": "Kerala, India",
      "date": "July 2024",
      "type": "Flood",
      "severity": "High",
      "description": "Heavy rains caused severe flooding in Wayanad district...",
      "source": "News Report"
    },
    ...
  ]
}
```

## ETL Ingestion Steps

1.  **Trigger:** Your ETL engine (e.g., Airflow, Prefect) sends a POST request to `/api/export` with a relevant query.
2.  **Extract:** Parse the returned JSON content.
3.  **Transform:** Map the fields (`location`, `date`, `type`, `severity`, `description`) to your data warehouse schema.
4.  **Load:** Insert the records into your database.

## Example (Python)

```python
import requests

url = "http://localhost:8000/api/export"
payload = {"query": "earthquakes last 24 hours"}
response = requests.post(url, json=payload)

if response.status_code == 200:
    data = response.json()
    print(f"Extracted {len(data['events'])} events.")
    # Process data['events']...
else:
    print("Error fetching data")
```
