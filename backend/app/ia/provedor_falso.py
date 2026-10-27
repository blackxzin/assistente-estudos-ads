import hashlib
import json
import random
import re


def _gerar_questoes_falsas(prompt: str) -> str:
    """Monta um JSON de simulado válido, reaproveitando os ids de trecho citados no prompt."""
    casamento_quantidade = re.search(r"Crie exatamente (\d+)", prompt)
    quantidade = int(casamento_quantidade.group(1)) if casamento_quantidade else 1
    ids_trechos = re.findall(r"\[trecho id=(\d+)\]", prompt)

    questoes = []
    for indice in range(quantidade):
        trecho_id = int(ids_trechos[indice % len(ids_trechos)]) if ids_trechos else None
        questoes.append(
            {
                "enunciado": f"Pergunta {indice + 1} sobre o material?",
                "alternativas": ["Alternativa A", "Alternativa B", "Alternativa C", "Alternativa D"],
                "correta": 0,
                "explicacao": f"Explicação da questão {indice + 1}, baseada no trecho citado.",
                "trecho_id": trecho_id,
            }
        )

    return json.dumps({"questoes": questoes})


class ProvedorFalso:
    """Provedor determinístico usado nos testes e em IA_PROVEDOR=falso. Nunca chama uma API real."""

    def __init__(self, dimensao_embedding: int):
        self.dimensao_embedding = dimensao_embedding

    async def gerar_texto(self, prompt: str) -> str:
        if "Crie exatamente" in prompt and "questoes" in prompt:
            return _gerar_questoes_falsas(prompt)

        if "Resuma o texto abaixo" in prompt:
            return "- Ponto principal 1\n- Ponto principal 2\n- Ponto principal 3"

        return f"[resposta falsa] {prompt[:120]}"

    async def gerar_embedding(self, texto: str) -> list[float]:
        semente = int(hashlib.sha256(texto.encode("utf-8")).hexdigest(), 16)
        gerador = random.Random(semente)
        return [gerador.uniform(-1, 1) for _ in range(self.dimensao_embedding)]
