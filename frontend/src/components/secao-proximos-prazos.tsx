import type { PrazoPainel } from "@/lib/api";
import { CartaoPainel } from "@/components/cartao-painel";
import { BadgeTipoPrazo } from "@/components/badge-tipo-prazo";
import { formatarData } from "@/lib/formato";

function encontrarProvaMaisProxima(prazos: PrazoPainel[]): string | null {
  const provas = prazos.filter((prazo) => prazo.tipo === "prova");
  if (provas.length === 0) return null;
  return provas.reduce((maisProxima, atual) => (atual.data < maisProxima.data ? atual : maisProxima))
    .id;
}

export function SecaoProximosPrazos({ prazos }: { prazos: PrazoPainel[] }) {
  const idProvaMaisProxima = encontrarProvaMaisProxima(prazos);

  return (
    <CartaoPainel titulo="Próximos prazos">
      {prazos.length === 0 ? (
        <p className="text-sm text-texto-suave">Nenhum prazo agendado.</p>
      ) : (
        <ul className="flex flex-col gap-2">
          {prazos.map((prazo) => (
            <li
              key={prazo.id}
              className={`flex items-center justify-between gap-2 rounded-md p-2 ${
                prazo.id === idProvaMaisProxima ? "border border-perigo bg-perigo/5" : ""
              }`}
            >
              <div className="min-w-0">
                <p className="truncate font-medium text-texto">{prazo.titulo}</p>
                <p className="text-xs text-texto-suave">{prazo.disciplina_nome}</p>
              </div>
              <div className="flex shrink-0 items-center gap-2">
                <BadgeTipoPrazo tipo={prazo.tipo} />
                <span className="text-sm text-texto-suave">{formatarData(prazo.data)}</span>
              </div>
            </li>
          ))}
        </ul>
      )}
    </CartaoPainel>
  );
}
