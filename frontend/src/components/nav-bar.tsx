"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/lib/auth-context";
import { ThemeToggle } from "@/components/theme-toggle";

const ITENS_NAVEGACAO = [
  { href: "/painel", rotulo: "Painel" },
  { href: "/disciplinas", rotulo: "Disciplinas" },
  { href: "/materiais", rotulo: "Materiais" },
  { href: "/revisoes", rotulo: "Revisões" },
] as const;

export function NavBar() {
  const pathname = usePathname();
  const { usuario, sair } = useAuth();

  return (
    <header className="sticky top-0 z-10 border-b border-borda bg-superficie/90 backdrop-blur">
      <div className="mx-auto flex max-w-5xl items-center gap-6 px-4 py-3">
        <span className="text-lg font-semibold tracking-tight">
          Assistente de Estudos
        </span>

        <nav aria-label="Navegação principal" className="flex-1">
          <ul className="flex gap-1 text-sm">
            {ITENS_NAVEGACAO.map((item) => {
              const ativo = pathname?.startsWith(item.href);
              return (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    aria-current={ativo ? "page" : undefined}
                    className={`rounded-md px-3 py-2 font-medium transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento ${
                      ativo
                        ? "bg-acento text-acento-texto"
                        : "text-texto-suave hover:bg-superficie-hover hover:text-texto"
                    }`}
                  >
                    {item.rotulo}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

        <div className="flex items-center gap-3">
          {usuario && (
            <span className="hidden text-sm text-texto-suave sm:inline">
              {usuario.nome}
            </span>
          )}
          <ThemeToggle />
          <button
            type="button"
            onClick={sair}
            className="rounded-md border border-borda px-3 py-2 text-sm font-medium transition-colors hover:bg-superficie-hover focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-acento"
          >
            Sair
          </button>
        </div>
      </div>
    </header>
  );
}
