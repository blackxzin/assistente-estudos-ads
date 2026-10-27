from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.uso_ia import UsoIA


class UsoIARepositorio:
    def __init__(self, sessao: AsyncSession):
        self.sessao = sessao

    async def incrementar_uso_do_dia(self, usuario_id: int) -> int:
        """Incrementa (ou cria) o contador de uso de IA do usuário hoje e retorna o novo total."""
        hoje = date.today()
        resultado = await self.sessao.execute(
            select(UsoIA).where(UsoIA.usuario_id == usuario_id, UsoIA.data == hoje).with_for_update()
        )
        uso = resultado.scalar_one_or_none()

        if uso is None:
            uso = UsoIA(usuario_id=usuario_id, data=hoje, contagem=1)
            self.sessao.add(uso)
        else:
            uso.contagem += 1

        await self.sessao.commit()
        await self.sessao.refresh(uso)
        return uso.contagem
