export function formatarDataHora(dataIso: string): string {
  const data = new Date(dataIso);
  if (Number.isNaN(data.getTime())) return dataIso;
  return new Intl.DateTimeFormat("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(data);
}

export function formatarData(data: string): string {
  const partes = data.split("-").map(Number);
  if (partes.length !== 3 || partes.some(Number.isNaN)) return data;
  const [ano, mes, dia] = partes;
  const dataLocal = new Date(ano, mes - 1, dia);
  return new Intl.DateTimeFormat("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  }).format(dataLocal);
}
