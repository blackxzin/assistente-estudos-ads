import { Botao } from "@/components/botao";

type Props = {
  mensagem: string;
  onTentarNovamente: () => void;
};

export function EstadoErro({ mensagem, onTentarNovamente }: Props) {
  return (
    <div role="alert" className="rounded-xl border border-perigo/40 bg-superficie p-6 text-center">
      <p className="font-medium text-perigo">Não foi possível carregar os dados</p>
      <p className="mt-1 text-sm text-texto-suave">{mensagem}</p>
      <Botao onClick={onTentarNovamente} className="mt-4">
        Tentar novamente
      </Botao>
    </div>
  );
}
