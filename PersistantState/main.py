from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from memory_agent.agent import memory_agent
from utils import call_agent_async
from dotenv import load_dotenv
import asyncio

load_dotenv()


# Step 1) initialise persistant session service
db_url = "sqlite:///./my_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)

#Step 2) define initial state
initial_state = {
    "user_name": "Jay Chaudhari",
    "reminders": [],
}

# Step 3) Find existing sesison with the given app name and user id or else new session ust be created
async def main_async():
    #setup contstants
    APP_NAME = "Memory agent"
    USER_ID = "jay_chaudhari"
    
    #check for existing sessions for this user
    existing_sessions = session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID,
    )
    
    if existing_sessions and len(existing_sessions.sessions) > 0:
        SESSION_ID = existing_sessions.sessions[0].id
        print(f"Using existing session: {SESSION_ID}")
    else:
        new_session = session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state,
        )
        SESSION_ID = new_session.id
        print(f"Created new session: {SESSION_ID}")

    # Step4) Create a runner

    runner = Runner(
        agent=memory_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # Step5) Interactivce conversation loop
    print("\nWelcome to Memory Agent Chat!")
    print("Your reminders will be remembered across conversations.")
    print("Type 'exit' or 'quit' to end the conversation.\n")
    
    while True:
        # Get user input
        user_input = input("You: ")
        
        # Check if user wants to exit
        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation. Your data has been saved to the database.")
            break
        
        # Process the user query through the agent
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)
        

if __name__ == "__main__":
    asyncio.run(main_async())