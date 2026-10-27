"use client";

import { useMemo, useState } from "react";
import { useAuth } from "@/lib/auth-context";
import { useRequisicao } from "@/lib/use-requisicao";
import {
  concluirRevisao,
  listarRevisoes,
  mensagemDeErro,
  type DesempenhoRevisao,
  type Revisao,
} from "@/lib/api";
import { formatarDataISO, primeiroDiaDoMes, ultimoDiaDoMes } from "@/lib/calendario";
import { Carregando } from "@/components/carregando";
import { EstadoErro } from "@/components/estado-erro";
import { EstadoVazio } from "@/components/estado-vazio";
import { CalendarioMensal } from "@/components/calendario-mensal";
import { ItemRevisao } from "@/components/item-revisao";

export function RevisoesCalendario() {
  const { token } = useAuth();
  const [mesReferencia, setMesReferencia] = useState(() => new Date());
  const [diaSelecionado, setDiaSelecionado] = useState(() => formatarDataISO(new Date()));
  const [idsAtualizando, setIdsAtualizando] = useState<Set<string>>(new Set());
  const [erroAcao, setErroAcao] = useState<string | null>(null);

  const de = formatarDataISO(primeiroDiaDoMes(mesReferencia));
  const ate = formatarDataISO(ultimoDiaDoMes(mesReferencia));

  const { estado, recarregar, atualizarDados } = useRequisicao(
    () => listarRevisoes(token as string, de, ate),
    [token, de, ate],
  );

  const contagemPorDia = useMemo(() => {
    if (estado.status !== "sucesso") return {};
    const contagem: Record<string, number> = {};
    for (const revisao of estado.dados) {
      contagem[revisao.data_prevista] = (contagem[revisao.data_prevista] ?? 0) + 1;
    }
    return contagem;
  }, [estado]);

  const revisoesDoDia =
    estado.status === "sucesso"
      ? estado.dados.filter((revisao) => revisao.data_prevista === diaSelecionado)
      : [];

  if (!token) return null;
  const tokenValido = token;

  function mudarMes(delta: number) {
    setMesReferencia((atual) => new Date(atual.getFullYear(), atual.getMonth() + delta, 1));
  }

  async function concluir(revisao: Revisao, desempenho: DesempenhoRevisao) {
    setIdsAtualizando((atual) => new Set(atual).add(revisao.id));
    setErroAcao(null);
    try {
      const atualizada = await concluirRevisao(tokenValido, revisao.id, desempenho);
      atualizarDados((lista) =>
        lista.map((item) => (item.id === atualizada.id ? atualizada : item)),
      );
    } catch (erro: unknown) {
      setErroAcao(mensagemDeErro(erro));
    } finally {
      setIdsAtualizando((atual) => {
        const novo = new Set(atual);
        novo.delete(revisao.id);
        return novo;
      });
    }
  }

  const tituloDia = new Date(`${diaSelecionado}T00:00:00`).toLocaleDateString("pt-BR", {
    weekday: "long",
    day: "2-digit",
    month: "long",
  });

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-semibold text-texto">Revisões</h1>
        <p className="mt-1 text-texto-suave">
          Acompanhe as revisões agendadas por repetição espaçada.
        </p>
      </div>

      {estado.status === "carregando" && <Carregando rotulo="Carregando revisões…" />}

      {estado.status === "erro" && (
        <EstadoErro mensagem={estado.mensagem} onTentarNovamente={recarregar} />
      )}

      {estado.status === "sucesso" && (
        <div className="grid gap-6 lg:grid-cols-[auto_1fr]">
          <CalendarioMensal
            mesReferencia={mesReferencia}
            diaSelecionado={diaSelecionado}
            contagemPorDia={contagemPorDia}
            onMudarMes={mudarMes}
            onSelecionarDia={setDiaSelecionado}
          />

          <div className="flex flex-col gap-3">
            <h2 className="font-medium capitalize text-texto">{tituloDia}</h2>

            {erroAcao && (
              <p role="alert" className="text-sm text-perigo">
                {erroAcao}
              </p>
            )}

            {revisoesDoDia.length === 0 ? (
              <EstadoVazio
                titulo="Nenhuma revisão neste dia"
                descricao="Selecione outro dia no calendário."
              />
            ) : (
              <ul className="flex flex-col gap-3">
                {revisoesDoDia.map((revisao) => (
                  <ItemRevisao
                    key={revisao.id}
                    revisao={revisao}
                    atualizando={idsAtualizando.has(revisao.id)}
                    onConcluir={(desempenho) => concluir(revisao, desempenho)}
                  />
                ))}
              </ul>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
