from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options={'api_version': 'v1'}
)

def get_embedding(text: str):
    try:
        # text-embedding-004 is the 2026 stable standard
        result = client.models.embed_content(
            model="text-embedding-004",
            contents=text
        )
        return result.embeddings[0].values
    except Exception as e:
        print(f"Embedding Error: {e}")
        return [0.0] * 768

def generate_match_reason(resume_text, job_requirements):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"In one sentence, why does this resume match these requirements? {job_requirements}. Resume: {resume_text}"
        )
        return response.text.strip()
    except:
        return "Match analysis ready for review."