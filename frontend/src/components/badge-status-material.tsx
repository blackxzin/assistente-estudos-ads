import type { StatusMaterial } from "@/lib/api";

const RUBRICAS: Record<StatusMaterial, { rotulo: string; className: string }> = {
  processando: {
    rotulo: "Processando",
    className: "bg-superficie-hover text-texto-suave",
  },
  pronto: {
    rotulo: "Pronto",
    className: "bg-acento/15 text-acento",
  },
  erro: {
    rotulo: "Erro",
    className: "bg-perigo/15 text-perigo",
  },
};

export function BadgeStatusMaterial({ status }: { status: StatusMaterial }) {
  const rubrica = RUBRICAS[status];
  return (
    <span
      role="status"
      className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium ${rubrica.className}`}
    >
      {status === "processando" && (
        <span
          aria-hidden="true"
          className="size-2.5 animate-spin rounded-full border-2 border-texto-suave border-t-transparent"
        />
      )}
      {rubrica.rotulo}
    </span>
  );
}
