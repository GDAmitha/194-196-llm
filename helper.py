import pdfplumber
import kagglehub

# Download latest version
#path = kagglehub.dataset_download("ravindrasinghrana/job-description-dataset")

#print("Path to dataset files:", path)

def extract_text_from_pdf(file_path: str) -> str:
    """
    Read pdf and return a string version of it.
    """
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def write_to_txt(content: str) -> None:
    """
    Write the given content to a text file.

    :param content: The string content to write into the file
    """
    with open("cv.txt", 'w') as file:
        file.write(content)

# # Example usage:
# resume_text = extract_text_from_pdf("JaeWon_Kim_Resume.pdf")
# print(resume_text)
