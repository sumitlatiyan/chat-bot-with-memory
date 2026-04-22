LANGGRAPH CHATBOT
=================

A conversational chatbot built using LangGraph that supports
multi-turn conversations, multiple parallel chat threads, and
in-memory state persistence using thread IDs.

The chatbot allows users to start new chats, continue previous chats,
and ask follow-up questions while preserving conversation context.


WHAT THIS CHATBOT CAN DO
------------------------
- Answer user queries using an LLM
- Maintain conversation context across multiple turns
- Support multiple chat threads simultaneously
- Allow switching between old and new conversations
- Keep previous chats intact while starting new ones
- Use in-memory state storage keyed by thread ID


STEPS TO USE
------------
1. Open the hosted web application if deployed
   OR run locally using:
      streamlit run filename.py

2. Type your query in the input box and press Enter

3. Ask follow-up questions — context is preserved

4. Click "New Chat" to start a fresh conversation
   (old chats remain available in the sidebar)

5. Switch between past conversations using the sidebar


HIGH-LEVEL FLOW
---------------
1. When the user sends their first message:
   - A unique Thread ID is generated
   - The message is sent to the LLM
   - Both Human and AI messages are stored using annotations
   - Messages are saved in session state

2. Conversation state is stored using an in-memory saver:
   - Data is stored in RAM only
   - Each conversation is keyed by Thread ID

3. When a new chat is started:
   - A new Thread ID is created
   - Session state is reset
   - Previous conversations remain untouched

4. When an old chat is selected:
   - chatbot.get_state() is called using the Thread ID
   - Stored messages are converted into Streamlit format
   - Full conversation history is displayed to the user


ARCHITECTURE OVERVIEW
---------------------
User Input
   |
   v
Streamlit UI
   |
   v
LangGraph StateGraph
   |
   v
Chat Node (LLM Invocation)
   |
   v
In-Memory Checkpointer (Thread-based state)
   |
   v
Updated Conversation State


TECH STACK
----------
- Language: Python
- UI Framework: Streamlit
- Conversational Framework: LangGraph
- LLM:
  - Groq (LLaMA 3.1 8B Instant)
- State Persistence:
  - InMemorySaver (RAM-based, thread-keyed)


KEY LANGGRAPH CONCEPTS USED
---------------------------
- StateGraph:
  Defines the chatbot workflow as graph nodes

- START → chat_node → END:
  Simple single-node conversational flow

- add_messages annotation:
  Ensures new messages are appended, not overwritten

- InMemorySaver:
  Stores conversation state per thread ID in RAM


CHAT STATE STRUCTURE
-------------------
messages:
- List of HumanMessage and AIMessage objects
- Automatically appended on every interaction


SESSION MANAGEMENT (STREAMLIT)
------------------------------
- thread_id:
  Unique identifier for each conversation

- message_history:
  Streamlit-friendly history of chat messages

- chat_threads:
  List of all thread IDs created during the session

- New Chat:
  Generates a new thread ID and resets current session state


PREREQUISITES
-------------
- Python 3.9+
- Streamlit installed
- Groq API key


ENVIRONMENT SETUP
-----------------
Create a file named Constants.py:

GROQ_API_KEY = "your_groq_api_key"

Set environment variable automatically when app starts.


INSTALLATION
------------
pip install streamlit langgraph langchain langchain-groq


HOW TO RUN
----------
streamlit run filename.py


LIMITATIONS
-----------
- Conversation state is stored only in memory (RAM)
- State is lost if application restarts
- Not suitable for long-term persistence without external storage
- Single-user session focused (multi-user needs DB)


FUTURE IMPROVEMENTS
-------------------
- Persistent storage (Redis / SQLite / Postgres)
- Multi-user authentication
- LangGraph multi-node workflows
- Tool calling and function execution
- Memory summarization for long chats


WHY THIS PROJECT MATTERS
------------------------
- Demonstrates correct usage of LangGraph state management
- Shows multi-threaded conversation handling
- Clean separation of backend graph logic and UI
- Strong foundation for production-grade AI chat systems


AUTHOR
------
Built by Sumit Latiyan