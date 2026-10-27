"use client";

import { useState } from "react";
import { useAuth } from "@/lib/auth-context";
import { useRequisicao } from "@/lib/use-requisicao";
import {
  atualizarDisciplina,
  criarDisciplina,
  excluirDisciplina,
  listarDisciplinas,
  mensagemDeErro,
  type DadosDisciplina,
  type Disciplina,
} from "@/lib/api";
import { Botao } from "@/components/botao";
import { Carregando } from "@/components/carregando";
import { EstadoErro } from "@/components/estado-erro";
import { EstadoVazio } from "@/components/estado-vazio";
import { CartaoDisciplina } from "@/components/cartao-disciplina";
import { Modal } from "@/components/modal";
import { FormularioDisciplina } from "@/components/formulario-disciplina";

export function ListaDisciplinas() {
  const { token } = useAuth();
  const { estado, recarregar, atualizarDados } = useRequisicao(
    () => listarDisciplinas(token as string),
    [token],
  );

  const [modalAberto, setModalAberto] = useState(false);
  const [disciplinaEditando, setDisciplinaEditando] = useState<Disciplina | null>(null);
  const [enviando, setEnviando] = useState(false);
  const [erroFormulario, setErroFormulario] = useState<string | null>(null);

  if (!token) return null;
  const tokenValido = token;

  function abrirCriacao() {
    setDisciplinaEditando(null);
    setErroFormulario(null);
    setModalAberto(true);
  }

  function abrirEdicao(disciplina: Disciplina) {
    setDisciplinaEditando(disciplina);
    setErroFormulario(null);
    setModalAberto(true);
  }

  async function salvar(dados: DadosDisciplina) {
    setEnviando(true);
    setErroFormulario(null);
    try {
      if (disciplinaEditando) {
        const atualizada = await atualizarDisciplina(
          tokenValido,
          disciplinaEditando.id,
          dados,
        );
        atualizarDados((lista) =>
          lista.map((item) => (item.id === atualizada.id ? atualizada : item)),
        );
      } else {
        const criada = await criarDisciplina(tokenValido, dados);
        atualizarDados((lista) => [...lista, criada]);
      }
      setModalAberto(false);
    } catch (erro: unknown) {
      setErroFormulario(mensagemDeErro(erro));
    } finally {
      setEnviando(false);
    }
  }

  async function excluir(disciplina: Disciplina) {
    const confirmado = window.confirm(
      `Excluir a disciplina "${disciplina.nome}"? Essa ação não pode ser desfeita.`,
    );
    if (!confirmado) return;

    try {
      await excluirDisciplina(tokenValido, disciplina.id);
      atualizarDados((lista) => lista.filter((item) => item.id !== disciplina.id));
    } catch (erro: unknown) {
      window.alert(mensagemDeErro(erro));
    }
  }

  const botaoNovaDisciplina = (
    <Botao onClick={abrirCriacao}>Nova disciplina</Botao>
  );

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-texto">Disciplinas</h1>
          <p className="mt-1 text-texto-suave">
            Organize as disciplinas que você está estudando.
          </p>
        </div>
        {estado.status === "sucesso" && estado.dados.length > 0 && botaoNovaDisciplina}
      </div>

      {estado.status === "carregando" && <Carregando rotulo="Carregando disciplinas…" />}

      {estado.status === "erro" && (
        <EstadoErro mensagem={estado.mensagem} onTentarNovamente={recarregar} />
      )}

      {estado.status === "sucesso" && estado.dados.length === 0 && (
        <EstadoVazio
          titulo="Nenhuma disciplina cadastrada"
          descricao="Crie sua primeira disciplina para começar a organizar seus estudos."
          acao={botaoNovaDisciplina}
        />
      )}

      {estado.status === "sucesso" && estado.dados.length > 0 && (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {estado.dados.map((disciplina) => (
            <CartaoDisciplina
              key={disciplina.id}
              disciplina={disciplina}
              onEditar={() => abrirEdicao(disciplina)}
              onExcluir={() => excluir(disciplina)}
            />
          ))}
        </div>
      )}

      <Modal
        aberto={modalAberto}
        titulo={disciplinaEditando ? "Editar disciplina" : "Nova disciplina"}
        onFechar={() => setModalAberto(false)}
      >
        <FormularioDisciplina
          key={disciplinaEditando?.id ?? "nova"}
          valoresIniciais={disciplinaEditando ?? undefined}
          enviando={enviando}
          erro={erroFormulario}
          onEnviar={salvar}
          onCancelar={() => setModalAberto(false)}
        />
      </Modal>
    </div>
  );
}
