import json
import pytest

from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.urlresolvers import reverse

from django.core.urlresolvers import resolve

from rest_framework import status

from model_mommy import mommy

from pracas.models import Praca

from authentication.tests.test_user import _admin_user
from authentication.tests.test_user import _common_user

User = get_user_model()
pytestmark = pytest.mark.django_db


@pytest.fixture
def _create_temporary_file(mocker):
    return mocker.Mock(spec=File, name='FileMock')


def test_get_URL_OK_from_Pracas(client):
    """
    Retorna 200 OK para a URL do endpoint que lista as Praças.
    """

    response = client.get(reverse('pracas:praca-list'), format='json')

    assert response.status_code == status.HTTP_200_OK


def test_return_a_list_of_Pracas(client):
    """
    Testa o retorno de uma lista de Praças
    """

    mommy.make(Praca, _quantity=5)

    response = client.get(reverse('pracas:praca-list'), format='json')

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
              'modelo_descricao', 'situacao', 'situacao_descricao', )

    praca = mommy.make(Praca, _quantity=5)

    response = client.get(reverse('pracas:praca-list'), format='json')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5
    for field in fields:
        assert field in response.data[0]


def test_returning_a_praca(client):
    """
    Testa o retorno de uma Praça especifica
    """

    pracas = mommy.make(Praca, _quantity=5)

    response = client.get(
        reverse('pracas:praca-detail', kwargs={'pk': pracas[0].pk}),
        format='json')

    assert response.status_code == status.HTTP_200_OK
    assert str(pracas[0].pk) in response.data['id_pub']


def test_return_a_praca_with_some_properties(client):
    """
    Testa o retorno de uma praça especifica com as seguintes propriedades:
    url, id_pub, nome, slug, municipio, uf, modelo, modelo_descricao, situacao
    e situacao_descricao.

    """

    fields = ('url', 'id_pub', 'nome', 'slug', 'municipio', 'uf', 'modelo',
              'modelo_descricao', 'situacao', 'situacao_descricao',
              'header_url')

    praca = mommy.make(Praca)

    response = client.get(
        reverse('pracas:praca-detail', kwargs={'pk': praca.pk}), format='json')

    assert response.status_code == status.HTTP_200_OK
    for field in fields:
        assert field in response.data


def test_not_returning_a_praca_giving_wrong_args(client):
    """
    Testa a a resposta da API ao tentar requisitar uma Praça com o código
    errado.
    """

    mommy.make(Praca)

    response = client.get(
        reverse('pracas:praca-detail', kwargs={'pk': 1}), format='json')

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

    response = client.post(reverse('pracas:praca-list'), praca, format='json')

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

    response = client.post(reverse('pracas:praca-list'), praca, format='json')

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

    response = client.post(reverse('pracas:praca-list'), praca, format='json')

    assert response.status_code == status.HTTP_201_CREATED


def test_update_Praca_information_without_credentials(client):
    """
    Testa atualizar as informações de uma praça usando PATCH sem credenciais de
    identificação
    """

    praca = mommy.make(Praca)

    praca_data = {'nome': 'Praça das Artes e Cultura'}

    response = client.patch(
        reverse('pracas:praca-detail', kwargs={'pk': praca.pk}),
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
        reverse('pracas:praca-detail', kwargs={'pk': praca.pk}),
        praca_data,
        content_type="application/json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_praca_information_as_admin_user(_admin_user, client):
    """
    Testa atualizar as informações de uma praça usando PATCH com credenciais de
    usuário gestor.
    """

    praca = mommy.make(Praca)

    praca_data = json.dumps({'nome': 'Praça das Artes e Cultura'})

    response = client.patch(
        reverse('pracas:praca-detail', kwargs={'pk': praca.pk}),
        praca_data,
        content_type="application/json")

    assert response.status_code == status.HTTP_200_OK


def test_return_five_nearest_pracas(client):
    """
    Retorna as cinco pracas mais proximas dado uma coordenada
    """

    fields = ('url', 'id_pub', 'nome', 'municipio', 'uf', 'modelo',
              'modelo_descricao', 'situacao', 'situacao_descricao',
              'header_url')

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

    response = client.get(
        reverse('pracas:praca-detail', kwargs={'pk': praca.id_pub}),
        format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['nome'] == "Praça CEU de Brasilia - DF"


def test_defining_a_slug_from_the_name(_admin_user, client):
    """
    Testa a construção automática de um slug a partir do nome da Praça
    """

    from django.utils.text import slugify

    praca = mommy.make(Praca, nome="Praça Fulano Cicrano")

    slug = slugify(praca.nome)

    response = client.get(
        reverse('pracas:praca-detail', kwargs={'pk': praca.id_pub}),
        format='json')

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

    response = client.get(
        reverse('pracas:praca-detail', kwargs={'pk': praca.id_pub}),
        format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['slug'] == slug


def test_upload_an_image_as_public_page_header(_create_temporary_file, client):
    """
    Testa o envio de uma imagem para ser utilizada no cabeçalho da pagina
    publica de uma Praça.

    """

    praca = mommy.make(Praca)

    test_file = _create_temporary_file
    test_file.name = 'header.jpg'

    response = client.post(
        reverse('pracas:praca-header_upload', kwargs={'pk': praca.id_pub}),
        {'header_img': test_file},
        format='multipart', )

    assert response.status_code == status.HTTP_200_OK
    assert 'header_url' in response.data
    assert 'header.jpg' in response.data['header_url']

    download_header = client.get(response.data['header_url'])
    assert download_header.status_code == status.HTTP_200_OK


def test_retorna_200_ok_enpoint_GG(client):
    """
    Testa o acesso ao endpoint de Grupo Gestor
    """

    url = "/api/v1/grupogestor/"

    response = client.get(url)
    namespace = resolve(url)

    assert response.status_code == status.HTTP_200_OK

    assert "{}:{}".format(namespace.namespace, namespace.url_name) == 'pracas:grupogestor-list'


def test_retorna_informacoes_sobre_GG(client):
    """
    Testa o retorno de informações sobre o Grupo Gestor de uma Praça
    """

    praca = mommy.make(Praca)
    gg = mommy.make('GrupoGestor', praca=praca)

    response = client.get(
        reverse('pracas:praca-detail', kwargs={'pk': praca.pk}))

    assert response.data['grupo_gestor']


def test_retorna_qtde_membros_GG(client):
    """
    Testa o retorno contendo a quantidade de membros prevista para o Grupo
    Gestor de uma Praça
    """

    praca = mommy.make(Praca)
    gg = mommy.make('GrupoGestor', praca=praca, previsao_espacos=5)

    response = client.get(
        reverse('pracas:praca-detail', kwargs={'pk': praca.pk}))

    assert response.data['grupo_gestor']['previsao_espacos'] == 5
