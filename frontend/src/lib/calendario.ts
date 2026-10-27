export function formatarDataISO(data: Date): string {
  const ano = data.getFullYear();
  const mes = String(data.getMonth() + 1).padStart(2, "0");
  const dia = String(data.getDate()).padStart(2, "0");
  return `${ano}-${mes}-${dia}`;
}

export function primeiroDiaDoMes(referencia: Date): Date {
  return new Date(referencia.getFullYear(), referencia.getMonth(), 1);
}

export function ultimoDiaDoMes(referencia: Date): Date {
  return new Date(referencia.getFullYear(), referencia.getMonth() + 1, 0);
}

export function gerarDiasDoMes(referencia: Date): (Date | null)[] {
  const primeiro = primeiroDiaDoMes(referencia);
  const ultimo = ultimoDiaDoMes(referencia);
  const diasVazios = primeiro.getDay();
  const dias: (Date | null)[] = Array.from({ length: diasVazios }, () => null);
  for (let dia = 1; dia <= ultimo.getDate(); dia += 1) {
    dias.push(new Date(referencia.getFullYear(), referencia.getMonth(), dia));
  }
  return dias;
}

export const NOMES_MES = [
  "Janeiro",
  "Fevereiro",
  "Março",
  "Abril",
  "Maio",
  "Junho",
  "Julho",
  "Agosto",
  "Setembro",
  "Outubro",
  "Novembro",
  "Dezembro",
];

export const NOMES_DIA_SEMANA = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];
