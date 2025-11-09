# Migration App

This Django app handles data migration from legacy Excel files to the GTMS database.

## Components

- **parsers/**: Excel file parsers for different data types
- **validators/**: Data validation utilities
- **management/commands/**: Django management commands for import

## Usage

```bash
# Import legacy tournament data
python manage.py import_legacy_data path/to/tournament.xlsm

# Dry run (validation only, no database changes)
python manage.py import_legacy_data path/to/tournament.xlsm --dry-run

# Verbose output
python manage.py import_legacy_data path/to/tournament.xlsm --verbose
```

## Excel File Format

The legacy Excel file should contain the following sheets:
- **Tournament Info**: Tournament metadata
- **Players**: Player list with handicaps
- **Course**: Course and hole configuration
- **Scores**: Individual hole scores
- **Results**: Final standings (optional, will be recalculated)
