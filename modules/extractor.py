import json
from .llmclient import call_llm

def extract_project_profile(description_path: str, output_path: str):
    """
    Reads the project description, calls the LLM to extract the profile,
    and saves the result to a JSON file.
    """
    try:
        with open(description_path, 'r') as f:
            description = f.read()
    except FileNotFoundError:
        print(f"Error: Description file not found at {description_path}")
        return

    prompt = [
    {
        "role": "system",
        "content": (
            "You are a strict JSON generator that converts a Product Requirements Document (PRD) "
            "written in plain English into a structured JSON specification.\n\n"

            "RULES:\n"
            "- Output ONLY valid JSON.\n"
            "- Do NOT include markdown, comments, explanations, or extra text.\n"
            "- The output MUST match the schema exactly.\n"
            "- Use concise, concrete language. No buzzwords.\n"
            "- Infer reasonable technical choices from the PRD when not explicitly stated.\n"
            "- If a value cannot be inferred, use null (not empty strings).\n"
            "- Do not invent features not implied by the PRD.\n\n"

            "SCHEMA:\n"
            "{\n"
            '  "name": string,\n'
            '  "budget_inr_per_month": number | null,\n'
            '  "description": string,\n'
            '  "tech_stack": {\n'
            '    "frontend": string | null,\n'
            '    "backend": string | null,\n'
            '    "database": string | null,\n'
            '    "proxy": string | null,\n'
            '    "hosting": string | null\n'
            '  },\n'
            '  "non_functional_requirements": string[]\n'
            "}\n\n"

            "FIELD GUIDELINES:\n"
            "- name: Short product name (2–5 words).\n"
            "- budget_inr_per_month: Monthly infrastructure + tooling cost estimate.\n"
            "- description: 1–2 sentence summary of what the product does.\n"
            "- tech_stack: Prefer common, production-ready tools.\n"
            "- non_functional_requirements: Short, clear requirements (e.g., 'Low latency', 'High availability')."
        ),
    },
    {
        "role": "user",
        "content": description,
    },
]


    print("Extracting project profile...")
    try:
        response_message = call_llm(prompt)
        response_content = response_message.content
        
        # Parse the JSON string to ensure validity before saving
        data = json.loads(response_content)

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
            
        print(f"Profile saved to {output_path}")
        return data
        
    except Exception as e:
        print(f"Error extracting profile: {e}")
        return None


