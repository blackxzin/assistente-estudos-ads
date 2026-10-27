from io import BytesIO

from pypdf import PdfReader


def extrair_paginas_pdf(conteudo_bytes: bytes) -> list[tuple[int, str]]:
    """Extrai o texto de cada página de um PDF, numerando a partir de 1."""
    leitor = PdfReader(BytesIO(conteudo_bytes))
    return [(indice + 1, pagina.extract_text() or "") for indice, pagina in enumerate(leitor.pages)]
