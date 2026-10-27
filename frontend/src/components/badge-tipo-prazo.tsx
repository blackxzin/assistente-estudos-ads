import type { TipoPrazo } from "@/lib/api";

const RUBRICAS: Record<TipoPrazo, { rotulo: string; className: string }> = {
  prova: {
    rotulo: "Prova",
    className: "bg-perigo/15 text-perigo",
  },
  trabalho: {
    rotulo: "Trabalho",
    className: "bg-acento/15 text-acento",
  },
};

export function BadgeTipoPrazo({ tipo }: { tipo: TipoPrazo }) {
  const rubrica = RUBRICAS[tipo];
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${rubrica.className}`}
    >
      {rubrica.rotulo}
    </span>
  );
}
