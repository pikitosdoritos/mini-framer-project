from fastapi import FastAPI, Depends, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        orm_mode = True

translations = {
    "en": "Hello! This is my API for Framer.",
    "uk": "Привіт! Це мій API для Framer.",
}

@app.get("/")
def read_root(accept_language: Optional[str] = Header(None)):
    lang = "en" # Default language
    if accept_language and accept_language.startswith("uk"):
        lang = "uk"
    return {"message": translations[lang]}

@app.post("/notes/", response_model=NoteResponse)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    db_note = models.Note(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@app.get("/notes/", response_model=List[NoteResponse])
def read_notes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    notes = db.query(models.Note).offset(skip).limit(limit).all()
    return notes