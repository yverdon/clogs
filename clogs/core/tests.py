import random
from math import cos, radians, sin

from django.db import connection
from django.test import TestCase, override_settings

from clogs.core.utils import wkt_from_line
