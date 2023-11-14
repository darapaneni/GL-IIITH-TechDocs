import os
import PyPDF2

# # Define the folder path containing the PDF files
# pdf_folder = "D://Capstone/document-similarity-master/data/source_repo"

# Create a dictionary to store key-value pairs (filename and text)
pdf_text_dict = {}

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    text = ""
    with open(pdf_file, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()
    return text

def iterate_files(pdf_folder):

    # Iterate through the PDF files in the folder
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_file_path = os.path.join(pdf_folder, filename)
            text = extract_text_from_pdf(pdf_file_path)
            pdf_text_dict[filename] = text
    return pdf_text_dict


