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
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Could not find input file at {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Extracting data
    job_description = "".join(lines[0:]).strip()

    return job_description

def read_file(file_path):
    try:
        with open(file_path, "r") as f:
            contents = f.read()
            print(f"[DEBUG] File read successful for file : {file_path}")
        return contents
    except FileNotFoundError:
        print(f"Error: The folder structure for '{file_path}' does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def write_file(file_path, contents):
    try:
        with open(file_path, "w") as f:
            f.write(contents)
            print(f"[DEBUG] File write successful for file : {file_path}")
    except FileNotFoundError:
        print(f"Error: The folder structure for '{file_path}' does not exist.")
    except PermissionError:
        print(f"Error: You don't have permission to write to '{file_path}'.")
    except TypeError:
        print(f"Error: 'contents' must be a string, not {type(contents).__name__}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



# --- Quick Test ---
if __name__ == "__main__":
    try:
        job_description = parse_job_input()
        print(f"JD Length: {len(job_description)} characters")
    except Exception as e:
        print(f"Error: {e}")