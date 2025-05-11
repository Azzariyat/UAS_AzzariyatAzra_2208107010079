import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

# inisialisasi Gemini client dan konfigurasi
# MODEL = "gemini-2.0-flash"
# client = genai.Client(api_key=GOOGLE_API_KEY)

MODEL = "gemini-pro"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(MODEL)

app = FastAPI(title="Intelligent Email Writer API")

class EmailRequest(BaseModel):
    category: str
    recipient: str
    subject: str
    tone: str
    language: str
    urgency_level: Optional[str] = "Biasa"
    points: List[str]
    example_email: Optional[str] = None

def build_prompt(body: EmailRequest) -> str:
    lines = [
        f"Tolong buatkan email dalam {body.language.lower()} yang {body.tone.lower()}",
        f"kepada {body.recipient}.",
        f"Subjek: {body.subject}.",
        f"Kategori email: {body.category}.",
        f"Tingkat urgensi: {body.urgency_level}.",
        "",
        "Isi email harus mencakup poin-poin berikut:",
    ]
    for point in body.points:
        lines.append(f"- {point}")
    if body.example_email:
        lines += ["", "Contoh email sebelumnya:", body.example_email]
    lines.append("")
    lines.append("Buat email yang profesional, jelas, dan padat.")
    return "\n".join(lines)

@app.post("/generate/")
async def generate_email(req: EmailRequest):
    prompt = build_prompt(req)

    try:
        response = model.generate_content(prompt)
        generated = response.text
        if not generated:
            raise HTTPException(status_code=500, detail="Tidak ada hasil dari Gemini API")
        return {"generated_email": generated}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))