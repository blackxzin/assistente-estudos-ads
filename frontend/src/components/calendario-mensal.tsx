"use client";

import { NOMES_DIA_SEMANA, NOMES_MES, formatarDataISO, gerarDiasDoMes } from "@/lib/calendario";

type Props = {
  mesReferencia: Date;
  diaSelecionado: string;
  contagemPorDia: Record<string, number>;
  onMudarMes: (delta: number) => void;
  onSelecionarDia: (dataIso: string) => void;
};

export function CalendarioMensal({
  mesReferencia,
  diaSelecionado,
  contagemPorDia,
  onMudarMes,
  onSelecionarDia,
}: Props) {
  const dias = gerarDiasDoMes(mesReferencia);
  const hojeIso = formatarDataISO(new Date());

  return (
    <div className="rounded-xl border border-borda bg-superficie p-4">
      <div className="mb-3 flex items-center justify-between">
        <button
          type="button"
          onClick={() => onMudarMes(-1)}
          aria-label="Mês anterior"
          className="rounded-md p-2 text-texto-suave transition-colors hover:bg-superficie-hover focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento"
        >
          ‹
        </button>
        <p className="font-medium text-texto">
          {NOMES_MES[mesReferencia.getMonth()]} de {mesReferencia.getFullYear()}
        </p>
        <button
          type="button"
          onClick={() => onMudarMes(1)}
          aria-label="Próximo mês"
          className="rounded-md p-2 text-texto-suave transition-colors hover:bg-superficie-hover focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento"
        >
          ›
        </button>
      </div>

      <div className="grid grid-cols-7 gap-1 text-center text-xs text-texto-suave">
        {NOMES_DIA_SEMANA.map((nome) => (
          <div key={nome} className="py-1">
            {nome}
          </div>
        ))}
      </div>

      <div className="mt-1 grid grid-cols-7 gap-1">
        {dias.map((dia, indice) => {
          if (!dia) return <div key={`vazio-${indice}`} />;

          const dataIso = formatarDataISO(dia);
          const contagem = contagemPorDia[dataIso] ?? 0;
          const selecionado = dataIso === diaSelecionado;
          const hoje = dataIso === hojeIso;

          return (
            <button
              key={dataIso}
              type="button"
              onClick={() => onSelecionarDia(dataIso)}
              aria-pressed={selecionado}
              aria-label={`${dia.getDate()} de ${NOMES_MES[dia.getMonth()]}${
                contagem > 0 ? `, ${contagem} revisão(ões)` : ""
              }`}
              className={`flex flex-col items-center gap-0.5 rounded-md p-2 text-sm transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento ${
                selecionado
                  ? "bg-acento text-acento-texto"
                  : hoje
                    ? "border border-acento text-texto"
                    : "text-texto hover:bg-superficie-hover"
              }`}
            >
              <span>{dia.getDate()}</span>
              {contagem > 0 && (
                <span
                  aria-hidden="true"
                  className={`size-1.5 rounded-full ${
                    selecionado ? "bg-acento-texto" : "bg-acento"
                  }`}
                />
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}
