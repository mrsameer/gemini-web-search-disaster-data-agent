from google import genai
from google.genai import types
import os
import json
from pydantic import BaseModel, Field
from typing import List, Optional

class Severity(BaseModel):
    deaths: str = Field(description="Number of deaths reported (e.g., '10', 'Unknown')")
    relocations: str = Field(description="Number of people relocated or displaced (e.g., '500', 'None')")
    level: Optional[str] = Field(description="Severity level (e.g., High, Medium, Low) for UI display")

class DisasterEvent(BaseModel):
    location: str = Field(description="The specific location of the disaster (City, Region, Country)")
    date: str = Field(description="The date of the disaster in DDMMYYYY, MMYYYY, or YYYY format")
    type: str = Field(description="The type of disaster (e.g., Earthquake, Flood, Wildfire)")
    severity: Severity = Field(description="Detailed severity information including deaths and relocations")
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
        # Retrieve label from environment variable, default to apdims-local
        owner_gemini_label = os.getenv("OWNER_GEMINI_LABEL", "apdims-local").lower()
        labels = {"owner-gemini": owner_gemini_label}

        # Step 1: Search (Text Mode)
        search_prompt = f"Search for recent natural disasters related to: '{query}'. Provide a detailed list of events found."
        
        search_response = self.client.models.generate_content(
            model=self.model_id,
            contents=search_prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                labels=labels
            )
        )
        
        if not search_response.text:
            return {"events": []}

        # Step 2: Extract (JSON Mode)
        extraction_prompt = f"""
        Analyze the following search results and extract key details for each disaster event.
        
        Search Results:
        {search_response.text}
        
        Requirements:
        1. Date must be in one of these formats: DDMMYYYY, MMYYYY, or YYYY.
        2. Severity must include 'deaths' and 'relocations' counts.
        3. Return the results as a JSON object matching the schema.
        """

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=extraction_prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=DisasterResponse,
                labels=labels
            )
        )
        
        try:
            # The response text should be a valid JSON string matching DisasterResponse
            return json.loads(response.text)
        except Exception as e:
            print(f"Error parsing response: {e}")
            return {"events": []}
