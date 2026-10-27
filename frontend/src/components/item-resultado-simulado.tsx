import type { ItemCorrecao } from "@/lib/api";

export function ItemResultadoSimulado({ item, numero }: { item: ItemCorrecao; numero: number }) {
  return (
    <li className="rounded-xl border border-borda bg-superficie p-5">
      <div className="flex items-start justify-between gap-3">
        <p className="font-medium text-texto">
          {numero}. {item.enunciado}
        </p>
        <span
          className={`inline-flex shrink-0 items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
            item.acertou ? "bg-acento/15 text-acento" : "bg-perigo/15 text-perigo"
          }`}
        >
          {item.acertou ? "Correto" : "Incorreto"}
        </span>
      </div>

      <div className="mt-3 flex flex-col gap-2">
        {item.alternativas.map((alternativa, indice) => {
          const ehCorreta = indice === item.correta;
          const ehEscolhida = item.escolhida !== null && indice === item.escolhida;
          const classeAlternativa = ehCorreta
            ? "border-acento bg-acento/10"
            : ehEscolhida
              ? "border-perigo bg-perigo/10"
              : "border-borda";

          return (
            <div
              key={indice}
              className={`rounded-md border px-3 py-2 text-texto ${classeAlternativa}`}
            >
              {alternativa}
              {ehCorreta && <span className="ml-2 text-xs text-acento">(resposta correta)</span>}
              {ehEscolhida && !ehCorreta && (
                <span className="ml-2 text-xs text-perigo">(sua resposta)</span>
              )}
            </div>
          );
        })}
      </div>

      <p className="mt-3 text-sm text-texto-suave">{item.explicacao}</p>
    </li>
  );
}
