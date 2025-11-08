# Legacy System Analysis Guide

## Overview
This document provides guidance for analyzing the legacy Excel/VBA system (`21ST SIBU AMATEUR OPEN GOLF CHAMPIONSHIP 2023.xlsm`) to extract critical business logic for the new GTMS system.

## Status
**PENDING**: The legacy Excel file has not yet been provided to the repository.

**Required File**: `21ST SIBU AMATEUR OPEN GOLF CHAMPIONSHIP 2023.xlsm`

**Location Expected**: `/home/user/todolist/legacy/`

## Analysis Objectives

### 1. Extract Golf Scoring Rules
The primary objective is to understand and document the exact scoring calculations used in the legacy system, including:

- **Stroke Play Scoring**:
  - How gross scores are calculated from hole scores
  - How handicap strokes are allocated per hole
  - How net scores are calculated (gross minus handicap)

- **Handicap System**:
  - Handicap index to playing handicap conversion formula
  - Course rating and slope rating usage
  - ESC (Equitable Stroke Control) rules, if applicable
  - Maximum hole scores based on handicap

- **Ranking Algorithm**:
  - How players are ranked (net score, gross score, or both)
  - Tie-breaking rules (e.g., back-nine comparison, last-six-holes, etc.)
  - Division-specific ranking logic

- **Tournament Format Specific Rules**:
  - Multi-round aggregation (how are multiple rounds combined?)
  - Cut rules, if any
  - Prize categories and eligibility

### 2. Map Excel Formulas to Algorithm Specifications

For each complex Excel formula or VBA function, we need to:

1. **Identify the formula/function location** (worksheet name, cell reference, or VBA module)
2. **Document inputs** (what data does it consume?)
3. **Document outputs** (what does it calculate?)
4. **Extract the logic** (translate Excel formula to pseudo-code)
5. **Identify dependencies** (what other formulas/functions does it rely on?)
6. **Create test cases** (input examples and expected outputs)

### 3. VBA Macro Analysis

VBA macros may contain critical business logic not visible in Excel formulas. Analysis should cover:

- **Macro triggers**: When and how are macros executed?
- **Data manipulation**: What data transformations occur in VBA?
- **Calculations**: Are there scoring calculations in VBA that aren't in formulas?
- **Validations**: What data validation rules are enforced?
- **Report generation**: How are leaderboards and reports generated?

### 4. Data Structure Analysis

Understanding the legacy data structure helps inform migration strategy:

- **Worksheets and their purposes**
- **Data relationships** (which sheets reference other sheets?)
- **Data types and formats**
- **Validation rules** (data validation, dropdown lists)
- **Lookup tables** (course configurations, handicap tables, etc.)

## Analysis Process

### Step 1: Initial File Inspection

```bash
# Once file is available, extract to legacy directory
mkdir -p /home/user/todolist/legacy
# Place file: 21ST SIBU AMATEUR OPEN GOLF CHAMPIONSHIP 2023.xlsm

# Use Python to inspect file structure
python3 << EOF
import openpyxl
import os

file_path = '/home/user/todolist/legacy/21ST SIBU AMATEUR OPEN GOLF CHAMPIONSHIP 2023.xlsm'

if os.path.exists(file_path):
    # Load workbook
    wb = openpyxl.load_workbook(file_path, keep_vba=True)

    print("Worksheets found:")
    for sheet_name in wb.sheetnames:
        print(f"  - {sheet_name}")

    print("\nVBA Modules (if accessible):")
    # Note: Full VBA extraction may require additional libraries like oletools
else:
    print("Legacy file not found. Please place the file in /home/user/todolist/legacy/")
EOF
```

### Step 2: Extract VBA Code

Use `oletools` or similar to extract VBA code for analysis:

```bash
# Install oletools if needed
pip install oletools

# Extract VBA code
olevba "/home/user/todolist/legacy/21ST SIBU AMATEUR OPEN GOLF CHAMPIONSHIP 2023.xlsm" > legacy/vba_extracted.txt
```

### Step 3: Document Formulas

For each worksheet with scoring calculations:

