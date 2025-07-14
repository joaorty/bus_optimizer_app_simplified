CREATE TABLE IF NOT EXISTS scenario (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_updated_at_scenario
BEFORE UPDATE ON scenario
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TABLE IF NOT EXISTS parameters(
  id SERIAL PRIMARY KEY,
  scenario_id INTEGER NOT NULL REFERENCES scenario(id) ON DELETE CASCADE,
  units_time INTEGER NOT NULL,
  wait_cost NUMERIC(6, 2) CHECK (wait_cost >= 0) NOT NULL,
  agglomeration_cost NUMERIC(6, 2) CHECK (agglomeration_cost >= 0) NOT NULL,
  acceptable_time_transfer INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS route(
  id SERIAL PRIMARY KEY,
  scenario_id INTEGER NOT NULL REFERENCES scenario(id) ON DELETE CASCADE,
  length_km NUMERIC(8,2) CHECK (length_km >= 0) NOT NULL,
  time_minutes INTEGER CHECK (time_minutes >= 0) NOT NULL,
  passengers INTEGER CHECK (passengers >= 0) NOT NULL
);

CREATE TABLE IF NOT EXISTS bus_type(
  id SERIAL PRIMARY KEY,
  scenario_id INTEGER NOT NULL REFERENCES scenario(id) ON DELETE CASCADE,
  seat_capacity INTEGER CHECK (seat_capacity > 0) NOT NULL,
  operational_cost_km NUMERIC(4, 2) CHECK (operational_cost_km >= 0) NOT NULL,
  load_factor NUMERIC(4, 2) CHECK (load_factor >= 1) NOT NULL,
  available_units INTEGER CHECK (available_units > 0) NOT NULL
);

CREATE TYPE solution_status AS ENUM ('Pending', 'Running', 'Completed', 'Failed');

CREATE TABLE IF NOT EXISTS solution(
  id SERIAL PRIMARY KEY,
  scenario_id INTEGER NOT NULL REFERENCES scenario(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  status solution_status NOT NULL DEFAULT 'Pending',
  objective_value NUMERIC(15, 2),
  solution_data JSONB,
  parameters_solution JSONB
);

CREATE TRIGGER trigger_update_updated_at_solution
BEFORE UPDATE ON solution
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE INDEX idx_parameters_scenario_id ON parameters(scenario_id);
CREATE INDEX idx_route_scenario_id ON route(scenario_id);
CREATE INDEX idx_bus_type_scenario_id ON bus_type(scenario_id);
CREATE INDEX idx_solution_scenario_id ON solution(scenario_id);