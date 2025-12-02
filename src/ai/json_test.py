from google import genai
import os
import json
from pathlib import Path

def main():
    # Load your params.json
    params_path = Path.cwd() / "config" / "params.json"
    params = json.loads(params_path.read_text())

    # enables my key and then sets up a prompt to parse my inputs json 
    # and export a outputs json 
    # currently the prompt is letting the llm see the json of the inputs 
    # and giving back a file based on what it takes from it, now i just need
    # to implement the hypothesis which shouldnt be too bad
    client = genai.Client(api_key="AIzaSyBRJlfZqcNpwIs5L_iKimUMIo9fED0uzLw")
    prompt = (
        f"""
    You are a JSON-only AI. Respond ONLY with valid JSON.

    Here is a config file:
    {json.dumps(params, indent=2)}

    Output a JSON with this structure:
    {{
    "summary": "...",
    "recommendations": ["...", "..."]
    }}

    No extra text.
    """
    )

    # makes sure the response contains a json
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    # creates a json file and prints out the content to the terminal
    result_json = json.loads(response.text)
    print(json.dumps(result_json, indent=2))

    # outputs the json file to the outputs folder
    out_path = Path.cwd() / "outputs" / "params_llm_analysis.json"
    out_path.write_text(json.dumps(result_json, indent=2))
    print("Saved analysis JSON to:", out_path)

if __name__ == "__main__":
    main()
