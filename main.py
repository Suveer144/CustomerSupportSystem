import ollama
import sqlite3
import time  

from agents.intake_agent import IntakeAgent
from agents.summary_agent import ConversationSummaryAgent
from agents.solution_agent import SolutionRecommendationAgent
from agents.routing_agent import TaskRoutingAgent
from agents.estimation_agent import ResolutionTimeEstimationAgent
from agents.specialist_agent import SpecialistAgent
from utils.data_loader import load_conversation_data

def stream_response(llm_model, prompt):
    """Streams the LLM's response and prints it to the console."""

    stream = llm_model.chat(model="mistral", messages=[{"role": "user", "content": prompt}], stream=True)
    for part in stream:
        yield part['message']['content']

def main():
    
    ollama.pull("mistral")  
    llm_model = ollama

   
    intake_agent = IntakeAgent(llm_model)
    summary_agent = ConversationSummaryAgent(llm_model)
    
    db_conn = sqlite3.connect('db/ticket_data.db')
    solution_agent = SolutionRecommendationAgent(llm_model, db_conn)
    routing_agent = TaskRoutingAgent()
   
    introduction = "Hello, I am your GenAI support assistant. I am trained to provide accurate and helpful answers to your questions. Please provide your query, and I will do my best to assist you. Type 'exit' to end the chat.\n"
    print(introduction)

    conversation_history = []  

    while True:  
        user_input = input("Customer: ")
        if user_input.lower() == "exit":
            print("Thank you for using our support system!")
            break

        customer_query = user_input
        conversation_history.append(f"Customer: {customer_query}")

        sentiment, category, priority = intake_agent.analyze_query(customer_query)
        print(f"Sentiment: {sentiment}, Category: {category}, Priority: {priority}", flush=True)

        specialist_agent = intake_agent.route_query(category, llm_model)

        print("Agent: Please wait while I prepare a response...", flush=True) 
        time.sleep(1) 

        response = ""
        for chunk in stream_response(llm_model, f"{customer_query}\n" + "\n".join(conversation_history)):
            response += chunk
            print(chunk, end="", flush=True)  
        print("\n")  

        conversation_history.append(f"Agent: {response}")

    db_conn.close()

if __name__ == "__main__":
    main()