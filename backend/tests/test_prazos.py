import pytest


async def _cadastrar_e_logar(cliente, email):
    dados = {"nome": "Usuario Teste", "email": email, "senha": "senha1234"}
    await cliente.post("/auth/cadastro", json=dados)
    login = await cliente.post("/auth/login", json={"email": email, "senha": dados["senha"]})
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


async def _criar_disciplina(cliente, cabecalhos, nome="Disciplina Teste"):
    resposta = await cliente.post("/disciplinas", json={"nome": nome}, headers=cabecalhos)
    return resposta.json()["id"]


@pytest.mark.asyncio
async def test_criar_e_listar_prazo(cliente):
    cabecalhos = await _cadastrar_e_logar(cliente, "prazo1@exemplo.com")
    disciplina_id = await _criar_disciplina(cliente, cabecalhos)

    resposta_criacao = await cliente.post(
        f"/disciplinas/{disciplina_id}/prazos",
        json={"titulo": "Prova 1", "tipo": "prova", "data": "2026-12-01"},
        headers=cabecalhos,
    )
    assert resposta_criacao.status_code == 201
    assert resposta_criacao.json()["concluido"] is False

    resposta_lista = await cliente.get(f"/disciplinas/{disciplina_id}/prazos", headers=cabecalhos)
    assert resposta_lista.status_code == 200
    assert len(resposta_lista.json()) == 1


@pytest.mark.asyncio
async def test_atualizar_e_remover_prazo(cliente):
    cabecalhos = await _cadastrar_e_logar(cliente, "prazo2@exemplo.com")
    disciplina_id = await _criar_disciplina(cliente, cabecalhos)
    criado = await cliente.post(
        f"/disciplinas/{disciplina_id}/prazos",
        json={"titulo": "Trabalho 1", "tipo": "trabalho", "data": "2026-11-15"},
        headers=cabecalhos,
    )
    prazo_id = criado.json()["id"]

    atualizado = await cliente.put(
        f"/prazos/{prazo_id}", json={"concluido": True}, headers=cabecalhos
    )
    assert atualizado.status_code == 200
    assert atualizado.json()["concluido"] is True

    removido = await cliente.delete(f"/prazos/{prazo_id}", headers=cabecalhos)
    assert removido.status_code == 204


@pytest.mark.asyncio
async def test_prazo_de_outro_usuario_retorna_404(cliente):
    cabecalhos_a = await _cadastrar_e_logar(cliente, "prazo3@exemplo.com")
    cabecalhos_b = await _cadastrar_e_logar(cliente, "prazo4@exemplo.com")
    disciplina_id = await _criar_disciplina(cliente, cabecalhos_a)
    criado = await cliente.post(
        f"/disciplinas/{disciplina_id}/prazos",
        json={"titulo": "Prova X", "tipo": "prova", "data": "2026-10-01"},
        headers=cabecalhos_a,
    )
    prazo_id = criado.json()["id"]

    resposta = await cliente.put(
        f"/prazos/{prazo_id}", json={"concluido": True}, headers=cabecalhos_b
    )
    assert resposta.status_code == 404

    resposta_delete = await cliente.delete(f"/prazos/{prazo_id}", headers=cabecalhos_b)
    assert resposta_delete.status_code == 404


@pytest.mark.asyncio
async def test_criar_prazo_para_disciplina_de_outro_usuario_retorna_404(cliente):
    cabecalhos_a = await _cadastrar_e_logar(cliente, "prazo5@exemplo.com")
    cabecalhos_b = await _cadastrar_e_logar(cliente, "prazo6@exemplo.com")
    disciplina_de_a = await _criar_disciplina(cliente, cabecalhos_a)

    resposta = await cliente.post(
        f"/disciplinas/{disciplina_de_a}/prazos",
        json={"titulo": "Prova intrusa", "tipo": "prova", "data": "2026-12-01"},
        headers=cabecalhos_b,
    )

    assert resposta.status_code == 404


@pytest.mark.asyncio
async def test_listar_prazos_de_disciplina_de_outro_usuario_retorna_404(cliente):
    cabecalhos_a = await _cadastrar_e_logar(cliente, "prazo7@exemplo.com")
    cabecalhos_b = await _cadastrar_e_logar(cliente, "prazo8@exemplo.com")
    disciplina_de_a = await _criar_disciplina(cliente, cabecalhos_a)

    resposta = await cliente.get(f"/disciplinas/{disciplina_de_a}/prazos", headers=cabecalhos_b)

    assert resposta.status_code == 404


@pytest.mark.asyncio
async def test_criar_prazo_em_disciplina_inexistente_retorna_404(cliente):
    cabecalhos = await _cadastrar_e_logar(cliente, "prazo9@exemplo.com")

    resposta = await cliente.post(
        "/disciplinas/999999/prazos",
        json={"titulo": "Prova", "tipo": "prova", "data": "2026-12-01"},
        headers=cabecalhos,
    )

    assert resposta.status_code == 404


@pytest.mark.asyncio
async def test_prazo_com_tipo_invalido_retorna_422(cliente):
    cabecalhos = await _cadastrar_e_logar(cliente, "prazo10@exemplo.com")
    disciplina_id = await _criar_disciplina(cliente, cabecalhos)

    resposta = await cliente.post(
        f"/disciplinas/{disciplina_id}/prazos",
        json={"titulo": "Palestra", "tipo": "palestra", "data": "2026-12-01"},
        headers=cabecalhos,
    )

    assert resposta.status_code == 422


@pytest.mark.asyncio
async def test_prazo_com_data_invalida_retorna_422(cliente):
    cabecalhos = await _cadastrar_e_logar(cliente, "prazo11@exemplo.com")
    disciplina_id = await _criar_disciplina(cliente, cabecalhos)

    resposta = await cliente.post(
        f"/disciplinas/{disciplina_id}/prazos",
        json={"titulo": "Prova", "tipo": "prova", "data": "não é uma data"},
        headers=cabecalhos,
    )

    assert resposta.status_code == 422
