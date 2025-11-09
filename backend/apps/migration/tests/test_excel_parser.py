"""
Tests for Excel parser
"""
import pytest
from pathlib import Path
from apps.migration.parsers.excel_parser import ExcelParser


class TestExcelParser:
    """Test Excel parser functionality"""

    def test_parser_initialization(self):
        """Test parser can be initialized"""
        parser = ExcelParser('test.xlsx')
        assert parser.file_path == 'test.xlsx'
        assert parser.workbook is None

    def test_default_course_generation(self):
        """Test default course generation"""
        parser = ExcelParser('test.xlsx')
        course = parser._generate_default_course()

        assert course['course_name'] == 'Default Course'
        assert course['par'] == 72
        assert len(course['holes']) == 18

    def test_default_holes_generation(self):
        """Test default 18 holes generation"""
        parser = ExcelParser('test.xlsx')
        holes = parser._generate_default_holes()

        assert len(holes) == 18

        # Check first hole
        assert holes[0]['hole_number'] == 1
        assert holes[0]['par'] in [3, 4, 5]
        assert 1 <= holes[0]['handicap_stroke_index'] <= 18

        # Check total par
        total_par = sum(h['par'] for h in holes)
        assert total_par == 72

        # Check stroke indices are unique
        stroke_indices = [h['handicap_stroke_index'] for h in holes]
        assert len(set(stroke_indices)) == 18
        assert set(stroke_indices) == set(range(1, 19))
