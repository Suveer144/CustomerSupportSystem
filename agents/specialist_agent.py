import ollama

class SpecialistAgent:
    def __init__(self, specialization, llm_model):
        """Initializes the SpecialistAgent."""
        self.specialization = specialization
        self.llm = llm_model

    def handle_query(self, query, conversation_history=""):
        """Handles a customer query."""
        prompt = f"You are a customer support agent specializing in {self.specialization}. Respond to the following customer query: '{query}'. {conversation_history}"
        try:
            response = self.llm.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
            return response["message"]["content"]
        except ollama.exceptions.OllamaError as e:
            print(f"Error handling query: {e}")
            return "I am experiencing difficulties. Please wait."

    def escalate_issue(self, issue_description, routing_agent):
        """Escalates an issue to another team."""
        return routing_agent.route_task(issue_description, self.specialization)

    def request_solution(self, query, solution_agent):
        """Requests a solution from the SolutionRecommendationAgent."""
        return solution_agent.recommend_solution(query, self.specialization)