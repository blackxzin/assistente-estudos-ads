import type { SimuladoResumo } from "@/lib/api";

const ALTURA_GRAFICO = 100;
const LARGURA_BARRA = 28;
const ESPACAMENTO = 14;

export function MiniGraficoDesempenho({ ultimos }: { ultimos: SimuladoResumo[] }) {
  const largura = ultimos.length * (LARGURA_BARRA + ESPACAMENTO) + ESPACAMENTO;

  return (
    <figure>
      <svg
        viewBox={`0 0 ${largura} ${ALTURA_GRAFICO + 24}`}
        width="100%"
        height={ALTURA_GRAFICO + 24}
        role="img"
        aria-hidden="true"
        className="max-w-full"
      >
        {ultimos.map((simulado, indice) => {
          const alturaBarra = Math.max((simulado.nota / 10) * ALTURA_GRAFICO, 2);
          const x = ESPACAMENTO + indice * (LARGURA_BARRA + ESPACAMENTO);
          const y = ALTURA_GRAFICO - alturaBarra;

          return (
            <g key={simulado.simulado_id}>
              <rect
                x={x}
                y={y}
                width={LARGURA_BARRA}
                height={alturaBarra}
                rx={4}
                className="fill-acento"
              />
              <text
                x={x + LARGURA_BARRA / 2}
                y={ALTURA_GRAFICO + 16}
                textAnchor="middle"
                className="fill-texto-suave text-[10px]"
              >
                {simulado.nota.toFixed(1)}
              </text>
            </g>
          );
        })}
      </svg>
      <figcaption className="sr-only">
        Notas dos últimos simulados:{" "}
        {ultimos.map((item) => `${item.material_titulo}: ${item.nota.toFixed(1)}`).join(", ")}
      </figcaption>
    </figure>
  );
}
