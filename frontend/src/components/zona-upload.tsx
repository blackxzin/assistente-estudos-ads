"use client";

import { useRef, useState, type DragEvent, type FormEvent } from "react";
import { removerExtensaoArquivo, validarArquivoMaterial } from "@/lib/materiais";
import { CampoTexto } from "@/components/campo-texto";
import { Botao } from "@/components/botao";

type Props = {
  enviando: boolean;
  onEnviar: (arquivo: File, titulo: string) => Promise<void>;
  onErro: (mensagem: string) => void;
};

export function ZonaUpload({ enviando, onEnviar, onErro }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [arrastando, setArrastando] = useState(false);
  const [arquivoPendente, setArquivoPendente] = useState<File | null>(null);
  const [titulo, setTitulo] = useState("");

  function processarArquivo(arquivo: File | undefined) {
    if (!arquivo) return;
    const erro = validarArquivoMaterial(arquivo);
    if (erro) {
      onErro(erro);
      return;
    }
    setArquivoPendente(arquivo);
    setTitulo(removerExtensaoArquivo(arquivo.name));
  }

  function lidarComDrop(evento: DragEvent<HTMLDivElement>) {
    evento.preventDefault();
    setArrastando(false);
    if (enviando) return;
    processarArquivo(evento.dataTransfer.files[0]);
  }

  async function lidarComEnvio(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    if (!arquivoPendente) return;
    const tituloFinal = titulo.trim() || removerExtensaoArquivo(arquivoPendente.name);
    await onEnviar(arquivoPendente, tituloFinal);
    setArquivoPendente(null);
    setTitulo("");
  }

  function cancelar() {
    setArquivoPendente(null);
    setTitulo("");
  }

  if (arquivoPendente) {
    return (
      <form
        onSubmit={lidarComEnvio}
        className="flex flex-col gap-3 rounded-xl border border-borda bg-superficie p-6"
      >
        <p className="text-sm text-texto-suave">
          Arquivo selecionado: <span className="font-medium text-texto">{arquivoPendente.name}</span>
        </p>

        <CampoTexto
          rotulo="Título (opcional)"
          name="titulo"
          value={titulo}
          onChange={(evento) => setTitulo(evento.target.value)}
          placeholder={removerExtensaoArquivo(arquivoPendente.name)}
        />

        <div className="flex gap-2">
          <Botao type="submit" carregando={enviando}>
            Enviar material
          </Botao>
          <button
            type="button"
            onClick={cancelar}
            disabled={enviando}
            className="rounded-md border border-borda px-4 py-2 font-medium text-texto transition-colors hover:bg-superficie-hover disabled:cursor-not-allowed disabled:opacity-60 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento"
          >
            Cancelar
          </button>
        </div>
      </form>
    );
  }

  return (
    <div
      onDragOver={(evento) => {
        evento.preventDefault();
        setArrastando(true);
      }}
      onDragLeave={() => setArrastando(false)}
      onDrop={lidarComDrop}
      className={`flex flex-col items-center gap-3 rounded-xl border-2 border-dashed p-8 text-center transition-colors ${
        arrastando ? "border-acento bg-acento/5" : "border-borda bg-superficie"
      }`}
    >
      <p className="text-sm text-texto-suave">Arraste um arquivo PDF ou de texto aqui, ou</p>

      <button
        type="button"
        onClick={() => inputRef.current?.click()}
        className="rounded-md border border-borda px-4 py-2 font-medium text-texto transition-colors hover:bg-superficie-hover focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento"
      >
        Selecionar arquivo
      </button>

      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.txt,application/pdf,text/plain"
        aria-label="Selecionar arquivo de material"
        className="sr-only"
        onChange={(evento) => {
          processarArquivo(evento.target.files?.[0]);
          evento.target.value = "";
        }}
      />

      <p className="text-xs text-texto-suave">PDF ou texto, até 10 MB.</p>
    </div>
  );
}
