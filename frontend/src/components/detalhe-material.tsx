"use client";

import { useEffect, useState, type FormEvent } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/lib/auth-context";
import { useRequisicao } from "@/lib/use-requisicao";
import {
  gerarResumoMaterial,
  gerarSimulado,
  mensagemDeErro,
  obterMaterial,
  perguntarMaterial,
} from "@/lib/api";
import { dividirTopicosResumo, type MensagemConversa } from "@/lib/materiais";
import { Botao } from "@/components/botao";
import { Carregando } from "@/components/carregando";
import { EstadoErro } from "@/components/estado-erro";
import { BadgeStatusMaterial } from "@/components/badge-status-material";
import { MensagemChat } from "@/components/mensagem-chat";
import { formatarDataHora } from "@/lib/formato";

const INTERVALO_POLLING_MS = 4000;

type Props = { materialId: string };

export function DetalheMaterial({ materialId }: Props) {
  const { token } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();
  const disciplinaId = searchParams.get("disciplinaId");

  const { estado, recarregar, atualizarDados } = useRequisicao(
    () => obterMaterial(token as string, materialId),
    [token, materialId],
  );

  const [gerandoResumo, setGerandoResumo] = useState(false);
  const [erroResumo, setErroResumo] = useState<string | null>(null);
  const [pergunta, setPergunta] = useState("");
  const [mensagens, setMensagens] = useState<MensagemConversa[]>([]);
  const [quantidadeQuestoes, setQuantidadeQuestoes] = useState(5);
  const [gerandoSimulado, setGerandoSimulado] = useState(false);
  const [erroSimulado, setErroSimulado] = useState<string | null>(null);

  const processando = estado.status === "sucesso" && estado.dados.status === "processando";

  useEffect(() => {
    if (!token || !processando) return;
    const intervalo = setInterval(() => {
      obterMaterial(token, materialId)
        .then((material) => atualizarDados(() => material))
        .catch(() => {});
    }, INTERVALO_POLLING_MS);
    return () => clearInterval(intervalo);
  }, [token, materialId, processando, atualizarDados]);

  if (!token) return null;
  const tokenValido = token;

  async function gerarResumo() {
    setGerandoResumo(true);
    setErroResumo(null);
    try {
      const atualizado = await gerarResumoMaterial(tokenValido, materialId);
      atualizarDados(() => atualizado);
    } catch (erro: unknown) {
      setErroResumo(mensagemDeErro(erro));
    } finally {
      setGerandoResumo(false);
    }
  }

  async function lidarComGerarSimulado(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    setGerandoSimulado(true);
    setErroSimulado(null);
    try {
      const simulado = await gerarSimulado(tokenValido, materialId, quantidadeQuestoes);
      const parametros = new URLSearchParams({ materialId });
      if (disciplinaId) parametros.set("disciplinaId", disciplinaId);
      router.push(`/simulados/${simulado.id}?${parametros.toString()}`);
    } catch (erro: unknown) {
      setErroSimulado(mensagemDeErro(erro));
    } finally {
      setGerandoSimulado(false);
    }
  }

  async function enviarPergunta(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    const texto = pergunta.trim();
    if (!texto) return;

    const id = crypto.randomUUID();
    setMensagens((lista) => [...lista, { id, pergunta: texto, enviando: true }]);
    setPergunta("");

    try {
      const resposta = await perguntarMaterial(tokenValido, materialId, texto);
      setMensagens((lista) =>
        lista.map((item) => (item.id === id ? { ...item, enviando: false, resposta } : item)),
      );
    } catch (erro: unknown) {
      const mensagemErro = mensagemDeErro(erro);
      setMensagens((lista) =>
        lista.map((item) =>
          item.id === id ? { ...item, enviando: false, erro: mensagemErro } : item,
        ),
      );
    }
  }

  return (
    <div className="flex flex-col gap-6">
      <div>
        <Link
          href={disciplinaId ? `/disciplinas/${disciplinaId}` : "/disciplinas"}
          className="text-sm font-medium text-acento hover:underline"
        >
          ← Voltar
        </Link>
      </div>

      {estado.status === "carregando" && <Carregando rotulo="Carregando material…" />}

      {estado.status === "erro" && (
        <EstadoErro mensagem={estado.mensagem} onTentarNovamente={recarregar} />
      )}

      {estado.status === "sucesso" && (
        <>
          <header className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <h1 className="text-2xl font-semibold text-texto">{estado.dados.titulo}</h1>
              <p className="mt-1 text-sm text-texto-suave">
                {formatarDataHora(estado.dados.criado_em)}
              </p>
            </div>
            <BadgeStatusMaterial status={estado.dados.status} />
          </header>

          {estado.dados.status === "processando" && (
            <p role="status" className="text-sm text-texto-suave">
              O material ainda está sendo processado. Isso pode levar alguns instantes…
            </p>
          )}

          {estado.dados.status === "erro" && (
            <p role="alert" className="text-sm text-perigo">
              Houve um erro ao processar este material. Tente enviá-lo novamente.
            </p>
          )}

          {estado.dados.status === "pronto" && (
            <>
              <section className="flex flex-col gap-3 rounded-xl border border-borda bg-superficie p-5">
                <div className="flex flex-wrap items-center justify-between gap-4">
                  <h2 className="text-lg font-semibold text-texto">Resumo</h2>
                  <Botao onClick={gerarResumo} carregando={gerandoResumo}>
                    {estado.dados.resumo ? "Gerar novamente" : "Gerar resumo"}
                  </Botao>
                </div>

                {erroResumo && (
                  <p role="alert" className="text-sm text-perigo">
                    {erroResumo}
                  </p>
                )}

                {estado.dados.resumo ? (
                  <ul className="list-disc space-y-1 pl-5 text-texto">
                    {dividirTopicosResumo(estado.dados.resumo).map((topico, indice) => (
                      <li key={indice}>{topico}</li>
                    ))}
                  </ul>
                ) : (
                  !gerandoResumo && (
                    <p className="text-sm text-texto-suave">Nenhum resumo gerado ainda.</p>
                  )
                )}
              </section>

              <section className="flex flex-col gap-4 rounded-xl border border-borda bg-superficie p-5">
                <h2 className="text-lg font-semibold text-texto">Perguntas sobre o material</h2>

                {mensagens.length > 0 && (
                  <ul className="flex flex-col gap-4">
                    {mensagens.map((mensagem) => (
                      <MensagemChat key={mensagem.id} mensagem={mensagem} />
                    ))}
                  </ul>
                )}

                <form onSubmit={enviarPergunta} className="flex items-end gap-2">
                  <div className="flex-1">
                    <label htmlFor="campo-pergunta" className="sr-only">
                      Pergunta sobre o material
                    </label>
                    <input
                      id="campo-pergunta"
                      type="text"
                      required
                      placeholder="Pergunte algo sobre este material…"
                      value={pergunta}
                      onChange={(evento) => setPergunta(evento.target.value)}
                      className="w-full rounded-md border border-borda bg-superficie px-3 py-2 text-texto placeholder:text-texto-suave focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento"
                    />
                  </div>
                  <Botao type="submit">Perguntar</Botao>
                </form>
              </section>

              <section className="flex flex-col gap-3 rounded-xl border border-borda bg-superficie p-5">
                <h2 className="text-lg font-semibold text-texto">Simulado</h2>
                <p className="text-sm text-texto-suave">
                  Gere questões de múltipla escolha a partir deste material.
                </p>

                <form
                  onSubmit={lidarComGerarSimulado}
                  className="flex flex-wrap items-end gap-3"
                >
                  <div className="flex flex-col gap-1.5">
                    <label htmlFor="quantidade-questoes" className="text-sm font-medium text-texto">
                      Número de questões
                    </label>
                    <input
                      id="quantidade-questoes"
                      type="number"
                      min={1}
                      max={20}
                      value={quantidadeQuestoes}
                      onChange={(evento) =>
                        setQuantidadeQuestoes(Number(evento.target.value))
                      }
                      className="w-24 rounded-md border border-borda bg-superficie px-3 py-2 text-texto focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento"
                    />
                  </div>
                  <Botao type="submit" carregando={gerandoSimulado}>
                    Gerar simulado
                  </Botao>
                </form>

                {erroSimulado && (
                  <p role="alert" className="text-sm text-perigo">
                    {erroSimulado}
                  </p>
                )}
              </section>
            </>
          )}
        </>
      )}
    </div>
  );
}
