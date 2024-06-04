import random
from copy import deepcopy
from math import cos, radians, sin

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Populate db with testdata"

    def add_arguments(self, parser):
        parser.add_argument("-s", "--size", type=int, default=1000)

