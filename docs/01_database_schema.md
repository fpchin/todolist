# Golf Tournament Management System - Database Schema Design

## Overview
This document defines the PostgreSQL database schema for the GTMS system. The schema is designed in Third Normal Form (3NF) to ensure data integrity, minimize redundancy, and support extensibility for future tournament formats.

## Entity Relationship Diagram

```
┌─────────────────┐         ┌─────────────────┐
│   Tournament    │         │     Player      │
├─────────────────┤         ├─────────────────┤
│ id (PK)         │         │ id (PK)         │
│ name            │         │ first_name      │
│ start_date      │         │ last_name       │
│ end_date        │         │ email           │
│ location        │         │ phone           │
│ format_type     │         │ club_affiliation│
│ status          │         │ date_of_birth   │
│ created_at      │         │ created_at      │
│ updated_at      │         │ updated_at      │
└─────────────────┘         └─────────────────┘
         │                           │
         │                           │
         │    ┌────────────────────┐ │
         └────│ TournamentPlayer   │─┘
              ├────────────────────┤
              │ id (PK)            │
              │ tournament_id (FK) │
              │ player_id (FK)     │
              │ handicap_index     │
              │ playing_handicap   │
              │ division           │
              │ registration_date  │
              │ status             │
              └────────────────────┘
                       │
                       │
         ┌─────────────┴─────────────┐
         │                           │
┌────────▼────────┐         ┌────────▼────────┐
│   TeeTime       │         │     Round       │
├─────────────────┤         ├─────────────────┤
│ id (PK)         │         │ id (PK)         │
│ tournament_id(FK)│        │ tournament_id(FK)│
│ round_id (FK)   │         │ round_number    │
│ tee_time        │         │ round_date      │
│ starting_hole   │         │ course_config(FK)│
│ created_at      │         │ status          │
└─────────────────┘         └─────────────────┘
         │
         │
┌────────▼────────┐
│   FlightPlayer  │
├─────────────────┤
│ id (PK)         │
│ tee_time_id (FK)│
│ player_id (FK)  │
│ position        │
└─────────────────┘
         │
         │
         │          ┌─────────────────┐
         │          │ CourseConfig    │
         │          ├─────────────────┤
         │          │ id (PK)         │
         │          │ course_name     │
         │          │ tee_color       │
         │          │ rating          │
         │          │ slope           │
         │          │ par             │
         │          │ created_at      │
         │          └─────────────────┘
         │                   │
         │                   │
         │          ┌────────▼────────┐
         │          │   HoleConfig    │
         │          ├─────────────────┤
         │          │ id (PK)         │
         │          │ course_config(FK)│
         │          │ hole_number     │
         │          │ par             │
         │          │ handicap_stroke │
         │          │ distance        │
         │          └─────────────────┘
         │
┌────────▼────────┐
│   HoleScore     │
├─────────────────┤
│ id (PK)         │
│ round_id (FK)   │
│ player_id (FK)  │
│ hole_number     │
│ strokes         │
│ putts           │
│ fairway_hit     │
│ green_in_reg    │
│ penalty_strokes │
│ verified        │
│ scorer_id (FK)  │
│ created_at      │
│ updated_at      │
└─────────────────┘

┌─────────────────┐         ┌─────────────────┐
│ HandicapHistory │         │     Result      │
├─────────────────┤         ├─────────────────┤
│ id (PK)         │         │ id (PK)         │
│ player_id (FK)  │         │ tournament_id(FK)│
│ handicap_index  │         │ player_id (FK)  │
│ effective_date  │         │ division        │
│ issuing_authority│        │ total_gross     │
│ created_at      │         │ total_net       │
└─────────────────┘         │ total_points    │
                            │ rank_overall    │
                            │ rank_division   │
                            │ prize_category  │
                            │ calculated_at   │
                            │ verified        │
                            └─────────────────┘
```

## Core Entities

### 1. Tournament
Stores tournament master data.

