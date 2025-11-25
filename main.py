from pipeline import run_pipeline
from pathlib import Path

def main():

    # just opens all the parameters and loads them into the pipeline
    root = Path.cwd()
    physics_path = root / "config" / "phys_param.json"
    algo_path    = root / "config" / "algo_param.json"
    inputs_path  = root / "data"   / "inputs.json"
    out_json     = root / "outputs" / "results.json"

    run_id, out_path = run_pipeline(physics_path, algo_path, inputs_path, out_json)
    print("run " + str(run_id) + "complete")
    print("Results saved to " + str(out_path))

if __name__ == "__main__":
    main()
