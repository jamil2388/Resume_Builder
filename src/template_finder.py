import os

def locate_template_assets(job_position, base_latex_path="../latex/resume"):
    """
    Finds the template folder and identifies specific .tex files.
    Priority for skills: additional_skills.tex > technologies.tex > skills.tex
    """
    jp_lower = job_position.lower()
    
    # 1. Locate the correct folder
    all_folders = [d for d in os.listdir(base_latex_path) if os.path.isdir(os.path.join(base_latex_path, d))]
    target_folder_name = next((f for f in all_folders if jp_lower in f.lower()), None)
    
    if not target_folder_name:
        raise FileNotFoundError(f"No template folder found matching position: {job_position}")

    folder_path = os.path.abspath(os.path.join(base_latex_path, target_folder_name))
    
    # 2. Identify Experience file
    exp_path = os.path.join(folder_path, "experience.tex")
    experience_file = exp_path if os.path.exists(exp_path) else None
    
    # 3. Identify Skills file with specific priority
    skills_file = None
    # Define priority order
    priority_list = ["additional_skills.tex", "technologies.tex", "skills.tex"]
    
    for filename in priority_list:
        potential_path = os.path.join(folder_path, filename)
        if os.path.exists(potential_path):
            print(f"found a skill file in : {potential_path}")
            skills_file = potential_path
            break  # Stop at the first one found
            
    return {
        "folder_root": folder_path,
        "experience": experience_file,
        "skills": skills_file
    }

def extract_tex_contents(asset_map):
    """
    Reads the content of the detected .tex files.
    
    Args:
        asset_map (dict): The dictionary returned by locate_template_assets
        
    Returns:
        dict: A dictionary containing the raw strings of the LaTeX files
    """
    content_data = {
        "experience": {"raw": "", "path": asset_map["experience"]},
        "skills": {"raw": "", "path": asset_map["skills"]}
    }

    for key in content_data:
        file_path = content_data[key]["path"]
        
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content_data[key]["raw"] = f.read()
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                content_data[key]["raw"] = None
        else:
            content_data[key]["raw"] = None
            
    return content_data


# --- Test ---
if __name__ == "__main__":
    try:
        prompt = input("enter a job position : \n")
        assets = locate_template_assets(prompt)
        extracted = extract_tex_contents(assets)

        print(f"Match found in folder: {os.path.basename(assets['folder_root'])}")
        print(f"Exp file: {os.path.basename(assets['experience']) if assets['experience'] else 'Not Found'}")
        print(f"Skills file: {os.path.basename(assets['skills']) if assets['skills'] else 'Not Found'}")

    
        print("--- Experience Snippet ---")
        print(extracted["experience"]["raw"][:100] if extracted["experience"]["raw"] else "No content")
        print("\n--- Skills Snippet ---")
        print(extracted["skills"]["raw"][:100] if extracted["skills"]["raw"] else "No content")


    except Exception as e:
        print(e)