**Fields:**
- `id`: UUID (Primary Key)
- `name`: VARCHAR(255) - Tournament name
- `start_date`: DATE - Tournament start date
- `end_date`: DATE - Tournament end date
- `location`: VARCHAR(255) - Tournament location
- `format_type`: VARCHAR(50) - ENUM('STROKEPLAY', 'STABLEFORD', 'MATCHPLAY', 'SCRAMBLE')
- `status`: VARCHAR(20) - ENUM('DRAFT', 'OPEN', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED')
- `created_at`: TIMESTAMP WITH TIME ZONE
- `updated_at`: TIMESTAMP WITH TIME ZONE

**Indexes:**
- PRIMARY KEY on `id`
- INDEX on `start_date, status`

### 2. Player
Stores player master data.

**Fields:**
- `id`: UUID (Primary Key)
- `first_name`: VARCHAR(100)
- `last_name`: VARCHAR(100)
- `email`: VARCHAR(255) UNIQUE
- `phone`: VARCHAR(20)
- `club_affiliation`: VARCHAR(255)
- `date_of_birth`: DATE
- `created_at`: TIMESTAMP WITH TIME ZONE
- `updated_at`: TIMESTAMP WITH TIME ZONE

**Indexes:**
- PRIMARY KEY on `id`
- UNIQUE INDEX on `email`
- INDEX on `last_name, first_name`

### 3. TournamentPlayer
Junction table linking players to tournaments with tournament-specific attributes.

**Fields:**
- `id`: UUID (Primary Key)
- `tournament_id`: UUID (Foreign Key -> Tournament.id)
- `player_id`: UUID (Foreign Key -> Player.id)
- `handicap_index`: DECIMAL(4,1) - Player's handicap index at registration
- `playing_handicap`: INTEGER - Calculated playing handicap for this tournament
- `division`: VARCHAR(50) - Player's division (e.g., 'Championship', 'A', 'B', 'C', 'Senior')
- `registration_date`: TIMESTAMP WITH TIME ZONE
- `status`: VARCHAR(20) - ENUM('REGISTERED', 'CONFIRMED', 'WITHDRAWN', 'DISQUALIFIED')

**Indexes:**
- PRIMARY KEY on `id`
- UNIQUE INDEX on `(tournament_id, player_id)`
- INDEX on `tournament_id`
- INDEX on `player_id`

### 4. CourseConfiguration
Stores golf course configuration data.

**Fields:**
- `id`: UUID (Primary Key)
- `course_name`: VARCHAR(255)
- `tee_color`: VARCHAR(50) - e.g., 'Blue', 'White', 'Red'
- `rating`: DECIMAL(4,1) - Course rating
- `slope`: INTEGER - Slope rating
- `par`: INTEGER - Total par for the course
- `created_at`: TIMESTAMP WITH TIME ZONE

**Indexes:**
- PRIMARY KEY on `id`
- INDEX on `course_name, tee_color`

### 5. HoleConfiguration
Stores per-hole configuration for each course.

**Fields:**
- `id`: UUID (Primary Key)
- `course_config_id`: UUID (Foreign Key -> CourseConfiguration.id)
- `hole_number`: INTEGER (1-18 or 1-9)
- `par`: INTEGER (3-5)
- `handicap_stroke_index`: INTEGER (1-18) - Stroke index for handicap allocation
- `distance`: INTEGER - Distance in yards/meters

**Indexes:**
- PRIMARY KEY on `id`
- UNIQUE INDEX on `(course_config_id, hole_number)`
- INDEX on `course_config_id`

### 6. Round
Stores round information within a tournament.

**Fields:**
- `id`: UUID (Primary Key)
- `tournament_id`: UUID (Foreign Key -> Tournament.id)
- `round_number`: INTEGER (1, 2, 3, 4)
- `round_date`: DATE
- `course_config_id`: UUID (Foreign Key -> CourseConfiguration.id)
- `status`: VARCHAR(20) - ENUM('SCHEDULED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED')

**Indexes:**
- PRIMARY KEY on `id`
- UNIQUE INDEX on `(tournament_id, round_number)`
- INDEX on `tournament_id`

### 7. TeeTime
Stores tee time (flight) information.

**Fields:**
- `id`: UUID (Primary Key)
- `tournament_id`: UUID (Foreign Key -> Tournament.id)
- `round_id`: UUID (Foreign Key -> Round.id)
- `tee_time`: TIMESTAMP WITH TIME ZONE - Scheduled tee time
- `starting_hole`: INTEGER - Starting hole number (for shotgun starts)
- `created_at`: TIMESTAMP WITH TIME ZONE

**Indexes:**
- PRIMARY KEY on `id`
- INDEX on `round_id, tee_time`

### 8. FlightPlayer
Junction table for players in a specific flight/tee time.

**Fields:**
- `id`: UUID (Primary Key)
- `tee_time_id`: UUID (Foreign Key -> TeeTime.id)
- `player_id`: UUID (Foreign Key -> Player.id)
- `position`: INTEGER - Position in the flight (1-4)

**Indexes:**
- PRIMARY KEY on `id`
- UNIQUE INDEX on `(tee_time_id, player_id)`
- UNIQUE INDEX on `(tee_time_id, position)`
- INDEX on `player_id`

### 9. HoleScore
Stores individual hole scores with detailed statistics.

**Fields:**
- `id`: UUID (Primary Key)
- `round_id`: UUID (Foreign Key -> Round.id)
- `player_id`: UUID (Foreign Key -> Player.id)
- `hole_number`: INTEGER (1-18)
- `strokes`: INTEGER - Number of strokes taken
- `putts`: INTEGER (nullable) - Number of putts
- `fairway_hit`: BOOLEAN (nullable) - Fairway hit indicator
- `green_in_regulation`: BOOLEAN (nullable) - GIR indicator
- `penalty_strokes`: INTEGER DEFAULT 0 - Penalty strokes
- `verified`: BOOLEAN DEFAULT FALSE - Score verification status
- `scorer_id`: UUID (Foreign Key -> Player.id, nullable) - Who entered the score
- `created_at`: TIMESTAMP WITH TIME ZONE
- `updated_at`: TIMESTAMP WITH TIME ZONE

**Indexes:**
- PRIMARY KEY on `id`
- UNIQUE INDEX on `(round_id, player_id, hole_number)`
- INDEX on `round_id, player_id`
- INDEX on `player_id`

### 10. HandicapHistory
Stores historical handicap records for players.

**Fields:**
- `id`: UUID (Primary Key)
- `player_id`: UUID (Foreign Key -> Player.id)
- `handicap_index`: DECIMAL(4,1)
- `effective_date`: DATE
- `issuing_authority`: VARCHAR(100) - e.g., 'USGA', 'R&A'
- `created_at`: TIMESTAMP WITH TIME ZONE

**Indexes:**
- PRIMARY KEY on `id`
- INDEX on `player_id, effective_date DESC`

### 11. Result
Stores calculated tournament results and rankings.

**Fields:**
- `id`: UUID (Primary Key)
- `tournament_id`: UUID (Foreign Key -> Tournament.id)
- `player_id`: UUID (Foreign Key -> Player.id)
- `division`: VARCHAR(50) - Division the player competed in
- `total_gross`: INTEGER - Total gross score
- `total_net`: INTEGER - Total net score (gross - handicap)
- `total_points`: INTEGER (nullable) - For Stableford scoring
- `rank_overall`: INTEGER - Overall ranking
- `rank_division`: INTEGER - Division ranking
- `prize_category`: VARCHAR(100) (nullable) - Prize category won
- `calculated_at`: TIMESTAMP WITH TIME ZONE
- `verified`: BOOLEAN DEFAULT FALSE

**Indexes:**
- PRIMARY KEY on `id`
- UNIQUE INDEX on `(tournament_id, player_id)`
- INDEX on `tournament_id, rank_overall`
- INDEX on `tournament_id, division, rank_division`

## Design Principles

### Third Normal Form (3NF) Compliance
1. **First Normal Form (1NF)**: All tables have atomic values and each column contains values of a single type.
2. **Second Normal Form (2NF)**: All non-key attributes are fully functionally dependent on the primary key.
3. **Third Normal Form (3NF)**: No transitive dependencies - all non-key attributes depend only on the primary key.

### Extensibility for Future Formats
- `Tournament.format_type` supports multiple scoring systems
- `Result.total_points` accommodates Stableford scoring
- Modular design allows adding new tables for format-specific rules without altering core schema

### Data Integrity
- All foreign keys have explicit relationships
- UNIQUE constraints prevent duplicate entries
- CHECK constraints enforce business rules (to be added in DDL)
- Timestamps for audit trail

### Performance Optimization
- Strategic indexing on frequently queried columns
- Denormalized `Result` table for fast leaderboard queries
- Separate `HandicapHistory` for temporal data without bloating Player table

## Next Steps
1. Generate PostgreSQL DDL migration scripts
2. Create database seed data for testing
3. Define database-level constraints and triggers
4. Create views for common queries (leaderboard, player stats)
