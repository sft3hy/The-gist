import streamlit as st
import base64
import os
from PyPDF2 import PdfReader
from pptx import Presentation


def get_base64_of_bin_file(png_file: str) -> str:
    with open(png_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

@st.cache_resource
def build_markup_for_logo(png_file: str) -> str:
    binary_string = get_base64_of_bin_file(png_file)
    return f"""
            <style>
                [data-testid="stSidebarHeader"] {{
                    background-image: url("data:image/png;base64,{binary_string}");
                    background-repeat: no-repeat;
                    background-size: 200px;
                    padding-bottom: 5rem;
                    background-position: top center;
                }}
            </style>
            """

def extract_text(file_path):
    """
    Extracts text from a PDF, PPTX, or TXT file.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: Extracted text from the file.
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    # Get the file extension
    file_extension = os.path.splitext(file_path)[1].lower()

    potential_already_extracted = f"text_extractions/{file_path.split('/')[-1]}.txt"
    if os.path.exists(potential_already_extracted):
        return open(potential_already_extracted, 'r').read()
    else:
    # Extract text based on file type
        if file_extension == '.pdf':
            return extract_text_from_pdf(file_path)
        elif file_extension == '.pptx':
            return extract_text_from_pptx(file_path)
        elif file_extension == '.txt':
            return extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    text = ""
    with open(file_path, 'rb') as pdf_file:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    write_text_to_extractions_folder(text, f"text_extractions/{file_path.split('/')[-1]}.txt")
    return text

def extract_text_from_pptx(file_path):
    """Extract text from a PPTX file."""
    text = ""
    presentation = Presentation(file_path)
    for slide in presentation.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                text += shape.text + "\n"
    write_text_to_extractions_folder(text, f"text_extractions/{file_path.split('/')[-1]}.txt")
    return text

def extract_text_from_txt(file_path):
    """Extract text from a TXT file."""
    with open(file_path, 'r', encoding='utf-8') as txt_file:
        text = txt_file.read()
        write_text_to_extractions_folder(text, f"text_extractions/{file_path.split('/')[-1]}.txt")
        return txt_file.read()

def write_text_to_extractions_folder(text, file_path):
    file_name = file_path.split('/')[-1]
    new_path = f"text_extractions/{file_name}"
    with open(new_path, 'w') as f:
        f.write(text)