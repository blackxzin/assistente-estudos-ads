"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth-context";

export default function PaginaInicial() {
  const router = useRouter();
  const { usuario, carregando } = useAuth();

  useEffect(() => {
    if (carregando) return;
    router.replace(usuario ? "/painel" : "/login");
  }, [carregando, usuario, router]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-fundo text-texto-suave">
      Carregando…
    </div>
  );
}
