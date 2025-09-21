import os
from pdf2image import convert_from_path

# Directory containing PDFs
input_dir = "."

# Loop through all PDF files in the directory
for filename in os.listdir(input_dir):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(input_dir, filename)
        base_name = os.path.splitext(filename)[0]

        # Convert PDF pages to images
        pages = convert_from_path(pdf_path, dpi=300)

        # Save each page as PNG
        for i, page in enumerate(pages, start=1):
            out_filename = f"{base_name}_page{i}.png"
            page.save(out_filename, "PNG")
            print(f"Saved: {out_filename}")
