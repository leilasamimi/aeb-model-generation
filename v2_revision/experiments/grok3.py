import os
import json
import time
import csv
import httpx
from pathlib import Path
from dotenv import load_dotenv
from tqdm import tqdm
import random

# -------------------------------------------------
# Configuration
# -------------------------------------------------
load_dotenv()
AVALAI_API_KEY="Enter your api key from avalai"

AVALAI_ENDPOINT = "https://api.avalai.ir/v1/chat/completions"

MAX_TOKENS = 4096


MODELS = {
    "grok3": "grok-3",
    
}


BASE_DIR = Path(__file__).resolve().parent.parent
PROMPT_FILE = BASE_DIR / "prompts" / "base_prompt.txt"
SCENARIO_FILE = BASE_DIR / "scenarios" / "scenarios.json"
RESULTS_DIR = BASE_DIR / "results"

# -------------------------------------------------
# Helpers
# -------------------------------------------------
def load_prompt():
    return PROMPT_FILE.read_text(encoding="utf-8")

def load_scenarios():
    with open(SCENARIO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def call_avalai(model_name, prompt_text, api_key, max_retries=5):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": prompt_text}
        ],
        "max_tokens": MAX_TOKENS
    }

    for attempt in range(max_retries):
        try:
            with httpx.Client(timeout=120.0) as client:
                response = client.post(
                    "https://api.avalai.ir/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                return response.json()

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"Rate limit hit. Retrying in {wait_time:.1f}s...")
                time.sleep(wait_time)
            else:
                raise

    #raise RuntimeError("Max retries exceeded due to rate limiting")
    time.sleep(5)
    print("Max retries exceeded due to rate limiting")
    return None


def extract_xmi(text):
    start = text.find("<aEBsystem:AEBSystem")
    end = text.find("</aEBsystem:AEBSystem>")
    if start != -1 and end != -1:
        return text[start:end + len("</aEBsystem:AEBSystem>")]
    return None


# -------------------------------------------------
# Main
# -------------------------------------------------
def main():
    load_dotenv()
    #api_key = os.getenv("AVALAI_API_KEY")

    #if not api_key:
    #    raise RuntimeError("AVALAI_API_KEY not found in environment")
    api_key = AVALAI_API_KEY
    if not api_key:
        raise RuntimeError("AVALAI_API_KEY is empty")
    prompt_base = load_prompt()
    scenarios = load_scenarios()

    RESULTS_DIR.mkdir(exist_ok=True)

    summary_rows = []

    for model_id, model_name in MODELS.items():
        model_dir = RESULTS_DIR / model_id
        model_dir.mkdir(exist_ok=True)

        print(f"\nRunning model: {model_name}")

        for scenario in tqdm(scenarios):
            scenario_id = scenario["id"]
            requirement = scenario["requirement"]

            full_prompt = (
                prompt_base
                + "\n\nNew Requirement:\n"
                + requirement
                + "\n\nGenerate the XMI model compliant with the AEB metamodel."
            )

            start_time = time.time()
            result = call_avalai(model_name, full_prompt, api_key)
            if result is None:
                summary_rows.append({
                    "model": model_name,
                    "scenario": scenario_id,
                    "time_sec": None,
                    "valid_xmi": False})
                continue
            elapsed = time.time() - start_time

            # Extract text
            text_output = result["choices"][0]["message"]["content"]



            raw_file = model_dir / f"{scenario_id}_raw.txt"
            raw_file.write_text(text_output, encoding="utf-8")

            xmi = extract_xmi(text_output)
            valid_xmi = xmi is not None

            if valid_xmi:
                xmi_file = model_dir / f"{scenario_id}.xmi"
                xmi_file.write_text(xmi, encoding="utf-8")

            summary_rows.append({
                "model": model_name,
                "scenario": scenario_id,
                "time_sec": round(elapsed, 2),
                "valid_xmi": valid_xmi
            })

    summary_file = RESULTS_DIR / "run_summary.csv"
    with open(summary_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["model", "scenario", "time_sec", "valid_xmi"]
        )
        writer.writeheader()
        writer.writerows(summary_rows)

    print("\nAll runs completed.")
    print(f"Summary written to {summary_file}")

if __name__ == "__main__":
    main()
