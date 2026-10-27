import type { MensagemConversa } from "@/lib/materiais";

export function MensagemChat({ mensagem }: { mensagem: MensagemConversa }) {
  return (
    <li className="flex flex-col gap-2">
      <p className="self-end rounded-xl bg-acento px-4 py-2 text-acento-texto">
        {mensagem.pergunta}
      </p>

      {mensagem.enviando && (
        <p role="status" className="text-sm text-texto-suave">
          Pensando…
        </p>
      )}

      {mensagem.erro && (
        <p role="alert" className="text-sm text-perigo">
          {mensagem.erro}
        </p>
      )}

      {mensagem.resposta && (
        <div className="flex flex-col gap-2 rounded-xl border border-borda bg-fundo px-4 py-3">
          <p className="text-texto">{mensagem.resposta.resposta}</p>

          {mensagem.resposta.citacoes.length === 0 ? (
            <p className="text-sm text-texto-suave">
              Não foram encontradas citações no material para esta resposta.
            </p>
          ) : (
            <ul className="flex flex-col gap-1">
              {mensagem.resposta.citacoes.map((citacao) => (
                <li key={citacao.trecho_id}>
                  <details className="rounded-md border border-borda bg-superficie p-2">
                    <summary className="cursor-pointer text-sm font-medium text-texto-suave">
                      Página {citacao.pagina}
                    </summary>
                    <p className="mt-2 text-sm text-texto">{citacao.trecho}</p>
                  </details>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </li>
  );
}
