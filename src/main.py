import os
from gemini_client import initialize_gemini, tailor_with_gemini
from template_finder import locate_and_populate_document
from parser import parse_job_input, create_parser
from output_handler import process_output



def generate_tailored_resume(job_info, tex_content):
    """Step 4: Communicate with Gemini API."""
    client = initialize_gemini()
    tailored_data = tailor_with_gemini(client, job_info, tex_content)

    print("Tailoring complete. Received updated Experience and Skills.")
    return tailored_data

def generate_tailored_cover_letter(job_info, tex_content):
    """Step 4: Communicate with Gemini API to generate the Cover Letter"""
    client = initialize_gemini()
    tailored_data = tailor_with_gemini(client, job_info, tex_content)

    print("Tailoring complete. Received updated Cover Letter.")
    return tailored_data


def main():

    args = create_parser()

    print("--- Starting Resume Tailoring Workflow ---")
    try:

        # Start Refactor
        # Step 1: Input
        job_info = get_job_context()

        # Step 2: Discovery
        assets = get_latex_assets(job_info['job_position'])

        # Step 3: Extraction
        tex_content = get_raw_content(assets)

        print("\n" + "=" * 40)
        print("SUCCESS: Data ready for the tailoring phase.")
        print("=" * 40)

        # Step 4: The AI Brain
        tailored_resume = generate_tailored_resume(job_info, tex_content)
        # tailored_cover_letter = generate_tailored_cover_letter(job_info, tex_content)

        print("\n" + "=" * 40)
        print("SUCCESS: Tailored content generated.")
        print("Sample of tailored Exp:", tailored_resume['experience'][:100] + "...")
        print("=" * 40)

        # Step 5: Output Generation - NEW!
        output_info = process_output(assets, tailored_resume)

        print(f"\nYour tailored resume is ready!")
        print(f"LaTeX files: {os.path.basename(output_info['temp_folder'])}")
        print(f"PDF: {os.path.basename(output_info['pdf_path'])}")
        print(f"PDF location: {os.path.dirname(output_info['pdf_path'])}/")

    except Exception as e:
        print(f"\n[ERROR]: {e}")


if __name__ == "__main__":
    main()