1. Identify all formula cells
2. Document the formula logic
3. Trace precedents and dependents
4. Create pseudo-code representation

### Step 4: Create Test Data Set

Extract a representative sample of historical data:

- At least 20 players
- Complete 18-hole scores
- Various handicap levels
- Multiple divisions
- Known final results (for validation)

### Step 5: Validate Understanding

Create test cases that:

1. Use historical input data
2. Run through documented algorithm
3. Compare output to legacy system's results
4. Achieve 100% match rate

## Expected Deliverables

### 1. Scoring Logic Formal Specification
**File**: `docs/04_scoring_logic_specification.md`

This document should contain:
- Detailed pseudo-code for all scoring algorithms
- Mathematical formulas in standard notation
- Flow diagrams for complex logic
- Edge case handling
- Test cases with expected results

### 2. VBA Pseudo-code Analysis
**File**: `docs/05_vba_analysis.md`

This document should contain:
- All VBA macros converted to pseudo-code
- Macro execution flow
- Data dependencies
- Critical business rules implemented in VBA

### 3. Historical Test Data Set
**File**: `legacy/test_data.json` or `legacy/test_data.csv`

This file should contain:
- Anonymized player data (or actual if permitted)
- Complete tournament data
- Expected results for validation

### 4. Data Migration Mapping
**File**: `docs/06_data_migration_mapping.md`

This document should map:
- Legacy data structure → New database schema
- Data transformations required
- Data cleansing rules
- Migration validation checks

## Common Golf Scoring Rules (Reference)

### USGA Handicap System Basics

**Playing Handicap Calculation** (as of World Handicap System):
```
Playing Handicap = Handicap Index × (Slope Rating / 113) + (Course Rating - Par)
```

**Net Score Calculation**:
```
Net Score = Gross Score - Playing Handicap
```

**Stroke Allocation by Hole**:
- Strokes are allocated based on the hole's handicap stroke index
- If playing handicap is 18, player gets 1 stroke on each hole
- If playing handicap is 10, player gets 1 stroke on holes with stroke index 1-10
- If playing handicap is 25, player gets 1 stroke on all 18 holes, plus an additional stroke on the 7 hardest holes (index 1-7)

**ESC (Equitable Stroke Control)**:
Maximum score per hole based on Course Handicap:
- 9 or less: Double Bogey
- 10-19: 7
- 20-29: 8
- 30-39: 9
- 40+: 10

### Tie-Breaking Rules (Common)

When players have the same net score, typical tie-breaking methods:

1. **Back-9 comparison**: Compare net scores on the back 9 holes
2. **Last 6 holes**: Compare net scores on holes 13-18
3. **Last 3 holes**: Compare net scores on holes 16-18
4. **Countback by handicap**: Player with lower handicap wins
5. **Sudden death playoff**: If applicable

**Note**: The actual tie-breaking rules used in the legacy system must be verified from the Excel file.

## Critical Constraints

### MUST Match Legacy System

The new system's scoring engine output **MUST** match the legacy system's results for historical data test cases. This is a critical requirement for system acceptance.

**Validation Process**:
1. Extract historical tournament data from Excel file
2. Run data through new scoring engine
3. Compare results cell-by-cell with legacy output
4. Investigate and resolve any discrepancies
5. Repeat until 100% match achieved

### Regression Testing

All scoring logic must have comprehensive regression tests:
- Minimum 50 test cases covering various scenarios
- Test cases include edge cases (ties, maximum handicaps, etc.)
- Tests run automatically in CI/CD pipeline
- Any changes to scoring logic must pass all regression tests

## Next Steps (When File is Available)

1. **Immediately upon receiving the file**:
   - Place file in `/home/user/todolist/legacy/`
   - Run initial inspection scripts
   - Extract VBA code

2. **Within 1 day**:
   - Complete worksheet-level analysis
   - Document all formulas and VBA macros
   - Identify critical business rules

3. **Within 2 days**:
   - Create scoring logic formal specification
   - Extract test data set
   - Begin validation testing

