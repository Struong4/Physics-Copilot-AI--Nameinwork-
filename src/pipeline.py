import json
from pathlib import Path
import numpy as np
from engine import euler_integrator
from storage import create_run, insert_result, export_run_to_json, find_run_by_config


# next task, get data from the database to retreive and combine json files
# make sure to search everytime incase we know the information already 
# so we check everything in the database incase it already exists for faster results

# pipeline is the connector that brings together the inputs, the engine,
# then computes and stores the data in the storage and outputs it in a json
# file to see results.

# make a heiractical json that seperates algo params as a key and have the physics as changeable
# as the other key, so put it togehter for one json config file
def load_json(path: Path):
    if not path.exists():
        raise FileNotFoundError("Missing file: " + str(path))
    else:
        # reads the json file and turns it into a python dictionary
        return json.loads(path.read_text())
    
def run_pipeline(params_path: Path, out_json_path: Path):
    params = load_json(params_path)
    algo = params["algorithm"]
    physics = params["physics"]
    inputs = params["inputs"]

    # ignores the run tag to make sure it doesn't take it into account
    algo_for_cache = {k: v for k, v in algo.items() if k != "run_tag"}

    # builds config dict for caching
    config = {
        "algorithm": algo_for_cache,
        "physics": physics,
        "inputs": inputs,
    }

    # calls on find run by config to see if this current config file
    # has already been used already
    existing_run_id = find_run_by_config(config)

    # if it was able to be found in the database, then we already have the results
    # so it just gives back the results that we already had access to
    if existing_run_id is not None:
        print("Reusing existing run" + str(existing_run_id) + "for this config")
        export_run_to_json(existing_run_id, out_json_path)
        return existing_run_id, out_json_path

   
    # loading in data and creating numpy arrays for the data
    mass        = float(physics["mass"])
    drag_coeff  = float(physics["drag_coefficient"])
    dt          = float(physics["time_step"])
    steps       = int(physics["steps"])
    save_every  = int(algo["save_every_n"])
    run_tag     = str(algo["run_tag"])
    pos         = np.array(inputs["initial_position"], dtype=float)
    vel         = np.array(inputs["initial_velocity"], dtype=float)
    gravity     = np.array(inputs["gravity"], dtype=float)

    run_id = create_run(run_tag, config)

    # the simulation loop that inserts results to the database for each iteration
    for step in range(steps + 1):
        if(step % save_every == 0):
            insert_result(run_id, step, float(pos[0]), float(pos[1]), float(vel[0]), float(vel[1]))
        if(step < steps):
            pos, vel = euler_integrator(pos, vel, dt, gravity, mass, drag_coeff)

    # output to a json file
    export_run_to_json(run_id, out_json_path)
    return(run_id, out_json_path)


