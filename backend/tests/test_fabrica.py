from app.config import configuracoes
from app.ia.fabrica import obter_provedor_embedding, obter_provedor_texto
from app.ia.provedor_anthropic import ProvedorAnthropic
from app.ia.provedor_falso import ProvedorFalso
from app.ia.provedor_openai import ProvedorOpenAI


def test_fabrica_texto_falso(monkeypatch):
    monkeypatch.setattr(configuracoes, "IA_PROVEDOR", "falso")
    assert isinstance(obter_provedor_texto(), ProvedorFalso)


def test_fabrica_texto_anthropic(monkeypatch):
    monkeypatch.setattr(configuracoes, "IA_PROVEDOR", "anthropic")
    assert isinstance(obter_provedor_texto(), ProvedorAnthropic)


def test_fabrica_texto_openai_por_padrao(monkeypatch):
    monkeypatch.setattr(configuracoes, "IA_PROVEDOR", "openai")
    assert isinstance(obter_provedor_texto(), ProvedorOpenAI)


def test_fabrica_embedding_falso(monkeypatch):
    monkeypatch.setattr(configuracoes, "EMBEDDING_PROVEDOR", "falso")
    assert isinstance(obter_provedor_embedding(), ProvedorFalso)


def test_fabrica_embedding_openai_por_padrao(monkeypatch):
    monkeypatch.setattr(configuracoes, "EMBEDDING_PROVEDOR", "openai")
    assert isinstance(obter_provedor_embedding(), ProvedorOpenAI)
