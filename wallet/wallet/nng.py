import logging

from django.conf import settings
from pynng import Pub0

pub: Pub0


def init_nng_publisher():
    global pub

    print("Initializing NNG publisher...")
    pub = Pub0()
    pub.listen(settings.NNG_INTERNAL_ADDRESS)


init_nng_publisher()
