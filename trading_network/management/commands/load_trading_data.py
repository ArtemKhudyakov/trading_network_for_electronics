from django.core.management import BaseCommand, call_command
from django.core.management.base import CommandError


class Command(BaseCommand):
    help = 'Загрузка тестовых данных для торговой сети'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fixture',
            type=str,
            default='trading_network_data',
            help='Имя фикстуры для загрузки (без расширения)'
        )

    def handle(self, *args, **options):
        fixture_name = options['fixture']

        self.stdout.write('Загрузка тестовых данных для торговой сети...')

        try:
            # Загружаем фикстуру
            call_command('loaddata', f'{fixture_name}.json', app_label='trading_network')

            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Тестовые данные успешно загружены из фикстуры {fixture_name}.json!'
                )
            )

            self.stdout.write('\nСозданные данные:')
            self.stdout.write('   • 8 продуктов (смартфоны, ноутбуки, планшеты и т.д.)')
            self.stdout.write('   • 10 звеньев торговой сети:')
            self.stdout.write('     - 3 завода (уровень 0)')
            self.stdout.write('     - 4 розничные сети (уровень 1)')
            self.stdout.write('     - 3 индивидуальных предпринимателя (уровень 2)')
            self.stdout.write('   • Иерархические связи между поставщиками')
            self.stdout.write('   • Реалистичные задолженности')

        except CommandError as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при загрузке данных: {e}')
            )