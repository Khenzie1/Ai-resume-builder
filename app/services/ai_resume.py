from google.generativeai import configure, GenerativeModel
from app.core.config import settings
from app.services.utils import combine_resume_fields
from fastapi import HTTPException

# Configure the Gemini API key
configure(api_key=settings.GEMINI_API_KEY)

def generate_resume_suggestions(
    name: str,
    education: str,
    experience: str,
    skills: str,
    location: str
) -> dict:
    """
    Generate an AI-powered, ATS-friendly resume summary using Gemini API.
    """
    prompt = f"""
    Create a globally optimized and ATS-friendly resume summary for:
    {combine_resume_fields(name, education, experience, skills, location)}
    """

    try:
        model = GenerativeModel("gemini-pro")  # Or use another available Gemini model
        response = model.generate_content(prompt)

        # Extract and return response text
        summary_text = getattr(response, "text", str(response))
        return {"summary": summary_text.strip()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")
