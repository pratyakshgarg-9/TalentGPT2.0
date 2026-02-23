from google import genai
import os, json, re
from dotenv import load_dotenv

# load_dotenv()

# # Force the API version to 'v1' to avoid the v1beta 404 error
# client = genai.Client(
#     api_key=os.getenv("GEMINI_API_KEY"),
#     http_options={'api_version': 'v1'}
# )

# def create_custom_quiz(requirements, hr_questions):
#     # Use the stable 2.5 Flash model for 2026
#     model_id = "gemini-2.5-flash" 
    
#     prompt = f"Create 3 MCQ technical questions for: {requirements}. HR focus: {hr_questions}. Return ONLY a raw JSON array."
    
#     try:
#         response = client.models.generate_content(model=model_id, contents=prompt)
#         # Robust JSON extraction
#         match = re.search(r'\[.*\]', response.text, re.DOTALL)
#         if match:
#             return json.loads(match.group(0))
#         return json.loads(response.text.strip())
#     except Exception as e:
#         print(f"FIXED AI ERROR: {e}") 
#         return [{"question": "System update in progress. Describe your experience.", "options": [], "answer": ""}]
import re
import json
client = genai.Client(
     api_key=os.getenv("GEMINI_API_KEY"),
     http_options={'api_version': 'v1'}
 )

def create_custom_quiz(requirements, hr_questions):
    model_id = "gemini-2.5-flash" 
    # Force the AI to use your job-specific requirements
    prompt = f"""
    Based on these specific job requirements: {requirements}. 
    And these HR focus points: {hr_questions}.
    Create 3 technical MCQ questions.
    Return ONLY a raw JSON array of objects with this structure:
    [
      {{
        "question": "The question text",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "answer": "The exact string of the correct option"
      }}
    ]
    Do not include markdown formatting or backticks.
    """
    
    try:
        response = client.models.generate_content(model=model_id, contents=prompt)
        # Remove potential markdown backticks that crash json.loads
        clean_text = re.sub(r'```json|```', '', response.text).strip()
        
        match = re.search(r'\[.*\]', clean_text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        return json.loads(clean_text)
    except Exception as e:
        print(f"Error: {e}") 
        # Emergency fallback if AI fails
        return [{"question": "Technical Check: Define the primary goal of this role.", "options": ["Execution", "Planning", "Optimization", "All of the above"], "answer": "All of the above"}]