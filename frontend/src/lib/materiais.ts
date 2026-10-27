import type { RespostaPergunta } from "@/lib/api";

export const TAMANHO_MAXIMO_MATERIAL_BYTES = 10 * 1024 * 1024;
export const TIPOS_MIME_ACEITOS_MATERIAL = ["application/pdf", "text/plain"];
export const EXTENSOES_ACEITAS_MATERIAL = [".pdf", ".txt"];

export function validarArquivoMaterial(arquivo: File): string | null {
  const nomeMinusculo = arquivo.name.toLowerCase();
  const extensaoValida = EXTENSOES_ACEITAS_MATERIAL.some((extensao) =>
    nomeMinusculo.endsWith(extensao),
  );
  const tipoValido = TIPOS_MIME_ACEITOS_MATERIAL.includes(arquivo.type) || extensaoValida;

  if (!tipoValido) {
    return "Envie um arquivo PDF ou de texto (.pdf ou .txt).";
  }
  if (arquivo.size > TAMANHO_MAXIMO_MATERIAL_BYTES) {
    return "O arquivo excede o tamanho máximo permitido (10 MB).";
  }
  return null;
}

export function removerExtensaoArquivo(nomeArquivo: string): string {
  const indice = nomeArquivo.lastIndexOf(".");
  return indice > 0 ? nomeArquivo.slice(0, indice) : nomeArquivo;
}

export function dividirTopicosResumo(resumo: string): string[] {
  return resumo
    .split("\n")
    .map((linha) => linha.replace(/^[-*•]\s*/, "").trim())
    .filter((linha) => linha.length > 0);
}

export type MensagemConversa = {
  id: string;
  pergunta: string;
  enviando: boolean;
  resposta?: RespostaPergunta;
  erro?: string;
};
