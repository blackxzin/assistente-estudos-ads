"use client";

import { useAuth } from "@/lib/auth-context";
import { useRequisicao } from "@/lib/use-requisicao";
import { obterPainel } from "@/lib/api";
import { Carregando } from "@/components/carregando";
import { EstadoErro } from "@/components/estado-erro";
import { SecaoProximosPrazos } from "@/components/secao-proximos-prazos";
import { SecaoRevisoesHoje } from "@/components/secao-revisoes-hoje";
import { SecaoDesempenho } from "@/components/secao-desempenho";

export function PainelPrincipal() {
  const { token } = useAuth();
  const { estado, recarregar } = useRequisicao(() => obterPainel(token as string), [token]);

  if (!token) return null;

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-semibold text-texto">Painel</h1>
        <p className="mt-1 text-texto-suave">Visão geral dos seus estudos.</p>
      </div>

      {estado.status === "carregando" && <Carregando rotulo="Carregando painel…" />}

      {estado.status === "erro" && (
        <EstadoErro mensagem={estado.mensagem} onTentarNovamente={recarregar} />
      )}

      {estado.status === "sucesso" && (
        <div className="grid gap-4 lg:grid-cols-3">
          <SecaoProximosPrazos prazos={estado.dados.proximos_prazos} />
          <SecaoRevisoesHoje revisoes={estado.dados.revisoes_hoje} />
          <SecaoDesempenho desempenho={estado.dados.desempenho} />
        </div>
      )}
    </div>
  );
}
