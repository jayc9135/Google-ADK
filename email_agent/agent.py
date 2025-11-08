from google.adk.agents import Agent
from pydantic import BaseModel, Field

class EmailContent(BaseModel):
    subject: str = Field(
        description="The subject of the email. Should be a concise and descriptive."
        )
    body: str = Field(
        description="The main content of the email. Should be well formatted with proper greeting, paragraphs and a closing."
        )


root_agent = Agent(
    name="email_agent",
    description="A agent that composes emails",
    model="gemini-2.5-flash",
    instruction="""
    You are an Email Generation Assistant.
    Your task is generate professionally written emails based on the user's request.
        GUIDELINES:
    - Create an appropriate subject line (concise and relevant)
    - Write a well-structured email body with:
    * Professional greeting
    * Clear and concise main content
    * Appropriate closing
    * Your name as signature
    - Suggest relevant attachments if applicable (empty list if none needed)
    - Email tone should match the purpose (formal for business, friendly for colleagues)
    - Keep emails concise but complete

    IMPORTANT: Your response MUST be valid JSON matching this structure:
    {
    "subject": "Subject line here",
    "body": "Email body here with proper paragraphs and formatting",
    }

    DO NOT include any explanations or additional text outside the JSON response.
    """,
    output_schema=EmailContent,
    output_key="email",
)