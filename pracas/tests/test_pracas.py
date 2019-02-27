import datetime
import json
import pytest

from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.urlresolvers import reverse

from django.core.urlresolvers import resolve

from rest_framework import status

from core.helper_functions import test_reverse as _

from model_mommy import mommy

from pracas.models import Praca
from pracas.models import ImagemPraca

from authentication.tests.test_user import _admin_user
from authentication.tests.test_user import _common_user

_list = _('pracas:praca-list')
_detail = _('pracas:praca-detail')
_imagem_list = _('pracas:imagempraca-list')
_imagem_detail = _('pracas:imagempraca-detail')
_parceiros_list = _('pracas:parceiro-list')
_parceiros_detail = _('pracas:parceiro-detail')
_grupogestor_list = _('pracas:grupogestor-list')
_grupogestor_detail = _('pracas:grupogestor-detail')
_membrogestor_list = _('pracas:membrogestor-list')
_membrogestor_detail = _('pracas:membrogestor-detail')

User = get_user_model()
pytestmark = pytest.mark.django_db


@pytest.fixture
def _create_temporary_file(mocker):
    return mocker.Mock(spec=File, name='FileMock')


def test_get_URL_OK_from_Pracas(client):
    """
    Retorna 200 OK para a URL do endpoint que lista as Praças.
    """

    response = client.get(_list(), format='json')

    assert response.status_code == status.HTTP_200_OK


def test_return_a_list_of_Pracas(client):
    """
    Testa o retorno de uma lista de Praças
    """

    mommy.make(Praca, _quantity=5)

    response = client.get(_list(), format='json')

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    assert len(response.data) == 5


def test_if_an_instance_of_list_result_has_some_properties(client):
    """
    Testa se um um dos itens(praca) de uma lista(pracas) tem
    as propriedades: url, id_pub, nome, municipio, uf, modelo,
    modelo_descricao, situacao e situacao_descricao.
    """

    fields = ('url', 'id_pub', 'nome', 'municipio', 'uf', 'modelo',
              'modelo_descricao', 'situacao', 'situacao_descricao', 'contrato',
              'repasse', 'data_inauguracao')

    praca = mommy.make(Praca, _quantity=5)

    response = client.get(_list(), format='json')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5
    for field in fields:
        assert field in response.data[0]


def test_returning_a_praca(client):
    """
    Testa o retorno de uma Praça especifica
    """

    pracas = mommy.make(Praca, _quantity=5)

    response = client.get(_detail(kwargs={'pk': pracas[0].pk}), format='json')

    assert response.status_code == status.HTTP_200_OK
    assert str(pracas[0].pk) in response.data['id_pub']


def test_return_a_praca_with_some_properties(client):
    """
    Testa o retorno de uma praça especifica com as seguintes propriedades:
    url, id_pub, nome, slug, municipio, uf, modelo, modelo_descricao,
    situacao, situacao_descricao, bio, telefone1, telefone2, fax, email1,
    email2, pagina, data_inauguracao, repasse, contrato, cabeçalho e
    localização geográfica.

    """

    fields = ('url', 'id_pub', 'nome', 'slug', 'municipio', 'uf', 'modelo',
              'modelo_descricao', 'situacao', 'situacao_descricao', 'bio',
              'telefone1', 'telefone2', 'fax', 'email1', 'email2', 'pagina',
              'data_inauguracao', 'repasse', 'contrato', 'header_img', 'lat',
              'long')

    praca = mommy.make(Praca)

    response = client.get(_detail(kwargs={'pk': praca.pk}), format='json')

    assert response.status_code == status.HTTP_200_OK
    for field in fields:
        assert field in response.data


