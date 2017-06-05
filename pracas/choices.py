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
    (1, PODER_PUBLICO),
    (2, SOCIEDADE_CIVIL),
    (3, MORADORES_ENTORNO),
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
