import os
from gemini_client import initialize_gemini, tailor_with_gemini
from template_finder import locate_template_assets, extract_tex_contents
from parser import parse_job_input

def get_job_context():
    """Step 1: Parse the input text file for JD and Position."""
    print("Reading job_description.txt...")
    job_data = parse_job_input("../docs/job_description.txt")
    
    print(f"Target Position: {job_data['job_position']}")
    print(f"JD Length: {len(job_data['job_description'])} characters")
    return job_data

def get_latex_assets(position):
    """Step 2: Find the template folder and file paths."""
    print("\nLocating LaTeX templates...")
    assets = locate_template_assets(position)
    
    print(f"Match found in folder: {os.path.basename(assets['folder_root'])}")
    print(f"Exp file: {os.path.basename(assets['experience']) if assets['experience'] else 'Not Found'}")
    print(f"Skills file: {os.path.basename(assets['skills']) if assets['skills'] else 'Not Found'}")
    return assets

def get_raw_content(assets):
    """Step 3: Extract text from the identified .tex files."""
    print("\nExtracting LaTeX content...")
    extracted = extract_tex_contents(assets)
    
    # Printing Snippets for verification
    if extracted["experience"]["raw"]:
        print(f"Experience Loaded: {len(extracted['experience']['raw'])} chars")
    if extracted["skills"]["raw"]:
        print(f"Skills Loaded: {len(extracted['skills']['raw'])} chars")
        
    return extracted

def generate_tailored_content(job_info, tex_content):
    """Step 4: Communicate with Gemini API."""
    client = initialize_gemini()
    tailored_data = tailor_with_gemini(client, job_info, tex_content)
    
    print("Tailoring complete. Received updated Experience and Skills.")
    return tailored_data

def main():
    print("--- Starting Resume Tailoring Workflow ---")
    try:
        # Step 1: Input
        job_info = get_job_context()
        
        # Step 2: Discovery
        assets = get_latex_assets(job_info['job_position'])
        
        # Step 3: Extraction
        tex_content = get_raw_content(assets)

        print("\n" + "="*40)
        print("SUCCESS: Data ready for the tailoring phase.")
        print("="*40)

        # New Step: The AI Brain
        tailored_content = generate_tailored_content(job_info, tex_content)

        print("\n" + "="*40)
        print("SUCCESS: Tailored content generated.")
        print("Sample of tailored Exp:", tailored_content['experience'][:100] + "...")
        print("="*40)

    except Exception as e:
        print(f"\n[ERROR]: {e}")

if __name__ == "__main__":
    main()