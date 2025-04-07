from fpdf import FPDF

def get_text_file(file_path):
    if not file_path.endswith('.txt'):
        raise ValueError("Only .txt files are supported.")
    with open(file_path, 'r', encoding="utf-8") as f:
        return f.read()

def create_file(data, output_path):
    if output_path.endswith(".pdf"):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=10)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for line in data.splitlines():
            safe_line = line.encode("latin-1", "replace").decode("latin-1")
            pdf.cell(0, 10, txt=safe_line, ln=True)

        pdf.output(output_path)
    else:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(data)
