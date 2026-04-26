import os
import json
import google.generativeai as genai
from PIL import Image

def analyze_community_report(report_input):
    """
    Uses Gemini to extract structured needs.
    report_input can be a string (text) or a PIL Image object (handwritten note).
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return {"error": "API key not found in environment."}
    
    genai.configure(api_key=api_key)
    
    # Using flash as it supports multimodal and is fast
    model = genai.GenerativeModel('gemini-flash-latest')
    
    prompt = """
    You are an AI assistant helping a local NGO process messy field reports.
    If you are provided with an image, read the handwriting or text in the image.
    If you are provided with text, read the text.
    
    Extract the core urgent community needs.
    
    Return a JSON object with the following structure exactly:
    {
        "location": "extracted location or 'Unknown'",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "urgency": "High", "Medium", or "Low",
        "primary_need": "e.g., Medical, Food, Shelter, Education, Repair",
        "summary": "1 short sentence summary of the issue",
        "required_volunteer_skills": ["List", "of", "1-3 skills needed"]
    }
    
    Note for lat/lon: Provide an approximate latitude/longitude if the location is known (e.g. New York, London, etc), otherwise default to 40.7128, -74.0060.
    
    Respond ONLY with valid JSON. Do not include markdown formatting like ```json.
    """
    
    contents = [prompt, report_input]
    
    try:
        response = model.generate_content(contents)
        text_response = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(text_response)
    except Exception as e:
        return {"error": str(e)}

def generate_dispatch_message(volunteer_name, task_summary, location):
    """Generates a personalized SMS dispatch message."""
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-flash-latest')
    
    prompt = f"""
    Write a short, urgent SMS text message (max 2 sentences) to dispatch a volunteer.
    Volunteer: {volunteer_name}
    Task: {task_summary}
    Location: {location}
    End the message asking them to reply YES to confirm.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating message: {e}"
