import ollama
import sqlite3

class SolutionRecommendationAgent:
    def __init__(self, llm_model, db_connection):
        self.llm = llm_model
        self.db = db_connection

    def recommend_solution(self, query, category):
        """Recommends a solution based on historical tickets."""
        solutions = self.search_tickets(category)
        if solutions:
            prompt = f"Based on these past solutions: '{solutions}', what is the best solution for the query: '{query}'?"
        else:
            prompt = f"There are no similar past solutions. Provide a general troubleshooting solution for the query: '{query}'"
        try:
            response = self.llm.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
            recommendation = response["message"]["content"]
            return recommendation
        except ollama.exceptions.OllamaError as e:
            print(f"Error recommending solution: {e}")
            return "Solution unavailable."

    def search_tickets(self, category):
        """Queries the database for similar tickets."""
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT solution FROM tickets WHERE issue_category = ?", (category,))
            results = cursor.fetchall()
            return [row[0] for row in results]
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []