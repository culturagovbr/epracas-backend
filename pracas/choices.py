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
    ('otr', OUTRO)
)
