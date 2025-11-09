from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from memory_agent.agent import memory_agent
from utils import call_agent_sync
from dotenv import load_dotenv

load_dotenv()


# initialise persistant session service
db_url = "sqlite:///./my_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)

#define initial state
initial_state = {
    "user_name": "Jay Chaudhari",
    "reminders": [],
}


async def main_async():
    #setup contstants
    APP_NAME = "Memory agent"
    USER_ID = "jay_chaudhari"
    
    #check for existing sessions for this user
    existing_sessions = session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID,
    )
    
    if existing_sessions and len(existing_sessions) > 0:
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


