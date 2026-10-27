import { DetalheDisciplina } from "@/components/detalhe-disciplina";

export default async function PaginaDisciplina(props: PageProps<"/disciplinas/[id]">) {
  const { id } = await props.params;
  return <DetalheDisciplina disciplinaId={id} />;
}
