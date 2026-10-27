import type { QuestaoSimulado } from "@/lib/api";

type Props = {
  questao: QuestaoSimulado;
  numero: number;
  selecionada: number | null;
  onSelecionar: (alternativa: number) => void;
};

export function QuestaoSimuladoItem({ questao, numero, selecionada, onSelecionar }: Props) {
  return (
    <fieldset className="rounded-xl border border-borda bg-superficie p-5">
      <legend className="font-medium text-texto">
        {numero}. {questao.enunciado}
      </legend>
      <div className="mt-3 flex flex-col gap-2">
        {questao.alternativas.map((alternativa, indice) => (
          <label
            key={indice}
            className={`flex items-center gap-3 rounded-md border px-3 py-2 transition-colors ${
              selecionada === indice
                ? "border-acento bg-acento/10"
                : "border-borda hover:bg-superficie-hover"
            }`}
          >
            <input
              type="radio"
              name={`questao-${questao.id}`}
              checked={selecionada === indice}
              onChange={() => onSelecionar(indice)}
              className="size-4 accent-acento"
            />
            <span className="text-texto">{alternativa}</span>
          </label>
        ))}
      </div>
    </fieldset>
  );
}
