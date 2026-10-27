"use client";

import { useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useAuth } from "@/lib/auth-context";
import { useRequisicao } from "@/lib/use-requisicao";
import {
  corrigirSimulado,
  mensagemDeErro,
  obterSimulado,
  type ResultadoSimulado,
} from "@/lib/api";
import { Botao } from "@/components/botao";
import { Carregando } from "@/components/carregando";
import { EstadoErro } from "@/components/estado-erro";
import { QuestaoSimuladoItem } from "@/components/questao-simulado";
import { ItemResultadoSimulado } from "@/components/item-resultado-simulado";

type Props = { simuladoId: string };

export function DetalheSimulado({ simuladoId }: Props) {
  const { token } = useAuth();
  const searchParams = useSearchParams();
  const materialId = searchParams.get("materialId");
  const disciplinaId = searchParams.get("disciplinaId");

  const { estado, recarregar } = useRequisicao(
    () => obterSimulado(token as string, simuladoId),
    [token, simuladoId],
  );

  const [respostas, setRespostas] = useState<Record<number, number>>({});
  const [resultado, setResultado] = useState<ResultadoSimulado | null>(null);
  const [enviando, setEnviando] = useState(false);
  const [erroEnvio, setErroEnvio] = useState<string | null>(null);

  if (!token) return null;
  const tokenValido = token;

  async function corrigir() {
    if (estado.status !== "sucesso") return;
    const totalQuestoes = estado.dados.questoes.length;
    if (Object.keys(respostas).length < totalQuestoes) {
      setErroEnvio("Responda todas as questões antes de corrigir.");
      return;
    }

    setEnviando(true);
    setErroEnvio(null);
    try {
      const corpo = Object.entries(respostas).map(([questaoId, alternativa]) => ({
        questao_id: Number(questaoId),
        alternativa,
      }));
      const resultadoCorrecao = await corrigirSimulado(tokenValido, simuladoId, corpo);
      setResultado(resultadoCorrecao);
    } catch (erro: unknown) {
      setErroEnvio(mensagemDeErro(erro));
    } finally {
      setEnviando(false);
    }
  }

  const linkVoltar = materialId
    ? `/materiais/${materialId}${disciplinaId ? `?disciplinaId=${disciplinaId}` : ""}`
    : "/disciplinas";

  return (
    <div className="flex flex-col gap-6">
      <div>
        <Link href={linkVoltar} className="text-sm font-medium text-acento hover:underline">
          ← Voltar ao material
        </Link>
      </div>

      {estado.status === "carregando" && <Carregando rotulo="Carregando simulado…" />}

      {estado.status === "erro" && (
        <EstadoErro mensagem={estado.mensagem} onTentarNovamente={recarregar} />
      )}

      {estado.status === "sucesso" && !resultado && (
        <>
          <div>
            <h1 className="text-2xl font-semibold text-texto">Simulado</h1>
            <p className="mt-1 text-texto-suave">
              {estado.dados.questoes.length} questões. Responda todas e clique em corrigir.
            </p>
          </div>

          <div className="flex flex-col gap-4">
            {estado.dados.questoes.map((questao, indice) => (
              <QuestaoSimuladoItem
                key={questao.id}
                questao={questao}
                numero={indice + 1}
                selecionada={respostas[questao.id] ?? null}
                onSelecionar={(alternativa) =>
                  setRespostas((atual) => ({ ...atual, [questao.id]: alternativa }))
                }
              />
            ))}
          </div>

          {erroEnvio && (
            <p role="alert" className="text-sm text-perigo">
              {erroEnvio}
            </p>
          )}

          <Botao onClick={corrigir} carregando={enviando} className="self-start">
            Corrigir
          </Botao>
        </>
      )}

      {resultado && (
        <>
          <div className="rounded-xl border border-borda bg-superficie p-6">
            <h1 className="text-2xl font-semibold text-texto">Resultado</h1>
            <p className="mt-2 text-3xl font-semibold text-acento">
              {resultado.nota.toFixed(1)}
              <span className="text-base text-texto-suave"> / 10</span>
            </p>
            <p className="mt-1 text-texto-suave">
              {resultado.acertos} de {resultado.total} questões corretas
            </p>
          </div>

          <ul className="flex flex-col gap-4">
            {resultado.itens.map((item, indice) => (
              <ItemResultadoSimulado key={item.questao_id} item={item} numero={indice + 1} />
            ))}
          </ul>
        </>
      )}
    </div>
  );
}
