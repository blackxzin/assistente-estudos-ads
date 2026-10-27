from datetime import date

from app.core.erros import NaoEncontrado
from app.models.revisao import Revisao, StatusRevisao
from app.repositories.material_repositorio import MaterialRepositorio
from app.repositories.prazo_repositorio import PrazoRepositorio
from app.repositories.revisao_repositorio import RevisaoRepositorio
from app.services.repeticao_espacada import ajustar_data_existente, primeira_revisao, proxima_revisao


class RevisaoServico:
    def __init__(
        self,
        repositorio_revisao: RevisaoRepositorio,
        repositorio_prazo: PrazoRepositorio,
        repositorio_material: MaterialRepositorio,
    ):
        self.repositorio_revisao = repositorio_revisao
        self.repositorio_prazo = repositorio_prazo
        self.repositorio_material = repositorio_material

    async def agendar_inicial(self, material_id: int, disciplina_id: int) -> Revisao:
        """Agenda a primeira revisão de um material assim que ele fica pronto."""
        data_prova = await self._data_da_prova(disciplina_id)
        data_prevista, etapa = primeira_revisao(date.today(), data_prova)
        return await self.repositorio_revisao.criar(material_id, data_prevista, etapa)

    async def reagendar_pendentes_da_disciplina(self, disciplina_id: int) -> None:
        """Reencaixa as revisões pendentes da disciplina quando a data da prova muda."""
        data_prova = await self._data_da_prova(disciplina_id)
        hoje = date.today()
        pendentes = await self.repositorio_revisao.listar_pendentes_por_disciplina(disciplina_id)

        for revisao in pendentes:
            nova_data = ajustar_data_existente(revisao.data_prevista, data_prova, hoje)
            if nova_data != revisao.data_prevista:
                await self.repositorio_revisao.atualizar(revisao, {"data_prevista": nova_data})

    async def concluir(self, revisao_id: int, usuario_id: int, desempenho: str) -> Revisao:
        revisao = await self.repositorio_revisao.buscar_por_id_e_usuario(revisao_id, usuario_id)
        if revisao is None:
            raise NaoEncontrado("Revisão não encontrada")

        material = await self.repositorio_material.buscar_por_id(revisao.material_id)
        data_prova = await self._data_da_prova(material.disciplina_id)

        data_prevista, nova_etapa = proxima_revisao(date.today(), revisao.etapa, desempenho, data_prova)
        revisao_concluida = await self.repositorio_revisao.atualizar(revisao, {"status": StatusRevisao.FEITA})
        await self.repositorio_revisao.criar(revisao.material_id, data_prevista, nova_etapa)

        return revisao_concluida

    async def _data_da_prova(self, disciplina_id: int) -> date | None:
        prova = await self.repositorio_prazo.buscar_prova_mais_proxima(disciplina_id)
        return prova.data if prova is not None else None
