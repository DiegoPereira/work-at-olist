from channels.models import Channel, Categories
from django.core.management.base import BaseCommand, CommandError
import channels.management.commands.importcategories_utils as utils


class Command(BaseCommand):
    help = 'Import a channel with its categories from a csv file    '

    def add_arguments(self, parser):
        parser.add_argument('channel_name', nargs='+', type=str)
        parser.add_argument('csv_filename', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            channel_name = options["channel_name"][0]
            channel = Channel.objects.filter(name=channel_name)
            if len(channel) == 1:
                channel_id = channel[0].id
                Categories.objects.filter(channel=channel_id).delete()
                channel.delete()
                self.stdout.write(self.style.SUCCESS(
                                  'Remove channel\'s old records'))
            channel = Channel.objects.create(name=options["channel_name"][0])
            csv_as_list = utils.csv_to_list(options["csv_filename"][0])
            fill_db = utils.fill_database(csv_as_list, channel)
            if fill_db:
                self.stdout.write(self.style.SUCCESS(
                                  'Successfully imported the channel'))
        except:
            CommandError("Channel and categories were not imported")
