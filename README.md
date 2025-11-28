# Gemini Web Search Disaster Data Agent

A real-time disaster monitoring application powered by **Google Gemini** with **Search Grounding**. This agent fetches, structures, and displays natural disaster information from across the web.

## 🚀 Features

- **Real-time Search**: Finds the latest disaster events (earthquakes, floods, wildfires, etc.) using Google Search.
- **Structured Data**: Uses Gemini to extract key details (Location, Date, Type, Severity, Description) into JSON.
- **Modern UI**: A premium, dark-themed React application for visualizing results.
- **ETL Integration**: API endpoint to export data for ingestion into data pipelines.

## 🛠️ Prerequisites

- Python 3.9+
- Node.js 18+
- Google Cloud Project with Vertex AI enabled (or Gemini API Key)

## 📦 Setup

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the root directory:

```env
GOOGLE_APPLICATION_CREDENTIALS=gemini-api-key.json
```

### 2. Frontend Setup

```bash
cd frontend
npm install
```

## 🏃‍♂️ Running the Application

### Start the Backend

```bash
# From the root directory
uvicorn backend.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.
Swagger UI: `http://localhost:8000/docs`

### Start the Frontend

```bash
# From the frontend directory
npm run dev
```

Open your browser to `http://localhost:5173`.

## 🖥️ Using the Web UI

1.  Enter a query in the search bar (e.g., "recent earthquakes in Japan", "floods in Brazil 2024").
2.  View the structured results in the grid.
3.  Click **"Export JSON"** to download the data.

## 🔄 ETL Integration Guide

The agent provides a REST API endpoint to export structured disaster data as JSON for your ETL pipeline.

**Endpoint:** `POST /api/export`
**URL:** `http://localhost:8000/api/export`
**Content-Type:** `application/json`

### Request Body

```json
{
  "query": "recent floods in India"
}
```

### Response

The API returns a JSON file containing a list of event objects.

```json
{
  "events": [
    {
      "location": "Kerala, India",
      "date": "July 2024",
      "type": "Flood",
      "severity": "High",
      "description": "Heavy rains caused severe flooding...",
      "source": "News Report"
    }
  ]
}
```

### Example (Python)

```python
import requests

url = "http://localhost:8000/api/export"
payload = {"query": "earthquakes last 24 hours"}
response = requests.post(url, json=payload)

if response.status_code == 200:
    data = response.json()
    print(f"Extracted {len(data['events'])} events.")
else:
    print("Error fetching data")
```
