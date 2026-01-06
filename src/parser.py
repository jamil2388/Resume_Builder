import os

def parse_job_input(file_path="../docs/job_description.txt"):
    """
    Reads the job_description.txt file.
    Assumes Line 1: Job Position
    Assumes Line 2+: Job Description
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Could not find input file at {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if len(lines) < 2:
        raise ValueError("The job_description.txt must have the Position on line 1 and the JD on line 2+.")

    # Extracting data
    job_position = lines[0].strip()
    job_description = "".join(lines[1:]).strip()

    return {
        "job_position": job_position,
        "job_description": job_description
    }

# --- Quick Test ---
if __name__ == "__main__":
    try:
        job_data = parse_job_input()
        print(f"Position: {job_data['job_position']}")
        print(f"JD Length: {len(job_data['job_description'])} characters")
    except Exception as e:
        print(f"Error: {e}")