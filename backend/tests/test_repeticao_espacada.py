from datetime import date, timedelta

from app.services.repeticao_espacada import (
    INTERVALOS_DIAS,
    ajustar_data_existente,
    primeira_revisao,
    proxima_revisao,
)

HOJE = date(2026, 1, 1)


def test_primeira_revisao_sem_prova_usa_intervalo_normal():
    data, etapa = primeira_revisao(HOJE, data_prova=None)

    assert etapa == 0
    assert data == HOJE + timedelta(days=INTERVALOS_DIAS[0])


def test_primeira_revisao_com_prova_distante_nao_altera_intervalo():
    data_prova = HOJE.replace(month=6)
    data, etapa = primeira_revisao(HOJE, data_prova)

    assert etapa == 0
    assert (data - HOJE).days == INTERVALOS_DIAS[0]


def test_lembrei_avanca_uma_etapa():
    data, etapa = proxima_revisao(HOJE, etapa_atual=1, desempenho="lembrei", data_prova=None)

    assert etapa == 2
    assert (data - HOJE).days == INTERVALOS_DIAS[2]


def test_lembrei_na_ultima_etapa_permanece_na_ultima():
    ultima_etapa = len(INTERVALOS_DIAS) - 1
    data, etapa = proxima_revisao(HOJE, etapa_atual=ultima_etapa, desempenho="lembrei", data_prova=None)

    assert etapa == ultima_etapa
    assert (data - HOJE).days == INTERVALOS_DIAS[ultima_etapa]


def test_dificil_repete_a_mesma_etapa():
    data, etapa = proxima_revisao(HOJE, etapa_atual=2, desempenho="dificil", data_prova=None)

    assert etapa == 2
    assert (data - HOJE).days == INTERVALOS_DIAS[2]


def test_esqueci_volta_para_etapa_zero():
    data, etapa = proxima_revisao(HOJE, etapa_atual=4, desempenho="esqueci", data_prova=None)

    assert etapa == 0
    assert (data - HOJE).days == INTERVALOS_DIAS[0]


def test_prova_no_passado_usa_intervalo_normal():
    data_prova = date(2025, 12, 1)
    data, etapa = proxima_revisao(HOJE, etapa_atual=4, desempenho="lembrei", data_prova=data_prova)

    assert (data - HOJE).days == INTERVALOS_DIAS[-1]


def test_prova_muito_proxima_comprime_o_intervalo():
    data_prova = date(2026, 1, 3)  # 2 dias a partir de HOJE
    data, etapa = proxima_revisao(HOJE, etapa_atual=4, desempenho="lembrei", data_prova=data_prova)

    assert etapa == 4
    assert data < data_prova
    assert data > HOJE


def test_prova_amanha_agenda_para_amanha_mesmo_sem_folga():
    data_prova = date(2026, 1, 2)  # 1 dia a partir de HOJE
    data, _etapa = proxima_revisao(HOJE, etapa_atual=0, desempenho="esqueci", data_prova=data_prova)

    assert data == data_prova


def test_ajustar_data_existente_nao_muda_se_ja_cabe_antes_da_prova():
    data_prevista = date(2026, 1, 5)
    data_prova = date(2026, 1, 20)

    assert ajustar_data_existente(data_prevista, data_prova, HOJE) == data_prevista


def test_ajustar_data_existente_encurta_quando_prova_antecipou():
    data_prevista = date(2026, 1, 20)
    data_prova = date(2026, 1, 5)

    nova_data = ajustar_data_existente(data_prevista, data_prova, HOJE)

    assert nova_data < data_prova
    assert nova_data > HOJE


def test_ajustar_data_existente_ignora_prova_no_passado():
    data_prevista = date(2026, 1, 20)
    data_prova = date(2025, 12, 1)

    assert ajustar_data_existente(data_prevista, data_prova, HOJE) == data_prevista


def test_ajustar_data_existente_sem_prova_nao_muda():
    data_prevista = date(2026, 1, 20)

    assert ajustar_data_existente(data_prevista, None, HOJE) == data_prevista
