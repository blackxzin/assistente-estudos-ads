export function Carregando({ rotulo = "Carregando…" }: { rotulo?: string }) {
  return (
    <div role="status" className="flex items-center gap-3 py-10 text-texto-suave">
      <span
        aria-hidden="true"
        className="size-4 animate-spin rounded-full border-2 border-borda border-t-acento"
      />
      <span>{rotulo}</span>
    </div>
  );
}
