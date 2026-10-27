from app.core.erros import NaoEncontrado
from app.models.disciplina import Disciplina
from app.repositories.disciplina_repositorio import DisciplinaRepositorio
from app.schemas.disciplina import DisciplinaAtualizacao, DisciplinaCriacao


class DisciplinaServico:
    def __init__(self, repositorio: DisciplinaRepositorio):
        self.repositorio = repositorio

    async def criar(self, usuario_id: int, dados: DisciplinaCriacao) -> Disciplina:
        return await self.repositorio.criar(usuario_id, dados.nome, dados.professor, dados.cor)

    async def listar(self, usuario_id: int) -> list[Disciplina]:
        return await self.repositorio.listar_por_usuario(usuario_id)

    async def obter(self, disciplina_id: int, usuario_id: int) -> Disciplina:
        disciplina = await self.repositorio.buscar_por_id_e_usuario(disciplina_id, usuario_id)
        if disciplina is None:
            raise NaoEncontrado("Disciplina não encontrada")
        return disciplina

    async def atualizar(
        self, disciplina_id: int, usuario_id: int, dados: DisciplinaAtualizacao
    ) -> Disciplina:
        disciplina = await self.obter(disciplina_id, usuario_id)
        campos = dados.model_dump(exclude_unset=True)
        return await self.repositorio.atualizar(disciplina, campos)

    async def remover(self, disciplina_id: int, usuario_id: int) -> None:
        disciplina = await self.obter(disciplina_id, usuario_id)
        await self.repositorio.remover(disciplina)
