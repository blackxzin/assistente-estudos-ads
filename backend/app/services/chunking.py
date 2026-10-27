def dividir_em_trechos(texto: str, tamanho_maximo: int, sobreposicao: int) -> list[str]:
    """Divide um texto em trechos de até `tamanho_maximo` caracteres, com sobreposição entre eles."""
    texto = texto.strip()
    if not texto:
        return []

    trechos = []
    inicio = 0
    tamanho_total = len(texto)

    while inicio < tamanho_total:
        fim = min(inicio + tamanho_maximo, tamanho_total)
        trechos.append(texto[inicio:fim])
        if fim == tamanho_total:
            break
        inicio = fim - sobreposicao

    return trechos
