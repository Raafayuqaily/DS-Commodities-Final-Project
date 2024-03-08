# This python file is designed to convert out Latex files into PDFs


import os
import subprocess
from pathlib import Path

# Define the directory where your .tex files are located
latex_dir = Path('/path/to/your/latex/files')
# Define the directory where you want to save your PDF files
output_dir = Path('/path/to/your/pdf/files')

# Ensure the output directory exists
output_dir.mkdir(parents=True, exist_ok=True)

# Find all .tex files in the directory
latex_files = latex_dir.glob('*.tex')

# Loop through the found .tex files and compile them into PDFs
for latex_file in latex_files:
    # Define the output PDF path
    pdf_path = output_dir / f"{latex_file.stem}.pdf"
    
    # Compile the LaTeX file into a PDF using the pdflatex command
    # The -output-directory option is used to specify where the PDF will be saved
    # This command may need to be adjusted depending on your LaTeX setup and file requirements
    subprocess.run(['pdflatex', '-interaction=nonstopmode', '-output-directory', str(output_dir), str(latex_file)], check=True)
    
    print(f"Compiled {latex_file.name} to PDF.")

print("All LaTeX files have been compiled to PDFs.")
