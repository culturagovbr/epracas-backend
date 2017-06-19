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
