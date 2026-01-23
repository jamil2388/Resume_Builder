import os
from gemini_client import initialize_gemini, tailor_document_with_gemini
from document_classes import Resume, CoverLetter
from template_finder import locate_and_populate_document
from parser import parse_job_input, create_parser
from output_handler import process_output

def resume_tailoring(args_dict):
    try:

        # Start Refactor
        # Step 1: Take job description, other details are already taken through args
        job_description = parse_job_input()

        # Step 2: Assets discovery
        print("=== Resume Template Finder ===")
        resume = Resume()
        populated_resume, folder = locate_and_populate_document(resume, args_dict['job_position'], "../latex")

        print(f"\nFolder: {folder}")
        print(f"Components loaded:")
        for comp_name in populated_resume.get_component_names():
            comp_data = populated_resume.get_component(comp_name)
            if comp_data and comp_data['content']:
                print(f"  - {comp_name}: {len(comp_data['content'])} chars")
            else:
                print(f"  - {comp_name}: Not found")

        # Step 3: Extraction
        tex_content = get_raw_content(assets)

        print("\n" + "=" * 40)
        print("SUCCESS: Data ready for the tailoring phase.")
        print("=" * 40)

        # Step 4: The AI Brain
        tailored_resume = generate_tailored_resume(job_description, tex_content)
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
    return

def cover_letter_tailoring():
    return

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

    args_dict = {
        'job_position' : args.job_position,
        'job_description' : args.job_description,
        'tailor_resume' : args.resume,
        'tailor_cover_letter' : args.cover_letter
    }

    if args_dict['tailor_resume']:
        print("--- Starting Resume Tailoring Workflow ---")
        resume_tailoring(args_dict)

    if args_dict['tailor_cover_letter']:
        print("--- Starting Cover Letter Tailoring Workflow ---")
        cover_letter_tailoring(args_dict)


if __name__ == "__main__":
    main()