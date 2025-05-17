from typing import Optional

def clean_input_text(text: Optional[str]) -> str:
    """Sanitize and normalize input text fields."""
    if not text:
        return ""
    return text.strip().replace("\n", " ").replace("\r", "")

def combine_resume_fields(name: str, education: str, experience: str, skills: str, location: str) -> str:
    """Formats resume fields into a structured text block for AI prompting."""
    return f"""
    Name: {clean_input_text(name)}
    Education: {clean_input_text(education)}
    Experience: {clean_input_text(experience)}
    Skills: {clean_input_text(skills)}
    Location: {clean_input_text(location)}
    """
