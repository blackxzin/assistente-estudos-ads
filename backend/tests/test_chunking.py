from app.services.chunking import dividir_em_trechos


def test_texto_vazio_retorna_lista_vazia():
    assert dividir_em_trechos("", tamanho_maximo=100, sobreposicao=10) == []


def test_texto_menor_que_tamanho_maximo_retorna_um_unico_trecho():
    assert dividir_em_trechos("curto", tamanho_maximo=100, sobreposicao=10) == ["curto"]


def test_divide_texto_maior_que_tamanho_maximo_em_varios_trechos():
    texto = "a" * 2500
    trechos = dividir_em_trechos(texto, tamanho_maximo=1000, sobreposicao=200)

    assert len(trechos) == 3
    assert all(len(trecho) <= 1000 for trecho in trechos)


def test_trechos_consecutivos_mantem_sobreposicao():
    texto = "0123456789" * 3
    trechos = dividir_em_trechos(texto, tamanho_maximo=10, sobreposicao=3)

    assert trechos[0][-3:] == trechos[1][:3]
