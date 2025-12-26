import json
from .llmclient import call_llm

def analyze_costs(profile_path: str, billing_path: str, output_path: str):
    """
    Analyzes billing data against the project profile and generates recommendations.
    """
    try:
        with open(profile_path, 'r') as f:
            profile = json.load(f)
        with open(billing_path, 'r') as f:
            billing_data = json.load(f)
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        return

  
    prompt=[
        {
            "role": "system",
            "content": (
                "You are a cloud cost optimization expert.\n\n"
                "Your task is to analyze cloud billing data and generate a cost "
                "optimization report.\n\n"
                "STRICT RULES:\n"
                "- Output ONLY valid JSON (no markdown, no explanations)\n"
                "- Use the billing data to infer realistic costs\n"
                "- Provide 6–10 recommendations\n"
                "- Recommendations must include AWS, Azure, GCP, and open-source/free-tier options\n"
                "- Some recommendations MUST suggest open-source alternatives\n"
                "- Include risks, effort, and potential savings\n\n"
                "Output JSON structure:\n"
                "{\n"
                '  "project_name": string,\n'
                '  "analysis": {\n'
                '    "total_monthly_cost": number,\n'
                '    "budget": number,\n'
                '    "budget_variance": number,\n'
                '    "service_costs": { string: number },\n'
                '    "high_cost_services": { string: number },\n'
                '    "is_over_budget": boolean\n'
                '  },\n'
                '  "recommendations": [\n'
                '    {\n'
                '      "title": string,\n'
                '      "service": string,\n'
                '      "current_cost": number,\n'
                '      "potential_savings": number,\n'
                '      "recommendation_type": string,\n'
                '      "description": string,\n'
                '      "implementation_effort": "low|medium|high",\n'
                '      "risk_level": "low|medium|high",\n'
                '      "steps": string[],\n'
                '      "cloud_providers": string[]\n'
                '    }\n'
                '  ],\n'
                '  "summary": {\n'
                '    "total_potential_savings": number,\n'
                '    "savings_percentage": number,\n'
                '    "recommendations_count": number,\n'
                '    "high_impact_recommendations": number\n'
                '  }\n'
                "}"
            ),
        },
        {
            "role": "user",
            "content": (
                "Project profile:\n"
                f"{json.dumps(profile, indent=2)}\n\n"
                "Billing data:\n"
                f"{json.dumps(billing_data, indent=2)}\n\n"
                "Generate the cost optimization report."
            ),
        },
    ]

    print("Analyzing costs and generating recommendations...")
    try:
        response_message = call_llm(prompt)
        response_content = response_message.content
        
        # Parse the JSON string to ensure validity before saving
        data = json.loads(response_content)

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
            
        print(f"Analysis saved to {output_path}")
        return data
        
    except Exception as e:
        print(f"Error analyzing costs: {e}")
        return None

if __name__ == "__main__":
    # Create a dummy description file for testing if needed, or just handle gracefully
    profile_path = "project_profile.json"
    billing_path = "project_billing.json"
    output_file = "project_analysis.json"
    analyze_costs(profile_path, billing_path, output_file)