4. **Within 3 days**:
   - Complete validation (100% match to legacy)
   - Finalize all analysis deliverables
   - Ready to proceed with Phase 2 implementation

## Questions to Answer Through Analysis

1. **Handicap System**:
   - Is the USGA/WHS formula used, or a custom formula?
   - Are there any modifications to standard handicap calculations?

2. **Scoring**:
   - Is ESC applied? If so, what are the max scores per hole?
   - Are there any special scoring rules (e.g., Stableford, modified Stableford)?

3. **Divisions**:
   - How are divisions determined (age, handicap range, both)?
   - Are there different rules for different divisions?

4. **Multi-Round Tournaments**:
   - How are multiple rounds aggregated?
   - Is there a cut after a certain round?

5. **Prizes/Categories**:
   - What prize categories exist (gross winner, net winner, best front-9, etc.)?
   - How are players eligible for multiple prizes?

6. **Data Validation**:
   - What score entry validations are in place?
   - How are impossible scores (e.g., 0, >15) handled?

## Analysis Tools

### Recommended Python Libraries

```python
# For Excel file analysis
import openpyxl          # Read .xlsx files
import xlrd              # Read .xls files (older format)
import pandas as pd      # Data analysis

# For VBA extraction
from oletools.olevba import VBA_Parser

# For formula parsing
import formulas          # Parse Excel formulas to Python

# For data validation
import jsonschema        # Validate extracted data
```

### Sample Analysis Script

```python
#!/usr/bin/env python3
"""
Legacy Excel Analysis Script
Extracts formulas, VBA code, and data from legacy GTMS Excel file.
"""

import openpyxl
import pandas as pd
from oletools.olevba import VBA_Parser
import json

def analyze_legacy_file(file_path):
    """Analyze the legacy Excel file and extract key information."""

    # Load workbook
    wb = openpyxl.load_workbook(file_path, data_only=False)

    # Extract worksheet names
    worksheets = wb.sheetnames
    print(f"Found {len(worksheets)} worksheets: {worksheets}")

    # Analyze each worksheet
    for sheet_name in worksheets:
        ws = wb[sheet_name]
        print(f"\n--- Analyzing {sheet_name} ---")

        # Find all formula cells
        formula_cells = []
        for row in ws.iter_rows():
            for cell in row:
                if cell.value and isinstance(cell.value, str) and cell.value.startswith('='):
                    formula_cells.append({
                        'cell': cell.coordinate,
                        'formula': cell.value
                    })

        print(f"Found {len(formula_cells)} formula cells")
        if formula_cells:
            print("Sample formulas:")
            for fc in formula_cells[:5]:  # Show first 5
                print(f"  {fc['cell']}: {fc['formula']}")

    # Extract VBA code
    print("\n--- Extracting VBA Code ---")
    vba_parser = VBA_Parser(file_path)
    if vba_parser.detect_vba_macros():
        for (filename, stream_path, vba_filename, vba_code) in vba_parser.extract_macros():
            print(f"Found VBA module: {vba_filename}")
            # Save VBA code to file
            with open(f"legacy/vba_{vba_filename}.txt", 'w') as f:
                f.write(vba_code)
    else:
        print("No VBA macros found")

    vba_parser.close()

if __name__ == "__main__":
    file_path = "/home/user/todolist/legacy/21ST SIBU AMATEUR OPEN GOLF CHAMPIONSHIP 2023.xlsm"
    analyze_legacy_file(file_path)
```

---

## Status Update

**Current Status**: Awaiting legacy Excel file

**Blocker**: Cannot complete Phase 1.1 (Legacy Logic Extraction) without the file

**Impact**:
- Phase 2.2 (Scoring Calculation Engine) depends on this analysis
- Can proceed with Phase 2.1 (Project Structure Setup) in parallel

**Action Required**:
Please provide the file: `21ST SIBU AMATEUR OPEN GOLF CHAMPIONSHIP 2023.xlsm`

Place it in: `/home/user/todolist/legacy/` directory

---

**Document Version**: 1.0
**Last Updated**: 2024-11-08
**Status**: Pending file availability
