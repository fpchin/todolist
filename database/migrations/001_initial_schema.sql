-- Golf Tournament Management System - Initial Schema Migration
-- PostgreSQL 12+ Required
-- Migration: 001_initial_schema
-- Created: 2024-11-08

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create custom ENUM types
CREATE TYPE tournament_status AS ENUM ('DRAFT', 'OPEN', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED');
CREATE TYPE tournament_format AS ENUM ('STROKEPLAY', 'STABLEFORD', 'MATCHPLAY', 'SCRAMBLE');
CREATE TYPE player_registration_status AS ENUM ('REGISTERED', 'CONFIRMED', 'WITHDRAWN', 'DISQUALIFIED');
CREATE TYPE round_status AS ENUM ('SCHEDULED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED');

-- =====================================================
-- Table: Tournament
-- =====================================================
CREATE TABLE tournament (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    location VARCHAR(255) NOT NULL,
    format_type tournament_format NOT NULL DEFAULT 'STROKEPLAY',
    status tournament_status NOT NULL DEFAULT 'DRAFT',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_tournament_dates CHECK (end_date >= start_date)
);

CREATE INDEX idx_tournament_start_date_status ON tournament(start_date, status);
CREATE INDEX idx_tournament_status ON tournament(status);

COMMENT ON TABLE tournament IS 'Master table for golf tournaments';
COMMENT ON COLUMN tournament.format_type IS 'Scoring format: STROKEPLAY, STABLEFORD, MATCHPLAY, or SCRAMBLE';

-- =====================================================
-- Table: Player
-- =====================================================
CREATE TABLE player (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    club_affiliation VARCHAR(255),
    date_of_birth DATE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_player_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

CREATE UNIQUE INDEX idx_player_email ON player(email);
CREATE INDEX idx_player_name ON player(last_name, first_name);

COMMENT ON TABLE player IS 'Master table for players/participants';
COMMENT ON COLUMN player.email IS 'Unique email address for player identification';

-- =====================================================
-- Table: HandicapHistory
-- =====================================================
CREATE TABLE handicap_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    player_id UUID NOT NULL REFERENCES player(id) ON DELETE CASCADE,
    handicap_index DECIMAL(4,1) NOT NULL,
    effective_date DATE NOT NULL,
    issuing_authority VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_handicap_index_range CHECK (handicap_index >= -5.0 AND handicap_index <= 54.0)
);

CREATE INDEX idx_handicap_history_player_date ON handicap_history(player_id, effective_date DESC);

COMMENT ON TABLE handicap_history IS 'Historical handicap records for players';
COMMENT ON COLUMN handicap_history.handicap_index IS 'USGA/WHS Handicap Index';

-- =====================================================
-- Table: TournamentPlayer
-- =====================================================
CREATE TABLE tournament_player (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tournament_id UUID NOT NULL REFERENCES tournament(id) ON DELETE CASCADE,
    player_id UUID NOT NULL REFERENCES player(id) ON DELETE CASCADE,
    handicap_index DECIMAL(4,1) NOT NULL,
    playing_handicap INTEGER NOT NULL,
    division VARCHAR(50) NOT NULL,
    registration_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status player_registration_status NOT NULL DEFAULT 'REGISTERED',

    CONSTRAINT chk_playing_handicap_range CHECK (playing_handicap >= 0 AND playing_handicap <= 54)
);

CREATE UNIQUE INDEX idx_tournament_player_unique ON tournament_player(tournament_id, player_id);
CREATE INDEX idx_tournament_player_tournament ON tournament_player(tournament_id);
CREATE INDEX idx_tournament_player_player ON tournament_player(player_id);
CREATE INDEX idx_tournament_player_division ON tournament_player(tournament_id, division);

COMMENT ON TABLE tournament_player IS 'Junction table linking players to tournaments with tournament-specific attributes';
COMMENT ON COLUMN tournament_player.playing_handicap IS 'Calculated handicap strokes for this specific tournament/course';

-- =====================================================
-- Table: CourseConfiguration
-- =====================================================
CREATE TABLE course_configuration (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_name VARCHAR(255) NOT NULL,
    tee_color VARCHAR(50) NOT NULL,
    rating DECIMAL(4,1) NOT NULL,
    slope INTEGER NOT NULL,
    par INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_course_rating CHECK (rating >= 60.0 AND rating <= 85.0),
    CONSTRAINT chk_course_slope CHECK (slope >= 55 AND slope <= 155),
    CONSTRAINT chk_course_par CHECK (par >= 27 AND par <= 90)
);

CREATE INDEX idx_course_config_name_tee ON course_configuration(course_name, tee_color);

COMMENT ON TABLE course_configuration IS 'Golf course configuration including rating and slope';
COMMENT ON COLUMN course_configuration.rating IS 'Course rating (expected score for scratch golfer)';
COMMENT ON COLUMN course_configuration.slope IS 'Slope rating (difficulty for bogey golfer vs scratch)';

-- =====================================================
-- Table: HoleConfiguration
-- =====================================================
CREATE TABLE hole_configuration (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_config_id UUID NOT NULL REFERENCES course_configuration(id) ON DELETE CASCADE,
    hole_number INTEGER NOT NULL,
    par INTEGER NOT NULL,
    handicap_stroke_index INTEGER NOT NULL,
    distance INTEGER NOT NULL,

    CONSTRAINT chk_hole_number CHECK (hole_number >= 1 AND hole_number <= 18),
    CONSTRAINT chk_hole_par CHECK (par >= 3 AND par <= 5),
    CONSTRAINT chk_hole_handicap_index CHECK (handicap_stroke_index >= 1 AND handicap_stroke_index <= 18),
    CONSTRAINT chk_hole_distance CHECK (distance > 0)
);

CREATE UNIQUE INDEX idx_hole_config_course_hole ON hole_configuration(course_config_id, hole_number);
CREATE INDEX idx_hole_config_course ON hole_configuration(course_config_id);

COMMENT ON TABLE hole_configuration IS 'Per-hole configuration for each course';
COMMENT ON COLUMN hole_configuration.handicap_stroke_index IS 'Stroke index for handicap allocation (1=hardest, 18=easiest)';

-- =====================================================
-- Table: Round
-- =====================================================
CREATE TABLE round (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tournament_id UUID NOT NULL REFERENCES tournament(id) ON DELETE CASCADE,
    round_number INTEGER NOT NULL,
    round_date DATE NOT NULL,
    course_config_id UUID NOT NULL REFERENCES course_configuration(id),
    status round_status NOT NULL DEFAULT 'SCHEDULED',

    CONSTRAINT chk_round_number CHECK (round_number >= 1 AND round_number <= 4)
);

CREATE UNIQUE INDEX idx_round_tournament_number ON round(tournament_id, round_number);
CREATE INDEX idx_round_tournament ON round(tournament_id);
CREATE INDEX idx_round_date ON round(round_date);

COMMENT ON TABLE round IS 'Individual rounds within a tournament';

-- =====================================================
-- Table: TeeTime
-- =====================================================
CREATE TABLE tee_time (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tournament_id UUID NOT NULL REFERENCES tournament(id) ON DELETE CASCADE,
    round_id UUID NOT NULL REFERENCES round(id) ON DELETE CASCADE,
    tee_time TIMESTAMP WITH TIME ZONE NOT NULL,
    starting_hole INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_starting_hole CHECK (starting_hole >= 1 AND starting_hole <= 18)
);

CREATE INDEX idx_tee_time_round_time ON tee_time(round_id, tee_time);
CREATE INDEX idx_tee_time_tournament ON tee_time(tournament_id);

COMMENT ON TABLE tee_time IS 'Tee times (flights) for tournament rounds';
COMMENT ON COLUMN tee_time.starting_hole IS 'Starting hole number (1 for regular start, varies for shotgun)';

-- =====================================================
-- Table: FlightPlayer
-- =====================================================
CREATE TABLE flight_player (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tee_time_id UUID NOT NULL REFERENCES tee_time(id) ON DELETE CASCADE,
    player_id UUID NOT NULL REFERENCES player(id) ON DELETE CASCADE,
    position INTEGER NOT NULL,

    CONSTRAINT chk_flight_position CHECK (position >= 1 AND position <= 4)
);

CREATE UNIQUE INDEX idx_flight_player_tee_time_player ON flight_player(tee_time_id, player_id);
CREATE UNIQUE INDEX idx_flight_player_tee_time_position ON flight_player(tee_time_id, position);
CREATE INDEX idx_flight_player_player ON flight_player(player_id);

COMMENT ON TABLE flight_player IS 'Players assigned to specific tee times/flights';
COMMENT ON COLUMN flight_player.position IS 'Position in the flight (1-4 players per flight)';

-- =====================================================
-- Table: HoleScore
-- =====================================================
CREATE TABLE hole_score (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    round_id UUID NOT NULL REFERENCES round(id) ON DELETE CASCADE,
    player_id UUID NOT NULL REFERENCES player(id) ON DELETE CASCADE,
    hole_number INTEGER NOT NULL,
    strokes INTEGER NOT NULL,
    putts INTEGER,
    fairway_hit BOOLEAN,
    green_in_regulation BOOLEAN,
    penalty_strokes INTEGER NOT NULL DEFAULT 0,
    verified BOOLEAN NOT NULL DEFAULT FALSE,
    scorer_id UUID REFERENCES player(id),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_hole_score_hole_number CHECK (hole_number >= 1 AND hole_number <= 18),
    CONSTRAINT chk_hole_score_strokes CHECK (strokes >= 1 AND strokes <= 20),
    CONSTRAINT chk_hole_score_putts CHECK (putts IS NULL OR (putts >= 0 AND putts <= 10)),
    CONSTRAINT chk_hole_score_penalty CHECK (penalty_strokes >= 0 AND penalty_strokes <= 10)
);

CREATE UNIQUE INDEX idx_hole_score_round_player_hole ON hole_score(round_id, player_id, hole_number);
CREATE INDEX idx_hole_score_round_player ON hole_score(round_id, player_id);
CREATE INDEX idx_hole_score_player ON hole_score(player_id);
CREATE INDEX idx_hole_score_verified ON hole_score(verified) WHERE verified = FALSE;

COMMENT ON TABLE hole_score IS 'Individual hole scores with detailed statistics';
COMMENT ON COLUMN hole_score.verified IS 'Score has been verified by scorer or official';
COMMENT ON COLUMN hole_score.scorer_id IS 'Player or official who entered the score';

-- =====================================================
-- Table: Result
-- =====================================================
CREATE TABLE result (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tournament_id UUID NOT NULL REFERENCES tournament(id) ON DELETE CASCADE,
    player_id UUID NOT NULL REFERENCES player(id) ON DELETE CASCADE,
    division VARCHAR(50) NOT NULL,
    total_gross INTEGER NOT NULL,
    total_net INTEGER NOT NULL,
    total_points INTEGER,
    rank_overall INTEGER NOT NULL,
    rank_division INTEGER NOT NULL,
    prize_category VARCHAR(100),
    calculated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    verified BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT chk_result_total_gross CHECK (total_gross > 0),
    CONSTRAINT chk_result_total_net CHECK (total_net > 0),
    CONSTRAINT chk_result_ranks CHECK (rank_overall > 0 AND rank_division > 0)
);

CREATE UNIQUE INDEX idx_result_tournament_player ON result(tournament_id, player_id);
CREATE INDEX idx_result_tournament_overall_rank ON result(tournament_id, rank_overall);
CREATE INDEX idx_result_tournament_division_rank ON result(tournament_id, division, rank_division);

COMMENT ON TABLE result IS 'Calculated tournament results and rankings';
COMMENT ON COLUMN result.total_points IS 'Total points (for Stableford format, NULL for stroke play)';
COMMENT ON COLUMN result.verified IS 'Results have been officially verified';

-- =====================================================
-- Triggers for updated_at timestamps
-- =====================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_tournament_updated_at BEFORE UPDATE ON tournament
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_player_updated_at BEFORE UPDATE ON player
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_hole_score_updated_at BEFORE UPDATE ON hole_score
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- Initial Data Integrity Views
-- =====================================================

-- View: Current Player Handicaps
CREATE OR REPLACE VIEW v_current_player_handicaps AS
SELECT DISTINCT ON (player_id)
    player_id,
    handicap_index,
    effective_date,
    issuing_authority
FROM handicap_history
ORDER BY player_id, effective_date DESC;

COMMENT ON VIEW v_current_player_handicaps IS 'Current handicap index for each player (most recent effective date)';

-- View: Tournament Leaderboard (Stroke Play)
CREATE OR REPLACE VIEW v_tournament_leaderboard AS
SELECT
    r.tournament_id,
    r.player_id,
    p.first_name,
    p.last_name,
    r.division,
    r.total_gross,
    r.total_net,
    r.rank_overall,
    r.rank_division,
    r.verified
FROM result r
JOIN player p ON r.player_id = p.id
ORDER BY r.tournament_id, r.rank_overall;

COMMENT ON VIEW v_tournament_leaderboard IS 'Tournament leaderboard with player details';

-- =====================================================
-- Grant permissions (adjust as needed for your deployment)
-- =====================================================
-- Example: GRANT ALL ON ALL TABLES IN SCHEMA public TO gtms_app_user;
-- Example: GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO gtms_app_user;

-- End of migration
