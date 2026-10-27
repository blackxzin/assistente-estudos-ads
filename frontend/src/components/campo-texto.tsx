import { useId, type InputHTMLAttributes } from "react";

type Props = InputHTMLAttributes<HTMLInputElement> & {
  rotulo: string;
  erro?: string;
};

export function CampoTexto({ rotulo, erro, id, ...resto }: Props) {
  const idGerado = useId();
  const idCampo = id ?? idGerado;
  const idErro = `${idCampo}-erro`;

  return (
    <div className="flex flex-col gap-1.5">
      <label htmlFor={idCampo} className="text-sm font-medium text-texto">
        {rotulo}
      </label>
      <input
        id={idCampo}
        aria-invalid={erro ? true : undefined}
        aria-describedby={erro ? idErro : undefined}
        className="rounded-md border border-borda bg-superficie px-3 py-2 text-texto placeholder:text-texto-suave focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento"
        {...resto}
      />
      {erro && (
        <p id={idErro} role="alert" className="text-sm text-perigo">
          {erro}
        </p>
      )}
    </div>
  );
}
