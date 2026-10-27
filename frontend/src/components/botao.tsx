import type { ButtonHTMLAttributes } from "react";

type Props = ButtonHTMLAttributes<HTMLButtonElement> & {
  carregando?: boolean;
};

export function Botao({
  carregando = false,
  disabled,
  children,
  type = "button",
  className = "",
  ...resto
}: Props) {
  return (
    <button
      type={type}
      disabled={disabled ?? carregando}
      aria-busy={carregando || undefined}
      className={`inline-flex items-center justify-center gap-2 rounded-md bg-acento px-4 py-2 font-medium text-acento-texto transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento ${className}`}
      {...resto}
    >
      {carregando ? "Aguarde…" : children}
    </button>
  );
}
