import google.generativeai as genai
import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv # Import load_dotenv

load_dotenv() # Load environment variables from .env file

class QuizGeneratorMCQ:
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        genai.configure(api_key=os.environ.get("AIzaSyAyuLsi1ssM49r6qVhVBRudvJBFabzeKbo"))
        self.model = genai.GenerativeModel(model_name)

    def generate_mcq_quiz(self, document_content: str, num_questions: int = 5) -> List[Dict[str, Any]]:
        """
        Generates multiple-choice questions (MCQs) from the given document content.
        """
        prompt = f"""
        You are an expert in creating multiple-choice questions (MCQs) from text.
        Generate {num_questions} MCQs based on the following document content.
        Each question should have 4 options (A, B, C, D) and a single correct answer.
        The output must be a JSON array of objects, where each object represents one MCQ.
        Each MCQ object should have the following structure:
        {{
            "question": "The question text",
            "options": {{
                "A": "Option A text",
                "B": "Option B text",
                "C": "Option C text",
                "D": "Option D text"
            }},
            "correct_answer": "B" (or A, C, D)
        }}

        Ensure the output is a valid JSON array.

        Document Content:
        {document_content}

        JSON MCQs:
        """

        try:
            response = self.model.generate_content(prompt)
            quiz_json_str = response.text
            # Attempt to clean up common issues with JSON responses from LLMs
            # Sometimes models return extra text or markdown code blocks
            if quiz_json_str.startswith("```json"):
                quiz_json_str = quiz_json_str[len("```json"):].strip()
            if quiz_json_str.endswith("```"):
                quiz_json_str = quiz_json_str[:-len("```")].strip()

            mcq_quiz = json.loads(quiz_json_str)
            return mcq_quiz
        except Exception as e:
            print(f"Error generating MCQ quiz: {e}")
            return [] # Return an empty list on error
