"use client";

import { useState, type FormEvent } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { CampoTexto } from "@/components/campo-texto";
import { Botao } from "@/components/botao";
import { useAuth, mensagemDeErro } from "@/lib/auth-context";

export default function PaginaCadastro() {
  const router = useRouter();
  const { cadastrarUsuario } = useAuth();
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  async function lidarComEnvio(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    setErro(null);
    setEnviando(true);
    try {
      await cadastrarUsuario(nome, email, senha);
      router.push("/painel");
    } catch (e: unknown) {
      setErro(mensagemDeErro(e));
    } finally {
      setEnviando(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-fundo px-4">
      <div className="w-full max-w-sm rounded-xl border border-borda bg-superficie p-8 shadow-sm">
        <h1 className="text-2xl font-semibold text-texto">Criar conta</h1>
        <p className="mt-1 text-sm text-texto-suave">
          Comece a organizar suas disciplinas e revisões.
        </p>

        <form onSubmit={lidarComEnvio} className="mt-6 flex flex-col gap-4" noValidate>
          <CampoTexto
            rotulo="Nome"
            type="text"
            name="nome"
            autoComplete="name"
            required
            value={nome}
            onChange={(e) => setNome(e.target.value)}
          />
          <CampoTexto
            rotulo="E-mail"
            type="email"
            name="email"
            autoComplete="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <CampoTexto
            rotulo="Senha"
            type="password"
            name="senha"
            autoComplete="new-password"
            minLength={8}
            required
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
          />

          {erro && (
            <p role="alert" className="text-sm text-perigo">
              {erro}
            </p>
          )}

          <Botao type="submit" carregando={enviando} className="mt-2 w-full">
            Criar conta
          </Botao>
        </form>

        <p className="mt-6 text-sm text-texto-suave">
          Já tem conta?{" "}
          <Link href="/login" className="font-medium text-acento hover:underline">
            Entrar
          </Link>
        </p>
      </div>
    </main>
  );
}
