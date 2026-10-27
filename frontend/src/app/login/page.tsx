"use client";

import { useState, type FormEvent } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { CampoTexto } from "@/components/campo-texto";
import { Botao } from "@/components/botao";
import { useAuth, mensagemDeErro } from "@/lib/auth-context";

export default function PaginaLogin() {
  const router = useRouter();
  const { entrarComCredenciais } = useAuth();
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  async function lidarComEnvio(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    setErro(null);
    setEnviando(true);
    try {
      await entrarComCredenciais(email, senha);
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
        <h1 className="text-2xl font-semibold text-texto">Entrar</h1>
        <p className="mt-1 text-sm text-texto-suave">
          Acesse sua conta para continuar seus estudos.
        </p>

        <form onSubmit={lidarComEnvio} className="mt-6 flex flex-col gap-4" noValidate>
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
            autoComplete="current-password"
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
            Entrar
          </Botao>
        </form>

        <p className="mt-6 text-sm text-texto-suave">
          Ainda não tem conta?{" "}
          <Link href="/cadastro" className="font-medium text-acento hover:underline">
            Cadastre-se
          </Link>
        </p>
      </div>
    </main>
  );
}
