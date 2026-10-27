"use client";

import { useEffect, useRef, useState } from "react";
import { mensagemDeErro } from "@/lib/api";

type Estado<T> =
  | { status: "carregando" }
  | { status: "erro"; mensagem: string }
  | { status: "sucesso"; dados: T };

export function useRequisicao<T>(buscar: () => Promise<T>, deps: unknown[]) {
  const [estado, setEstado] = useState<Estado<T>>({ status: "carregando" });
  const [versao, setVersao] = useState(0);
  const buscarRef = useRef(buscar);

  useEffect(() => {
    buscarRef.current = buscar;
  });

  useEffect(() => {
    buscarRef
      .current()
      .then((dados) => setEstado({ status: "sucesso", dados }))
      .catch((erro: unknown) => setEstado({ status: "erro", mensagem: mensagemDeErro(erro) }));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [...deps, versao]);

  function recarregar() {
    setEstado({ status: "carregando" });
    setVersao((v) => v + 1);
  }

  function atualizarDados(atualizar: (dados: T) => T) {
    setEstado((atual) =>
      atual.status === "sucesso" ? { status: "sucesso", dados: atualizar(atual.dados) } : atual,
    );
  }

  return { estado, recarregar, atualizarDados };
}
