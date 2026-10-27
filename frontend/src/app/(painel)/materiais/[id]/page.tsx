import { Suspense } from "react";
import { DetalheMaterial } from "@/components/detalhe-material";
import { Carregando } from "@/components/carregando";

export default async function PaginaMaterial(props: PageProps<"/materiais/[id]">) {
  const { id } = await props.params;
  return (
    <Suspense fallback={<Carregando rotulo="Carregando material…" />}>
      <DetalheMaterial materialId={id} />
    </Suspense>
  );
}
