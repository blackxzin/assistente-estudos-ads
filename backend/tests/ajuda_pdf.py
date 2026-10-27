from io import BytesIO

from reportlab.pdfgen import canvas


def gerar_pdf_bytes(linhas: list[str]) -> bytes:
    """Gera um PDF simples e real (via reportlab), usado só nos testes de extração."""
    buffer = BytesIO()
    desenho = canvas.Canvas(buffer)
    y = 700
    for linha in linhas:
        desenho.drawString(72, y, linha)
        y -= 20
    desenho.showPage()
    desenho.save()
    return buffer.getvalue()
