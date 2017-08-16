PARCEIRO_RAMO_ATIVIDADE = (
    (1, "agricultura, pecuária, produção florestal, pesca e aqüicultura"),
    (2, "indústrias extrativas"),
    (3, "indústrias de transformação"),
    (4, "eletricidade e gás"),
    (5, "água, esgoto, atividades de gestão de resíduos e descontaminação"),
    (6, "construção"),
    (7, "comércio; reparação de veículos automotores e motocicletas"),
    (8, "transporte, armazenagem e correio"),
    (9, "alojamento e alimentação"),
    (10, "informação e comunicação"),
    (11, "atividades financeiras, de seguros e serviços relacionados"),
    (12, "atividades imobiliárias"),
    (13, "atividades profissionais, científicas e técnicas"),
    (14, "atividades administrativas e serviços complementares"),
    (15, "administração pública, defesa e seguridade social"),
    (16, "educação"),
    (17, "saúde humana e serviços sociais"),
    (18, "artes, cultura, esporte e recreação"),
    (19, "outras atividades de serviços"),
    (20, "serviços domésticos"),
    (21, "organismos internacionais e outras instituições extraterritoriais"),
)

# Grupo Gestor Origem Choices
"""
Lista de escolhas para a Origem de um Membro do Grupo Gestor de uma Praça
"""

PODER_PUBLICO = "Poder Publico"
SOCIEDADE_CIVIL = "Sociedade Civil"
MORADORES_ENTORNO = "Moradores do Entorno"

ORIGEM_CHOICES = (
    ('pp', PODER_PUBLICO),
    ('sc', SOCIEDADE_CIVIL),
    ('me', MORADORES_ENTORNO),
)

# Tipo de Documento de Constituição
"""
Lista de escolhas para o Tipo de Documento de Constituição de um Grupo Gestor
"""

DECRETO = "Decreto"
PORTARIA = "Portaria"
LEI = "Lei"
NAO_FORMALIZADO = "Não Formalizado"

DOCUMENTO_CHOICES = (
    ('d', DECRETO),
    ('p', PORTARIA),
    ('l', LEI),
    ('n', NAO_FORMALIZADO)
)

# Tipo de Membros da Unidade Gestora Local
"""
Lista de escolhas para o Tipo de Membro da Unidade Gestora Local de uma Praça
"""

COORD_GERAL = "Coordenador Geral"
COORD_ENG = "Coordenador de Engenharia (responsável pela obra)"
COORD_CULT = "Coordenador de Cultura"
COORD_ESP = "Coordenador de Esporte"
COORD_ASS = "Coordenador de Assistência Social"
COORD_DSE = "Coordenador de Desenvolvimento Econômico"
COORD_SEGC = "Coordenador de Segurança Cidadã"
COORD_ID = "Coordenador de Inclusão Digital"

MEMBRO_UGL_CHOICES = (
    ('cg', COORD_GERAL),
    ('ce', COORD_ENG),
    ('cc', COORD_CULT),
    ('ces', COORD_ESP),
    ('cas', COORD_ASS),
    ('cds', COORD_DSE),
    ('csc', COORD_SEGC),
    ('cid', COORD_ID),
)

# Tipo de Escolaridade de RH
"""
Lista de escolhas para a escolaridade do RH de uma Praça
"""
SEM_ESCOLARIDADE = "Sem Escolaridade"
FUNDAMENTAL_INCOMPLETO = "Ensino Fundamental Incompleto"
FUNDAMENTAL_COMPLETO = "Ensino Fundamental Completo"
MEDIO_INCOMPLETO = "Ensino Médio Incompleto"
MEDIO_COMPLETO = "Ensino Médio Completo"
TECNICO_INCOMPLETO = "Ensino Técnico Incompleto"
TECNICO_COMPLETO = "Ensino Técnico Completo"
SUPERIOR_INCOMPLETO = "Ensino Superior Incompleto"
SUPERIOR_COMPLETO = "Ensino Superior Completo"
ESPECIALIZACAO = "Especialização"
MESTRADO = "Mestrado"
DOUTORADO = "Doutorado"

ESCOLARIDADE_CHOICES = (
    ('se', SEM_ESCOLARIDADE),
    ('efi', FUNDAMENTAL_INCOMPLETO),
    ('efc', FUNDAMENTAL_COMPLETO),
    ('emi', MEDIO_INCOMPLETO),
    ('emc', MEDIO_COMPLETO),
    ('eti', TECNICO_INCOMPLETO),
    ('etc', TECNICO_COMPLETO),
    ('esi', SUPERIOR_INCOMPLETO),
    ('esc', SUPERIOR_COMPLETO),
    ('esp', ESPECIALIZACAO),
    ('mes', MESTRADO),
    ('doc', DOUTORADO),
)

# Tipo de Formação de RH
"""
Lista de escolhas para a Formação do RH de uma Praça
"""

BIBLIOTECONOMIA = "Biblioteconomia"
EDUCACAO_FISICA = "Educação física"
SERVICO_SOCIAL = "Serviço Social"
PSICOLOGIA = "Psicologia"
PEDAGOGIA = "Pedagogia"
SONOPLASTIA = "Sonoplastia e iluminação"
AUDIOVISUAL = "Audiovisual"
OUTROS = "Outros"

