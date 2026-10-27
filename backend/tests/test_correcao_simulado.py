from dataclasses import dataclass

from app.services.correcao_simulado import corrigir_simulado


@dataclass
class _QuestaoFalsa:
    id: int
    enunciado: str
    alternativas: list[str]
    correta: int
    explicacao: str
    trecho_id: int | None = None


def _questoes(quantidade: int) -> list[_QuestaoFalsa]:
    return [
        _QuestaoFalsa(id=i, enunciado=f"Q{i}", alternativas=["A", "B", "C", "D"], correta=0, explicacao="exp")
        for i in range(quantidade)
    ]


def test_todas_corretas_da_nota_dez():
    questoes = _questoes(4)
    respostas = {q.id: 0 for q in questoes}

    nota, acertos, total, _itens = corrigir_simulado(questoes, respostas)

    assert nota == 10.0
    assert acertos == 4
    assert total == 4


def test_todas_erradas_da_nota_zero():
    questoes = _questoes(4)
    respostas = {q.id: 3 for q in questoes}

    nota, acertos, _total, _itens = corrigir_simulado(questoes, respostas)

    assert nota == 0.0
    assert acertos == 0


def test_metade_correta_da_nota_cinco():
    questoes = _questoes(4)
    respostas = {questoes[0].id: 0, questoes[1].id: 0, questoes[2].id: 3, questoes[3].id: 3}

    nota, acertos, _total, _itens = corrigir_simulado(questoes, respostas)

    assert acertos == 2
    assert nota == 5.0


def test_questao_sem_resposta_conta_como_errada_e_escolhida_e_none():
    questoes = _questoes(1)

    nota, acertos, _total, itens = corrigir_simulado(questoes, respostas_por_questao={})

    assert acertos == 0
    assert nota == 0.0
    assert itens[0]["escolhida"] is None
    assert itens[0]["acertou"] is False


def test_lista_vazia_de_questoes_da_nota_zero_sem_erro():
    nota, acertos, total, itens = corrigir_simulado([], {})

    assert nota == 0.0
    assert acertos == 0
    assert total == 0
    assert itens == []


def test_itens_preservam_dados_da_questao():
    questoes = _questoes(1)
    questoes[0].trecho_id = 42

    _nota, _acertos, _total, itens = corrigir_simulado(questoes, {questoes[0].id: 0})

    item = itens[0]
    assert item["questao_id"] == questoes[0].id
    assert item["enunciado"] == questoes[0].enunciado
    assert item["alternativas"] == questoes[0].alternativas
    assert item["correta"] == questoes[0].correta
    assert item["explicacao"] == questoes[0].explicacao
    assert item["trecho_id"] == 42
