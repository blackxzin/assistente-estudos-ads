from app.core.erros import NaoEncontrado
from app.ia.provedor import ProvedorIA
from app.models.material import Material
from app.repositories.material_repositorio import MaterialRepositorio
from app.repositories.trecho_repositorio import TrechoRepositorio


class ResumoServico:
    def __init__(
        self,
        repositorio_material: MaterialRepositorio,
        repositorio_trecho: TrechoRepositorio,
        provedor_texto: ProvedorIA,
    ):
        self.repositorio_material = repositorio_material
        self.repositorio_trecho = repositorio_trecho
        self.provedor_texto = provedor_texto

    async def gerar_resumo(self, material_id: int, usuario_id: int) -> Material:
        material = await self.repositorio_material.buscar_por_id_e_usuario(material_id, usuario_id)
        if material is None:
            raise NaoEncontrado("Material não encontrado")

        trechos = await self.repositorio_trecho.listar_por_material(material_id)
        texto_completo = "\n".join(trecho.conteudo for trecho in trechos)
        prompt = f"Resuma o texto abaixo em tópicos objetivos:\n\n{texto_completo}"
        resumo = await self.provedor_texto.gerar_texto(prompt)

        return await self.repositorio_material.atualizar(material, {"resumo": resumo})
