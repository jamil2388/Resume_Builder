# Project Milestones

This file will be used to track the major milestones and development phases of the Resume Builder project.

## Phase 1: Core Functionality for Resume
- [x] Implement argument parsing for job position, document type (resume), and job description input method.
- [x] Develop classes for LaTeX document representation (Resume) and their components.
- [x] Implement logic for discovering and populating LaTeX templates based on job position.
- [x] Integrate with Gemini API for document tailoring.
- [x] Define clear prompting strategies for resume tailoring.
- [x] Implement parsing of Gemini API responses.
- [x] Develop functionality to create temporary folders and write tailored LaTeX content.
- [x] Implement LaTeX to PDF compilation using `pdflatex`.

## Phase 2: Expose Resume Tailoring via API
- [x] Branch : feature/api
- [ ] Use FastAPI for the API development.
- [ ] Create a POST endpoint (e.g., `/tailor-resume`) that accepts `job_position` and `job_description`.
- [ ] Refactor core logic in `src/main.py` to be easily callable by the API handler.
- [ ] Implement logic to return the compiled PDF file as the API response.
- [ ] Add basic validation for input parameters and error handling for the tailoring/compilation process.
- [ ] Test the API endpoint to ensure it successfully delivers the `Resume_Jamil_Ahmed.pdf`.



## Phase 3: Core Functionality for Cover Letter
- [ ] Implement argument parsing for job position, document type (cover letter), and job description input method.
- [ ] Develop classes for LaTeX document representation (CoverLetter) and their components.
- [ ] Implement logic for discovering and populating LaTeX templates based on job position.
- [ ] Integrate with Gemini API for document tailoring.
- [ ] Define clear prompting strategies for cover letter tailoring.
- [ ] Implement parsing of Gemini API responses.
- [ ] Develop functionality to create temporary folders and write tailored LaTeX content.
- [ ] Implement LaTeX to PDF compilation using `pdflatex`.

## Phase 4: Enhancements & Robustness
- [ ] Improve error handling and user feedback for all stages (e.g., API errors, file not found, compilation issues).
- [ ] Add support for interactive job description input.
- [ ] Implement cover letter tailoring workflow (currently `pass`).
- [ ] Allow users to specify output file names or locations.
- [ ] Add more flexible template management (e.g., different template styles, user-defined templates).
- [ ] Implement unit and integration tests for core functionalities.

## Phase 5: Advanced Features
- [ ] Implement a GUI or web interface for easier interaction.
- [ ] Support for multiple resume/cover letter profiles.
- [ ] Version control for generated documents.
- [ ] Integration with other AI models or services.
- [ ] Automated deployment/sharing of generated PDFs.

## Phase 6: Documentation & Deployment
- [ ] Comprehensive README and usage instructions.
- [ ] API documentation.
- [ ] Packaging and distribution (e.g., PyPI).
- [ ] Example templates and configurations.
