import json
from pathlib import Path
from engine import euler_integrator
from storage import create_run, insert_result, export_run_to_json


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
    
def run_pipeline(physics_path: Path, algo_path: Path, inputs_path: Path, out_json_path: Path):
    physics = load_json(physics_path)
    algo    = load_json(algo_path)
    inputs  = load_json(inputs_path)

    # creating variables from the inputs json file 
    # This was the psudo coded idea i started with
    # pos = inputs_path["initial_position"]
    # vel = inputs_path["initial_velocity"]
    # steps = physics_path["steps"]
    # save_every = algo_path["save_every_n"]

    mass        = float(physics["mass"])
    drag_coeff  = float(physics["drag_coefficient"])
    dt          = float(physics["time_step"])
    steps       = int(physics["steps"])
    save_every  = int(algo["save_every_n"])
    run_tag     = str(algo["run_tag"])
    pos = [float(inputs["initial_position"][0]), float(inputs["initial_position"][1])]
    vel = [float(inputs["initial_velocity"][0]), float(inputs["initial_velocity"][1])]
    gravity = [float(inputs["gravity"][0]), float(inputs["gravity"][1])]

    run_id = create_run(run_tag)

    # the simulation loop that inserts results to the database for each iteration
    for step in range(steps + 1):
        if(step % save_every == 0):
            insert_result(run_id, step, pos[0], pos[1], vel[0], vel[1])
        if(step < steps):
            pos, vel = euler_integrator(pos, vel, dt, gravity, mass, drag_coeff)

    # output to a json file
    export_run_to_json(run_id, out_json_path)
    return(run_id, out_json_path)


