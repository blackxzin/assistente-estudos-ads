import json
import re

from pydantic import ValidationError

from app.core.erros import ErroAplicacao, NaoEncontrado
from app.ia.provedor import ProvedorIA
from app.models.simulado import Simulado
from app.repositories.material_repositorio import MaterialRepositorio
from app.repositories.simulado_repositorio import SimuladoRepositorio
from app.repositories.trecho_repositorio import TrechoRepositorio
from app.schemas.simulado import CorrecaoResposta, QuestaoGerada, SimuladoGerado
from app.services.correcao_simulado import corrigir_simulado

MAX_TENTATIVAS_GERACAO = 3


def _extrair_json(texto: str) -> str:
    """Remove cercas de código (```json ... ```) que o LLM costuma adicionar ao redor do JSON."""
    texto = texto.strip()
    bloco = re.search(r"```(?:json)?\s*(.*?)\s*```", texto, re.DOTALL)
    return bloco.group(1) if bloco else texto


def _montar_prompt(trechos: list, quantidade: int) -> str:
    contexto = "\n\n".join(f"[trecho id={trecho.id}] {trecho.conteudo}" for trecho in trechos)
    return (
        f"Crie exatamente {quantidade} questões de múltipla escolha, baseadas SOMENTE nos trechos abaixo. "
        "Cada questão deve ter 4 alternativas, indicar o índice (0 a 3) da alternativa correta, uma "
        "explicação da resposta e o id do trecho em que se baseou (campo trecho_id, com um dos ids "
        "informados). Responda APENAS com um JSON no formato "
        '{"questoes": [{"enunciado": "...", "alternativas": ["...", "...", "...", "..."], '
        '"correta": 0, "explicacao": "...", "trecho_id": 1}]}, sem texto fora do JSON.\n\n'
        f"Trechos:\n{contexto}"
    )


class SimuladoServico:
    def __init__(
        self,
        repositorio_simulado: SimuladoRepositorio,
        repositorio_trecho: TrechoRepositorio,
        repositorio_material: MaterialRepositorio,
        provedor_texto: ProvedorIA,
    ):
        self.repositorio_simulado = repositorio_simulado
        self.repositorio_trecho = repositorio_trecho
        self.repositorio_material = repositorio_material
        self.provedor_texto = provedor_texto

    async def gerar(self, material_id: int, usuario_id: int, quantidade: int) -> Simulado:
        material = await self.repositorio_material.buscar_por_id_e_usuario(material_id, usuario_id)
        if material is None:
            raise NaoEncontrado("Material não encontrado")

        trechos = await self.repositorio_trecho.listar_por_material(material_id)
        if not trechos:
            raise ErroAplicacao("Material ainda não possui conteúdo processado", status_code=400)

        questoes = await self._gerar_questoes_validadas(trechos, quantidade)
        return await self.repositorio_simulado.criar(material_id, questoes)

    async def _gerar_questoes_validadas(self, trechos: list, quantidade: int) -> list[QuestaoGerada]:
        ids_validos = {trecho.id for trecho in trechos}
        prompt = _montar_prompt(trechos, quantidade)
        ultimo_erro: Exception | None = None

        for _tentativa in range(MAX_TENTATIVAS_GERACAO):
            texto_resposta = await self.provedor_texto.gerar_texto(prompt)
            try:
                dados = json.loads(_extrair_json(texto_resposta))
                questoes = SimuladoGerado.model_validate(dados).questoes
            except (json.JSONDecodeError, ValidationError) as erro:
                ultimo_erro = erro
                continue

            for questao in questoes:
                if questao.trecho_id not in ids_validos:
                    questao.trecho_id = None
            return questoes

        raise ErroAplicacao(
            "Não foi possível gerar o simulado agora, tente novamente", status_code=502
        ) from ultimo_erro

    async def corrigir(
        self, simulado_id: int, usuario_id: int, respostas: list[tuple[int, int]]
    ) -> CorrecaoResposta:
        simulado = await self.repositorio_simulado.buscar_por_id_e_usuario(simulado_id, usuario_id)
        if simulado is None:
            raise NaoEncontrado("Simulado não encontrado")

        respostas_por_questao = dict(respostas)
        nota, acertos, total, itens = corrigir_simulado(simulado.questoes, respostas_por_questao)

        respostas_para_salvar = [
            (item["questao_id"], item["escolhida"], item["acertou"]) for item in itens
        ]
        await self.repositorio_simulado.salvar_correcao(simulado, nota, respostas_para_salvar)

        return CorrecaoResposta(nota=nota, acertos=acertos, total=total, itens=itens)
