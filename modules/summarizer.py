from enum import Enum
from typing import Dict, Any, List
import google.generativeai as genai
import os
import json # To parse the JSON output from the model
from dotenv import load_dotenv # Import load_dotenv

load_dotenv() # Load environment variables from .env file

class DataType(Enum):
    PDF = "pdf"
    TEXT = "text"
    WEB_PAGE = "web_page"

class FileInfo:
    def __init__(self, file_name: str, file_type: DataType, content: str):
        self.file_name = file_name
        self.file_type = file_type
        self.content = content

class Summarizer:
    def __init__(self, model_name: str = "gemini-pro"):
        # Configure the generative AI client
        # It's assumed that the API key is available via an environment variable (e.g., GOOGLE_API_KEY)
        genai.configure(api_key=os.environ.get("AIzaSyAyuLsi1ssM49r6qVhVBRudvJBFabzeKbo"))
        self.model = genai.GenerativeModel(model_name)

    def generate_summary(self, file_info: FileInfo) -> Dict[str, Any]:
        """
        Generates a structured summary from the given file content using the Gemini model.
        """
        prompt = f"""
        You are an expert summarizer. Your task is to analyze the provided document content
        and generate a structured summary in JSON format. The summary should include:
        1.  A concise 'title' for the document.
        2.  A 'main_summary' that provides an overview.
        3.  'study_notes' as a list of bullet points.
        4.  'important_concepts' as a dictionary where keys are concepts and values are their definitions.
        5.  'key_ideas' as a list of bullet points.

        Ensure the output is a valid JSON object.

        Document Name: {file_info.file_name}
        Document Content:
        {file_info.content}

        JSON Summary:
        """

        try:
            response = self.model.generate_content(prompt)
            # Assuming the model returns a text response that is a JSON string
            summary_json_str = response.text
            summary_dict = json.loads(summary_json_str)
            return summary_dict
        except Exception as e:
            print(f"Error generating summary: {e}")
            # Fallback to mock data or raise an error
            mock_summary = {
                "title": f"Summary of {file_info.file_name} (Error)",
                "main_summary": "Could not generate summary due to an error.",
                "study_notes": [],
                "important_concepts": {},
                "key_ideas": []
            }
            return mock_summary