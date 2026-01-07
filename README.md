# AI-Powered Resume and Cover Letter Tailor

This project automates the process of tailoring a LaTeX resume and cover letter to a specific job description using the power of generative AI. It analyzes a job description, selects the particular resume template from a collection, and then uses the Google Gemini Pro model to rewrite the resume content and cover letter to better match the job requirements and previous work history.

## Features

- **AI-Powered Content Generation:** Leverages the Gemini Pro model to intelligently rewrite and tailor the resume content, highlighting relevant experience and skills.
- **Automated Workflow:** Orchestrates the entire process from parsing the job description to replacing the LaTex template while tailoring the resume and/or cover letter.

## How It Works

1.  **Parse Job Description:** The script starts by reading a job description and job position from `docs/job_description.txt`.
2.  **Find Best Template:** It then scans the `latex/resume` directory to find the matching template resume based on the position, which contains multiple resume templates (each in its own subdirectory).
3.  **Create New Resume:** A new directory for the generated resume is created in the `out/` directory, and the contents of the best-matching template are copied into it.
4.  **Tailor with AI:** The content of the chosen resume template is combined with the job description keywords into a prompt for the Gemini Pro model. The model is instructed to rewrite the resume to align with the job requirements.
5.  **Save the Result:** The AI-generated LaTeX code is then saved back into the main `.tex` file in the newly created resume directory.

## Requirements

- Python 3.x
- Google Gemini API Key
- `google-generativeai`
- `scikit-learn`
- `numpy`

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: A `requirements.txt` file would need to be created for this. Based on the code, it would contain `google-generativeai`, `scikit-learn`, and `numpy`)*

3.  **Set up your API Key:**
    You need to set your Google Gemini API key as an environment variable.
    ```bash
    export GEMINI_API_KEY='your_api_key_here'
    ```
    On Windows, you can use:
    ```bash
    set GEMINI_API_KEY='your_api_key_here'
    ```

## Usage

1.  **Add Job Description:** Place the job description and job position you want to target in the `docs/job_description.txt` file.
2.  **Add Resume Templates:** Place your LaTeX resume templates in the `latex/resume/` directory. Each resume should be in its own subdirectory (e.g., `latex/resume/Resume_John_ML/`, `latex/resume/Resume_John_DA_Temp/` - given ML = Machine Learning, DA = Data Analyst etc.). Please note that the job positions should be abbreviated in the template names such that they can be mentioned in the `docs/job_description.txt` before feeding to gemini.
3.  **Add Cover Letter Templates:**Place your LaTeX cover letter templates in the `latex/cover_letter/` directory. Each resume should be in its own subdirectory (e.g., `latex/cover_letter/Cover_Letter_John_ML_Temp/`, `latex/cover_letter/cover_letter_John_DA/`).
4.  **Run the script:**
    ```bash
    python src/main.py
    ```
5.  **Find your tailored resume and/or cover letter:** The generated resume will be located in a new subdirectory inside the `pdf/` directory.

## Project Structure

```
.
├── docs/
│   └── job_description.txt   # Input job position (abbreviation) and description
├── latex/
│   └── resume/               # Directory for different LaTeX resume templates
|   └── cover_letter/         # Directory for different LaTeX cover_letter templates
├── pdf/                      # Output directory for generated resumes
├── src/
│   ├── main.py               # Main script to run the process
│   ├── gemini_client.py      # Handles interaction with the Gemini API
│   ├── parser.py             # Parses job descriptions and resume templates
│   └── template_finder.py    # Finds the best resume template
└── .gitignore
```
