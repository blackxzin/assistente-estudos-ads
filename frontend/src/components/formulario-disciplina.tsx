"use client";

import { useState, type FormEvent } from "react";
import { CampoTexto } from "@/components/campo-texto";
import { Botao } from "@/components/botao";
import { PALETA_CORES_DISCIPLINA } from "@/lib/cores-disciplina";
import type { DadosDisciplina } from "@/lib/api";

type Props = {
  valoresIniciais?: DadosDisciplina;
  enviando: boolean;
  erro: string | null;
  onEnviar: (dados: DadosDisciplina) => void;
  onCancelar: () => void;
};

function validar(dados: DadosDisciplina): Partial<Record<keyof DadosDisciplina, string>> {
  const erros: Partial<Record<keyof DadosDisciplina, string>> = {};
  if (dados.nome.trim().length < 2) {
    erros.nome = "Informe o nome da disciplina.";
  }
  if (dados.professor.trim().length < 2) {
    erros.professor = "Informe o nome do professor.";
  }
  return erros;
}

export function FormularioDisciplina({
  valoresIniciais,
  enviando,
  erro,
  onEnviar,
  onCancelar,
}: Props) {
  const [nome, setNome] = useState(valoresIniciais?.nome ?? "");
  const [professor, setProfessor] = useState(valoresIniciais?.professor ?? "");
  const [cor, setCor] = useState(valoresIniciais?.cor ?? PALETA_CORES_DISCIPLINA[0].valor);
  const [errosCampo, setErrosCampo] = useState<Partial<Record<keyof DadosDisciplina, string>>>(
    {},
  );

  function lidarComEnvio(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    const dados: DadosDisciplina = { nome: nome.trim(), professor: professor.trim(), cor };
    const erros = validar(dados);
    setErrosCampo(erros);
    if (Object.keys(erros).length > 0) return;
    onEnviar(dados);
  }

  return (
    <form onSubmit={lidarComEnvio} className="flex flex-col gap-4" noValidate>
      <CampoTexto
        rotulo="Nome da disciplina"
        name="nome"
        required
        value={nome}
        onChange={(e) => setNome(e.target.value)}
        erro={errosCampo.nome}
      />
      <CampoTexto
        rotulo="Professor"
        name="professor"
        required
        value={professor}
        onChange={(e) => setProfessor(e.target.value)}
        erro={errosCampo.professor}
      />

      <fieldset>
        <legend className="text-sm font-medium text-texto">Cor</legend>
        <div role="radiogroup" aria-label="Cor da disciplina" className="mt-2 flex flex-wrap gap-2">
          {PALETA_CORES_DISCIPLINA.map((opcao) => (
            <button
              key={opcao.valor}
              type="button"
              role="radio"
              aria-checked={cor === opcao.valor}
              aria-label={opcao.nome}
              title={opcao.nome}
              onClick={() => setCor(opcao.valor)}
              className={`size-8 rounded-full border-2 transition-transform focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento ${
                cor === opcao.valor ? "scale-110 border-texto" : "border-transparent"
              }`}
              style={{ backgroundColor: opcao.valor }}
            />
          ))}
        </div>
      </fieldset>

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
