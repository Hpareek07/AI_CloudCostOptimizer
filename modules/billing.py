import json
from .llmclient import call_llm

def generate_mock_billing(profile_path: str, output_path: str):
    """
    Generates synthetic billing data based on the project profile.
    """
    try:
        with open(profile_path, 'r') as f:
            profile = json.load(f)
    except FileNotFoundError:
        print(f"Error: Profile file not found at {profile_path}")
        return

    project_name = profile.get("name", "Project")
    hosting_provider = profile.get("tech_stack", {}).get("hosting", "AWS")
    budget = profile.get("budget_inr_per_month", 5000)

    prompt=[
        {
            "role": "system",
            "content": (
                "You are a cloud billing simulator.\n"
                "Generate realistic, synthetic monthly cloud billing data.\n\n"
                "Rules:\n"
                "- Output ONLY valid JSON (no markdown, no explanation)\n"
                "- Output an array of 12–20 records\n"
                "- Distribute costs across compute, database, storage, networking, monitoring\n"
                "- Cloud-agnostic but realistic\n"
                "- Use realistic regions, usage units, and descriptions\n\n"
                "Each record MUST contain:\n"
                "month, service, resource_id, region, usage_type,\n"
                "usage_quantity, unit, cost_inr, desc"
            ),
        },
        {
            "role": "user",
            "content": (
                "Project profile:\n"
                f"{json.dumps(profile, indent=2)}\n\n"
                "Generate mock billing data for one month."
            ),
        },
    ]

    print("Generating synthetic billing data...")
    try:
        response_message = call_llm(prompt)
        response_content = response_message.content
        
        # Parse the JSON string to ensure validity before saving
        data = json.loads(response_content)

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
            
        print(f"Billing saved to {output_path}")
        return data
        
    except Exception as e:
        print(f"Error extracting profile: {e}")
        return None

if __name__ == "__main__":
    # Create a dummy description file for testing if needed, or just handle gracefully
    output_file = "project_billing.json"
    profile_path= "project_profile.json"
    generate_mock_billing(profile_path, output_file)