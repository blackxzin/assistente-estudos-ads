import type { ReactNode } from "react";

type Props = {
  titulo: string;
  descricao: string;
  acao?: ReactNode;
};

export function EstadoVazio({ titulo, descricao, acao }: Props) {
  return (
    <div className="rounded-xl border border-dashed border-borda bg-superficie p-10 text-center">
      <p className="font-medium text-texto">{titulo}</p>
      <p className="mt-1 text-sm text-texto-suave">{descricao}</p>
      {acao && <div className="mt-4 flex justify-center">{acao}</div>}
    </div>
  );
}
