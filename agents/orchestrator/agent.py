import logging
from google.adk.agents import Agent
from agents.orchestrator.prompt import OA_PROMPT

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")

# Thiết lập logging chi tiết để theo dõi luồng hoạt động
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

MODEL_NAME = 'gemini-2.0-flash-exp'

# Định nghĩa OrchestratorAgent bằng ADK
# Dựa trên vai trò đã mô tả trong DESIGN.md
orchestrator_agent = Agent(
    name="OrchestratorAgent",
    model=MODEL_NAME, 
    description="Agent điều phối trung tâm, 'bộ não' của hệ thống.",
    instruction=OA_PROMPT,
    tools=[],
)

logger.info("OrchestratorAgent has been defined.")