def test_not_returning_a_praca_giving_wrong_args(client):
    """
    Testa a a resposta da API ao tentar requisitar uma Praça com o código
    errado.
    """

    mommy.make(Praca)

    response = client.get(_detail(kwargs={'pk': 1}), format='json')

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_a_new_praca_without_proper_identification(client):
    """
    Testa criar uma nova Praça utilizando POST, sem autenticação
    """

    praca = {
        'nome': 'Praça Fulano Cicrano',
        'contrato': '36338510',
        'regiao': 'N',
        'uf': 'am',
        'municipio': 'Manaus',
        'modelo': 'g',
        'situacao': 'i'
    }

    response = client.post(_list(), praca, format='json')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_a_new_praca_as_common_user(_common_user, client):
    """
    Testa criar uma nova Praça utilizando POST, identificado como usuário comum
    """

    praca = {
        'nome': 'Praça Fulano Cicrano',
        'contrato': '36338510',
        'regiao': 'N',
        'uf': 'am',
        'municipio': 'Manaus',
        'modelo': 'g',
        'situacao': 'i'
    }

    response = client.post(_list(), praca, format='json')

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_a_new_praca_as_admin_user(_admin_user, client):
    """
    Testa criar uma nova Praça utilizando POST, identificado como gestor do
    Ministério
    """

    praca = {
        'nome': 'Praça Fulano Cicrano',
        'contrato': '36338510',
        'regiao': 'N',
        'uf': 'am',
        'municipio': 'Manaus',
        'modelo': 'g',
        'situacao': 'i'
    }

    response = client.post(_list(), praca, format='json')

    assert response.status_code == status.HTTP_201_CREATED


