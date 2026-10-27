"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/lib/auth-context";
import { useRequisicao } from "@/lib/use-requisicao";
import {
  enviarMaterial,
  excluirMaterial,
  listarMateriais,
  mensagemDeErro,
  type Material,
} from "@/lib/api";
import { Carregando } from "@/components/carregando";
import { EstadoErro } from "@/components/estado-erro";
import { EstadoVazio } from "@/components/estado-vazio";
import { ZonaUpload } from "@/components/zona-upload";
import { ItemMaterial } from "@/components/item-material";

const INTERVALO_POLLING_MS = 4000;

type Props = { disciplinaId: string };

export function SecaoMateriais({ disciplinaId }: Props) {
  const { token } = useAuth();
  const { estado, recarregar, atualizarDados } = useRequisicao(
    () => listarMateriais(token as string, disciplinaId),
    [token, disciplinaId],
  );

  const [enviando, setEnviando] = useState(false);
  const [erroUpload, setErroUpload] = useState<string | null>(null);

  const algumProcessando =
    estado.status === "sucesso" &&
    estado.dados.some((material) => material.status === "processando");

  useEffect(() => {
    if (!token || !algumProcessando) return;
    const intervalo = setInterval(() => {
      listarMateriais(token, disciplinaId)
        .then((lista) => atualizarDados(() => lista))
        .catch(() => {});
    }, INTERVALO_POLLING_MS);
    return () => clearInterval(intervalo);
  }, [token, disciplinaId, algumProcessando, atualizarDados]);

  if (!token) return null;
  const tokenValido = token;

  async function enviarArquivo(arquivo: File, titulo: string) {
    setEnviando(true);
    setErroUpload(null);
    try {
      const material = await enviarMaterial(tokenValido, disciplinaId, arquivo, titulo);
      atualizarDados((lista) => [material, ...lista]);
    } catch (erro: unknown) {
      setErroUpload(mensagemDeErro(erro));
    } finally {
      setEnviando(false);
    }
  }

  async function excluir(material: Material) {
    const confirmado = window.confirm(
      `Excluir o material "${material.titulo}"? Essa ação não pode ser desfeita.`,
    );
    if (!confirmado) return;

    try {
      await excluirMaterial(tokenValido, material.id);
      atualizarDados((lista) => lista.filter((item) => item.id !== material.id));
    } catch (erro: unknown) {
      window.alert(mensagemDeErro(erro));
    }
  }

  return (
    <section className="flex flex-col gap-4">
      <h2 className="text-xl font-semibold text-texto">Materiais</h2>

      <ZonaUpload enviando={enviando} onEnviar={enviarArquivo} onErro={setErroUpload} />

      {erroUpload && (
        <p role="alert" className="text-sm text-perigo">
          {erroUpload}
        </p>
      )}

      {estado.status === "carregando" && <Carregando rotulo="Carregando materiais…" />}

      {estado.status === "erro" && (
        <EstadoErro mensagem={estado.mensagem} onTentarNovamente={recarregar} />
      )}

      {estado.status === "sucesso" && estado.dados.length === 0 && (
        <EstadoVazio
          titulo="Nenhum material enviado"
          descricao="Envie PDFs ou arquivos de texto para gerar resumos e tirar dúvidas com a IA."
        />
      )}

      {estado.status === "sucesso" && estado.dados.length > 0 && (
        <ul className="flex flex-col gap-3">
          {estado.dados.map((material) => (
            <ItemMaterial
              key={material.id}
              material={material}
              disciplinaId={disciplinaId}
              onExcluir={() => excluir(material)}
            />
          ))}
        </ul>
      )}
    </section>
  );
}
