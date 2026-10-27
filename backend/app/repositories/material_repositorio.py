from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.disciplina import Disciplina
from app.models.material import Material, StatusMaterial, TipoMaterial


class MaterialRepositorio:
    def __init__(self, sessao: AsyncSession):
        self.sessao = sessao

    async def criar(self, disciplina_id: int, titulo: str, tipo: TipoMaterial) -> Material:
        material = Material(
            disciplina_id=disciplina_id,
            titulo=titulo,
            tipo=tipo,
            status=StatusMaterial.PROCESSANDO,
        )
        self.sessao.add(material)
        await self.sessao.commit()
        await self.sessao.refresh(material)
        return material

    async def listar_por_disciplina(self, disciplina_id: int) -> list[Material]:
        resultado = await self.sessao.execute(select(Material).where(Material.disciplina_id == disciplina_id))
        return list(resultado.scalars().all())

    async def buscar_por_id(self, material_id: int) -> Material | None:
        resultado = await self.sessao.execute(select(Material).where(Material.id == material_id))
        return resultado.scalar_one_or_none()

    async def buscar_por_id_e_usuario(self, material_id: int, usuario_id: int) -> Material | None:
        resultado = await self.sessao.execute(
            select(Material)
            .join(Disciplina, Material.disciplina_id == Disciplina.id)
            .where(Material.id == material_id, Disciplina.usuario_id == usuario_id)
        )
        return resultado.scalar_one_or_none()

    async def atualizar(self, material: Material, dados: dict) -> Material:
        for campo, valor in dados.items():
            setattr(material, campo, valor)
        await self.sessao.commit()
        await self.sessao.refresh(material)
        return material

    async def remover(self, material: Material) -> None:
        await self.sessao.delete(material)
        await self.sessao.commit()
