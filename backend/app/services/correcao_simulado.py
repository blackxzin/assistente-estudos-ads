from typing import Protocol


class QuestaoCorrigivel(Protocol):
    id: int
    enunciado: str
    alternativas: list[str]
    correta: int
    explicacao: str
    trecho_id: int | None


def corrigir_simulado(
    questoes: list[QuestaoCorrigivel], respostas_por_questao: dict[int, int]
) -> tuple[float, int, int, list[dict]]:
    """Corrige um simulado a partir das questões e das respostas escolhidas. Função pura, sem I/O."""
    itens = []
    acertos = 0

    for questao in questoes:
        escolhida = respostas_por_questao.get(questao.id)
        acertou = escolhida == questao.correta
        if acertou:
            acertos += 1

        itens.append(
            {
                "questao_id": questao.id,
                "enunciado": questao.enunciado,
                "alternativas": questao.alternativas,
                "escolhida": escolhida,
                "correta": questao.correta,
                "acertou": acertou,
                "explicacao": questao.explicacao,
                "trecho_id": questao.trecho_id,
            }
        )

    total = len(questoes)
    nota = round((acertos / total) * 10, 2) if total else 0.0
    return nota, acertos, total, itens
