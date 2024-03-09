# This python file is designed to convert out Latex files into PDFs

import os
import subprocess
from pathlib import Path
import config

# Set the directory where your LaTeX files are stored and where the PDFs should be saved
# Assuming they are in the reports folder and will be saved there as well
LATEX_DIR = Path(config.OUTPUT_DIR)

# Ensure the output directory exists
LATEX_DIR.mkdir(parents=True, exist_ok=True)

# Find all .tex files in the directory
latex_files = list(LATEX_DIR.glob('*.tex'))

# Loop through the found .tex files and compile them into PDFs
for latex_file in latex_files:
    # Define the output PDF path
    pdf_path = LATEX_DIR / f"{latex_file.stem}.pdf"

    # Compile the LaTeX file into a PDF using the pdflatex command
    # The --output-directory option is used to specify where the PDF will be saved
    # This command may need to be adjusted depending on your LaTeX setup and file requirements
    subprocess.run(['pdflatex', '-interaction=nonstopmode', '-output-directory', str(LATEX_DIR), str(latex_file)], check=True)

    print(f"Compiled {latex_file.name} to PDF.")

print("All LaTeX files have been compiled to PDFs.")
