#coding: utf-8

import csv

from django.core.management.base import BaseCommand, CommandError

from core.models import Praca


class Command(BaseCommand):
    help = 'Carrega a lista de praças a partir de um arquivo CSV pré-determinado'


    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **kwargs):
        print(args)
