from fastapi import FastAPI, HTTPException, Request, Form, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from main import resume_tailoring
import os

app = FastAPI(title="Resume Builder API")

class ResumeRequest(BaseModel):
    job_position: str
    job_description: str

@app.post("/tailor-resume")
async def tailor_resume_api(
    request: Request,
    job_position: Optional[str] = Form(None),
    job_description: Optional[str] = Form(None),
    description_file: Optional[UploadFile] = File(None)
):
    """
    Endpoint to tailor a resume. 
    Accepts:
    1. JSON (application/json)
    2. Form Fields (multipart/form-data)
    3. File Upload (multipart/form-data)
    """
    try:
        content_type = request.headers.get("Content-Type", "")
        
        pos = None
        desc = None

        # Case 1: JSON
        if "application/json" in content_type:
            try:
                data = await request.json()
                pos = data.get("job_position")
                desc = data.get("job_description")
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid JSON format")

        # Case 2 & 3: Multipart/Form-data
        elif "multipart/form-data" in content_type:
            pos = job_position
            
            # If a file is uploaded, use its content as the description
            if description_file:
                file_content = await description_file.read()
                desc = file_content.decode("utf-8")
            else:
                desc = job_description
        
        else:
            raise HTTPException(status_code=415, detail="Unsupported Media Type. Use application/json or multipart/form-data")

        # Validation
        if not pos or not desc:
            raise HTTPException(status_code=400, detail="Missing job_position or job_description")

        # Minimal args_dict for main logic
        args_dict = {
            'job_position': pos,
            'job_description': 1,  # Placeholder
            'tailor_resume': 1,
            'tailor_cover_letter': 0
        }
        
        pdf_path = resume_tailoring(args_dict, job_description=desc)
        
        if pdf_path and os.path.exists(pdf_path):
            return FileResponse(
                path=pdf_path, 
                media_type='application/pdf', 
                filename=os.path.basename(pdf_path)
            )
        else:
            raise HTTPException(status_code=500, detail="Generated PDF not found.")
            
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"[API ERROR]: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to the Resume Builder API. Use POST /tailor-resume to generate a tailored resume."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