FORMACAO_CHOICES = (
    ('bib', BIBLIOTECONOMIA),
    ('edf', EDUCACAO_FISICA),
    ('ss', SERVICO_SOCIAL),
    ('psi', PSICOLOGIA),
    ('ped', PEDAGOGIA),
    ('son', SONOPLASTIA),
    ('aud', AUDIOVISUAL),
    ('otr', OUTROS),
)

# Tipo de Vinculo de RH
"""
Lista de tipos de vinculos do RH de uma Praça
"""

SERVIDOR_ESTATUTARIO = "Servidor Estatutário"
SERVIDOR_TEMPORARIO = "Servidor Temporário"
EMPREGADO_PUBLICO = "Empregado Público (CLT)"
COMISSIONADO = "Comissionado"
TERCEIRIZADO = "Terceirizado"
COOPERADO = "Trabalhador de Empresa , Cooperativa ou Entidade Prestadora de Serviços"
VOLUNTARIO = "Voluntário"
OUTRO = "Outro vínculo não permanente"

VINCULO_CHOICES = (
    ('se', SERVIDOR_ESTATUTARIO),
    ('st', SERVIDOR_TEMPORARIO),
    ('ep', EMPREGADO_PUBLICO),
    ('com', COMISSIONADO),
    ('ter', TERCEIRIZADO),
    ('coo', COOPERADO),
    ('vol', VOLUNTARIO),
    ('otr', OUTRO),
)

# Area de Atuação de Atores
"""
Lista de Áreas de Atuação de Atores de uma Praça
"""

ASSISTENCIA_SOCIAL = "Assistencia Social"
COMERCIO = "Comércio, Serviço e Produção"
CULTURA = "Cultura"
ENSINO = "Ensino e Pesquisa"
ESPORTE = "Esporte"
SAUDE = "Saúde"
COMUNICACAO = "Veículos de Comunicação Local"
OUTROS = "Outros"

ATUACAO_CHOICES = (
    ('asso', ASSISTENCIA_SOCIAL),
    ('comr', COMERCIO),
    ('cult', CULTURA),
    ('ens', ENSINO),
    ('espt', ESPORTE),
    ('saud', SAUDE),
    ('com', COMUNICACAO),
    ('otr', OUTROS)
)

# Descrição de Atividade do Ator
"""
Lista de Descrições de Atividades de Atores de uma Praça
"""

ARTES_CENICAS = "artes cênicas, espetáculos e atividades complementares"
CRIACAO_ARTISTICA = "criação artística"
GESTAO_DE_ESPACOS = "gestão de espaços para artes cênicas, espetáculos e outras atividades artísticas"
ATIVIDADES_BIBLIOTECAS = "atividades de bibliotecas e arquivos"
ATIVIDADES_MUSEUS = "atividades de museus e de exploração, restauração artística e conservação de lugares e prédios históricos e atrações similares"
ATIVIDADES_JARDINS = "atividades de jardins botânicos, zoológicos, parques nacionais, reservas ecológicas e áreas de proteção ambiental"
GESTAO_ESPORTES = "gestão de instalações de esportes"
CLUBES_SOCIAIS = "clubes sociais, esportivos e similares"
ATIVIDADES_FISICAS = "atividades de condicionamento físico"
ATIVIDADES_ESPORTIVAS_NE = "atividades esportivas não especificadas anteriormente"
PARQUES_DIVERSAO = "parques de diversão e parques temáticos"
ATIVIDADES_RECREACAO = "atividades de recreação e lazer não especificadas anteriormente"
EDUCACAO_INFANTIL = "educação infantil e ensino fundamental"
ENSINO_MEDIO = "ensino médio"
EDUCACAO_SUPERIOR = "educação superior"
EDUCACAO_PROFISSIONAL = "educação profissional de nível técnico e tecnológico"
ATIVIDADES_APOIO = "atividades de apoio à educação"
OUTRAS_ATIVIDADES_ENSINO = "outras atividades de ensino"
ATIVIDADES_CINEMATOGRAFICAS = "atividades cinematográficas, produção de vídeos e de programas de televisão"
ATIVIDADES_SOM = "atividades de gravação de som e de edição de música"
ATIVIDADES_RADIO = "atividades de rádio"
ATIVIDADES_TELEVISAO = "atividades de televisão"
ATIVIDADES_SAUDE = "atividades de atenção à saúde humana integradas com assistência social, prestadas em residências coletivas e particulares"

DESCRICAO_CHOICES = (
    (1, ARTES_CENICAS),
    (2, CRIACAO_ARTISTICA),
    (3, GESTAO_DE_ESPACOS),
    (4, ATIVIDADES_BIBLIOTECAS),
    (5, ATIVIDADES_MUSEUS),
    (6, ATIVIDADES_JARDINS),
    (7, GESTAO_ESPORTES),
    (8, CLUBES_SOCIAIS),
    (9, ATIVIDADES_FISICAS),
    (10, ATIVIDADES_ESPORTIVAS_NE),
    (11, PARQUES_DIVERSAO),
    (12, ATIVIDADES_RECREACAO),
    (13, EDUCACAO_INFANTIL),
    (14, ENSINO_MEDIO),
    (15, EDUCACAO_SUPERIOR),
    (16, EDUCACAO_PROFISSIONAL),
    (17, ATIVIDADES_APOIO),
    (18, OUTRAS_ATIVIDADES_ENSINO),
    (19, ATIVIDADES_CINEMATOGRAFICAS),
    (20, ATIVIDADES_SOM),
    (21, ATIVIDADES_TELEVISAO),
    (22, ATIVIDADES_SAUDE),
)
