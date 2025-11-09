import uuid

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from question_answering_agent import question_answering_agent


# load the env vars

load_dotenv()


# mention the info
APP_NAME="Jay's AI assisstant"
USER_ID = "jay_chaudhari"
SESSION_ID = str(uuid.uuid4())

initial_state = {
    "user_name": "Jay Chaudhari",
    "user_preferences": """
    I like to play cricket.
    I like to cycle.
    """
}

# create a session service incstance
stateful_session_service = InMemorySessionService()

# create a new stateful session using the service instance
stateful_session = stateful_session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state,
)
print("Session created")
print(f"Session id: {SESSION_ID}")

# create a runner which contains the agent and the session instances
runner = Runner(
    agent=question_answering_agent,
    app_name=APP_NAME,
    session_service= stateful_session_service,
)

# create a message (user prompt) using types
new_message = types.Content(
    role="user",
    parts=[types.Part(text="whats my name? What do i do?")]
)

# start the runner for given user_id and session_id
for event in runner.run(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=new_message,
):
    if event.is_final_response():
        if event.content and event.content.parts:
            print(f"Final response: {event.content.parts[0].text}")

print("SESSION EVENT EXPLORATION")
session = stateful_session_service.get_session(
    app_name=APP_NAME,
    session_id=SESSION_ID,
    user_id=USER_ID,
)
print(session)

print("FINAL SESSION STATE")
for key, value in session.state.items():
    print(f"{key}: {value}")