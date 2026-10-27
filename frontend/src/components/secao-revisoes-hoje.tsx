import Link from "next/link";
import type { Revisao } from "@/lib/api";
import { CartaoPainel } from "@/components/cartao-painel";

export function SecaoRevisoesHoje({ revisoes }: { revisoes: Revisao[] }) {
  return (
    <CartaoPainel
      titulo="Revisões de hoje"
      acao={
        <Link
          href="/revisoes"
          className="text-sm font-medium text-acento hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento"
        >
          Ver todas
        </Link>
      }
    >
      {revisoes.length === 0 ? (
        <p className="text-sm text-texto-suave">Nenhuma revisão para hoje.</p>
      ) : (
        <ul className="flex flex-col gap-2">
          {revisoes.map((revisao) => (
            <li key={revisao.id} className="rounded-md p-2">
              <p className="font-medium text-texto">{revisao.material_titulo}</p>
              <p className="text-xs text-texto-suave">{revisao.disciplina_nome}</p>
            </li>
          ))}
        </ul>
      )}
    </CartaoPainel>
  );
}
