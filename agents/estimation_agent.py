import ollama
import datetime

class ResolutionTimeEstimationAgent:
    def __init__(self, llm_model):
        self.llm = llm_model

    def estimate_resolution_time(self, ticket_details, historical_data):
        """Estimates the time to resolve a ticket."""

        prompt = f"Estimate the resolution time for a ticket with details: '{ticket_details}' based on historical data: '{historical_data}'. Provide the estimate in hours."
        try:
            response = self.llm.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
            estimate = response["message"]["content"]
            
            try:
                hours = int(estimate.split(' ')[0])  
                resolution_time = datetime.timedelta(hours=hours)
                return resolution_time
            except ValueError:
                print("Could not parse estimated time. Returning default.")
                return datetime.timedelta(hours=24) 
        except ollama.exceptions.OllamaError as e:
            print(f"Error estimating resolution time: {e}")
            return datetime.timedelta(hours=24)  # Default estimate

    def identify_potential_delays(self, ticket_progress):
        """Identifies potential delays in ticket resolution (placeholder)."""
        # This could involve analyzing ticket updates, agent workload, etc.
        if "waiting for customer response" in ticket_progress.lower():
            return "Potential delay: Waiting on customer input."
        else:
            return "No delays detected."