import type { DesempenhoRevisao, Revisao } from "@/lib/api";

type Props = {
  revisao: Revisao;
  atualizando: boolean;
  onConcluir: (desempenho: DesempenhoRevisao) => void;
};

const RUBRICAS_STATUS: Record<Revisao["status"], { rotulo: string; className: string }> = {
  pendente: { rotulo: "Pendente", className: "bg-superficie-hover text-texto-suave" },
  feita: { rotulo: "Feita", className: "bg-acento/15 text-acento" },
  pulada: { rotulo: "Pulada", className: "bg-perigo/15 text-perigo" },
};

export function ItemRevisao({ revisao, atualizando, onConcluir }: Props) {
  const rubrica = RUBRICAS_STATUS[revisao.status];

  return (
    <li className="flex flex-col gap-3 rounded-xl border border-borda bg-superficie p-4">
      <div className="flex flex-wrap items-start justify-between gap-2">
        <div>
          <p className="font-medium text-texto">{revisao.material_titulo}</p>
          <p className="text-sm text-texto-suave">{revisao.disciplina_nome}</p>
          <p className="text-xs text-texto-suave">Etapa {revisao.etapa}</p>
        </div>
        <span
          className={`inline-flex shrink-0 items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${rubrica.className}`}
        >
          {rubrica.rotulo}
        </span>
      </div>

      {revisao.status === "pendente" && (
        <div className="flex flex-wrap gap-2" aria-busy={atualizando || undefined}>
          <button
            type="button"
            disabled={atualizando}
            onClick={() => onConcluir("lembrei")}
            className="rounded-md border border-acento px-3 py-1.5 text-sm font-medium text-acento transition-colors hover:bg-acento/10 disabled:cursor-not-allowed disabled:opacity-60 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento"
          >
            Lembrei
          </button>
          <button
            type="button"
            disabled={atualizando}
            onClick={() => onConcluir("dificil")}
            className="rounded-md border border-aviso px-3 py-1.5 text-sm font-medium text-aviso transition-colors hover:bg-aviso/10 disabled:cursor-not-allowed disabled:opacity-60 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento"
          >
            Difícil
          </button>
          <button
            type="button"
            disabled={atualizando}
            onClick={() => onConcluir("esqueci")}
            className="rounded-md border border-perigo px-3 py-1.5 text-sm font-medium text-perigo transition-colors hover:bg-perigo/10 disabled:cursor-not-allowed disabled:opacity-60 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento"
          >
            Esqueci
          </button>
        </div>
      )}
    </li>
  );
}
