import PyPDF2

def extract_text(pdf_file):

    text = ""

    with open(pdf_file, 'rb') as file:

        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted

    return text