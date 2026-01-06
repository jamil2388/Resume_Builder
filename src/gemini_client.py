from google import genai

import os
import json
from dotenv import load_dotenv


def initialize_gemini():
    """Configures Gemini once for the session."""
    # Load variables from .env file
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    # DEBUG PRINTS
    if not api_key:
        print("[DEBUG] API Key is empty or None!")
    else:
        # Prints first 4 and last 4 chars to verify without exposing the whole key
        print(f"[DEBUG] API Key found: {api_key[:4]}...{api_key[-4:]}")
    
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Check your .env file.")

    client = genai.Client(api_key=api_key)
    
    return client


def tailor_with_gemini(client, job_info, extracted_content):
    """
    Feeds JD and LaTeX content to Gemini and returns tailored LaTeX strings.
    """
    
    # Constructing the prompt
    prompt = f"""
    You are an expert resume writer and LaTeX specialist. 
    TASK: Tailor the following LaTeX resume sections to better align with the Job Description (JD).
    
    JOB POSITION: {job_info['job_position']}
    JOB DESCRIPTION:
    {job_info['job_description']}

    ORIGINAL LATEX EXPERIENCE:
    {extracted_content['experience']['raw']}

    ORIGINAL LATEX SKILLS:
    {extracted_content['skills']['raw']}

    INSTRUCTIONS:
    1. Rephrase experience bullet points to highlight JD keywords.
    2. Update the skills section to prioritize technologies mentioned in the JD.
    3. STRICT RULE: Maintain all LaTeX commands, environments (itemize, etc.), and special characters.
    4. RETURN ONLY A JSON OBJECT with keys "experience" and "skills". No conversational filler.
    """

    # print(f"propagated client : {client}")
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    
    # Cleaning the response to ensure it's valid JSON
    clean_text = response.text.replace('```json', '').replace('```', '').strip()
    return json.loads(clean_text)