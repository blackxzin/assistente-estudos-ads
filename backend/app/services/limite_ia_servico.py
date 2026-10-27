from app.config import configuracoes
from app.core.erros import LimiteIAExcedido
from app.repositories.uso_ia_repositorio import UsoIARepositorio


class LimiteIAServico:
    def __init__(self, repositorio: UsoIARepositorio):
        self.repositorio = repositorio

    async def verificar_e_registrar(self, usuario_id: int) -> None:
        """Conta o uso de hoje e bloqueia quando o usuário estoura o limite diário de IA."""
        contagem = await self.repositorio.incrementar_uso_do_dia(usuario_id)
        if contagem > configuracoes.LIMITE_IA_DIARIO:
            raise LimiteIAExcedido()
