from app.models.base import Base
from app.models.disciplina import Disciplina
from app.models.material import Material, StatusMaterial, TipoMaterial
from app.models.prazo import Prazo
from app.models.questao import Questao
from app.models.resposta_simulado import RespostaSimulado
from app.models.revisao import Revisao, StatusRevisao
from app.models.simulado import Simulado
from app.models.trecho import Trecho
from app.models.uso_ia import UsoIA
from app.models.usuario import Usuario

__all__ = [
    "Base",
    "Disciplina",
    "Material",
    "Prazo",
    "Questao",
    "RespostaSimulado",
    "Revisao",
    "Simulado",
    "StatusMaterial",
    "StatusRevisao",
    "Trecho",
    "TipoMaterial",
    "UsoIA",
    "Usuario",
]
