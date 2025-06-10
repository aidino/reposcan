# file: code_scan_agent.py
import json # Needed for pretty printing dicts
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from agents.sast.prompt import SCAN_PROMPT
from pathlib import Path

from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

PATH_TO_YOUR_MCP_SERVER_SCRIPT = str((Path(__file__).parent / "server.py").resolve())

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")

MODEL_NAME = 'gpt-4o-mini'

root_agent = LlmAgent(
        model=LiteLlm(model=MODEL_NAME),  
        name="code_scan_agent",
        # Mô tả ngắn gọn về vai trò của Agent
        description="Một tác tử AI chuyên nghiệp, có khả năng phân tích mã nguồn và phát hiện lỗ  hổng.",
        # Chỉ dẫn chi tiết (system prompt) cho Agent
        instruction=SCAN_PROMPT,
        # Cung cấp danh sách các công cụ cho Agent
        tools=[
            MCPToolset(
                connection_params=StdioServerParameters(
                    command='python3', # Command to run your MCP server script
                    args=[PATH_TO_YOUR_MCP_SERVER_SCRIPT], # Argument is the path to the script
                )
            )
        ],
    )
