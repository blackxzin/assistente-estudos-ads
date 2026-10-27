ASSINATURA_PDF = b"%PDF-"


def eh_pdf_valido(conteudo: bytes) -> bool:
    """Confere a assinatura (magic bytes) de um PDF, além do content-type informado pelo cliente."""
    return conteudo.startswith(ASSINATURA_PDF)


def decodificar_texto_utf8(conteudo: bytes) -> str | None:
    """Decodifica bytes como UTF-8; retorna None se não for um texto UTF-8 válido."""
    try:
        return conteudo.decode("utf-8")
    except UnicodeDecodeError:
        return None
