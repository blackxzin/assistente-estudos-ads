"use client";

import { useId } from "react";
import type { Prazo } from "@/lib/api";
import { BadgeTipoPrazo } from "@/components/badge-tipo-prazo";
import { formatarData } from "@/lib/formato";

type Props = {
  prazo: Prazo;
  atualizandoConclusao: boolean;
  onAlternarConcluido: (concluido: boolean) => void;
  onEditar: () => void;
  onExcluir: () => void;
};

export function ItemPrazo({
  prazo,
  atualizandoConclusao,
  onAlternarConcluido,
  onEditar,
  onExcluir,
}: Props) {
  const idCheckbox = useId();

  return (
    <li className="flex flex-wrap items-center gap-4 rounded-xl border border-borda bg-superficie p-4">
      <input
        id={idCheckbox}
        type="checkbox"
        checked={prazo.concluido}
        disabled={atualizandoConclusao}
        onChange={(e) => onAlternarConcluido(e.target.checked)}
        className="size-5 rounded border-borda accent-acento"
      />

      <div className="min-w-0 flex-1">
        <label
          htmlFor={idCheckbox}
          className={`block font-medium text-texto ${prazo.concluido ? "line-through text-texto-suave" : ""}`}
        >
          {prazo.titulo}
        </label>
        <div className="mt-1 flex items-center gap-2 text-sm text-texto-suave">
          <BadgeTipoPrazo tipo={prazo.tipo} />
          <span>{formatarData(prazo.data)}</span>
        </div>
      </div>

      <div className="flex items-center gap-1">
        <button
          type="button"
          onClick={onEditar}
          aria-label={`Editar prazo ${prazo.titulo}`}
          className="rounded-md p-2 text-texto-suave transition-colors hover:bg-superficie-hover hover:text-texto focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento"
        >
          <span aria-hidden="true">✏️</span>
        </button>
        <button
          type="button"
          onClick={onExcluir}
          aria-label={`Excluir prazo ${prazo.titulo}`}
          className="rounded-md p-2 text-texto-suave transition-colors hover:bg-superficie-hover hover:text-perigo focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento"
        >
          <span aria-hidden="true">🗑️</span>
        </button>
      </div>
    </li>
  );
}
