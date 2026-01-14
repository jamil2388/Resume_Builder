"""
LaTeX Document Classes
Represents Resume and Cover Letter documents with their respective components.
Each component maps to a corresponding .tex file.
"""


class LatexDocument:
    """Base class for LaTeX documents with components."""
    
    def __init__(self, components):
        """
        Initialize with a list of component names.
        Each component maps to a .tex file.
        
        Args:
            components (list): List of component names
        """
        self.components = {name: None for name in components}
    
    def set_component(self, component_name, file_path, content=None):
        """
        Set a component with its file path and optional content.
        
        Args:
            component_name (str): Name of the component (e.g., 'experience')
            file_path (str): Path to the .tex file
            content (str, optional): Content of the file
        """
        if component_name not in self.components:
            raise ValueError(f"Unknown component: {component_name}. Valid: {list(self.components.keys())}")
        
        self.components[component_name] = {
            'path': file_path,
            'content': content
        }
    
    def get_component(self, component_name):
        """
        Get a component's data.
        
        Args:
            component_name (str): Name of the component
            
        Returns:
            dict or None: Dictionary with 'path' and 'content' keys, or None if not set
        """
        return self.components.get(component_name)
    
    def get_all_components(self):
        """
        Get all components.
        
        Returns:
            dict: All components with their data
        """
        return self.components
    
    def has_component(self, component_name):
        """
        Check if component exists in this document type.
        
        Args:
            component_name (str): Name of the component
            
        Returns:
            bool: True if component exists
        """
        return component_name in self.components
    
    def get_component_names(self):
        """
        Get list of all component names.
        
        Returns:
            list: List of component names
        """
        return list(self.components.keys())


class Resume(LatexDocument):
    """
    Represents a LaTeX resume document.
    
    Components:
        - experience: experience.tex
        - technologies: technologies.tex (or skills.tex, additional.tex variants)
    """
    
    def __init__(self):
        super().__init__(['experience', 'technologies'])


class CoverLetter(LatexDocument):
    """
    Represents a LaTeX cover letter document.
    
    Components:
        - username: username.tex
        - user_details: user_details.tex
        - recruiter: recruiter.tex
        - date: date.tex
        - body: body.tex
    """
    
    def __init__(self):
        super().__init__(['username', 'user_details', 'recruiter', 'date', 'body'])


# --- Quick Test ---
if __name__ == "__main__":

    sample_path_to_resume = "../latex/resume/Resume_Jamil_ML"
    sample_path_to_cover_letter = "../latex/cover_letter/Cover_Letter_Jamil_ML"

    # Test Resume
    print("=== Testing Resume Class ===")
    resume = Resume()
    print(f"Resume components: {resume.get_component_names()}")
    
    resume.set_component("experience", f"{sample_path_to_resume}/experience.tex", "Latex content here")
    resume.set_component("technologies", f"{sample_path_to_resume}/technologies.tex", "Technologies part here")
    
    exp = resume.get_component("experience")
    print(f"Experience: {exp['path']}")
    print(f"Has content: {exp['content'] is not None}")
    
    # Test CoverLetter
    print("\n=== Testing CoverLetter Class ===")
    cover_letter = CoverLetter()
    print(f"CoverLetter components: {cover_letter.get_component_names()}")
    
    cover_letter.set_component('recruiter', f"{sample_path_to_cover_letter}/recruiter.tex", 'Dear Hiring Manager')
    cover_letter.set_component('body', f"{sample_path_to_cover_letter}/body.tex", 'I am writing to...')
    
    recruiter = cover_letter.get_component('recruiter')
    print(f"Recruiter: {recruiter['path']}")
    
    # Test error handling
    print("\n=== Testing Error Handling ===")
    try:
        resume.set_component('invalid_component', '/path/to/file.tex')
    except ValueError as e:
        print(f"Caught error: {e}")