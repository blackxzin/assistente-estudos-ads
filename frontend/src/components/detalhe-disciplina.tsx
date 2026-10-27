"use client";

import { useState } from "react";
import Link from "next/link";
import { useAuth } from "@/lib/auth-context";
import { useRequisicao } from "@/lib/use-requisicao";
import {
  atualizarPrazo,
  criarPrazo,
  excluirPrazo,
  listarPrazos,
  mensagemDeErro,
  obterDisciplina,
  type DadosPrazo,
  type Prazo,
} from "@/lib/api";
import { Botao } from "@/components/botao";
import { Carregando } from "@/components/carregando";
import { EstadoErro } from "@/components/estado-erro";
import { EstadoVazio } from "@/components/estado-vazio";
import { Modal } from "@/components/modal";
import { FormularioPrazo } from "@/components/formulario-prazo";
import { ItemPrazo } from "@/components/item-prazo";
import { SecaoMateriais } from "@/components/secao-materiais";

type Props = { disciplinaId: string };

export function DetalheDisciplina({ disciplinaId }: Props) {
  const { token } = useAuth();

  const disciplinaRequisicao = useRequisicao(
    () => obterDisciplina(token as string, disciplinaId),
    [token, disciplinaId],
  );
  const prazosRequisicao = useRequisicao(
    () => listarPrazos(token as string, disciplinaId),
    [token, disciplinaId],
  );

  const [modalAberto, setModalAberto] = useState(false);
  const [prazoEditando, setPrazoEditando] = useState<Prazo | null>(null);
  const [enviando, setEnviando] = useState(false);
  const [erroFormulario, setErroFormulario] = useState<string | null>(null);
  const [idsAtualizando, setIdsAtualizando] = useState<Set<string>>(new Set());

  if (!token) return null;
  const tokenValido = token;

  function abrirCriacao() {
    setPrazoEditando(null);
    setErroFormulario(null);
    setModalAberto(true);
  }

  function abrirEdicao(prazo: Prazo) {
    setPrazoEditando(prazo);
    setErroFormulario(null);
    setModalAberto(true);
  }

  async function salvar(dados: DadosPrazo) {
    setEnviando(true);
    setErroFormulario(null);
    try {
      if (prazoEditando) {
        const atualizado = await atualizarPrazo(tokenValido, prazoEditando.id, dados);
        prazosRequisicao.atualizarDados((lista) =>
          lista.map((item) => (item.id === atualizado.id ? atualizado : item)),
        );
      } else {
        const criado = await criarPrazo(tokenValido, disciplinaId, dados);
        prazosRequisicao.atualizarDados((lista) => [...lista, criado]);
      }
      setModalAberto(false);
    } catch (erro: unknown) {
      setErroFormulario(mensagemDeErro(erro));
    } finally {
      setEnviando(false);
    }
  }

  async function excluir(prazo: Prazo) {
    const confirmado = window.confirm(
      `Excluir o prazo "${prazo.titulo}"? Essa ação não pode ser desfeita.`,
    );
    if (!confirmado) return;

    try {
      await excluirPrazo(tokenValido, prazo.id);
      prazosRequisicao.atualizarDados((lista) => lista.filter((item) => item.id !== prazo.id));
    } catch (erro: unknown) {
      window.alert(mensagemDeErro(erro));
    }
  }

  async function alternarConcluido(prazo: Prazo, concluido: boolean) {
    setIdsAtualizando((atual) => new Set(atual).add(prazo.id));
    try {
      const atualizado = await atualizarPrazo(tokenValido, prazo.id, { concluido });
      prazosRequisicao.atualizarDados((lista) =>
        lista.map((item) => (item.id === atualizado.id ? atualizado : item)),
      );
    } catch (erro: unknown) {
      window.alert(mensagemDeErro(erro));
    } finally {
      setIdsAtualizando((atual) => {
        const novo = new Set(atual);
        novo.delete(prazo.id);
        return novo;
      });
    }
  }

  const botaoNovoPrazo = <Botao onClick={abrirCriacao}>Novo prazo</Botao>;

  return (
    <div className="flex flex-col gap-6">
      <div>
        <Link href="/disciplinas" className="text-sm font-medium text-acento hover:underline">
          ← Voltar para disciplinas
        </Link>
      </div>

      {disciplinaRequisicao.estado.status === "carregando" && (
        <Carregando rotulo="Carregando disciplina…" />
      )}

      {disciplinaRequisicao.estado.status === "erro" && (
        <EstadoErro
          mensagem={disciplinaRequisicao.estado.mensagem}
          onTentarNovamente={disciplinaRequisicao.recarregar}
        />
      )}

      {disciplinaRequisicao.estado.status === "sucesso" && (
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <span
              aria-hidden="true"
              className="size-4 shrink-0 rounded-full"
              style={{ backgroundColor: disciplinaRequisicao.estado.dados.cor }}
            />
            <div>
              <h1 className="text-2xl font-semibold text-texto">
                {disciplinaRequisicao.estado.dados.nome}
              </h1>
              <p className="text-sm text-texto-suave">
                {disciplinaRequisicao.estado.dados.professor}
              </p>
            </div>
          </div>
          {prazosRequisicao.estado.status === "sucesso" &&
            prazosRequisicao.estado.dados.length > 0 &&
            botaoNovoPrazo}
        </div>
      )}

      {prazosRequisicao.estado.status === "carregando" && (
        <Carregando rotulo="Carregando prazos…" />
      )}

      {prazosRequisicao.estado.status === "erro" && (
        <EstadoErro
          mensagem={prazosRequisicao.estado.mensagem}
          onTentarNovamente={prazosRequisicao.recarregar}
        />
      )}

      {prazosRequisicao.estado.status === "sucesso" &&
        prazosRequisicao.estado.dados.length === 0 && (
          <EstadoVazio
            titulo="Nenhum prazo cadastrado"
            descricao="Cadastre provas e trabalhos para acompanhar os prazos desta disciplina."
            acao={botaoNovoPrazo}
          />
        )}

      {prazosRequisicao.estado.status === "sucesso" && prazosRequisicao.estado.dados.length > 0 && (
        <ul className="flex flex-col gap-3">
          {prazosRequisicao.estado.dados.map((prazo) => (
            <ItemPrazo
              key={prazo.id}
              prazo={prazo}
              atualizandoConclusao={idsAtualizando.has(prazo.id)}
              onAlternarConcluido={(concluido) => alternarConcluido(prazo, concluido)}
              onEditar={() => abrirEdicao(prazo)}
              onExcluir={() => excluir(prazo)}
            />
          ))}
        </ul>
      )}

      <Modal
        aberto={modalAberto}
        titulo={prazoEditando ? "Editar prazo" : "Novo prazo"}
        onFechar={() => setModalAberto(false)}
      >
        <FormularioPrazo
          key={prazoEditando?.id ?? "novo"}
          valoresIniciais={prazoEditando ?? undefined}
          enviando={enviando}
          erro={erroFormulario}
          onEnviar={salvar}
          onCancelar={() => setModalAberto(false)}
        />
      </Modal>

      <SecaoMateriais disciplinaId={disciplinaId} />
    </div>
  );
}
