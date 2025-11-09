from google.adk.agents import SequentialAgent

from .sub_agents.recommender_agent import action_recommender_agent
from .sub_agents.scorer_agent import lead_scorer_agent
from .sub_agents.validator_agent import lead_validator_agent

# Create the sequential agent with minimal callback
root_agent = SequentialAgent(
    name="LeadQualificationPipeline",
    sub_agents=[lead_validator_agent, lead_scorer_agent, action_recommender_agent],
    description="A pipeline that validates, scores, and recommends actions for sales leads",
)