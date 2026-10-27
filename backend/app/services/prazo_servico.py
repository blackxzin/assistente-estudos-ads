from app.core.erros import NaoEncontrado
from app.models.prazo import Prazo
from app.repositories.disciplina_repositorio import DisciplinaRepositorio
from app.repositories.prazo_repositorio import PrazoRepositorio
from app.schemas.prazo import PrazoAtualizacao, PrazoCriacao


class PrazoServico:
    def __init__(self, repositorio: PrazoRepositorio, repositorio_disciplina: DisciplinaRepositorio):
        self.repositorio = repositorio
        self.repositorio_disciplina = repositorio_disciplina

    async def _garantir_disciplina_do_usuario(self, disciplina_id: int, usuario_id: int) -> None:
        disciplina = await self.repositorio_disciplina.buscar_por_id_e_usuario(disciplina_id, usuario_id)
        if disciplina is None:
            raise NaoEncontrado("Disciplina não encontrada")

    async def criar(self, disciplina_id: int, usuario_id: int, dados: PrazoCriacao) -> Prazo:
        await self._garantir_disciplina_do_usuario(disciplina_id, usuario_id)
        return await self.repositorio.criar(disciplina_id, dados.titulo, dados.tipo, dados.data)

    async def listar(self, disciplina_id: int, usuario_id: int) -> list[Prazo]:
        await self._garantir_disciplina_do_usuario(disciplina_id, usuario_id)
        return await self.repositorio.listar_por_disciplina(disciplina_id)

    async def obter(self, prazo_id: int, usuario_id: int) -> Prazo:
        prazo = await self.repositorio.buscar_por_id_e_usuario(prazo_id, usuario_id)
        if prazo is None:
            raise NaoEncontrado("Prazo não encontrado")
        return prazo

    async def atualizar(self, prazo_id: int, usuario_id: int, dados: PrazoAtualizacao) -> Prazo:
        prazo = await self.obter(prazo_id, usuario_id)
        campos = dados.model_dump(exclude_unset=True)
        return await self.repositorio.atualizar(prazo, campos)

    async def remover(self, prazo_id: int, usuario_id: int) -> None:
        prazo = await self.obter(prazo_id, usuario_id)
        await self.repositorio.remover(prazo)
