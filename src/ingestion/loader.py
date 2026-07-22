# Load the text from the files that you want the RAG to work with

import fitz
import os


def load_documents(folder_path):

    documents = []

    pdf_files = os.listdir(folder_path) # Get all files

    for file in pdf_files: # For each file in files

        if file.endswith(".pdf") or file.endswith(".txt"):

            pdf_path = os.path.join(folder_path, file) # Get the file full path

            doc = fitz.open(pdf_path) # Open the pdf file

            text = ""

            # Get all pages of the file, one by one
            for page in doc: 

                text += page.get_text()

            documents.append({
                "filename": file,
                "text": text
            })

            doc.close()

    return documents

