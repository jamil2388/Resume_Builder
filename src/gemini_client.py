from google import genai

import os
import json
from dotenv import load_dotenv
from document_classes import Resume, CoverLetter


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


def tailor_document_with_gemini(client, job_info, document_obj):
    """
    Feeds JD and LaTeX content to Gemini and returns tailored LaTeX strings.
    Works with both Resume and CoverLetter objects.

    Args:
        client: Gemini API client
        job_info (dict): Job position and job description
        document_obj: Instance of Resume or CoverLetter with populated components

    Returns:
        dict: Dictionary with component names as keys and tailored LaTeX as values
    """
    # Extract component content from document
    component_content = _extract_component_content(document_obj)

    # Build appropriate prompt based on document type
    if isinstance(document_obj, Resume):
        prompt = _build_resume_prompt(job_info, component_content)
    elif isinstance(document_obj, CoverLetter):
        prompt = _build_cover_letter_prompt(job_info, component_content)
    else:
        raise TypeError("document_obj must be Resume or CoverLetter")

    # Call Gemini API
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

    # Parse and return
    return _parse_gemini_response(response.text)


def _extract_component_content(document_obj):
    """
    Extracts content from all components in the document.

    Args:
        document_obj: Instance of Resume or CoverLetter

    Returns:
        dict: Component names mapped to their content
    """
    content = {}

    for component_name in document_obj.get_component_names():
        comp_data = document_obj.get_component(component_name)
        if comp_data and comp_data['content']:
            content[component_name] = comp_data['content']
        else:
            content[component_name] = None

    return content


def _build_resume_prompt(job_info, component_content):
    """
    Builds tailoring prompt for Resume.

    Args:
        job_info (dict): Job position and description
        component_content (dict): Component names to content mapping

    Returns:
        str: Prompt for Gemini
    """
    prompt = f"""
    You are an expert resume writer and LaTeX specialist.
    TASK: Tailor the following LaTeX resume sections to better align with the Job Description (JD).
    
    JOB POSITION: {job_info['job_position']}
    
    JOB DESCRIPTION:
    {job_info['job_description']}
    
    ORIGINAL LATEX SECTIONS:
    """

    for component_name in component_content.keys():
        # Add each component that has content
        # e.g., prompt += f"\n--- EXPERIENCE ---\n{component_content['experience']}\n"
        print(f"[DEBUG]\n--- {str(component_name).upper()} ---\n{component_content[component_name]}")
        prompt += f"\n--- {str(component_name).upper()} ---\n{component_content[component_name]}"


    prompt += """
    INSTRUCTIONS:
    1. Rephrase experience bullet points to highlight JD keywords and relevant accomplishments.
    2. Update the technologies section to prioritize technologies mentioned in the JD.
    3. STRICT RULE: Maintain all LaTeX commands, environments (itemize, section, etc.), and special characters.
    4. Keep the structure and formatting identical to the original.
    5. RETURN ONLY A JSON OBJECT with keys matching the section names: "experience" and "technologies".
    6. No conversational filler, explanations, or markdown code blocks.
    
    OUTPUT FORMAT:
    {
        "experience": "tailored LaTeX content here",
        "technologies": "tailored LaTeX content here"
    }
    """

    return prompt


def _build_cover_letter_prompt(job_info, component_content):
    """
    Builds tailoring prompt for Cover Letter.

    Args:
        job_info (dict): Job position and description
        component_content (dict): Component names to content mapping

    Returns:
        str: Prompt for Gemini
    """
    prompt = f"""
    You are an expert cover letter writer and LaTeX specialist.
    TASK: Tailor the following LaTeX cover letter sections to better align with the Job Description (JD).
    
    JOB POSITION: {job_info['job_position']}
    
    JOB DESCRIPTION:
    {job_info['job_description']}
    
    ORIGINAL LATEX SECTIONS:
    """

    # Add each component that has content
    for component_name in ['date', 'body']:
        prompt += f"\n--- {component_name.upper()} ---\n{component_content[component_name]}\n"

    prompt += """
    INSTRUCTIONS:
    1. Tailor the body to highlight relevant experience and skills from the JD.
    2. Update date to current or remove if template-based.
    3. STRICT RULE: Maintain all LaTeX commands, environments, and special characters.
    4. Keep the structure and formatting identical to the original.
    5. RETURN ONLY A JSON OBJECT with keys: "date", "body".
    6. No conversational filler, explanations, or markdown code blocks.
    
    OUTPUT FORMAT:
    {
        "date": "LaTeX content",
        "body": "tailored LaTeX content here"
    }
    """

    return prompt


def _parse_gemini_response(response_text):
    """
    Parses Gemini's response text into a dictionary.
    Handles markdown code blocks and JSON parsing.

    Args:
        response_text (str): Raw response from Gemini

    Returns:
        dict: Parsed JSON response
    """
    # Clean up markdown code blocks
    clean_text = response_text.replace('```json', '').replace('```', '').strip()

    try:
        return json.loads(clean_text)
    except json.JSONDecodeError as e:
        print("[ERROR] Failed to parse Gemini response as JSON")
        print(f"Response preview: {clean_text[:200]}")
        raise ValueError(f"Invalid JSON response from Gemini: {e}")


# --- Test ---
if __name__ == "__main__":
    from document_classes import Resume

    # Mock setup
    resume = Resume()
    resume.set_component('experience', '../latex/resume/Resume_Jamil_DA/experience.tex', '\\section{Experience}\n\\item Did stuff')
    resume.set_component('technologies', '../latex/resume/Resume_Jamil_DA/technologies.tex', '\\section{Technologies}\n\\item Python')

    job_info = {
        'job_position': 'ML',
        'job_description': 'Looking for ML engineer with PyTorch experience...'
    }

    # Test prompt building
    content = _extract_component_content(resume)
    prompt = _build_resume_prompt(job_info, content)

    print("=== Generated Prompt ===")
    print(prompt[:500])
