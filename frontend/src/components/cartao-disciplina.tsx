import Link from "next/link";
import type { Disciplina } from "@/lib/api";

type Props = {
  disciplina: Disciplina;
  onEditar: () => void;
  onExcluir: () => void;
};

export function CartaoDisciplina({ disciplina, onEditar, onExcluir }: Props) {
  return (
    <div className="flex flex-col overflow-hidden rounded-xl border border-borda bg-superficie">
      <div aria-hidden="true" className="h-2" style={{ backgroundColor: disciplina.cor }} />
      <div className="flex flex-1 flex-col gap-3 p-5">
        <div>
          <h2 className="text-lg font-semibold text-texto">{disciplina.nome}</h2>
          <p className="text-sm text-texto-suave">{disciplina.professor}</p>
        </div>

        <div className="mt-auto flex items-center justify-between gap-2 pt-2">
          <Link
            href={`/disciplinas/${disciplina.id}`}
            className="text-sm font-medium text-acento hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento"
          >
            Ver prazos
          </Link>
          <div className="flex items-center gap-1">
            <button
              type="button"
              onClick={onEditar}
              aria-label={`Editar ${disciplina.nome}`}
              className="rounded-md p-2 text-texto-suave transition-colors hover:bg-superficie-hover hover:text-texto focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento"
            >
              <span aria-hidden="true">✏️</span>
            </button>
            <button
              type="button"
              onClick={onExcluir}
              aria-label={`Excluir ${disciplina.nome}`}
              className="rounded-md p-2 text-texto-suave transition-colors hover:bg-superficie-hover hover:text-perigo focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento"
            >
              <span aria-hidden="true">🗑️</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
