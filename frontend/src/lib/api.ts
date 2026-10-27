const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.status = status;
    this.name = "ApiError";
  }
}

async function extrairMensagemErro(resposta: Response): Promise<string> {
  if (resposta.status === 429) {
    return "Limite de uso da IA atingido. Tente novamente em alguns instantes.";
  }
  if (resposta.status === 413) {
    return "O arquivo excede o tamanho máximo permitido (10 MB).";
  }
  if (resposta.status === 415) {
    return "Tipo de arquivo não suportado. Envie um PDF ou um arquivo de texto.";
  }

  try {
    const dados = await resposta.json();
    if (typeof dados?.detail === "string") return dados.detail;
    if (Array.isArray(dados?.detail)) {
      return dados.detail.map((item: { msg?: string }) => item.msg).join(", ");
    }
    if (typeof dados?.erro === "string") return dados.erro;
  } catch {
    // corpo sem JSON válido
  }
  return "Ocorreu um erro inesperado. Tente novamente.";
}

type Opcoes = {
  token?: string | null;
  corpo?: unknown;
  metodo?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
};

export async function apiFetch<T>(caminho: string, opcoes: Opcoes = {}): Promise<T> {
  const { token, corpo, metodo = "GET" } = opcoes;

  const cabecalhos: Record<string, string> = {};
  if (token) {
    cabecalhos.Authorization = `Bearer ${token}`;
  }

  let corpoRequisicao: BodyInit | undefined;
  if (corpo instanceof FormData) {
    corpoRequisicao = corpo;
  } else if (corpo !== undefined) {
    cabecalhos["Content-Type"] = "application/json";
    corpoRequisicao = JSON.stringify(corpo);
  }

  const resposta = await fetch(`${BASE_URL}${caminho}`, {
    method: metodo,
    headers: cabecalhos,
    body: corpoRequisicao,
  });

  if (!resposta.ok) {
    throw new ApiError(resposta.status, await extrairMensagemErro(resposta));
  }

  if (resposta.status === 204) {
    return undefined as T;
  }

  return (await resposta.json()) as T;
}

export type Usuario = {
  id: string;
  nome: string;
  email: string;
};

export type RespostaLogin = {
  access_token: string;
};

export function cadastrar(nome: string, email: string, senha: string) {
  return apiFetch<Usuario>("/auth/cadastro", {
    metodo: "POST",
    corpo: { nome, email, senha },
  });
}

export function entrar(email: string, senha: string) {
  return apiFetch<RespostaLogin>("/auth/login", {
    metodo: "POST",
    corpo: { email, senha },
  });
}

export function buscarUsuarioAtual(token: string) {
  return apiFetch<Usuario>("/auth/eu", { token });
}

export function mensagemDeErro(erro: unknown): string {
  if (erro instanceof ApiError) return erro.message;
  if (erro instanceof Error) return erro.message;
  return "Ocorreu um erro inesperado. Tente novamente.";
}

export type Disciplina = {
  id: string;
  nome: string;
  professor: string;
  cor: string;
};

export type DadosDisciplina = {
  nome: string;
  professor: string;
  cor: string;
};

export type TipoPrazo = "prova" | "trabalho";

export type Prazo = {
  id: string;
  titulo: string;
  tipo: TipoPrazo;
  data: string;
  concluido: boolean;
};

export type DadosPrazo = {
  titulo: string;
  tipo: TipoPrazo;
  data: string;
  concluido: boolean;
};

export function listarDisciplinas(token: string) {
  return apiFetch<Disciplina[]>("/disciplinas", { token });
}

export function criarDisciplina(token: string, dados: DadosDisciplina) {
  return apiFetch<Disciplina>("/disciplinas", { metodo: "POST", token, corpo: dados });
}

export function obterDisciplina(token: string, id: string) {
  return apiFetch<Disciplina>(`/disciplinas/${id}`, { token });
}

export function atualizarDisciplina(token: string, id: string, dados: DadosDisciplina) {
  return apiFetch<Disciplina>(`/disciplinas/${id}`, { metodo: "PUT", token, corpo: dados });
}

export function excluirDisciplina(token: string, id: string) {
  return apiFetch<void>(`/disciplinas/${id}`, { metodo: "DELETE", token });
}

export function listarPrazos(token: string, disciplinaId: string) {
  return apiFetch<Prazo[]>(`/disciplinas/${disciplinaId}/prazos`, { token });
}

export function criarPrazo(token: string, disciplinaId: string, dados: DadosPrazo) {
  return apiFetch<Prazo>(`/disciplinas/${disciplinaId}/prazos`, {
    metodo: "POST",
    token,
    corpo: dados,
  });
}

