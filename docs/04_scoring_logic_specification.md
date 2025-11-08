# Golf Tournament Management System - Scoring Logic Formal Specification

## Status
**DRAFT - PENDING LEGACY ANALYSIS**

This document will contain the detailed scoring algorithms extracted from the legacy Excel/VBA system. It will be populated once the legacy file analysis (Phase 1.1) is complete.

## Document Purpose
This specification defines the exact algorithms and business rules for golf tournament scoring, ensuring the new system produces identical results to the legacy system.

## Table of Contents
1. Handicap Calculation
2. Gross Score Calculation
3. Net Score Calculation
4. Stroke Allocation
5. Ranking Algorithm
6. Tie-Breaking Rules
7. Division-Specific Rules
8. Test Cases

---

## 1. Handicap Calculation

### 1.1 Handicap Index to Playing Handicap Conversion

**Status**: PENDING - To be extracted from legacy system

**Expected Formula**:
```
Playing Handicap = Handicap Index × (Slope Rating ÷ 113) + (Course Rating - Par)
```

**Rounding Rules**: TBD

**Constraints**:
- Minimum Playing Handicap: TBD
- Maximum Playing Handicap: TBD

**Test Cases**: To be created from historical data

---

## 2. Gross Score Calculation

### 2.1 Total Gross Score

**Status**: PENDING

**Algorithm**:
```
Total Gross Score = Sum of all 18 hole scores
```

**Validations**:
- Minimum score per hole: TBD
- Maximum score per hole: TBD
- Handling of incomplete rounds: TBD

**ESC (Equitable Stroke Control)**:
- To be determined from legacy system
- Maximum scores per hole based on handicap

---

## 3. Net Score Calculation

### 3.1 Hole-by-Hole Net Score

**Status**: PENDING

**Algorithm**: To be extracted

**Stroke Allocation Method**: To be determined

---

## 4. Stroke Allocation

### 4.1 Stroke Index Application

**Status**: PENDING

**Algorithm**: To be extracted from legacy VBA code

**Logic**:
- How strokes are distributed across holes
- Handling of high handicaps (>18)
- Double-stroke allocation rules

---

## 5. Ranking Algorithm

### 5.1 Overall Ranking

**Status**: PENDING

**Primary Sort**: Net Score (ascending)

**Secondary Sort (Tie-breaking)**: To be determined

### 5.2 Division Ranking

**Status**: PENDING

**Division Categories**: To be extracted

**Ranking Method**: To be determined

---

## 6. Tie-Breaking Rules

### 6.1 Net Score Ties

**Status**: PENDING - Critical for accurate implementation

**Tie-Breaking Sequence**:
1. TBD (e.g., back-9 comparison)
2. TBD (e.g., last-6-holes)
3. TBD

**Detailed Algorithm**: To be extracted from legacy system

---

## 7. Division-Specific Rules

### 7.1 Division Categories

**Status**: PENDING

**Divisions**: To be determined from legacy data

**Eligibility Criteria**: To be extracted

---

## 8. Test Cases

### 8.1 Regression Test Suite

**Status**: PENDING - Will be created from historical tournament data

**Test Case Format**:
```json
{
  "test_case_id": "TC001",
  "description": "Standard net score calculation",
  "inputs": {
    "handicap_index": 10.5,
    "course_rating": 72.1,
    "slope_rating": 131,
    "par": 72,
    "hole_scores": [4, 5, 3, 4, 5, 4, 3, 5, 4, 4, 4, 5, 3, 4, 5, 4, 4, 5]
  },
  "expected_outputs": {
    "playing_handicap": "TBD",
    "gross_score": 75,
    "net_score": "TBD"
  }
}
```

**Minimum Test Coverage**:
- 50+ test cases from historical data
- Edge cases (max/min handicaps, ties, incomplete rounds)
- All division categories
- Multi-round scenarios

---

## 9. Implementation Notes

### 9.1 Scoring Engine Design Principles

1. **Pure Functions**: All scoring functions must be pure (no side effects)
2. **Idempotent**: Same input always produces same output
3. **Testable**: Separated from database layer
4. **Documented**: All formulas clearly commented
5. **Validated**: 100% match with legacy system results

### 9.2 Module Structure

**Proposed Location**: `backend/gtms/scoring/engine.py`

**Key Functions** (to be implemented):
```python
def calculate_playing_handicap(
    handicap_index: Decimal,
    slope_rating: int,
    course_rating: Decimal,
    par: int
) -> int:
    """Calculate playing handicap for a specific course."""
    pass

def calculate_gross_score(
    hole_scores: List[int]
) -> int:
    """Calculate total gross score from hole scores."""
    pass

def apply_esc(
    hole_score: int,
    hole_par: int,
    playing_handicap: int,
    hole_stroke_index: int
) -> int:
    """Apply Equitable Stroke Control to a hole score."""
    pass

def calculate_net_score(
    hole_scores: List[HoleScoreData],
    playing_handicap: int,
    course_config: CourseConfigData
) -> int:
    """Calculate net score with stroke allocation."""
    pass

def rank_players(
    player_scores: List[PlayerScoreData],
    tie_breaker_rules: TieBreakerConfig
) -> List[RankedPlayer]:
    """Rank players with tie-breaking logic."""
    pass
```

---

## 10. Validation Requirements

### 10.1 Legacy System Validation

**Acceptance Criteria**:
- New scoring engine must produce **identical results** to legacy system
- Validation performed on minimum 20 historical player records
- 100% match rate required

**Validation Process**:
1. Extract historical data from legacy Excel file
2. Run through new scoring engine
3. Compare results
4. Document and resolve any discrepancies
5. Repeat until 100% match

### 10.2 Ongoing Regression Testing

- All test cases run automatically in CI/CD
- Any changes to scoring logic must pass all regression tests
- New test cases added for any discovered edge cases

---

## Appendix A: Golf Scoring Reference

### USGA Handicap System (Reference)

**World Handicap System (2020+)**:
```
Handicap Index = (Sum of best 8 of last 20 Score Differentials) / 8

Score Differential = (Adjusted Gross Score - Course Rating) × (113 / Slope Rating)

Playing Handicap = Handicap Index × (Slope Rating / 113) + (Course Rating - Par)
```

**Note**: The actual formulas used in the legacy system may differ and must be verified.

### Common Stroke Play Rules

- **Gross Score**: Total strokes without handicap adjustment
- **Net Score**: Gross score minus playing handicap (applied per hole)
- **Stroke Index**: Holes ranked by difficulty (1 = hardest, 18 = easiest)
- **ESC**: Maximum score per hole to prevent one bad hole from inflating handicap

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2024-11-08 | AI Agent | Initial draft template |
| 1.0 | TBD | AI Agent | Populated with legacy system analysis |

---

**Next Steps**:
1. Complete legacy Excel file analysis (Phase 1.1)
2. Populate this document with extracted algorithms
3. Create comprehensive test suite from historical data
4. Validate scoring engine implementation against legacy results

**Status**: AWAITING LEGACY FILE - `21ST SIBU AMATEUR OPEN GOLF CHAMPIONSHIP 2023.xlsm`
