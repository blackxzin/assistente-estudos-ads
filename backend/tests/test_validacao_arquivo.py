from app.services.validacao_arquivo import decodificar_texto_utf8, eh_pdf_valido


def test_eh_pdf_valido_aceita_assinatura_correta():
    assert eh_pdf_valido(b"%PDF-1.4\n...resto do arquivo")


def test_eh_pdf_valido_rejeita_conteudo_sem_assinatura():
    assert not eh_pdf_valido(b"isso nao e um pdf")


def test_decodificar_texto_utf8_aceita_texto_valido():
    assert decodificar_texto_utf8("conteúdo em português".encode()) == "conteúdo em português"


def test_decodificar_texto_utf8_rejeita_bytes_invalidos():
    assert decodificar_texto_utf8(b"\xff\xfe\x00\x01") is None
