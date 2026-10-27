from app.repositories.prazo_repositorio import PrazoRepositorio
from app.repositories.revisao_repositorio import RevisaoRepositorio
from app.repositories.simulado_repositorio import SimuladoRepositorio
from app.schemas.painel import DesempenhoResposta, PainelResposta, PrazoPainelResposta, UltimoSimuladoResposta
from app.schemas.revisao import RevisaoResposta

LIMITE_ULTIMOS_SIMULADOS = 5


class PainelServico:
    def __init__(
        self,
        repositorio_prazo: PrazoRepositorio,
        repositorio_revisao: RevisaoRepositorio,
        repositorio_simulado: SimuladoRepositorio,
    ):
        self.repositorio_prazo = repositorio_prazo
        self.repositorio_revisao = repositorio_revisao
        self.repositorio_simulado = repositorio_simulado

    async def montar(self, usuario_id: int) -> PainelResposta:
        prazos = await self.repositorio_prazo.listar_nao_concluidos_por_usuario(usuario_id)
        revisoes = await self.repositorio_revisao.listar_pendentes_de_hoje_por_usuario(usuario_id)
        media, total = await self.repositorio_simulado.calcular_media_e_total_por_usuario(usuario_id)
        ultimos = await self.repositorio_simulado.listar_corrigidos_por_usuario(
            usuario_id, LIMITE_ULTIMOS_SIMULADOS
        )

        return PainelResposta(
            proximos_prazos=[
                PrazoPainelResposta(
                    id=prazo.id,
                    titulo=prazo.titulo,
                    tipo=prazo.tipo,
                    data=prazo.data,
                    disciplina_nome=nome,
                )
                for prazo, nome in prazos
            ],
            revisoes_hoje=[
                RevisaoResposta(
                    id=revisao.id,
                    material_id=revisao.material_id,
                    material_titulo=titulo,
                    disciplina_nome=nome,
                    data_prevista=revisao.data_prevista,
                    etapa=revisao.etapa,
                    status=revisao.status,
                )
                for revisao, titulo, nome in revisoes
            ],
            desempenho=DesempenhoResposta(
                media_nota=media,
                total_simulados=total,
                ultimos=[
                    UltimoSimuladoResposta(
                        simulado_id=simulado.id,
                        material_titulo=titulo,
                        nota=simulado.nota,
                        data=simulado.corrigido_em.date(),
                    )
                    for simulado, titulo in ultimos
                ],
            ),
        )
