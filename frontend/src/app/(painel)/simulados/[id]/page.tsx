import { Suspense } from "react";
import { DetalheSimulado } from "@/components/detalhe-simulado";
import { Carregando } from "@/components/carregando";

export default async function PaginaSimulado(props: PageProps<"/simulados/[id]">) {
  const { id } = await props.params;
  return (
    <Suspense fallback={<Carregando rotulo="Carregando simulado…" />}>
      <DetalheSimulado simuladoId={id} />
    </Suspense>
  );
}
