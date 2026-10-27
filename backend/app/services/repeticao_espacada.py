from datetime import date, timedelta

INTERVALOS_DIAS = [1, 3, 7, 14, 30]


def _ajustar_para_prova(data_referencia: date, intervalo: int, data_prova: date | None) -> int:
    """Encurta o intervalo para nunca agendar além da prova. Prova no passado ou ausente: intervalo normal."""
    if data_prova is None:
        return intervalo

    dias_restantes = (data_prova - data_referencia).days
    if dias_restantes <= 0:
        return intervalo

    limite = dias_restantes - 1 if dias_restantes > 1 else dias_restantes
    return min(intervalo, max(1, limite))


def primeira_revisao(data_referencia: date, data_prova: date | None) -> tuple[date, int]:
    """Agenda a primeira revisão (etapa 0) a partir da data em que o material ficou pronto."""
    intervalo = _ajustar_para_prova(data_referencia, INTERVALOS_DIAS[0], data_prova)
    return data_referencia + timedelta(days=intervalo), 0


def proxima_revisao(
    data_referencia: date, etapa_atual: int, desempenho: str, data_prova: date | None
) -> tuple[date, int]:
    """Calcula a próxima revisão a partir do desempenho relatado na revisão concluída hoje."""
    if desempenho == "esqueci":
        nova_etapa = 0
    elif desempenho == "dificil":
        nova_etapa = etapa_atual
    elif desempenho == "lembrei":
        nova_etapa = min(etapa_atual + 1, len(INTERVALOS_DIAS) - 1)
    else:
        raise ValueError(f"desempenho inválido: {desempenho}")

    intervalo = _ajustar_para_prova(data_referencia, INTERVALOS_DIAS[nova_etapa], data_prova)
    return data_referencia + timedelta(days=intervalo), nova_etapa


def ajustar_data_existente(data_prevista: date, data_prova: date | None, hoje: date) -> date:
    """Reencaixa uma revisão já agendada quando a prova da disciplina muda de data."""
    if data_prova is None or data_prova <= hoje or data_prevista <= data_prova:
        return data_prevista

    limite = data_prova - timedelta(days=1)
    return max(limite, hoje + timedelta(days=1))
