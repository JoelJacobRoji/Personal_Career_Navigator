from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pathlib import Path

def text_to_pdf(text_file, pdf_file):
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter
    y = height - 50  # start near top

    with open(text_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            c.drawString(50, y, line)
            y -= 14  # move down each line
            if y < 50:  # new page if close to bottom
                c.showPage()
                y = height - 50

    c.save()
    print(f"PDF created at: {pdf_file}")

if __name__ == "__main__":
    base = Path(__file__).parent
    txt_path = base / "sample_data" / "sample_linkedin_content.txt"
    pdf_path = base / "sample_data" / "sample_linkedin.pdf"

    text_to_pdf(txt_path, pdf_path)
