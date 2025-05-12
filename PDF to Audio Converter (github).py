#!/usr/bin/env python3

import os
import re
import PyPDF2
from TTS.api import TTS

def extract_text_by_chapter(pdf_path):
    print("📖 Extracting chapters from PDF...")
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        all_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                all_text += text + "\n"

    # Split on "Chapter" headings (e.g., "Chapter 1", "CHAPTER TWO")
    chapter_pattern = r"(Chapter\s+\d+|CHAPTER\s+\w+)"
    parts = re.split(chapter_pattern, all_text, flags=re.IGNORECASE)

    # Re-join the chapter titles with their content
    chapters = []
    i = 1
    while i < len(parts) - 1:
        title = parts[i].strip()
        content = parts[i + 1].strip()
        if content:
            chapters.append((title, content))
        i += 2

    print(f"✅ Found {len(chapters)} chapters.")
    return chapters

def generate_audio_from_chapters(pdf_path):
    output_folder = os.path.dirname(pdf_path)
    chapters = extract_text_by_chapter(pdf_path)

    # Load Coqui TTS once
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

    for idx, (title, text) in enumerate(chapters, start=1):
        chapter_filename = f"chapter_{idx}.wav"
        output_path = os.path.join(output_folder, chapter_filename)
        print(f"🎧 Generating: {chapter_filename} ({title})")

        try:
            tts.tts_to_file(text=text, file_path=output_path)
        except Exception as e:
            print(f"⚠️ Error in {title}: {e}")

    print("✅ All chapters converted to audio.")

# 📍 Set your PDF path here
generate_audio_from_chapters("example.pdf")