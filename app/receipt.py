from datetime import datetime

from fpdf import FPDF


def generate_receipt_pdf(sale_id: int, created_at: str, items: list[dict], total: float) -> bytes:
    pdf = FPDF(format=(105, 148))  # A6 in mm; nicht als Namens-String unterstuetzt
    pdf.add_page()
    pdf.set_font("helvetica", size=10)

    date_display = datetime.fromisoformat(created_at).strftime("%d.%m.%Y %H:%M")

    pdf.cell(0, 6, "Kassenbon", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(0, 6, f"Beleg-Nr. {sale_id}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Datum: {date_display}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    for item in items:
        line = f"{item['quantity']}x {item['name']}"
        price = f"{item['line_total']:.2f} EUR"
        pdf.cell(0, 6, line, new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 6, price, new_x="LMARGIN", new_y="NEXT", align="R")

    pdf.ln(4)
    pdf.set_font("helvetica", style="B", size=11)
    pdf.cell(0, 6, f"Summe: {total:.2f} EUR", new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())
