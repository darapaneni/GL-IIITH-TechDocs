import os
import glob
import PyPDF2

def incoming_doc(pdf_directory):

    # List all PDF files in the directory
    pdf_files = glob.glob(os.path.join(pdf_directory, '*.pdf'))

    # Sort PDF files by modification time in descending order (most recent first)
    pdf_files.sort(key=os.path.getmtime, reverse=True)

    # Read the most recent PDF file
    if pdf_files:
        most_recent_pdf_file = pdf_files[0]
    # else:
    #     print("No PDF files found in the directory.")

    # Open the PDF file and read its content
    with open(most_recent_pdf_file, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        lst=[]
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            lst.append(text)
            # print(text)

    return str(lst)    