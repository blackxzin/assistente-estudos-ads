import json

import pytest

from app.ia.provedor_falso import ProvedorFalso


@pytest.mark.asyncio
async def test_gerar_texto_para_prompt_de_simulado_retorna_json_valido():
    provedor = ProvedorFalso(dimensao_embedding=8)
    prompt = (
        "Crie exatamente 3 questões de múltipla escolha, baseadas SOMENTE nos trechos abaixo. "
        'Responda APENAS com um JSON no formato {"questoes": [...]}.\n\n'
        "Trechos:\n[trecho id=10] conteúdo do trecho dez\n[trecho id=11] conteúdo do trecho onze"
    )

    resposta = await provedor.gerar_texto(prompt)
    dados = json.loads(resposta)

    assert len(dados["questoes"]) == 3
    for questao in dados["questoes"]:
        assert len(questao["alternativas"]) == 4
        assert questao["trecho_id"] in (10, 11)


@pytest.mark.asyncio
async def test_gerar_texto_para_prompt_de_resumo_retorna_topicos():
    provedor = ProvedorFalso(dimensao_embedding=8)
    prompt = "Resuma o texto abaixo em tópicos objetivos:\n\nConteúdo qualquer do material."

    resposta = await provedor.gerar_texto(prompt)

    assert resposta.startswith("-")


@pytest.mark.asyncio
async def test_gerar_texto_generico_para_outros_prompts():
    provedor = ProvedorFalso(dimensao_embedding=8)

    resposta = await provedor.gerar_texto("Responda a pergunta do usuário usando os trechos.")

    assert "[resposta falsa]" in resposta
