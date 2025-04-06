import os

def load_conversation_data(directory):
    """Loads conversation data from text files in a directory."""
    conversations = {}
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # Extract Conversation ID from filename (assuming filename is like "TECH_001.txt")
                    conversation_id = os.path.splitext(filename)[0]
                    conversations[conversation_id] = content
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return conversations

if __name__ == '__main__':
    data_dir = 'data'
    conversations = load_conversation_data(data_dir)
    for cid, content in conversations.items():
        print(f"Conversation ID: {cid}\n{content}\n{'-'*40}")