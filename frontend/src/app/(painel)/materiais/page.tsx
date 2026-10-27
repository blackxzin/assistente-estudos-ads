import { EstadoVazio } from "@/components/estado-vazio";

export default function PaginaMateriais() {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-semibold text-texto">Materiais</h1>
        <p className="mt-1 text-texto-suave">
          Seus arquivos, resumos e anotações de estudo.
        </p>
      </div>

      <EstadoVazio
        titulo="Nenhum material cadastrado"
        descricao="Em breve você poderá enviar e organizar materiais aqui."
      />
    </div>
  );
}