export function atualizarPrazo(token: string, id: string, dados: Partial<DadosPrazo>) {
  return apiFetch<Prazo>(`/prazos/${id}`, { metodo: "PUT", token, corpo: dados });
}

export function excluirPrazo(token: string, id: string) {
  return apiFetch<void>(`/prazos/${id}`, { metodo: "DELETE", token });
}

export type StatusMaterial = "processando" | "pronto" | "erro";

export type Material = {
  id: string;
  titulo: string;
  tipo: string;
  status: StatusMaterial;
  resumo: string | null;
  criado_em: string;
};

export type Citacao = {
  trecho_id: string;
  pagina: number;
  trecho: string;
};

export type RespostaPergunta = {
  resposta: string;
  citacoes: Citacao[];
};

export function listarMateriais(token: string, disciplinaId: string) {
  return apiFetch<Material[]>(`/disciplinas/${disciplinaId}/materiais`, { token });
}

export function enviarMaterial(token: string, disciplinaId: string, arquivo: File, titulo: string) {
  const formData = new FormData();
  formData.append("titulo", titulo);
  formData.append("arquivo", arquivo);
  return apiFetch<Material>(`/disciplinas/${disciplinaId}/materiais`, {
    metodo: "POST",
    token,
    corpo: formData,
  });
}

export function obterMaterial(token: string, id: string) {
  return apiFetch<Material>(`/materiais/${id}`, { token });
}

export function excluirMaterial(token: string, id: string) {
  return apiFetch<void>(`/materiais/${id}`, { metodo: "DELETE", token });
}

export function gerarResumoMaterial(token: string, id: string) {
  return apiFetch<Material>(`/materiais/${id}/resumo`, { metodo: "POST", token });
}

export function perguntarMaterial(token: string, id: string, pergunta: string) {
  return apiFetch<RespostaPergunta>(`/materiais/${id}/perguntas`, {
    metodo: "POST",
    token,
    corpo: { pergunta },
  });
}

export type QuestaoSimulado = {
  id: number;
  enunciado: string;
  alternativas: string[];
};

export type Simulado = {
  id: string;
  material_id: string;
  criado_em: string;
  questoes: QuestaoSimulado[];
};

export type RespostaQuestao = {
  questao_id: number;
  alternativa: number;
};

export type ItemCorrecao = {
  questao_id: number;
  enunciado: string;
  alternativas: string[];
  escolhida: number | null;
  correta: number;
  acertou: boolean;
  explicacao: string;
  trecho_id: number | null;
};

export type ResultadoSimulado = {
  nota: number;
  acertos: number;
  total: number;
  itens: ItemCorrecao[];
};

export function gerarSimulado(token: string, materialId: string, quantidade: number) {
  return apiFetch<Simulado>(`/materiais/${materialId}/simulados`, {
    metodo: "POST",
    token,
    corpo: { quantidade },
  });
}

export function obterSimulado(token: string, id: string) {
  return apiFetch<Simulado>(`/simulados/${id}`, { token });
}

export function corrigirSimulado(token: string, id: string, respostas: RespostaQuestao[]) {
  return apiFetch<ResultadoSimulado>(`/simulados/${id}/corrigir`, {
    metodo: "POST",
    token,
    corpo: { respostas },
  });
}

export type StatusRevisao = "pendente" | "feita" | "pulada";

export type Revisao = {
  id: string;
  material_id: string;
  material_titulo: string;
  disciplina_nome: string;
  data_prevista: string;
  etapa: number;
  status: StatusRevisao;
};

export type DesempenhoRevisao = "lembrei" | "dificil" | "esqueci";

export function listarRevisoes(token: string, de: string, ate: string) {
  const parametros = new URLSearchParams({ de, ate });
  return apiFetch<Revisao[]>(`/revisoes?${parametros.toString()}`, { token });
}

export function concluirRevisao(token: string, id: string, desempenho: DesempenhoRevisao) {
  return apiFetch<Revisao>(`/revisoes/${id}/concluir`, {
    metodo: "POST",
    token,
    corpo: { desempenho },
  });
}

export type PrazoPainel = {
  id: string;
  titulo: string;
  tipo: TipoPrazo;
  data: string;
  disciplina_nome: string;
};

export type SimuladoResumo = {
  simulado_id: string;
  material_titulo: string;
  nota: number;
  data: string;
};

export type DesempenhoPainel = {
  media_nota: number | null;
  total_simulados: number;
  ultimos: SimuladoResumo[];
};

export type Painel = {
  proximos_prazos: PrazoPainel[];
  revisoes_hoje: Revisao[];
  desempenho: DesempenhoPainel;
};

export function obterPainel(token: string) {
  return apiFetch<Painel>("/painel", { token });
}
