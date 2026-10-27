"use client";

import { useEffect, useId, useRef, type ReactNode } from "react";

type Props = {
  aberto: boolean;
  titulo: string;
  onFechar: () => void;
  children: ReactNode;
};

export function Modal({ aberto, titulo, onFechar, children }: Props) {
  const dialogRef = useRef<HTMLDialogElement>(null);
  const idTitulo = useId();

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    if (aberto && !dialog.open) {
      dialog.showModal();
    } else if (!aberto && dialog.open) {
      dialog.close();
    }
  }, [aberto]);

  return (
    <dialog
      ref={dialogRef}
      onClose={onFechar}
      onClick={(evento) => {
        if (evento.target === dialogRef.current) onFechar();
      }}
      aria-labelledby={idTitulo}
      className="w-full max-w-md rounded-xl border border-borda bg-superficie p-0 text-texto backdrop:bg-black/50"
    >
      <div className="p-6">
        <div className="mb-4 flex items-center justify-between gap-4">
          <h2 id={idTitulo} className="text-lg font-semibold">
            {titulo}
          </h2>
          <button
            type="button"
            onClick={onFechar}
            aria-label="Fechar"
            className="rounded-md p-1 text-texto-suave transition-colors hover:bg-superficie-hover hover:text-texto focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento"
          >
            <span aria-hidden="true">✕</span>
          </button>
        </div>
        {children}
      </div>
    </dialog>
  );
}
