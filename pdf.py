import PyPDF2


print("Student ID: antchr2155")  

# Get user input
metadata_tag = input("Choose a metadata tag to view: /Author /Keywords /CreationDate ")


pdf_path = r"C:\PythonFiles\PA\pdf\example.pdf"

try:
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        info = reader.metadata
        print(info)

        # Displaying  the requested metadata tag
        if info:
            if metadata_tag in info:
                print(f"{metadata_tag}: {info[metadata_tag]}")
            else:
                print(f"Metadata tag '{metadata_tag}' not found.")
        else:
            print("No metadata found in the PDF.")

except FileNotFoundError:
    print(f"Error: PDF file not found at {pdf_path}")
except Exception as e:
    print(f"An error occurred: {e}")