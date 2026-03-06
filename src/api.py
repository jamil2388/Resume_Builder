from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from main import resume_tailoring
import os

app = FastAPI(title="Resume Builder API")

class ResumeRequest(BaseModel):
    job_position: str
    job_description: str

@app.post("/tailor-resume")
async def tailor_resume_api(request: ResumeRequest):
    """
    Endpoint to tailor a resume based on job position and description.
    Returns the compiled PDF file.
    """
    try:
        # We need to provide a minimal args_dict that resume_tailoring expects
        args_dict = {
            'job_position': request.job_position,
            'job_description': 1,  # Placeholder, not used when job_description is passed directly
            'tailor_resume': 1,
            'tailor_cover_letter': 0
        }
        
        pdf_path = resume_tailoring(args_dict, job_description=request.job_description)
        
        if pdf_path and os.path.exists(pdf_path):
            return FileResponse(
                path=pdf_path, 
                media_type='application/pdf', 
                filename=os.path.basename(pdf_path)
            )
        else:
            raise HTTPException(status_code=500, detail="Generated PDF not found.")
            
    except Exception as e:
        print(f"[API ERROR]: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to the Resume Builder API. Use POST /tailor-resume to generate a tailored resume."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
