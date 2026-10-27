"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import {
  buscarUsuarioAtual,
  cadastrar,
  entrar,
  type Usuario,
} from "@/lib/api";

export { mensagemDeErro } from "@/lib/api";

const CHAVE_TOKEN = "assistente-estudos:token";

interface AuthContextValue {
  usuario: Usuario | null;
  token: string | null;
  carregando: boolean;
  entrarComCredenciais: (email: string, senha: string) => Promise<void>;
  cadastrarUsuario: (nome: string, email: string, senha: string) => Promise<void>;
  sair: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [usuario, setUsuario] = useState<Usuario | null>(null);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    const tokenSalvo = window.localStorage.getItem(CHAVE_TOKEN);
    if (!tokenSalvo) {
      Promise.resolve().then(() => setCarregando(false));
      return;
    }

    buscarUsuarioAtual(tokenSalvo)
      .then((dadosUsuario) => {
        setToken(tokenSalvo);
        setUsuario(dadosUsuario);
      })
      .catch(() => {
        window.localStorage.removeItem(CHAVE_TOKEN);
      })
      .finally(() => setCarregando(false));
  }, []);

  const entrarComCredenciais = useCallback(async (email: string, senha: string) => {
    const resposta = await entrar(email, senha);
    const dadosUsuario = await buscarUsuarioAtual(resposta.access_token);
    window.localStorage.setItem(CHAVE_TOKEN, resposta.access_token);
    setToken(resposta.access_token);
    setUsuario(dadosUsuario);
  }, []);

  const cadastrarUsuario = useCallback(
    async (nome: string, email: string, senha: string) => {
      await cadastrar(nome, email, senha);
      await entrarComCredenciais(email, senha);
    },
    [entrarComCredenciais],
  );

  const sair = useCallback(() => {
    window.localStorage.removeItem(CHAVE_TOKEN);
    setToken(null);
    setUsuario(null);
  }, []);

  const valor = useMemo(
    () => ({ usuario, token, carregando, entrarComCredenciais, cadastrarUsuario, sair }),
    [usuario, token, carregando, entrarComCredenciais, cadastrarUsuario, sair],
  );

  return <AuthContext.Provider value={valor}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const contexto = useContext(AuthContext);
  if (!contexto) {
    throw new Error("useAuth precisa ser usado dentro de um AuthProvider");
  }
  return contexto;
}
