import type { ReactNode } from "react";

type Props = {
  titulo: string;
  acao?: ReactNode;
  children: ReactNode;
};

export function CartaoPainel({ titulo, acao, children }: Props) {
  return (
    <div className="flex flex-col gap-3 rounded-xl border border-borda bg-superficie p-5">
      <div className="flex items-center justify-between gap-2">
        <h2 className="font-semibold text-texto">{titulo}</h2>
        {acao}
      </div>
      {children}
    </div>
  );
}
