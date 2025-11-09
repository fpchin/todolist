"""
Django management command to import legacy Excel data
"""
import logging
from django.core.management.base import BaseCommand, CommandError
from apps.migration.parsers.excel_parser import ExcelParser
from apps.migration.validators.data_validator import MigrationValidator
from apps.migration.importers.data_importer import DataImporter

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import tournament data from legacy Excel file'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Path to the Excel file to import'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Validate data without importing to database'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Verbose output'
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        dry_run = options['dry_run']
        verbose = options['verbose']

        if verbose:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        self.stdout.write(self.style.SUCCESS('=== Legacy Data Import Tool ==='))
        self.stdout.write(f'File: {file_path}')
        self.stdout.write(f'Mode: {"DRY RUN" if dry_run else "IMPORT"}\n')

        try:
            # Step 1: Parse Excel file
            self.stdout.write(self.style.WARNING('Step 1: Parsing Excel file...'))
            parser = ExcelParser(file_path)
            data = parser.parse()

            self.stdout.write(self.style.SUCCESS('✓ Parsing complete'))
            self.stdout.write(f'  - Tournament: {data.get("tournament", {}).get("name", "N/A")}')
            self.stdout.write(f'  - Players: {len(data.get("players", []))}')
            self.stdout.write(f'  - Course holes: {len(data.get("course", {}).get("holes", []))}')
            self.stdout.write(f'  - Scores: {len(data.get("scores", []))}\n')

            # Step 2: Validate data
            self.stdout.write(self.style.WARNING('Step 2: Validating data...'))
            validator = MigrationValidator()
            is_valid, errors, warnings = validator.validate_all(data)

            if warnings:
                self.stdout.write(self.style.WARNING(f'Warnings ({len(warnings)}):'))
                for warning in warnings[:10]:  # Show first 10
                    self.stdout.write(f'  ⚠ {warning}')
                if len(warnings) > 10:
                    self.stdout.write(f'  ... and {len(warnings) - 10} more warnings')

            if not is_valid:
                self.stdout.write(self.style.ERROR(f'\n✗ Validation failed with {len(errors)} errors:'))
                for error in errors:
                    self.stdout.write(self.style.ERROR(f'  ✗ {error}'))
                raise CommandError('Data validation failed. Please fix errors and try again.')

            self.stdout.write(self.style.SUCCESS('✓ Validation passed\n'))

            # Step 3: Import data
            if dry_run:
                self.stdout.write(self.style.SUCCESS('Dry run complete - no data imported'))
                self.stdout.write('Use without --dry-run to import data to database')
            else:
                self.stdout.write(self.style.WARNING('Step 3: Importing data to database...'))
                importer = DataImporter(dry_run=False)
                stats = importer.import_data(data)

                self.stdout.write(self.style.SUCCESS('\n✓ Import complete!'))
                self.stdout.write(importer.get_summary())

                # Step 4: Calculate results
                self.stdout.write(self.style.WARNING('\nStep 4: Calculating tournament results...'))
                from apps.scores.services import ScoringService
                from apps.tournaments.models import Tournament

                tournament = Tournament.objects.latest('created_at')
                scoring_service = ScoringService()

                try:
                    results = scoring_service.calculate_tournament_results(str(tournament.id))
                    self.stdout.write(self.style.SUCCESS(f'✓ Calculated results for {len(results)} players'))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'⚠ Result calculation skipped: {e}'))

            self.stdout.write(self.style.SUCCESS('\n=== Import Complete ==='))

        except FileNotFoundError:
            raise CommandError(f'File not found: {file_path}')
        except Exception as e:
            raise CommandError(f'Import failed: {str(e)}')
