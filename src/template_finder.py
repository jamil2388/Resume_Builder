import os
from document_classes import Resume, CoverLetter


def find_template_folder(document_obj, job_position, base_latex_path="../latex"):
    """
    Finds the template folder matching the job position.

    Args:
        document_obj: Instance of Resume or CoverLetter
        job_position (str): Job position abbreviation (e.g., 'ML', 'DA')
        base_latex_path (str): Base path to latex templates

    Returns:
        str: Absolute path to the template folder
    """
    doc_type_path = _get_document_type_path(document_obj, base_latex_path)

    jp_lower = job_position.lower()
    all_folders = [d for d in os.listdir(doc_type_path)
                   if os.path.isdir(os.path.join(doc_type_path, d))]

    target_folder_name = next((f for f in all_folders if jp_lower in f.lower()), None)

    if not target_folder_name:
        raise FileNotFoundError(
            f"No template folder found matching position: {job_position} in {doc_type_path}"
        )

    folder_path = os.path.abspath(os.path.join(doc_type_path, target_folder_name))
    print(f" Found template folder: {target_folder_name}")

    return folder_path


def find_component_file(folder_path, component_name):
    """
    Finds the .tex file for a given component.

    Args:
        folder_path (str): Path to the template folder
        component_name (str): Name of the component

    Returns:
        str or None: Path to the file if found, None otherwise
    """
    file_path = os.path.join(folder_path, f"{component_name}.tex")

    if os.path.exists(file_path):
        return file_path

    return None


def read_component_file(file_path):
    """
    Reads the content of a .tex file.

    Args:
        file_path (str): Path to the .tex file

    Returns:
        str or None: File content or None if error
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"  ✗ Error reading {file_path}: {e}")
        return None


def populate_document(document_obj, folder_path):
    """
    Populates all components in the document object with file paths and content.

    Args:
        document_obj: Instance of Resume or CoverLetter
        folder_path (str): Path to the template folder

    Returns:
        None (modifies document_obj in place)
    """
    for component_name in document_obj.get_component_names():
        file_path = find_component_file(folder_path, component_name)

        if file_path:
            content = read_component_file(file_path)
            document_obj.set_component(component_name, file_path, content)
            print(f"   Loaded: {component_name}.tex")
        else:
            print(f"   Not found: {component_name}.tex")


def locate_and_populate_document(document_obj, job_position, base_latex_path="../latex"):
    """
    Complete workflow: finds template folder and populates document object.

    Args:
        document_obj: Instance of Resume or CoverLetter
        job_position (str): Job position abbreviation
        base_latex_path (str): Base path to latex templates

    Returns:
        tuple: (populated document object, folder_path)
    """
    doc_type = "Resume" if isinstance(document_obj, Resume) else "Cover Letter"
    print(f"[INFO] Searching for {doc_type} template...")

    folder_path = find_template_folder(document_obj, job_position, base_latex_path)
    populate_document(document_obj, folder_path)

    return document_obj, folder_path


def _get_document_type_path(document_obj, base_latex_path):
    """
    Determines the document type path (resume or cover_letter).

    Args:
        document_obj: Instance of Resume or CoverLetter
        base_latex_path (str): Base path to latex templates

    Returns:
        str: Path to document type folder
    """
    if isinstance(document_obj, Resume):
        return os.path.join(base_latex_path, "resume")
    elif isinstance(document_obj, CoverLetter):
        return os.path.join(base_latex_path, "cover_letter")
    else:
        raise TypeError("document_obj must be an instance of Resume or CoverLetter")


# --- Test ---
if __name__ == "__main__":
    try:
        print("=== Testing Resume Template Finder ===")
        resume = Resume()
        populated_resume, folder = locate_and_populate_document(resume, "ML", "../latex")

        print(f"\nFolder: {folder}")
        print(f"Components loaded:")
        for comp_name in populated_resume.get_component_names():
            comp_data = populated_resume.get_component(comp_name)
            if comp_data and comp_data['content']:
                print(f"  - {comp_name}: {len(comp_data['content'])} chars")
            else:
                print(f"  - {comp_name}: Not found")

        print("\n=== Testing CoverLetter Template Finder ===")
        try:
            cover_letter = CoverLetter()
            populated_cl, cl_folder = locate_and_populate_document(cover_letter, "ML", "../latex")
            print(f"CoverLetter folder: {cl_folder}")
        except FileNotFoundError as e:
            print(f"CoverLetter test skipped: {e}")

    except Exception as e:
        print(f"Error: {e}")