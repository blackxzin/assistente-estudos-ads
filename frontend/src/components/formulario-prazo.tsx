"use client";

import { useId, useState, type FormEvent } from "react";
import { CampoTexto } from "@/components/campo-texto";
import { Botao } from "@/components/botao";
import type { DadosPrazo, TipoPrazo } from "@/lib/api";

type Props = {
  valoresIniciais?: DadosPrazo;
  enviando: boolean;
  erro: string | null;
  onEnviar: (dados: DadosPrazo) => void;
  onCancelar: () => void;
};

type ErrosFormulario = Partial<Record<"titulo" | "data", string>>;

function validar(dados: DadosPrazo): ErrosFormulario {
  const erros: ErrosFormulario = {};
  if (dados.titulo.trim().length < 2) {
    erros.titulo = "Informe um título para o prazo.";
  }
  if (!dados.data) {
    erros.data = "Informe a data do prazo.";
  }
  return erros;
}

export function FormularioPrazo({ valoresIniciais, enviando, erro, onEnviar, onCancelar }: Props) {
  const [titulo, setTitulo] = useState(valoresIniciais?.titulo ?? "");
  const [tipo, setTipo] = useState<TipoPrazo>(valoresIniciais?.tipo ?? "prova");
  const [data, setData] = useState(valoresIniciais?.data ?? "");
  const [concluido, setConcluido] = useState(valoresIniciais?.concluido ?? false);
  const [errosCampo, setErrosCampo] = useState<ErrosFormulario>({});
  const idTipo = useId();
  const idConcluido = useId();

  function lidarComEnvio(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    const dados: DadosPrazo = { titulo: titulo.trim(), tipo, data, concluido };
    const erros = validar(dados);
    setErrosCampo(erros);
    if (Object.keys(erros).length > 0) return;
    onEnviar(dados);
  }

  return (
    <form onSubmit={lidarComEnvio} className="flex flex-col gap-4" noValidate>
      <CampoTexto
        rotulo="Título"
        name="titulo"
        required
        value={titulo}
        onChange={(e) => setTitulo(e.target.value)}
        erro={errosCampo.titulo}
      />

      <div className="flex flex-col gap-1.5">
        <label htmlFor={idTipo} className="text-sm font-medium text-texto">
          Tipo
        </label>
        <select
          id={idTipo}
          value={tipo}
          onChange={(e) => setTipo(e.target.value as TipoPrazo)}
          className="rounded-md border border-borda bg-superficie px-3 py-2 text-texto focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento"
        >
          <option value="prova">Prova</option>
          <option value="trabalho">Trabalho</option>
        </select>
      </div>

      <CampoTexto
        rotulo="Data"
        type="date"
        name="data"
        required
        value={data}
        onChange={(e) => setData(e.target.value)}
        erro={errosCampo.data}
      />

      <div className="flex items-center gap-2">
        <input
          id={idConcluido}
          type="checkbox"
          checked={concluido}
          onChange={(e) => setConcluido(e.target.checked)}
          className="size-4 rounded border-borda accent-acento"
        />
        <label htmlFor={idConcluido} className="text-sm text-texto">
          Concluído
        </label>
      </div>

      {erro && (
        <p role="alert" className="text-sm text-perigo">
          {erro}
        </p>
      )}

      <div className="mt-2 flex justify-end gap-2">
        <button
          type="button"
          onClick={onCancelar}
          className="rounded-md border border-borda px-4 py-2 font-medium text-texto transition-colors hover:bg-superficie-hover focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento"
        >
          Cancelar
        </button>
        <Botao type="submit" carregando={enviando}>
          Salvar
        </Botao>
      </div>
    </form>
  );
}
