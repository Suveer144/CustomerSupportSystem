import ollama
import json
from agents.specialist_agent import SpecialistAgent  


class IntakeAgent:
    def __init__(self, llm_model):
        self.llm = llm_model

    def analyze_query(self, query):
        """Analyzes the customer query for sentiment, category, and priority."""
        prompt = f"Analyze this customer query: '{query}'. Provide sentiment, issue category, and priority in JSON format. The JSON should have keys: 'sentiment', 'category', and 'priority'. If the query does not contain enough information to determine the priority, set the priority to 'Medium'."
        try:
            response = self.llm.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
            analysis = response["message"]["content"]
            analysis_json = json.loads(analysis)
            sentiment = analysis_json.get("sentiment", "Neutral")
            category = analysis_json.get("category", "General")
            priority = analysis_json.get("priority", "Medium")
        except (json.JSONDecodeError, KeyError, ollama.exceptions.OllamaError) as e:
            print(f"Error analyzing query: {e}. Using default values.")
            sentiment = "Neutral"
            category = "General"
            priority = "Medium"
        return sentiment, category, priority

    def route_query(self, category, llm_model):
        """Routes the query to the appropriate specialist agent."""
        # Simple routing logic (can be made more sophisticated)
        if category == "Technical Support":
            return SpecialistAgent("Technical Support", llm_model)
        elif category == "Billing":
            return SpecialistAgent("Billing", llm_model)
        else:
            return SpecialistAgent("General Support", llm_model)