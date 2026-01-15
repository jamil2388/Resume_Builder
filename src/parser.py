import os
import argparse

def create_parser():
    """
        Create an argument parser

        Args:
            Empty

        Returns:
            argparse.Namespace : An object containing the parsed argument values.
    """
    print(f"\n==Create argument parser==\n")
    parser = argparse.ArgumentParser()

    # Add optional arguments
    parser.add_argument("-jp", "--job_position", required = True, type=str, help="The job position abbreviation. e.g., ML, SD, DA etc.")
    parser.add_argument("-jd", "--job_description", type = int, default = 1, help = "Add the job description in a popup. 1 = Add, 0 = Use existing")
    parser.add_argument("-r", "--resume", type = int, default = 1, help = "Tailor Resume. 1 = Tailor, 0 = Ignore")
    parser.add_argument("-cl", "--cover_letter", type = int, default = 1, help = "Tailor Cover Letter. 1 = Tailor, 0 = Ignore")

    args = parser.parse_args()

    return args

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

def read_file(file_path):
    with open(file_path, "r") as f:
        contents = f.read()
    return contents

def write_file(file_path, contents):
    with open(file_path, "w+") as f:
        f.write(contents)
    return



# --- Quick Test ---
if __name__ == "__main__":
    try:
        job_data = parse_job_input()
        print(f"Position: {job_data['job_position']}")
        print(f"JD Length: {len(job_data['job_description'])} characters")
    except Exception as e:
        print(f"Error: {e}")