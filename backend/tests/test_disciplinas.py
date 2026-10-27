import pytest


async def _cadastrar_e_logar(cliente, email):
    dados = {"nome": "Usuario Teste", "email": email, "senha": "senha1234"}
    await cliente.post("/auth/cadastro", json=dados)
    login = await cliente.post("/auth/login", json={"email": email, "senha": dados["senha"]})
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_criar_e_listar_disciplina(cliente):
    cabecalhos = await _cadastrar_e_logar(cliente, "aluno1@exemplo.com")

    resposta_criacao = await cliente.post(
        "/disciplinas",
        json={"nome": "Cálculo I", "professor": "Fulano", "cor": "#ff0000"},
        headers=cabecalhos,
    )
    assert resposta_criacao.status_code == 201

    resposta_lista = await cliente.get("/disciplinas", headers=cabecalhos)
    assert resposta_lista.status_code == 200
    assert len(resposta_lista.json()) == 1


@pytest.mark.asyncio
async def test_usuario_nao_acessa_disciplina_de_outro(cliente):
    cabecalhos_a = await _cadastrar_e_logar(cliente, "aluno2@exemplo.com")
    cabecalhos_b = await _cadastrar_e_logar(cliente, "aluno3@exemplo.com")

    resposta_criacao = await cliente.post(
        "/disciplinas", json={"nome": "Física"}, headers=cabecalhos_a
    )
    disciplina_id = resposta_criacao.json()["id"]

    resposta = await cliente.get(f"/disciplinas/{disciplina_id}", headers=cabecalhos_b)

    assert resposta.status_code == 404


@pytest.mark.asyncio
async def test_atualizar_e_remover_disciplina(cliente):
    cabecalhos = await _cadastrar_e_logar(cliente, "aluno4@exemplo.com")
    criada = await cliente.post("/disciplinas", json={"nome": "Química"}, headers=cabecalhos)
    disciplina_id = criada.json()["id"]

    atualizada = await cliente.put(
        f"/disciplinas/{disciplina_id}", json={"nome": "Química Orgânica"}, headers=cabecalhos
    )
    assert atualizada.status_code == 200
    assert atualizada.json()["nome"] == "Química Orgânica"

    removida = await cliente.delete(f"/disciplinas/{disciplina_id}", headers=cabecalhos)
    assert removida.status_code == 204

    buscada = await cliente.get(f"/disciplinas/{disciplina_id}", headers=cabecalhos)
    assert buscada.status_code == 404


@pytest.mark.asyncio
async def test_outro_usuario_nao_pode_atualizar_disciplina(cliente):
    cabecalhos_a = await _cadastrar_e_logar(cliente, "aluno5@exemplo.com")
    cabecalhos_b = await _cadastrar_e_logar(cliente, "aluno6@exemplo.com")
    criada = await cliente.post("/disciplinas", json={"nome": "Biologia"}, headers=cabecalhos_a)
    disciplina_id = criada.json()["id"]

    resposta = await cliente.put(
        f"/disciplinas/{disciplina_id}", json={"nome": "Hackeada"}, headers=cabecalhos_b
    )

    assert resposta.status_code == 404


@pytest.mark.asyncio
async def test_outro_usuario_nao_pode_remover_disciplina(cliente):
    cabecalhos_a = await _cadastrar_e_logar(cliente, "aluno7@exemplo.com")
    cabecalhos_b = await _cadastrar_e_logar(cliente, "aluno8@exemplo.com")
    criada = await cliente.post("/disciplinas", json={"nome": "Geografia"}, headers=cabecalhos_a)
    disciplina_id = criada.json()["id"]

    resposta = await cliente.delete(f"/disciplinas/{disciplina_id}", headers=cabecalhos_b)

    assert resposta.status_code == 404

    ainda_existe = await cliente.get(f"/disciplinas/{disciplina_id}", headers=cabecalhos_a)
    assert ainda_existe.status_code == 200


@pytest.mark.asyncio
async def test_disciplina_inexistente_retorna_404(cliente):
    cabecalhos = await _cadastrar_e_logar(cliente, "aluno9@exemplo.com")

    resposta_get = await cliente.get("/disciplinas/999999", headers=cabecalhos)
    resposta_put = await cliente.put("/disciplinas/999999", json={"nome": "X"}, headers=cabecalhos)
    resposta_delete = await cliente.delete("/disciplinas/999999", headers=cabecalhos)

    assert resposta_get.status_code == 404
    assert resposta_put.status_code == 404
    assert resposta_delete.status_code == 404


@pytest.mark.asyncio
async def test_cor_invalida_retorna_422(cliente):
    cabecalhos = await _cadastrar_e_logar(cliente, "aluno10@exemplo.com")

    resposta = await cliente.post(
        "/disciplinas", json={"nome": "Arte", "cor": "vermelho"}, headers=cabecalhos
    )

    assert resposta.status_code == 422