def test_update_Praca_information_without_credentials(client):
    """
    Testa atualizar as informações de uma praça usando PATCH sem credenciais de
    identificação
    """

    praca = mommy.make(Praca)

    praca_data = {'nome': 'Praça das Artes e Cultura'}

    response = client.patch(
        _detail(kwargs={'pk': praca.pk}),
        praca_data,
        content_type="application/json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_Praca_information_as_common_user(_common_user, client):
    """
    Testa atualizar as informações de uma praça usando PATCH com credenciais de
    um usuário comum.
    """

    praca = mommy.make(Praca)

    praca_data = json.dumps({'nome': 'Praça das Artes e Cultura'})

    response = client.patch(
        _detail(kwargs={'pk': praca.pk}),
        praca_data,
        content_type="application/json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_Praca_information_as_manager(_common_user, client):
    """
    Testa atualizar as informações de uma praça usando PATCH com credenciais de
    Gestor da Praça.
    """

    praca = mommy.make(Praca)
    gestor = mommy.make('Gestor', praca=praca, user=_common_user, atual=True)

    praca_data = json.dumps({'nome': 'Praça das Artes e Cultura'})

    response = client.patch(
        _detail(kwargs={'pk': praca.pk}),
        praca_data,
        content_type="application/json")

    assert response.status_code == status.HTTP_200_OK


def test_update_praca_information_as_admin_user(_admin_user, client):
    """
    Testa atualizar as informações de uma praça usando PATCH com credenciais de
    usuário gestor.
    """

    praca = mommy.make(Praca)

    praca_data = json.dumps({'nome': 'Praça das Artes e Cultura'})

    response = client.patch(
        _detail(kwargs={'pk': praca.pk}),
        praca_data,
        content_type="application/json")

    assert response.status_code == status.HTTP_200_OK


def test_excluir_praca_como_usuario_anonimo(client):
    """
    Testa a exclusão de uma Praça por um usuário sem credenciais de
    identificação
    """

    praca = mommy.make(Praca)

    response = client.delete(_detail(kwargs={'pk': praca.pk}))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_excluir_praca_como_usuario_identificado(_common_user, client):
    """
    Testa a exclusão de uma Praça por um usuário comum identificado.
    """

    praca = mommy.make(Praca)

    response = client.delete(_detail(kwargs={'pk': praca.pk}))

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_excluir_praca_como_gestor_de_praca(_common_user, client):
    """
    Testa a exclusão de uma Praça por seu próprio Gestor
    """

    praca = mommy.make(Praca)
    gestor = mommy.make('Gestor', praca=praca, user=_common_user, atual=True)

    response = client.delete(_detail(kwargs={'pk': praca.pk}))

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_excluir_praca_como_administrador(_admin_user, client):
    """
    Testa a exclusão de uma Praça por um administrador
    """

    praca = mommy.make(Praca)

    response = client.delete(_detail(kwargs={'pk': praca.pk}))

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_return_five_nearest_pracas(client):
    """
    Retorna as cinco pracas mais proximas dado uma coordenada
    """

    fields = ('url', 'id_pub', 'nome', 'municipio', 'uf', 'modelo',
              'modelo_descricao', 'situacao', 'situacao_descricao',
              'header_img')

    data = {'lat': -15.7833, 'long': -47.9167}

    for i in range(10):
        mommy.make(Praca, _fill_optional=['lat', 'long'])

    response = client.post(reverse('pracas:distancia'), data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5
    assert sorted(
        response.data, key=lambda praca: praca['distancia']) == response.data
    for result in response.data:
        for field in fields:
            assert field in result


def test_defining_a_name_if_user_leave_it_blank(_admin_user, client):
    """
    Testa a situação onde um usuário deixa o nome da Praça em branco
    e o sistema define o nome da praça como CEU + Nome da Cidade e UF

    """

    praca = mommy.make(Praca, nome="", municipio="Brasilia", uf="df")

    response = client.get(_detail(kwargs={'pk': praca.id_pub}), format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['nome'] == "Praça CEU de Brasilia - DF"


def test_defining_a_slug_from_the_name(_admin_user, client):
    """
    Testa a construção automática de um slug a partir do nome da Praça
    """

    from django.utils.text import slugify

    praca = mommy.make(Praca, nome="Praça Fulano Cicrano")

    slug = slugify(praca.nome)

    response = client.get(_detail(kwargs={'pk': praca.id_pub}), format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['slug'] == slug


def test_defining_a_name_and_a_slug(client):
    """
    Testa a definição automatica de um nome de Praça e uma slug, a partir
    do nome do municipio e da UF.
    """

    from django.utils.text import slugify

    praca = mommy.make(Praca, nome="")

    slug = slugify(praca.nome)

    response = client.get(_detail(kwargs={'pk': praca.id_pub}), format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['slug'] == slug


def test_upload_an_image_as_public_page_header_wo_credentials(
        _create_temporary_file, client):
    """
    Testa o envio de uma imagem para ser utilizada no cabeçalho da pagina
    publica de uma Praça, sem credenciais de identificação
    """

    praca = mommy.make(Praca)

    test_file = _create_temporary_file
    test_file.name = 'header.jpg'

    response = client.post(
        _imagem_list(kwargs={'praca_pk': praca.pk}),
        data={'header': True, 'arquivo': test_file},
        format='multipart')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_upload_an_image_as_public_page_header_w_credentials(
        _create_temporary_file, _common_user, client):
    """
    Testa o envio de uma imagem para ser utilizada no cabeçalho da pagina
    publica de uma Praça, com credenciais, porém, sem permissões de gestor da
    Praça
    """

    praca = mommy.make(Praca)

    test_file = _create_temporary_file

    response = client.post(
        _imagem_list(kwargs={'praca_pk': praca.pk}),
        data={'header': True, 'arquivo': test_file},
        format='multipart')

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_upload_an_image_as_public_page_header(
        _create_temporary_file, _common_user, client):
    """
    Testa o envio de uma imagem para ser utilizada no cabeçalho da pagina
    publica de uma Praça.
    """

    praca = mommy.make(Praca)
    gestor = mommy.make('Gestor', praca=praca, user=_common_user, atual=True)

    test_file = _create_temporary_file
    test_file.name = 'header.jpg'

    response = client.post(
        _imagem_list(kwargs={'praca_pk': praca.pk}),
        {'arquivo': test_file, 'header': True},
        format='multipart')

    assert response.status_code == status.HTTP_201_CREATED
    assert 'header_img' in response.data
    assert 'header.jpg' in response.data['header_img']

    download_header = client.get(response.data['header_img'])
    assert download_header.status_code == status.HTTP_200_OK


def test_upload_an_image_to_a_Praca_gallery_without_credentials(
    _create_temporary_file, client):
    """
    Testa o envio de uma imagem para a galeria de uma Praça sem utilizar
    credenciais de identificação.
    """

    praca = mommy.make(Praca)

    test_file = _create_temporary_file
    test_file.name = 'foto.jpg'

    response = client.post(
        _imagem_list(kwargs={'praca_pk': praca.pk}),
        {'arquivo': test_file},
        format='multipart')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_upload_an_image_to_a_Praca_gallery_with_credentials(
    _create_temporary_file, _common_user, client):
    """
    Testa o envio de uma imagem para a galeria de uma Praça utilizando
    credenciais de identificação.
    """

    praca = mommy.make(Praca)

    test_file = _create_temporary_file
    test_file.name = 'foto.jpg'

    response = client.post(
        _imagem_list(kwargs={'praca_pk': praca.pk}),
        {'arquivo': test_file},
        format='multipart')

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_upload_an_image_to_a_Praca_gallery_as_manager(
    _create_temporary_file, _common_user, client):
    """
    Testa o envio de uma imagem para a galeria de uma Praça utilizando
    credenciais de gestor da Praça.
    """

    praca = mommy.make(Praca)
    gestor = mommy.make('Gestor', user=_common_user, praca=praca, atual=True)

    test_file = _create_temporary_file
    test_file.name = 'foto.jpg'

    response = client.post(
        _imagem_list(kwargs={'praca_pk': praca.pk}),
        {'arquivo': test_file},
        format='multipart')

    assert response.status_code == status.HTTP_201_CREATED
    assert str(response.data['praca']) in response.data['arquivo']
    assert response.data['id_pub'] in response.data['arquivo']


def test_excluir_imagem_de_uma_Praca_como_gestor_da_praca(
        _create_temporary_file, _common_user, client):
    """
    Testa a exclusão de uma imagem da galeria de uma Praça utilizando
    credenciais de gestor da Praça.
    """

    praca = mommy.make(Praca)
    gestor = mommy.make('Gestor', user=_common_user, praca=praca, atual=True)
    imagem = mommy.make('ImagemPraca', praca=praca)

    test_file = _create_temporary_file
    test_file.name = 'foto.jpg'

    response = client.delete(
        _imagem_detail(kwargs={'praca_pk': praca.pk, 'pk': imagem.pk}))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    with pytest.raises(ImagemPraca.DoesNotExist):
        imagem.refresh_from_db()


def test_change_title_of_an_image_at_gallery_wo_credentials(
    _create_temporary_file, client):
    """
    Testa a alteração de informações de uma imagem da galeria de uma Praca, sem
    utilizar credenciais de identificação.
    """

    praca = mommy.make(Praca)
    imagem = mommy.make('ImagemPraca', praca=praca)

    data = json.dumps({
        "titulo": "Titulo Teste",
        "descricao": "Descrição Teste"
    })

    image_response = client.patch(
        _imagem_detail(kwargs={'praca_pk': praca.pk, 'pk': imagem.pk}),
        data, content_type="application/json")

    assert image_response.status_code == status.HTTP_401_UNAUTHORIZED


def test_change_title_of_an_image_at_gallery_w_credentials(
    _create_temporary_file, _common_user, client):
    """
    Testa a alteração de informações de uma imagem da galeria de uma Praca,
    utilizando credenciais de identificação.
    """

    praca = mommy.make(Praca)
    imagem = mommy.make('ImagemPraca', praca=praca)

    data = json.dumps({
        "titulo": "Titulo Teste",
        "descricao": "Descrição Teste"
    })

    image_response = client.patch(
        _imagem_detail(kwargs={'praca_pk': praca.pk, 'pk': imagem.pk}),
        data, content_type="application/json")

    assert image_response.status_code == status.HTTP_403_FORBIDDEN


def test_change_title_of_an_image_at_gallery_as_manager(
    _create_temporary_file, _common_user, client):
    """
    Testa a alteração de informações de uma imagem da galeria de uma Praca,
    utilizando credenciais de identificação de um gestor de Praça
    """

    praca = mommy.make(Praca)
    imagem = mommy.make('ImagemPraca', praca=praca)
    gestor = mommy.make('Gestor', praca=praca, user=_common_user, atual=True)

    data = json.dumps({
        "titulo": "Titulo Teste",
        "descricao": "Descrição Teste"
    })

    image_response = client.patch(
        _imagem_detail(kwargs={'praca_pk': praca.pk, 'pk': imagem.pk}),
        data, content_type="application/json")

    assert image_response.status_code == status.HTTP_200_OK


def test_change_title_of_an_image_at_gallery_as_minc_manager(
    _create_temporary_file, _admin_user, client):
    """
    Testa a alteração de informações de uma imagem da galeria de uma Praca,
    utilizando credenciais de identificação de um gestor do MinC
    """

    praca = mommy.make(Praca)
    imagem = mommy.make('ImagemPraca', praca=praca)

    data = json.dumps({
        "titulo": "Titulo Teste",
        "descricao": "Descrição Teste"
    })

    image_response = client.patch(
        _imagem_detail(kwargs={'praca_pk': praca.pk, 'pk': imagem.pk}),
        data, content_type="application/json")

    assert image_response.status_code == status.HTTP_200_OK


@pytest.mark.skip
def test_retorna_200_ok_enpoint_GG(client):
    """
    Testa o acesso ao endpoint de Grupo Gestor
    """

    url = "/api/v1/grupogestor/"

    response = client.get(url)
    namespace = resolve(url)

    assert response.status_code == status.HTTP_200_OK

    assert f"{namespace.namespace}:{namespace.url_name}" == 'pracas:grupogestor-list'


def test_retornar_informacoes_sobre_GG(client):
    """
    Testa o retorno de informações sobre o Grupo Gestor de uma Praça
    """

    gg = mommy.make('GrupoGestor')

    response = client.get(_grupogestor_detail(
                                  kwargs={
                                      'praca_pk': gg.praca.pk,
                                      'pk': gg.pk
                                  }))

    assert response.status_code == status.HTTP_200_OK


def test_cria_um_novo_grupo_gestor_sem_credenciais(client):
    """
    Testa a criação de um novo Grupo Gestor de uma Praça
    """

    praca = mommy.make('Praca')
    data = json.dumps({'praca': f'{praca.pk}', 'previsao_espacos': 5})

    response = client.post(_grupogestor_list(kwargs={'praca_pk': praca.pk}), data,
                           content_type="application/json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_cria_um_novo_grupo_gestor_com_credenciais(_common_user, client):
    """
    Testa a criação de um novo Grupo Gestor de uma Praça, utilizando um usuário
    identificado.
    """

    praca = mommy.make('Praca')
    data = json.dumps({'praca': f'{praca.pk}', 'previsao_espacos': 5})

    response = client.post(_grupogestor_list(kwargs={'praca_pk': praca.pk}), data, content_type="application/json")

    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_arquiva_um_GG_sem_credenciais(client):
    """
    Testa a finalização de um Grupo Gestor de uma Praça quando não esta logado
    """

    finalizacao = json.dumps({'data_finalizacao': '2018-01-01'})
    gg = mommy.make('GrupoGestor')

    response = client.delete(_grupogestor_detail(
                                  kwargs={
                                      'praca_pk': gg.praca.pk,
                                      'pk': gg.pk
                                  }),finalizacao)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_arquiva_um_GG_com_credenciais(_common_user, client):
    """
    Testa a finalização de um Grupo Gestor de uma Praça quando esta logado
    """

    finalizacao = json.dumps({'data_finalizacao': '2018-01-01'})
    gg = mommy.make('GrupoGestor')

    response = client.delete(_grupogestor_detail(
                                  kwargs={
                                      'praca_pk': gg.praca.pk,
                                      'pk': gg.pk
                                  }),finalizacao)

    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_arquivar_um_GG_como_gestor_da_Praca(_common_user, client):
    """
    Testa arquivar um MembroGestor de um GrupoGestor ativo, usando o verbo
    DELETE, com permissões sobre a Praça.
    """

    praca = mommy.make(Praca)
    gestor = mommy.make('Gestor', praca=praca, user=_common_user, atual=True)
    gg = mommy.make('GrupoGestor', praca=praca)
    finalizacao = json.dumps({'data_finalizacao': '2018-01-01'})

    response = client.delete(_grupogestor_detail(
        kwargs={
            'praca_pk': gg.praca.pk,
            'pk': gg.pk
        }),
        finalizacao,
        content_type="application/json"
        )

    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_retorna_informacoes_sobre_GG(client):
    """
    Testa o retorno de informações sobre o Grupo Gestor de uma Praça
    """

    praca = mommy.make(Praca)
    gg = mommy.make('GrupoGestor', praca=praca)

    response = client.get(_detail(kwargs={'pk': praca.pk}))

    assert response.data['grupo_gestor']


def test_retorna_os_gg_de_uma_praca(client):
    """
    Testa o retorno dos Grupos Gestores exclusivos de uma Praça
    """

    praca = mommy.make(Praca)
    gg = mommy.make('GrupoGestor', praca=praca)
    gg2 = mommy.make('GrupoGestor', praca=praca,
                     _fill_optional=['data_finalizacao'])
    gg3 = mommy.make('GrupoGestor', _quantity=2)

    response = client.get(_grupogestor_list(kwargs={'praca_pk': praca.pk}))

    assert len(response.data) == 2


def test_retorna_qtde_membros_GG(client):
    """
    Testa o retorno contendo a quantidade de membros prevista para o Grupo
    Gestor de uma Praça
    """

    praca = mommy.make(Praca)
    gg = mommy.make('GrupoGestor', praca=praca, previsao_espacos=5)

    response = client.get(_detail(kwargs={'pk': praca.pk}))

    assert response.data['grupo_gestor']['previsao_espacos'] == 5


def test_cadastra_um_novo_membro_no_GG(client):
    """
    Testa a persistencia de um novo membro no Grupo Gestor de uma Praça sem
    utilizar credenciais de idenfiticação
    """

    praca = mommy.make(Praca)
    gg = mommy.make('GrupoGestor', praca=praca)

    data = json.dumps({
        'nome': 'Cicrano Fulano',
        'origem': 'sc',
        'data_posse': f'{datetime.date.today()}',
    })

    response = client.post(_grupogestor_list(kwargs={'praca_pk': praca.pk}))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_cadastra_um_novo_membro_no_GG_com_credenciais(_common_user, client):
    """
    Testa a persistencia de um novo membro no Grupo Gestor de uma Praça
    utilizando credenciais de idenfiticação
    """

    praca = mommy.make(Praca)
    gg = mommy.make('GrupoGestor', praca=praca)

    data = json.dumps({
        'nome': 'Cicrano Fulano',
        'origem': '2',
        'data_posse': f'{datetime.date.today()}',
    })

    response = client.post(_membrogestor_list(
        kwargs={'grupogestor_pk': gg.pk, 'praca_pk': praca.pk}),
        data, content_type="application/json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_cadastra_um_novo_membro_no_GG_como_gestor(_common_user, client):
    """
    Testa a persistencia de um novo membro no Grupo Gestor de uma Praça
    utilizando credenciais de idenfiticação como gestor de Praça
    """

    praca = mommy.make(Praca)
    gestor = mommy.make('Gestor', praca=praca, user=_common_user, atual=True)
    gg = mommy.make('GrupoGestor', praca=praca)

    data = json.dumps({
        'nome': 'Cicrano Fulano',
        'origem': 'sc',
        'data_posse': f'{datetime.date.today()}',
    })

    response = client.post(_membrogestor_list(
        kwargs={'praca_pk': praca.pk, 'grupogestor_pk': gg.pk}),
        data, content_type="application/json")

    assert response.status_code == status.HTTP_201_CREATED


def test_verifica_se_um_membro_GG_retorna_determinados_campos(client):
    """
    Testa o retorno dos campos "origem", "data_posse",
    "data_desligamento", "documento_posse", "tipo_documento", "titularidade",
    "nome", "telefone" e "email", nas informações sobre os
    membros de um Grupo Gestor """

    campos = {"origem", "data_posse", "data_desligamento", "documento_posse",
              "tipo_documento", "titularidade", "nome", "telefone",
              "email"}

    praca = mommy.make(Praca)
    gestor = mommy.make('Gestor', praca=praca, atual=True)
    grupo_gestor = mommy.make('GrupoGestor', praca=praca)
    membro = mommy.make('MembroGestor', grupo_gestor=grupo_gestor)

    response = client.get(_membrogestor_list(
        kwargs={'praca_pk': praca.pk,
                'grupogestor_pk': grupo_gestor.pk}),
        content_type="application/json")

    assert campos.issubset(response.json()[0])


def test_arquivar_um_membro_gestor_de_um_GG_sem_permissoes(client):
    """
    Testa arquivar um MembroGestor de um GrupoGestor ativo, usando o verbo
    DELETE, sem ter credenciais de acesso.
    """

    praca = mommy.make(Praca)
    grupo_gestor = mommy.make('GrupoGestor', praca=praca)
    membro = mommy.make('MembroGestor', grupo_gestor=grupo_gestor)

    response = client.delete(_membrogestor_detail(kwargs={
        'praca_pk': praca.pk, 'grupogestor_pk': grupo_gestor.pk, 'pk': membro.pk
        })
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_arquivar_um_membro_gestor_de_um_GG_com_credenciais(_common_user, client):
    """
    Testa arquivar um MembroGestor de um GrupoGestor ativo, usando o verbo
    DELETE, com usuário logado, sem permissões sobre a Praça.
    """

    praca = mommy.make(Praca)
    grupo_gestor = mommy.make('GrupoGestor', praca=praca)
    membro = mommy.make('MembroGestor', grupo_gestor=grupo_gestor)

    response = client.delete(_membrogestor_detail(kwargs={
        'praca_pk': praca.pk, 'grupogestor_pk': grupo_gestor.pk, 'pk': membro.pk
        })
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_arquivar_um_membro_gestor_de_um_GG_como_gestor_da_Praca(_common_user, client):
    """
    Testa arquivar um MembroGestor de um GrupoGestor ativo, usando o verbo
    DELETE, com permissões sobre a Praça.
    """

    praca = mommy.make(Praca)
    gestor = mommy.make('Gestor', praca=praca, user=_common_user, atual=True)
    grupo_gestor = mommy.make('GrupoGestor', praca=praca)
    membro = mommy.make('MembroGestor', grupo_gestor=grupo_gestor)

    desligamento = json.dumps({'data_desligamento': '2018-01-01'})

    response = client.delete(_membrogestor_detail(kwargs={
        'praca_pk': praca.pk, 'grupogestor_pk': grupo_gestor.pk, 'pk': membro.pk
        }),
        desligamento,
        content_type="application/json"
    )

    from pracas.models import MembroGestor
    membrogestor = MembroGestor.objects.get(pk=membro.pk)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert membrogestor.data_desligamento

@pytest.mark.skip
def test_retorna_200_ok_enpoint_parceiros(client):
    """
    Testa o acesso ao endpoint de Parceiros da Praça
    """

    url = "/api/v1/parceiros/"

    response = client.get(url)
    namespace = resolve(url)

    assert response.status_code == status.HTTP_200_OK
    assert f"{namespace.namespace}:{namespace.url_name}" == 'pracas:parceiro-list'


def test_retornar_informacoes_sobre_parceiros(client):
    """
    Testa o retorno de informações sobre os Parceiros de uma Praça
    """

    praca = mommy.make('Praca')
    parceiro = mommy.make('Parceiro', praca=praca)

    fields = ('nome', 'email', 'ramo_atividade')

    response = client.get(_detail(kwargs={'pk': praca.pk}))

    assert response.status_code == status.HTTP_200_OK
    assert response.data['parceiros']
    for field in fields:
        assert field in response.data['parceiros'][0]


def test_persiste_um_parceiro_sem_credenciais_identificacao(client):
    """
    Testa a criação de um novo Parceiro sem utilizar credenciais de
    identificação
    """

    praca = mommy.make('Praca')

    data = json.dumps({
        'praca': str(praca.pk),
        'nome': 'Fulano',
        'endereco': 'Praca Sao Jorge, n5',
        'telefone': 22555554444,
        'email': 'fulano@cicrano.com.br',
        'ramo_atividade': 1,
        'acoes': 'Apoio a grupos de leitura',
        'tempo_parceria': 366,
    })

    response = client.post(
        _parceiros_list(kwargs={'praca_pk': praca.pk}),
        data, content_type="application/json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_persiste_um_parceiro_com_credenciais_identificacao(_common_user,
                                                            client):
    """
    Testa a criação de um novo Parceiro utilizando credenciais de
    identificação, porém sem acessos de gestor de uma Praça.
    """

    praca = mommy.make('Praca')

    data = json.dumps({
        'praca': str(praca.pk),
        'nome': 'Fulano',
        'endereco': 'Praca Sao Jorge, n5',
        'telefone': 22555554444,
        'email': 'fulano@cicrano.com.br',
        'ramo_atividade': 1,
        'acoes': 'Apoio a grupos de leitura',
        'tempo_parceria': 366,
    })

    response = client.post(_parceiros_list(kwargs={'praca_pk': praca.pk}),
                           data, content_type="application/json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_persiste_um_parceiro_com_permissoes_de_gestor(_common_user,
                                                       client):
    """
    Testa a criação de um novo Parceiro utilizando credenciais de
    identificação e acessos de gestor de uma Praça.
    """

    praca = mommy.make('Praca')
    gestor = mommy.make('Gestor', praca=praca, user=_common_user, atual=True)

    data = json.dumps({
        'praca': str(praca.pk),
        'nome': 'Fulano',
        'endereco': 'Praca Sao Jorge, n5',
        'telefone': 22555554444,
        'email': 'fulano@cicrano.com.br',
        'ramo_atividade': 1,
        'acoes': 'Apoio a grupos de leitura',
        'tempo_parceria': 366,
    })

    response = client.post(_parceiros_list(kwargs={'praca_pk': praca.pk}),
                           data, content_type="application/json")

    assert response.status_code == status.HTTP_201_CREATED


def test_persiste_um_parceiro_com_permissoes_de_gestor(_admin_user,
                                                       client):
    """
    Testa a criação de um novo Parceiro utilizando credenciais de
    identificação de gestor do Ministério.
    """

    praca = mommy.make('Praca')

    data = json.dumps({
        'praca': str(praca.pk),
        'nome': 'Fulano',
        'endereco': 'Praca Sao Jorge, n5',
        'telefone': 22555554444,
        'email': 'fulano@cicrano.com.br',
        'ramo_atividade': 1,
        'acoes': 'Apoio a grupos de leitura',
        'tempo_parceria': 366,
    })

    response = client.post(_parceiros_list(kwargs={'praca_pk': praca.pk}),
                           data, content_type="application/json")

    assert response.status_code == status.HTTP_201_CREATED


def test_mudar_o_numero_de_contrato_de_uma_Praca_por_um_gestor_de_Praca(_common_user, client):
    """
    Testa a alteração do numero de contrato de uma Praça por um gestor de Praça
    """

    praca = mommy.make('Praca')
    gestor = mommy.make('Gestor', user=_common_user, praca=praca, atual=True)

    data = json.dumps({
        'contrato': 12345678
    })

    response = client.patch(_detail(kwargs={'pk': praca.pk}),
                            data, content_type="application/json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_mudar_o_numero_de_contrato_de_uma_Praca_por_um_gestor_MinC(_admin_user, client):
    """
    Testa a alteração do numero de contrato de uma Praça por um gestor MinC
    """

    praca = mommy.make('Praca')

    data = json.dumps({
        'contrato': 12345678
    })

    response = client.patch(_detail(kwargs={'pk': praca.pk}),
                            data, content_type="application/json")

    assert response.status_code == status.HTTP_200_OK


def test_mudar_o_valor_de_repasse_de_uma_Praca_por_um_gestor_de_Praca(_common_user, client):
    """
    Testa a alteração do valor de repasse para a construção da Praça, pelo
    gestor da Praça
    """

    praca = mommy.make('Praca')
    gestor = mommy.make('Gestor', user=_common_user, praca=praca, atual=True)

    data = json.dumps({
        'repasse': 0
    })

    response = client.patch(_detail(kwargs={'pk': praca.pk}),
                            data, content_type="application/json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_mudar_o_valor_de_repasse_de_uma_Praca_por_um_gestor_MinC(_admin_user, client):
    """
    Testa a alteração do valor de repasse para a construção da Praça, pelo
    gestor MinC
    """

    praca = mommy.make('Praca')

    data = json.dumps({
        'repasse': 0
    })

    response = client.patch(_detail(kwargs={'pk': praca.pk}),
                            data, content_type="application/json")

    assert response.status_code == status.HTTP_200_OK


def test_mudar_o_modelo_de_Praca_pelo_gestor_de_Praca(_common_user, client):
    """
    Testa a alteração do modelo de uma Praça, pelo gestor da Praça
    """

    praca = mommy.make('Praca')
    gestor = mommy.make('Gestor', user=_common_user, praca=praca, atual=True)

    data = json.dumps({
        'modelo': 'm'
    })

    response = client.patch(_detail(kwargs={'pk': praca.pk}),
                            data, content_type="application/json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_mudar_o_modelo_de_Praca_por_um_gestor_MinC(_admin_user, client):
    """
    Testa a alteração do modelo de uma Praça, pelo gestor MinC
    """

    praca = mommy.make('Praca')

    data = json.dumps({
        'modelo': 'm'
    })

    response = client.patch(_detail(kwargs={'pk': praca.pk}),
                            data, content_type="application/json")

    assert response.status_code == status.HTTP_200_OK


def test_propriedades_de_um_membro_UGL(client):
    """
    Testa a existencia de determinadas propriedades de um membro da Unidade
    Gestora Local de uma Praça.
    """

    praca = mommy.make('Praca')
    ugl = mommy.make('MembroUgl', praca=praca)

    fields = ('tipo', 'nome', 'telefone', 'email')

    response = client.get(_detail(kwargs={'pk': praca.pk}),
                          content_type="application/json")

    for field in fields:
        assert field in response.data['unidade_gestora'][0]


def test_busca_praca_por_municipio_com_acento(client):
    """
    Testa a busca por nome do município da praça ignorando os acentos
    """

    praca = mommy.make('Praca', municipio='Ceilândia')
    mommy.make('Praca', _quantity=5)

    search = 'ceilandia'

    response = client.get(_list(), {"search": search},
                          content_type="application/json")

    assert str(praca.id_pub) == response.data[0]['id_pub']
