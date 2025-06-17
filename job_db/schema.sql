CREATE TABLE job_profiles (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  skills TEXT[] NOT NULL,
  experience_level VARCHAR(100)
);
