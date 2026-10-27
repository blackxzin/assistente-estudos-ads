from app.config import configuracoes
from app.core.erros import NaoEncontrado
from app.ia.provedor import ProvedorIA
from app.models.material import Material, StatusMaterial, TipoMaterial
from app.repositories.disciplina_repositorio import DisciplinaRepositorio
from app.repositories.material_repositorio import MaterialRepositorio
from app.repositories.trecho_repositorio import TrechoRepositorio
from app.services.chunking import dividir_em_trechos
from app.services.extracao_pdf import extrair_paginas_pdf


class MaterialServico:
    def __init__(
        self,
        repositorio_material: MaterialRepositorio,
        repositorio_trecho: TrechoRepositorio | None = None,
        repositorio_disciplina: DisciplinaRepositorio | None = None,
        provedor_embedding: ProvedorIA | None = None,
    ):
        self.repositorio_material = repositorio_material
        self.repositorio_trecho = repositorio_trecho
        self.repositorio_disciplina = repositorio_disciplina
        self.provedor_embedding = provedor_embedding

    async def criar_a_partir_de_pdf(
        self, disciplina_id: int, usuario_id: int, titulo: str, conteudo_bytes: bytes
    ) -> Material:
        await self._garantir_disciplina_do_usuario(disciplina_id, usuario_id)
        material = await self.repositorio_material.criar(disciplina_id, titulo, TipoMaterial.PDF)
        return await self._processar(material, extrair_paginas_pdf(conteudo_bytes))

    async def criar_a_partir_de_texto(
        self, disciplina_id: int, usuario_id: int, titulo: str, texto: str
    ) -> Material:
        await self._garantir_disciplina_do_usuario(disciplina_id, usuario_id)
        material = await self.repositorio_material.criar(disciplina_id, titulo, TipoMaterial.TEXTO)
        return await self._processar(material, [(None, texto)])

    async def _processar(self, material: Material, paginas: list[tuple[int | None, str]]) -> Material:
        try:
            posicao = 0
            for pagina, texto_pagina in paginas:
                for trecho_texto in dividir_em_trechos(
                    texto_pagina, configuracoes.TAMANHO_TRECHO, configuracoes.SOBREPOSICAO_TRECHO
                ):
                    if not trecho_texto.strip():
                        continue
                    embedding = await self.provedor_embedding.gerar_embedding(trecho_texto)
                    await self.repositorio_trecho.criar(material.id, trecho_texto, pagina, posicao, embedding)
                    posicao += 1
            return await self.repositorio_material.atualizar(material, {"status": StatusMaterial.PRONTO})
        except Exception:
            return await self.repositorio_material.atualizar(material, {"status": StatusMaterial.ERRO})

    async def listar(self, disciplina_id: int, usuario_id: int) -> list[Material]:
        await self._garantir_disciplina_do_usuario(disciplina_id, usuario_id)
        return await self.repositorio_material.listar_por_disciplina(disciplina_id)

    async def obter(self, material_id: int, usuario_id: int) -> Material:
        material = await self.repositorio_material.buscar_por_id_e_usuario(material_id, usuario_id)
        if material is None:
            raise NaoEncontrado("Material não encontrado")
        return material

    async def remover(self, material_id: int, usuario_id: int) -> None:
        material = await self.obter(material_id, usuario_id)
        await self.repositorio_material.remover(material)

    async def _garantir_disciplina_do_usuario(self, disciplina_id: int, usuario_id: int) -> None:
        disciplina = await self.repositorio_disciplina.buscar_por_id_e_usuario(disciplina_id, usuario_id)
        if disciplina is None:
            raise NaoEncontrado("Disciplina não encontrada")
