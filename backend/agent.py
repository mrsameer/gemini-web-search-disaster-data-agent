from google import genai
from google.genai import types
import os
import json
from pydantic import BaseModel, Field
from typing import List, Optional

class DisasterEvent(BaseModel):
    location: str = Field(description="The specific location of the disaster (City, Region, Country)")
    date: str = Field(description="The date or timeframe of the disaster")
    type: str = Field(description="The type of disaster (e.g., Earthquake, Flood, Wildfire)")
    severity: Optional[str] = Field(description="Severity or magnitude of the disaster if available")
    description: str = Field(description="A brief summary of what happened")
    source: str = Field(description="The source of the information")

class DisasterResponse(BaseModel):
    events: List[DisasterEvent]

class DisasterAgent:
    def __init__(self):
        # The SDK will automatically pick up GOOGLE_APPLICATION_CREDENTIALS from env
        self.client = genai.Client(vertexai=True, location="asia-south1")
        self.model_id = "gemini-2.5-flash"

    def search_and_extract(self, query: str) -> dict:
        prompt = f"""
        Search for recent natural disasters related to: '{query}'.
        Extract key details for each event found.
        Return the results as a JSON object with a list of events.
        """

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                response_mime_type="application/json",
                response_schema=DisasterResponse
            )
        )
        
        try:
            # The response text should be a valid JSON string matching DisasterResponse
            return json.loads(response.text)
        except Exception as e:
            print(f"Error parsing response: {e}")
            return {"events": []}
