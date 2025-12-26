import os
import sys
import json
from modules.extractor import extract_project_profile
from modules.billing import generate_mock_billing
from modules.analyzer import analyze_costs

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
DESCRIPTION_FILE = os.path.join(DATA_DIR, 'project_description.txt')
PROFILE_FILE = os.path.join(DATA_DIR, 'project_profile.json')
BILLING_FILE = os.path.join(DATA_DIR, 'mock_billing.json')
REPORT_FILE = os.path.join(DATA_DIR, 'cost_optimization_report.json')

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("=========================================")
    print("      AI Cloud Cost Optimizer CLI        ")
    print("=========================================")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def input_description():
    ensure_data_dir()
    print("\n--- Enter Project Description ---")
    print("Type your project description below. Press Ctrl+Z (Win) then Enter to finish:")
    try:
        lines = sys.stdin.read()
        if lines.strip():
            with open(DESCRIPTION_FILE, 'w') as f:
                f.write(lines)
            print(f"\nDescription saved to {DESCRIPTION_FILE}")
            
            # Auto-run extraction
            print("Extracting profile...")
            extract_project_profile(DESCRIPTION_FILE, PROFILE_FILE)
        else:
            print("\nNo input provided.")
    except Exception as e:
        print(f"\nError saving description: {e}")

def run_analysis():
    ensure_data_dir()
    print("\n--- Running Complete Cost Analysis ---")
    
    if not os.path.exists(DESCRIPTION_FILE):
        print(f"Error: {DESCRIPTION_FILE} not found. Please enter a description first.")
        return

    # Step 1: Extract Profile (if not already fresher than description?) 
    # For now, just re-run to be safe or check headers. Let's re-run strictly if missing.
    if not os.path.exists(PROFILE_FILE):
         print("Generating Project Profile...")
         if not extract_project_profile(DESCRIPTION_FILE, PROFILE_FILE):
             return

    # Step 2: Generate Billing
    print("\nGenerating Synthetic Billing Data...")
    if not generate_mock_billing(PROFILE_FILE, BILLING_FILE):
        return

    # Step 3: Analyze
    print("\nAnalyzing Costs & Generating Recommendations...")
    if not analyze_costs(PROFILE_FILE, BILLING_FILE, REPORT_FILE):
        return

    print("\nAnalysis Complete! Report generated.")

def view_recommendations():
    print("\n--- Recommendations ---")
    if not os.path.exists(REPORT_FILE):
        print("No report found. Please run the analysis first.")
        return

    try:
        with open(REPORT_FILE, 'r') as f:
            report = json.load(f)
        
        print(f"Project: {report.get('project_name')}")
        analysis = report.get('analysis', {})
        print(f"Total Cost: {analysis.get('total_monthly_cost')} INR (Budget: {analysis.get('budget')} INR)")
        print(f"Variance: {analysis.get('budget_variance')} INR")
        print("\nTop Recommendations:")
        
        recs = report.get('recommendations', [])
        for i, rec in enumerate(recs, 1):
            print(f"{i}. {rec.get('title')} ({rec.get('service')})")
            print(f"   Savings: {rec.get('potential_savings')} INR | Type: {rec.get('recommendation_type')}")
            print(f"   Provider Options: {', '.join(rec.get('cloud_providers', []))}")
            print("-" * 30)
            
    except Exception as e:
        print(f"Error reading report: {e}")

def export_report():
    print("\n--- Export Report ---")
    if not os.path.exists(REPORT_FILE):
        print("No report found to export.")
        return
    
    print(f"Report is available at: {REPORT_FILE}")
    print("You can copy this individual file or view it directly.")

def main():
    while True:
        # clear_screen() # Optional: keep history visible might be better for debugging
        print_header()
        print("1. Enter New Project Description")
        print("2. Run Complete Cost Analysis")
        print("3. View Recommendations")
        print("4. Export Report")
        print("5. Exit")
        
        choice = input("\nSelect an option (1-5): ")
        
        if choice == '1':
            input_description()
        elif choice == '2':
            run_analysis()
        elif choice == '3':
            view_recommendations()
        elif choice == '4':
            export_report()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
