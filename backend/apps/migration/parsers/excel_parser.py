"""
Excel parser for legacy tournament data
"""
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet

logger = logging.getLogger(__name__)


class ExcelParser:
    """Parse legacy Excel tournament files"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.workbook = None
        self.data = {
            'tournament': {},
            'course': {},
            'players': [],
            'scores': [],
        }

    def parse(self) -> Dict[str, Any]:
        """Parse the entire Excel file"""
        try:
            self.workbook = load_workbook(self.file_path, data_only=True)
            logger.info(f"Loaded workbook: {self.file_path}")
            logger.info(f"Sheets available: {self.workbook.sheetnames}")

            # Parse each section
            self._parse_tournament_info()
            self._parse_course_info()
            self._parse_players()
            self._parse_scores()

            return self.data

        except Exception as e:
            logger.error(f"Error parsing Excel file: {e}")
            raise
        finally:
            if self.workbook:
                self.workbook.close()

    def _parse_tournament_info(self) -> None:
        """Extract tournament metadata"""
        # Try common sheet names
        sheet_names = ['Tournament', 'Tournament Info', 'Info', 'Details']
        sheet = self._find_sheet(sheet_names)

        if not sheet:
            logger.warning("Tournament info sheet not found, using defaults")
            # Extract from filename
            filename = self.file_path.split('/')[-1].replace('.xlsm', '').replace('.xlsx', '')
            self.data['tournament'] = {
                'name': filename,
                'location': 'Unknown',
                'start_date': datetime.now().date(),
                'end_date': datetime.now().date(),
                'format_type': 'STROKEPLAY',
                'status': 'DRAFT',
                'max_players': 200,
            }
            return

        # Look for specific cells/patterns
        tournament_data = {}
        for row in sheet.iter_rows(max_row=20, max_col=5):
            for i, cell in enumerate(row):
                if cell.value:
                    label = str(cell.value).lower()
                    value_cell = row[i + 1] if i + 1 < len(row) else None

                    if 'tournament' in label or 'name' in label:
                        tournament_data['name'] = value_cell.value if value_cell else ''
                    elif 'location' in label or 'venue' in label or 'course' in label:
                        tournament_data['location'] = value_cell.value if value_cell else ''
                    elif 'start' in label or 'date' in label:
                        if value_cell and isinstance(value_cell.value, datetime):
                            tournament_data['start_date'] = value_cell.value.date()
                    elif 'end' in label:
                        if value_cell and isinstance(value_cell.value, datetime):
                            tournament_data['end_date'] = value_cell.value.date()

        self.data['tournament'] = tournament_data
        logger.info(f"Parsed tournament info: {tournament_data}")

    def _parse_course_info(self) -> None:
        """Extract course and hole configuration"""
        sheet_names = ['Course', 'Course Info', 'Holes', 'Scorecard']
        sheet = self._find_sheet(sheet_names)

        if not sheet:
            logger.warning("Course info sheet not found, using defaults")
            self.data['course'] = self._generate_default_course()
            return

        course_data = {
            'course_name': '',
            'tee_color': 'White',
            'rating': 72.0,
            'slope': 113,
            'par': 72,
            'holes': []
        }

        # Look for hole data (usually in a table)
        header_row = None
        for row_idx, row in enumerate(sheet.iter_rows(max_row=50)):
            # Find header row
            row_values = [str(cell.value).lower() if cell.value else '' for cell in row]
            if 'hole' in row_values or 'no' in row_values or '#' in row_values:
                header_row = row_idx + 1
                break

        if header_row:
            # Parse hole data
            for row in sheet.iter_rows(min_row=header_row + 1, max_row=header_row + 18):
                hole_num = None
                par = 4
                stroke_index = 1
                distance = 350

                for i, cell in enumerate(row[:10]):  # First 10 columns
                    if i == 0 and cell.value:  # Hole number
                        try:
                            hole_num = int(cell.value)
                        except (ValueError, TypeError):
                            continue
                    elif cell.value:
                        # Try to identify par, SI, distance
                        try:
                            val = int(cell.value)
                            if 3 <= val <= 5:
                                par = val
                            elif 1 <= val <= 18:
                                stroke_index = val
                            elif val > 100:
                                distance = val
                        except (ValueError, TypeError):
                            pass

                if hole_num and 1 <= hole_num <= 18:
                    course_data['holes'].append({
                        'hole_number': hole_num,
                        'par': par,
                        'handicap_stroke_index': stroke_index,
                        'distance': distance,
                    })

        # If no holes found, generate defaults
        if not course_data['holes']:
            logger.warning("No hole data found, generating defaults")
            course_data['holes'] = self._generate_default_holes()
        else:
            course_data['par'] = sum(h['par'] for h in course_data['holes'])

        self.data['course'] = course_data
        logger.info(f"Parsed course with {len(course_data['holes'])} holes, par {course_data['par']}")

    def _parse_players(self) -> None:
        """Extract player list with handicaps"""
        sheet_names = ['Players', 'Participants', 'Registration', 'Entry List']
        sheet = self._find_sheet(sheet_names)

        if not sheet:
            logger.warning("Players sheet not found")
            return

        players = []
        header_row = None

        # Find header row
        for row_idx, row in enumerate(sheet.iter_rows(max_row=20)):
            row_values = [str(cell.value).lower() if cell.value else '' for cell in row]
            if any(keyword in ' '.join(row_values) for keyword in ['name', 'player', 'handicap']):
                header_row = row_idx + 1
                break

        if not header_row:
            logger.warning("Could not find player header row")
            return

        # Parse player rows
        for row in sheet.iter_rows(min_row=header_row + 1, max_row=200):
            if not row[0].value:  # Skip empty rows
                continue

            player_data = {
                'first_name': '',
                'last_name': '',
                'email': '',
                'handicap_index': 0.0,
                'division': 'Championship',
            }

            # Try to extract name (could be one field or split)
            name = str(row[0].value).strip()
            if name:
                parts = name.split()
                if len(parts) >= 2:
                    player_data['first_name'] = parts[0]
                    player_data['last_name'] = ' '.join(parts[1:])
                else:
                    player_data['first_name'] = name
                    player_data['last_name'] = ''

            # Generate email
            player_data['email'] = f"{name.replace(' ', '.').lower()}@golf.local"

            # Look for handicap in subsequent cells
            for cell in row[1:10]:
                if cell.value:
                    try:
                        hcp = float(cell.value)
                        if 0 <= hcp <= 54:
                            player_data['handicap_index'] = hcp
                            break
                    except (ValueError, TypeError):
                        # Try to find division
                        if isinstance(cell.value, str):
                            division = cell.value.strip()
                            if any(div in division.upper() for div in ['CHAMP', 'A', 'B', 'C', 'SENIOR', 'LADIES']):
                                player_data['division'] = division

            if player_data['first_name']:
                players.append(player_data)

        self.data['players'] = players
        logger.info(f"Parsed {len(players)} players")

    def _parse_scores(self) -> None:
        """Extract individual hole scores"""
        sheet_names = ['Scores', 'Results', 'Scorecard', 'Round 1', 'R1']
        sheet = self._find_sheet(sheet_names)

        if not sheet:
            logger.warning("Scores sheet not found")
            return

        scores = []
        # This is complex and depends heavily on Excel layout
        # For now, log that we found the sheet
        logger.info(f"Found scores sheet, parsing not yet implemented")

        self.data['scores'] = scores

    def _find_sheet(self, possible_names: List[str]) -> Optional[Worksheet]:
        """Find a sheet by trying multiple possible names"""
        if not self.workbook:
            return None

        for name in possible_names:
            if name in self.workbook.sheetnames:
                return self.workbook[name]

        # Try case-insensitive match
        sheet_names_lower = {s.lower(): s for s in self.workbook.sheetnames}
        for name in possible_names:
            if name.lower() in sheet_names_lower:
                return self.workbook[sheet_names_lower[name.lower()]]

        return None

    def _generate_default_course(self) -> Dict[str, Any]:
        """Generate default course configuration"""
        return {
            'course_name': 'Default Course',
            'tee_color': 'White',
            'rating': 72.0,
            'slope': 113,
            'par': 72,
            'holes': self._generate_default_holes(),
        }

    def _generate_default_holes(self) -> List[Dict[str, int]]:
        """Generate default 18-hole configuration"""
        # Standard par 72 layout
        pars = [4, 4, 4, 3, 4, 5, 4, 3, 5,  # Front 9 = 36
                4, 4, 3, 5, 4, 4, 4, 3, 4]   # Back 9 = 36
        stroke_indices = [1, 11, 5, 15, 3, 9, 7, 17, 13,
                          2, 8, 16, 6, 12, 4, 10, 18, 14]
        distances = [380, 390, 350, 160, 420, 520, 400, 180, 510,
                     370, 410, 170, 490, 380, 360, 400, 150, 390]

        holes = []
        for i in range(18):
            holes.append({
                'hole_number': i + 1,
                'par': pars[i],
                'handicap_stroke_index': stroke_indices[i],
                'distance': distances[i],
            })
        return holes
