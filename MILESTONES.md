# Project Milestones

This file will be used to track the major milestones and development phases of the Resume Builder project.

## Phase 1: Core Functionality (Completed/In Progress)
- [ ] Implement argument parsing for job position, document type (resume/cover letter), and job description input method.
- [ ] Develop classes for LaTeX document representation (Resume, CoverLetter) and their components.
- [ ] Implement logic for discovering and populating LaTeX templates based on job position.
- [ ] Integrate with Gemini API for document tailoring.
- [ ] Define clear prompting strategies for resume and cover letter tailoring.
- [ ] Implement parsing of Gemini API responses.
- [ ] Develop functionality to create temporary folders and write tailored LaTeX content.
- [ ] Implement LaTeX to PDF compilation using `pdflatex`.

## Phase 2: Enhancements & Robustness
- [ ] Improve error handling and user feedback for all stages (e.g., API errors, file not found, compilation issues).
- [ ] Add support for interactive job description input.
- [ ] Implement cover letter tailoring workflow (currently `pass`).
- [ ] Allow users to specify output file names or locations.
- [ ] Add more flexible template management (e.g., different template styles, user-defined templates).
- [ ] Implement unit and integration tests for core functionalities.

## Phase 3: Advanced Features
- [ ] Implement a GUI or web interface for easier interaction.
- [ ] Support for multiple resume/cover letter profiles.
- [ ] Version control for generated documents.
- [ ] Integration with other AI models or services.
- [ ] Automated deployment/sharing of generated PDFs.

## Phase 4: Documentation & Deployment
- [ ] Comprehensive README and usage instructions.
- [ ] API documentation.
- [ ] Packaging and distribution (e.g., PyPI).
- [ ] Example templates and configurations.
