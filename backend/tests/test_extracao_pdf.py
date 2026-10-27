from app.services.extracao_pdf import extrair_paginas_pdf
from tests.ajuda_pdf import gerar_pdf_bytes


def test_extrai_texto_e_numero_da_pagina_de_um_pdf_real():
    conteudo = gerar_pdf_bytes(["Conteudo de teste do material"])

    paginas = extrair_paginas_pdf(conteudo)

    assert len(paginas) == 1
    numero_pagina, texto = paginas[0]
    assert numero_pagina == 1
    assert "Conteudo de teste do material" in texto
