import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from apps.shop_analyzer.integrations.etsy.sync import EtsySync

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sync the data from Etsy'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        sync = EtsySync(settings.ETSY_KEYSTRING)

        sync.sync()
