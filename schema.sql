-- Catbuild360 database schema (SQLite)
CREATE TABLE IF NOT EXISTS gallery (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  category TEXT NOT NULL,          -- plans | elevations | interiors | stages | finishes | completed | pooja
  title TEXT NOT NULL,
  image TEXT NOT NULL,
  sort_order INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS packages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  rate_per_sqft INTEGER NOT NULL,
  image TEXT,
  items TEXT NOT NULL              -- JSON array of strings
);
CREATE TABLE IF NOT EXISTS specs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  section TEXT NOT NULL,
  items TEXT NOT NULL              -- JSON array of strings
);
CREATE TABLE IF NOT EXISTS enquiries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  phone TEXT NOT NULL,
  package TEXT,
  message TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
