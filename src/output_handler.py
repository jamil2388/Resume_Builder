import os
import shutil
import subprocess
from pathlib import Path


def find_or_create_temp_folder(base_folder_path, create_temp_folder = True):
    """
    Finds or creates a Temp version of the base template folder.

    Args:
        base_folder_path (str): Path to the base template folder (e.g., '../latex/resume/Resume_Jamil_ML')

    Returns:
        str: Path to the Temp folder
    """
    # Get the folder name and parent directory
    base_folder_name = os.path.basename(base_folder_path)
    parent_dir = os.path.dirname(base_folder_path)

    # Create the Temp folder name
    temp_folder_name = f"{base_folder_name}_Temp"
    temp_folder_path = os.path.join(parent_dir, temp_folder_name)

    if create_temp_folder:
        # Check if Temp folder exists
        if os.path.exists(temp_folder_path):
            print(f"Found existing Temp folder: {temp_folder_name}")
            return temp_folder_path

        # If not, create it by copying the base folder
        print(f"Temp folder not found. Creating: {temp_folder_name}")
        try:
            shutil.copytree(base_folder_path, temp_folder_path)
            print(f"Successfully created Temp folder by copying base template")
            return temp_folder_path
        except Exception as e:
            raise RuntimeError(f"Failed to create Temp folder: {e}")
    return temp_folder_path


def compile_latex_to_pdf(temp_folder_path):
    """
    Compiles the main.tex file in the Temp folder to PDF.

    Args:
        temp_folder_path (str): Path to the Temp folder containing main.tex

    Returns:
        str: Path to the final PDF in pdf/ directory
    """
    print("\n" + "=" * 50)
    print("STEP: PDF Compilation")
    print("=" * 50)

    # Get the folder name to construct PDF name
    temp_folder_name = os.path.basename(temp_folder_path)
    pdf_name = f"{temp_folder_name}.pdf"
    generic_name = "Resume_Jamil_Ahmed.pdf"

    # Define paths
    main_tex = os.path.join(temp_folder_path, "main.tex")
    # Go up from latex/resume/Resume_Jamil_ML_Temp to project root, then to output/pdf
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(temp_folder_path)))
    pdf_output_dir = os.path.join(project_root, "output", "pdf")
    final_pdf_path = os.path.join(pdf_output_dir, pdf_name)
    final_pdf_path_renamed = os.path.join(pdf_output_dir, generic_name) # Final file in generic name

    # Check if main.tex exists
    if not os.path.exists(main_tex):
        raise FileNotFoundError(f"main.tex not found in {temp_folder_path}")

    # Ensure pdf/ directory exists
    os.makedirs(pdf_output_dir, exist_ok=True)

    # Check if we're overwriting before compilation
    if os.path.exists(final_pdf_path):
        print(f"Overwriting existing file: {pdf_name}")

    # Run pdflatex twice (standard for LaTeX)
    print(f"Compiling {temp_folder_name}/main.tex...")

    try:
        # First compilation
        print("Running pdflatex (1/2)...")
        result1 = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "main.tex"],
            cwd=temp_folder_path,
            capture_output=True,
            text=True,
            timeout=60
        )

        # Second compilation (for references)
        print("Running pdflatex (2/2)...")
        result2 = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "main.tex"],
            cwd=temp_folder_path,
            capture_output=True,
            text=True,
            timeout=60
        )

        # Check if PDF was generated
        temp_pdf = os.path.join(temp_folder_path, "main.pdf")
        if not os.path.exists(temp_pdf):
            # Try to find error in log
            log_file = os.path.join(temp_folder_path, "main.log")
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    log_content = f.read()
                    # Find the first error
                    print("\n--- LaTeX Errors ---")
                    for line in log_content.split('\n'):
                        if line.startswith('!'):
                            print(line)
            raise RuntimeError("PDF compilation failed. Check main.log in Temp folder for details.")

        # Copy PDF to final location
        shutil.copy2(temp_pdf, final_pdf_path)
        shutil.copy2(temp_pdf, final_pdf_path_renamed)
        print(f"PDF successfully generated: {pdf_name} and {generic_name}")
        print(f"Output location: {pdf_output_dir}/")

        return final_pdf_path

    except subprocess.TimeoutExpired:
        raise RuntimeError("PDF compilation timed out (exceeded 60 seconds)")
    except FileNotFoundError:
        raise RuntimeError(
            "pdflatex not found. Please install LaTeX (e.g., 'sudo apt-get install texlive-full' on Ubuntu)")
    except Exception as e:
        raise RuntimeError(f"PDF compilation failed: {e}")


# --- Test ---
if __name__ == "__main__":
    # Mock test data
    mock_assets = {
        'folder_root': '../latex/resume/Resume_Jamil_ML',
        'pdf_folder': '../output/pdf',
        'experience': '../latex/resume/Resume_Jamil_ML/experience.tex',
        'skills': '../latex/resume/Resume_Jamil_ML/technologies.tex'
    }

    pdf_output_path = compile_latex_to_pdf(mock_assets['folder_root'])
    print(pdf_output_path)