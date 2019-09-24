from rest_framework import serializers

from authentication.serializers import UserSerializer

from .models import Gestor
from .models import ProcessoVinculacao
from .models import ArquivosProcessoVinculacao
from .models import RegistroProcessoVinculacao


class GestorBaseSerializer(serializers.ModelSerializer):
  url = serializers.URLField(source='get_absolute_url', read_only=True)
  nome = serializers.CharField(source='user.full_name', read_only=True)
  email = serializers.EmailField(source='user.email', read_only=True)
  user_id_pub = serializers.CharField(source='user.id_pub', read_only=True)
  profile_picture_url = serializers.CharField(
    source='user.profile_picture_url', read_only=True)
  praca = serializers.SerializerMethodField(read_only=True)

  def get_praca(self, obj):
    from pracas.serializers import PracaListSerializer
    serializer = PracaListSerializer(
      obj.praca,
      fields=('nome', 'url', 'municipio', 'uf', 'regiao', 'header_img',
              'situacao', 'situacao_descricao', 'data_inauguracao'))
    return serializer.data

  class Meta:
    model = Gestor
    fields = ('url', 'id_pub', 'user_id_pub', 'nome', 'email',
              'profile_picture_url', 'data_inicio_gestao',
              'data_encerramento_gestao', 'atual', 'praca')


class GestorListSerializer(GestorBaseSerializer):
  class Meta:
    model = Gestor
    fields = ('url', 'id_pub', 'nome', 'email', 'profile_picture_url',
              'data_inicio_gestao', 'data_encerramento_gestao', 'atual',
              'praca')


class GestorSerializer(serializers.ModelSerializer):
  url = serializers.URLField(source='get_absolute_url', read_only=True)
  nome = serializers.CharField(source='user.full_name', read_only=True)
  email = serializers.EmailField(source='user.email', read_only=True)
  user_id_pub = serializers.CharField(source='user.id_pub', read_only=True)
  profile_picture_url = serializers.CharField(
    source='user.profile_picture_url', read_only=True)
  praca = serializers.SerializerMethodField(read_only=True)

  def get_praca(self, obj):
    from pracas.serializers import PracaListSerializer
    serializer = PracaListSerializer(
      obj.praca,
      fields=('nome', 'url', 'municipio', 'uf', 'regiao', 'header_img'))
    return serializer.data

  class Meta:
    model = Gestor
    fields = ('url', 'id_pub', 'user_id_pub', 'nome', 'email', 'praca',
              'profile_picture_url')


class ArquivosProcessoVinculacaoSerializer(serializers.ModelSerializer):
  url = serializers.URLField(source='get_absolute_url', read_only=True)

  class Meta:
    model = ArquivosProcessoVinculacao
    fields = ('url', 'id_pub', 'data_envio', 'tipo', 'verificado',
              'comentarios', 'verificado_por', 'arquivo')


class RegistroProcessoVinculacaoSerializer(serializers.ModelSerializer):
  class Meta:
    model = RegistroProcessoVinculacao
    fields = ('data', 'situacao', 'descricao')


class ProcessoVinculacaoListSerializer(serializers.ModelSerializer):
  url = serializers.URLField(source='get_absolute_url', read_only=True)
  praca = serializers.SerializerMethodField(read_only=True)
  user = UserSerializer(read_only=True)

  def get_praca(self, obj):
    from pracas.serializers import PracaListSerializer
    serializer = PracaListSerializer(obj.praca)
    return serializer.data

  class Meta:
    model = ProcessoVinculacao
    fields = ('url', 'id_pub', 'praca', 'user', 'data_abertura',
              'data_finalizacao', 'finalizado')


class ProcessoVinculacaoDetailSerializer(serializers.ModelSerializer):
  url = serializers.URLField(source='get_absolute_url', read_only=True)
  praca = serializers.SerializerMethodField(read_only=True)
  user = UserSerializer(read_only=True)
  files = ArquivosProcessoVinculacaoSerializer(many=True, read_only=True)
  registro = RegistroProcessoVinculacaoSerializer(many=True, read_only=True)

  def get_praca(self, obj):
    from pracas.serializers import PracaListSerializer
    serializer = PracaListSerializer(obj.praca)
    return serializer.data

  class Meta:
    model = ProcessoVinculacao
    fields = ('url', 'id_pub', 'praca', 'user', 'data_abertura',
              'data_finalizacao', 'aprovado', 'finalizado', 'files',
              'despacho', 'registro')


class ProcessoVinculacaoSerializer(serializers.ModelSerializer):
  url = serializers.URLField(source='get_absolute_url', read_only=True)
  user = UserSerializer(
    read_only=True, default=serializers.CurrentUserDefault())
  files = ArquivosProcessoVinculacaoSerializer(many=True, required=False)

  class Meta:
    model = ProcessoVinculacao
    fields = ('url', 'id_pub', 'praca', 'user', 'data_abertura',
              'aprovado', 'files', )
    read_only_fields = ('data_abertura', )
