from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import configuracoes
from app.core.erros import registrar_tratadores_de_erro
from app.routers import auth, disciplinas, materiais, painel, prazos, revisoes, saude, simulados


def create_app() -> FastAPI:
    """Monta a aplicação FastAPI e registra routers e tratadores de erro."""
    app = FastAPI(title="Assistente de Estudos ADS")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=configuracoes.origens_cors,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    registrar_tratadores_de_erro(app)
    app.include_router(saude.router)
    app.include_router(auth.router)
    app.include_router(disciplinas.router)
    app.include_router(prazos.router)
    app.include_router(materiais.router)
    app.include_router(simulados.router)
    app.include_router(revisoes.router)
    app.include_router(painel.router)
    return app


app = create_app()
