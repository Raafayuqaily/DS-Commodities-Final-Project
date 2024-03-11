"""
This script compiles a LaTeX file into a PDF document using the pdflatex engine. It takes the path to a LaTeX file as an input argument, converts it to PDF, and saves the output in the same location with the same name but with a .pdf extension. If the compilation fails, it provides error messages and exits. The script is designed to be used as a standalone tool or integrated into a larger LaTeX project workflow.
"""

from pathlib import Path
import subprocess
import sys

latex_path = "reports/Final_Report.tex"

def latex_to_document(latex_file):
    """
    This function uses the 'pdflatex' command to compile a LaTeX file specified by 'latex_file' into a PDF. 
    It checks for compilation success and informs the user of the outcome. If there are compilation errors, 
    it provides a message to check the log file for details.
    """
    output_pdf = Path(latex_file).with_suffix('.pdf')
    try:
        # Attempt to compile the LaTeX file into a PDF
        result = subprocess.run(['pdflatex', '-interaction=nonstopmode', str(latex_file)], check=True, capture_output=True)
        print(result.stdout.decode())
        print(result.stderr.decode())
    except subprocess.CalledProcessError as e:
        print(e.output.decode())
        print(f"Compilation errors in {latex_file}. Check the log file for details.")
        return  # Exit the function if compilation failed

    # Check if the PDF was created successfully
    if not output_pdf.exists():
        print(f"Looking for PDF at: {output_pdf}")
        raise FileNotFoundError(f"Failed to create the PDF {output_pdf}. Check your LaTeX file for errors.")
    else:
        print(f"Successfully created {output_pdf}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python latex_to_document.py <latex_file.tex>")
        sys.exit(1)

    latex_file_path = sys.argv[1]
    latex_to_document(latex_file_path)