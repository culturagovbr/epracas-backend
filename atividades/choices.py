CINETEATRO = 'Cineteatro'
BIBLIOTECA = 'Biblioteca'
LAB_MULTIMIDIA = 'Laboratório Multimídia'
QUADRA = 'Quadra'
SALA_MULTIUSO = 'Sala Multiuso'
CRAS = 'CRAS'
PISTA_SKATE = 'Pista de Skate'
AREAS_EXTERNAS = 'Areas Externas'

ESPACOS_CHOICES = (
    (1, CINETEATRO),
    (2, BIBLIOTECA),
    (3, LAB_MULTIMIDIA),
    (4, QUADRA),
    (5, SALA_MULTIUSO),
    (6, CRAS),
    (7, PISTA_SKATE),
    (8, AREAS_EXTERNAS),
)

APRESENTACAO = 'Apresentação'
ATENDIMENTO = 'Atendimento'
COMERCIALIZACAO = 'Comercialização de Produtos'
CURSO = 'Curso'
ESPETACULO = 'Espetaculo'
EXPOSICAO = 'Exposição'
FEIRA = 'Feira de Trocas'
OFICINA = 'Oficina'
PALESTRA = 'Palestra'
REUNIAO = 'Reunião'
SEMINARIO = 'Seminário'
SHOW = 'Show'
FESTAS = 'Festas'
OUTROS = 'Outros'

TIPO_ATIVIDADE_CHOICES = (
    (1, APRESENTACAO),
    (2, ATENDIMENTO),
    (3, COMERCIALIZACAO),
    (4, CURSO),
    (5, ESPETACULO),
    (6, EXPOSICAO),
    (7, FEIRA),
    (8, OFICINA),
    (9, PALESTRA),
    (10, REUNIAO),
    (11, SEMINARIO),
    (12, SHOW),
    (13, FESTAS),
    (14, OUTROS),
)

BAIRRO = 'Bairro da Praça CEU'
BAIRRO_ENTORNO = 'Bairros do Entorno da Praça'
MUNICIPIO = 'Munícipio'
MUNICIPIO_ENTORNO = 'Municipios do Entorno'
ESTADO = 'Estado'

TERRITORIO_CHOICES = (
    (1, BAIRRO),
    (2, BAIRRO_ENTORNO),
    (3, MUNICIPIO),
    (4, MUNICIPIO_ENTORNO),
    (5, ESTADO),
)

EGRESSOS_SISTEMA_PRISIONAL = "Egressos do Sistema Prisional"
FAMILIAS_PRESOS = "Famílias de presos do Sistema Carcerário"
JOVENS_SOCIOEDUCATIVAS = "Jovens em medidas socioeducativas"
VITIMAS_DE_VIOLENCIA = "Pessoas ou grupos vítimas de violência"
PESSOAS_SOFRIMENTO_PSIQUICO = "Pessoas em sofrimento psíquico"
POPULACAO_SITUACAO_RUA = "População em situação de rua"
CATADORES_RECICLAVEIS = "Catadores de material reciclável"
ATINGIDOS_INFRAESTRUTURA = "Atingidos por empreendimento de Infraestrutura"
IMIGRANTES = "Imigrantes"
FAMILIAS_ACAMPADAS = "Familias acampadas"
AGRICULTURES_FAMILIARES = "Agricultures Familiares"
ASSENTADOS_REFORMA_AGRARIA = "Assentados da Reforma Agrária"
POVOS_MATRIZ_AFRICANA = "Povos e Comunidades Tradicionais de Matriz Africana"
QUILOMBOLAS = "Quilombolas"
INDIGENAS = "Indígenas"
EXTRATIVISTAS = "Extrativistas"
PESCADORES = "Pescadores artesanais"
RIBEIRINHOS = "Ribeirinhos"
SERTANEJOS = "Sertanejos"
CIGANOS = "Ciganos"
LGBT = "População de Lésbicas, Gays, Bissexuais, Travestis, Transexuais e Transgêneros - LGBT"
MULHERES = "Mulheres"
PESSOAS_DEFICIENCIA = "Pessoas com Deficiência"
POPULACAO_NEGRA = "População negra"
ESTUDANTES = "Estudantes"
GRUPOS_ARTISTAS = "Grupos Artísticos e Culturais Independentes"
MESTRES_CULTURA_POPULAR = "Mestres, praticantes, brincantes e grupos das culturas populares, urbanas e rurais."

PUBLICO_CHOICES = (
    (1, EGRESSOS_SISTEMA_PRISIONAL),
    (2, FAMILIAS_PRESOS),
    (3, JOVENS_SOCIOEDUCATIVAS),
    (4, VITIMAS_DE_VIOLENCIA),
    (5, PESSOAS_SOFRIMENTO_PSIQUICO),
    (6, POPULACAO_SITUACAO_RUA),
    (7, CATADORES_RECICLAVEIS),
    (8, ATINGIDOS_INFRAESTRUTURA),
    (9, IMIGRANTES),
    (10, FAMILIAS_ACAMPADAS),
    (11, AGRICULTURES_FAMILIARES),
    (12, ASSENTADOS_REFORMA_AGRARIA),
    (13, POVOS_MATRIZ_AFRICANA),
    (14, QUILOMBOLAS),
    (15, INDIGENAS),
    (16, EXTRATIVISTAS),
    (17, PESCADORES),
    (18, RIBEIRINHOS),
    (19, SERTANEJOS),
    (20, CIGANOS),
    (21, LGBT),
    (22, MULHERES),
    (23, PESSOAS_DEFICIENCIA),
    (24, POPULACAO_NEGRA),
    (25, ESTUDANTES),
    (26, GRUPOS_ARTISTAS),
    (27, MESTRES_CULTURA_POPULAR),
)


CRIANCAS = "Crianças (0 a 12 anos)"
ADOLESCENTES = "Adolescentes (13 a 17 anos)"
JOVENS = "Jovens (18 a 29)"
ADULTOS = "Adultos (30 a 59)"
IDOSOS = "Idosos (60 anos ou mais)"
LIVRE = "Livre"

FAIXA_ETARIA_CHOICES = (
    (1, CRIANCAS),
    (2, ADOLESCENTES),
    (3, JOVENS),
    (4, ADULTOS),
    (5, IDOSOS),
    (6, LIVRE),
)
