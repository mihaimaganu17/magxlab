DROP TABLE IF EXISTS samples;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS project_samples;

CREATE TABLE samples (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sha256 TEXT UNIQUE NOT NULL,
    file_type TEXT NOT NULL,
    added_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    disk_path TEXT NOT NULL
);

CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    db_disk_path TEXT NOT NULL,
    plugins_folder_path TEXT NOT NULL
);

CREATE TABLE project_samples (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id INTEGER,
    project_id INTEGER,
    FOREIGN KEY(sample_id) REFERENCES samples(id),
    FOREIGN KEY(project_id) REFERENCES projects(id)
);

