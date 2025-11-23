import google.generativeai as genai
import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv # Import load_dotenv

load_dotenv() # Load environment variables from .env file

class QuizGeneratorMixed:
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        genai.configure(api_key=os.environ.get("AIzaSyAyuLsi1ssM49r6qVhVBRudvJBFabzeKbo"))
        self.model = genai.GenerativeModel(model_name)

    def generate_mixed_quiz(self, document_content: str, num_mcq: int = 3, num_tf: int = 2, num_sa: int = 1) -> Dict[str, Any]:
        """
        Generates a mixed quiz with MCQs, True/False, and Short-answer questions from the given document content.
        """
        prompt = f"""
        You are an expert in creating diverse quizzes from text.
        Generate a mixed quiz consisting of:
        - {num_mcq} Multiple-Choice Questions (MCQ)
        - {num_tf} True/False questions
        - {num_sa} Short-Answer questions

        All questions should be based on the provided document content.
        The output must be a single JSON object with three keys: "mcqs", "true_false", and "short_answers".

        **MCQ Format (inside the "mcqs" array):**
        Each MCQ object should have:
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

        **True/False Format (inside the "true_false" array):**
        Each True/False object should have:
        {{
            "question": "The statement to be judged True or False",
            "answer": "True" (or "False")
        }}

        **Short Answer Format (inside the "short_answers" array):</b>
        Each Short Answer object should have:
        {{
            "question": "The short answer question",
            "required_keywords": ["keyword1", "keyword2", ...]
        }}
        For short answer questions, provide a list of keywords that should be present in a correct answer.

        Ensure the entire output is a single, valid JSON object.

        Document Content:
        {document_content}

        JSON Mixed Quiz:
        """

        try:
            response = self.model.generate_content(prompt)
            quiz_json_str = response.text
            # Attempt to clean up common issues with JSON responses from LLMs
            if quiz_json_str.startswith("```json"):
                quiz_json_str = quiz_json_str[len("```json"):].strip()
            if quiz_json_str.endswith("```"):
                quiz_json_str = quiz_json_str[:-len("```")].strip()
            
            mixed_quiz = json.loads(quiz_json_str)
            return mixed_quiz
        except Exception as e:
            print(f"Error generating mixed quiz: {e}")
            return {"mcqs": [], "true_false": [], "short_answers": []} # Return empty structure on error
