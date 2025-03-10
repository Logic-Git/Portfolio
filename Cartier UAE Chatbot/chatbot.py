import sys
from retrieval import query_knowledge
from google import genai
from config import GEMINI_API_KEY, MAX_RESULTS, CONVERSATION_HISTORY_LENGTH
import os
from colorama import init, Fore

# Initialize Gemini client for text generation.
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# Initialize colorama for Windows support
init()


class Chatbot:
    def __init__(self):
        self.history = []  # List of dicts with keys 'user' and 'agent'

    def get_recent_history(self, n=CONVERSATION_HISTORY_LENGTH):
        """
        Returns a formatted string of the last n conversation turns.
        Best practice: include the last CONVERSATION_HISTORY_LENGTH exchanges.
        """
        recent = self.history[-n:]
        history_text = ""
        for turn in recent:
            history_text += f"User: {turn['user']}\nAgent: {turn['agent']}\n"
        return history_text

    def enhance_query(self, query: str, history: str = "") -> str:
        """
        Enhance the user's query by correcting spelling, grammar, and completing incomplete sentences.
        Uses conversation history for better context understanding.
        """
        prompt = f"""
You are a query enhancement assistant for Cartier UAE customer service.
Your task is to optimize the customer query by:
1. Correcting spelling mistakes
2. Fixing grammar
3. Completing incomplete sentences
4. Using relevant context from the conversation history.

Overall, you are making a query for an RAG system. Your query will be vectorized to obtain matches.
Therefore, you should try to modify the user query as little as possible so as not to get the wrong information.
At the same time, you should try to include keywords (if in the context or wrongly spelled but in the query) that you think matching the relevant information in the vector database.
Also you should make sure the query complies with the above four points.

Previous Conversation Context:
{history}

Original Query: {query}

Enhanced Query:"""
        try:
            response = gemini_client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt
            )
            enhanced = response.text.strip()
            return enhanced
        except Exception as e:
            print(f"Error enhancing query: {e}")
            return query

    def summarize_context(self, history: str, query: str) -> str:
        """
        Summarize the conversation history and the current query as briefly as possible without losing essential context.
        """
        prompt = f"""
You are a summarization assistant for a Cartier UAE customer service chatbot.
Summarize the following conversation context and the current query concisely, ensuring no loss of important details.
Conversation History:
{history}

Current Query:
{query}

Summarized Context:"""
        try:
            response = gemini_client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt
            )
            summary = response.text.strip()
            return summary
        except Exception as e:
            print(f"Error summarizing context: {e}")
            return history

    def generate_answer(self, user_message: str):
        # Get conversation history for context
        conversation_history = self.get_recent_history(n=CONVERSATION_HISTORY_LENGTH)

        # Step 1: Enhance the incoming query with conversation context
        enhanced_query = self.enhance_query(user_message, history=conversation_history)

        # Step 2: Retrieve relevant context from the knowledge base using the enhanced query.
        retrieved_docs = query_knowledge(enhanced_query, n_results=MAX_RESULTS)
        if not retrieved_docs:
            answer = "I apologize, but I don't have access to the knowledge base yet. Please make sure to run 'python ingest_database.py' first to initialize the system with the product and policy information."
            self.history.append({"user": user_message, "agent": answer})
            return answer

        context_text = "\n\n".join(retrieved_docs)

        # Step 3: Summarize conversation context along with the enhanced query
        summarized_context = self.summarize_context(conversation_history, user_message)

        # Step 4: Construct the final prompt for answer generation using original user query
        final_prompt = f"""
You are a customer support assistant for Cartier UAE. Answer the customer's query using only the provided knowledge.
Do not rely on any external information.

Summarized Conversation Context:
{summarized_context}

Retrieved Knowledge:
{context_text}

Customer Query:
{user_message}

Also do the following:
If you think that the Customer Query is unrelated to Cartier UAE, tell the customer that you can only answer questions related to Cartier UAE.
If the Customer Query is related to Cartier UAE, but the answer is not in the retrieved knowledge, tell the customer that you do not have the information needed to answer their question.
If the Customer Query is just a regular greeting like Hello or Goodbye, respond appropriately and courteously.

Final Answer:"""

        try:
            response = gemini_client.models.generate_content(
                model="gemini-2.0-flash", contents=final_prompt
            )
            answer = response.text.strip()
        except Exception as e:
            answer = f"Error generating response: {e}"

        # Append the current turn to the conversation history.
        self.history.append({"user": user_message, "agent": answer})
        return answer


def main():
    bot = Chatbot()
    welcome_message = """Hi! I am the customer support Chatbot for Cartier UAE. You can ask me any questions about Cartier products available for online purchase or our policies regarding product purchases.

How may I assist you today? (Type 'exit' to end our conversation)
"""
    print(welcome_message)

    while True:
        user_input = input(f"{Fore.GREEN}You:{Fore.RESET} ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("Thank you for choosing Cartier UAE. Have a wonderful day!")
            sys.exit()
        answer = bot.generate_answer(user_input)
        print(f"{Fore.RED}Agent:{Fore.RESET} {answer}")


if __name__ == "__main__":
    main()
