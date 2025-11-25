from pipeline import run_pipeline
from pathlib import Path

def main():

    # just opens all the parameters and loads them into the pipeline
    root = Path.cwd()
    params_path = root / "config" / "params.json"
    out_json = root / "outputs" / "results.json"

    run_id, out_path = run_pipeline(params_path, out_json)
    print("run " + str(run_id) + "complete")
    print("Results saved to " + str(out_path))

if __name__ == "__main__":
    main()
