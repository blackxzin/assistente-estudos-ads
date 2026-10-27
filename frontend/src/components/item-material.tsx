import Link from "next/link";
import type { Material } from "@/lib/api";
import { BadgeStatusMaterial } from "@/components/badge-status-material";
import { formatarDataHora } from "@/lib/formato";

type Props = {
  material: Material;
  disciplinaId: string;
  onExcluir: () => void;
};

export function ItemMaterial({ material, disciplinaId, onExcluir }: Props) {
  return (
    <li className="flex flex-wrap items-center gap-4 rounded-xl border border-borda bg-superficie p-4">
      <div className="min-w-0 flex-1">
        <Link
          href={`/materiais/${material.id}?disciplinaId=${disciplinaId}`}
          className="font-medium text-texto hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento"
        >
          {material.titulo}
        </Link>
        <div className="mt-1 flex items-center gap-2 text-sm text-texto-suave">
          <BadgeStatusMaterial status={material.status} />
          <span>{formatarDataHora(material.criado_em)}</span>
        </div>
      </div>

      <button
        type="button"
        onClick={onExcluir}
        aria-label={`Excluir material ${material.titulo}`}
        className="rounded-md p-2 text-texto-suave transition-colors hover:bg-superficie-hover hover:text-perigo focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento"
      >
        <span aria-hidden="true">🗑️</span>
      </button>
    </li>
  );
}
