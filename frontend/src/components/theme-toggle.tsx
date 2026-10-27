"use client";

import { useSyncExternalStore } from "react";
import { useTheme } from "next-themes";

function inscreverSemAlteracoes() {
  return () => {};
}

function useMontado(): boolean {
  return useSyncExternalStore(
    inscreverSemAlteracoes,
    () => true,
    () => false,
  );
}

export function ThemeToggle() {
  const { resolvedTheme, setTheme } = useTheme();
  const montado = useMontado();

  if (!montado) {
    return <div className="size-9 rounded-full" aria-hidden="true" />;
  }

  const escuro = resolvedTheme === "dark";

  return (
    <button
      type="button"
      onClick={() => setTheme(escuro ? "light" : "dark")}
      aria-label={escuro ? "Ativar tema claro" : "Ativar tema escuro"}
      title={escuro ? "Ativar tema claro" : "Ativar tema escuro"}
      className="flex size-9 items-center justify-center rounded-full border border-borda bg-superficie text-texto transition-colors hover:bg-superficie-hover focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento"
    >
      <span aria-hidden="true">{escuro ? "☀️" : "🌙"}</span>
    </button>
  );
}
