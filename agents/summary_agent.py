import ollama

class ConversationSummaryAgent:
    def __init__(self, llm_model):
        self.llm = llm_model

    def summarize_conversation(self, conversation_history):
        """Summarizes the customer support conversation."""
        prompt = f"Summarize this customer support conversation: '{conversation_history}'. Extract key information and action items."
        try:
            response = self.llm.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
            summary = response["message"]["content"]
            return summary
        except ollama.exceptions.OllamaError as e:
            print(f"Error summarizing conversation: {e}")
            return "Summary unavailable."