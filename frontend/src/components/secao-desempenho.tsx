import type { DesempenhoPainel } from "@/lib/api";
import { CartaoPainel } from "@/components/cartao-painel";
import { MiniGraficoDesempenho } from "@/components/mini-grafico-desempenho";

export function SecaoDesempenho({ desempenho }: { desempenho: DesempenhoPainel }) {
  return (
    <CartaoPainel titulo="Desempenho nos simulados">
      {desempenho.total_simulados === 0 ? (
        <p className="text-sm text-texto-suave">Nenhum simulado realizado ainda.</p>
      ) : (
        <>
          <p className="text-sm text-texto-suave">
            Média:{" "}
            <span className="font-medium text-texto">
              {desempenho.media_nota !== null ? desempenho.media_nota.toFixed(1) : "—"}
            </span>{" "}
            · {desempenho.total_simulados} simulado(s)
          </p>
          <MiniGraficoDesempenho ultimos={desempenho.ultimos} />
        </>
      )}
    </CartaoPainel>
  );
}
