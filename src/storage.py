import sqlite3 # built in library for pythons databases
import json
from pathlib import Path

# run code like this python src/main.py in the big folder
# runs sqlite in the root of the current working directory
ROOT = Path.cwd()
DB_PATH = ROOT / "db" / "runs.sqlite"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# my db file exists so do not need this line, but if running off fresh state will create directory
# DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_connection():

    # command to open the sqlite file in db directory
    conn = sqlite3.connect(DB_PATH)

    # Table for the metadata of each simulation run
    # creates a run table that logs the id that automaticaly increments
    # shows the run tag in the algo param json, and the date it was crated
    # adding a new section for caching the data
    conn.execute("""
        CREATE TABLE IF NOT EXISTS runs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_tag TEXT NOT NULL,
            config_json TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Table for the saved simulation results, shows the id if the specifc run that
    # correlates with the id in runs table, then shows the output variables that
    # would be shown in the results json as well.

    conn.execute("""
        CREATE TABLE IF NOT EXISTS results(
            run_id INTEGER NOT NULL,
            step INTEGER NOT NULL,
            x REAL,
            y REAL,
            vx REAL,
            vy REAL,
            FOREIGN KEY(run_id) REFERENCES runs(id)
        )
    """)

    # Useful indexes for faster lookups that help when looking up specific run occurance
    conn.execute("CREATE INDEX IF NOT EXISTS idx_runs_tag ON runs(run_tag)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_results_run_step ON results(run_id, step)")

    return conn

def find_run_by_config(config_dict):
    # the parameter added would be the params.json file, and will go through the
    # config_json table and if a previous file matches, it will just run the same config
    # by memory to save time, if not itll just run as normal
    config_json = json.dumps(config_dict, sort_keys=True)
    with get_connection() as conn:
        row = conn.execute("SELECT id FROM runs WHERE config_json = ? LIMIT 1", (config_json,)).fetchone()
    if row is None:
        return None
    return row[0]
    

def create_run(run_tag, config_dict):
    # after each simulation, stores that specfic simulation into 
    # a table with each existing simulation for memory
    # makes sure connection is properly committed like a HTTP OK 
    # and inserts a new row for the speicfic run in the runs table
    config_json = json.dumps(config_dict, sort_keys=True)
    with get_connection() as conn:
        cur = conn.execute("INSERT INTO runs(run_tag, config_json) VALUES (?, ?)", (run_tag, config_json))
        return cur.lastrowid

def insert_result(run_id, step, x, y, vx, vy):
    # inserts one step of the simulation into the results table
    # inserts a row of each output in the results table
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO results(run_id, step, x, y, vx, vy) VALUES (?, ?, ?, ?, ?, ?)",
            (run_id, step, x, y, vx, vy)
        )

def export_run_to_json(run_id, out_path: Path):
    # Export all results of a run into a JSON file
    # this code gets all the info from the run row spefiic to the run
    with get_connection() as conn:
        run_row = conn.execute(
            "SELECT id, run_tag, created_at FROM runs WHERE id=?",
            (run_id,)
        ).fetchone()

        #this code gets every row from each output from each step like the results table
        rows = conn.execute(
            "SELECT step, x, y, vx, vy FROM results WHERE run_id=? ORDER BY step",
            (run_id,)
        ).fetchall()

    # creates a JSON payload that just turns the each output from each row in the database
    # into the results json for it to be read and given back to user 
    payload = {
        "run": {
            "id": run_row[0],
            "run_tag": run_row[1],
            "created_at": run_row[2]
        },
        "results": [
            {
                "step": r[0],
                "x": r[1],
                "y": r[2],
                "vx": r[3],
                "vy": r[4]
            }
            for r in rows
        ]
    }

    # checks if outputs folder exists and writes to the results.json file
    # of everything that was taken from the payload 
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2))

    # change everything into numpy for practice