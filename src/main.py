import os
from gemini_client import initialize_gemini, tailor_document_with_gemini, form_document_object
from document_classes import Resume, CoverLetter
from template_finder import locate_and_populate_document
from parser import parse_job_input, create_parser, write_file
from output_handler import process_output

def resume_tailoring(args_dict):
    """
    Creates a Resume object, populates the object with template material,
    tailors the material using API (gemini), and then replaces the tailored contents with
    the template ones, finally saves it in the designated output path

    Args:
        args_dict (dict): Dict containing the necessary arguments parsed from user input

    Returns: None
    """

    try:

        # Start Refactor
        # Step 1: Take job description, other details are already taken through args
        job_description = parse_job_input()
        job_info = {
            'job_position' : args_dict['job_position'],
            'job_description' : job_description
        }

        # Step 2: Assets discovery
        print("=== Resume Template Finder ===")
        resume = Resume()
        populated_resume_obj, folder = locate_and_populate_document(resume, args_dict['job_position'], "../latex")

        # DEBUG for document object components
        print(f"[DEBUG]\nFolder: {folder}")
        print(f"[DEBUG] Components loaded:")
        for comp_name in populated_resume_obj.get_component_names():
            comp_data = populated_resume_obj.get_component(comp_name)
            if comp_data and comp_data['content']:
                print(f"[DEBUG]  - {comp_name}: {len(comp_data['content'])} chars")
            else:
                print(f"[DEBUG]  - {comp_name}: Not found")


        print("\n" + "=" * 40)
        print("SUCCESS: Data ready for the tailoring phase.")
        print("=" * 40)

        # Step 3: Generate prompt based on the object and get response
        client = initialize_gemini()
        tailored_resume = tailor_document_with_gemini(client, job_info, populated_resume_obj) # the tailored resume should contain keys and values
        # tailored_cover_letter = generate_tailored_cover_letter(job_info, tex_content)

        print("\n" + "=" * 40)
        print("SUCCESS: Tailored content generated.")
        print(f"Sample of tailored {list(tailored_resume.keys())[0]}", tailored_resume[list(tailored_resume.keys())[0]][:100] + "...")
        print("=" * 40)

        # Step 5: Output Generation
        tailored_resume_obj = form_document_object("resume", populated_resume_obj, tailored_resume)
        # Output tailored resume to the right place
        for key, component in tailored_resume_obj.get_all_components().items():
            print(f"[DEBUG] Writing file {component['path']} ... ")
            write_file(component['path'], component['content'])

        print(f"\nYour tailored resume is ready!")
        print(f"LaTeX files: {os.path.basename(output_info['temp_folder'])}")
        print(f"PDF: {os.path.basename(output_info['pdf_path'])}")
        print(f"PDF location: {os.path.dirname(output_info['pdf_path'])}/")

    except Exception as e:
        print(f"\n[ERROR]: {e}")
    return

def cover_letter_tailoring():
    pass


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