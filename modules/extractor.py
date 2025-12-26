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
                "You are a JSON-only generator. "
                "Return ONLY valid JSON. "
                "Do not include explanations or markdown.\n\n"
                "JSON format:\n"
                "{"
                '"name": string,'
                '"budget_inr_per_month": number,'
                '"description": string,'
                '"tech_stack": {'
                    '"frontend": string,'
                    '"backend": string,'
                    '"database": string,'
                    '"proxy": string,'
                    '"hosting": string'
                '},'
                '"non_functional_requirements": string[]'
                "}"
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


