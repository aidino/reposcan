# file: code_scan_agent.py
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from typing import List, Dict, Any
import asyncio


APP_NAME = "sast_app"
USER_ID = "1234"
SESSION_ID = "session1234"

# Import hàm quét mã chúng ta đã xây dựng từ file trước
from sast_tool_wrapper import run_semgrep_scan

# ---- Bước 1: Định nghĩa các công cụ mà Agent có thể sử dụng ----

def scan_project(source_path: str) -> Dict[str, Any]:
    """
    Chạy công cụ phân tích tĩnh Semgrep trên một dự án mã nguồn để tìm các vấn đề bảo mật và chất lượng mã.
    
    Args:
        source_path (str): Đường dẫn đến thư mục dự án cần quét
        
    Returns:
        Dict[str, Any]: Kết quả phân tích từ Semgrep bao gồm các vấn đề được tìm thấy
    """
    # Sử dụng các quy tắc mặc định có sẵn
    default_rules = [
        "./semgrep-rules/python",
        "./semgrep-rules/generic", 
        "./semgrep-rules/javascript",
        "./semgrep-rules/dockerfile"
    ]
    
    return run_semgrep_scan(source_path, default_rules)

# ---- Bước 2: Xây dựng Tác tử (Agent) ----

# Định nghĩa "bộ não" của hệ thống. Chúng ta cung cấp cho nó các chỉ dẫn
# và danh sách các công cụ nó được phép sử dụng.
scan_agent = LlmAgent(
    model="gemini-2.0-flash",  # Sử dụng model Gemini Flash mới nhất
    name="code_scan_agent",
    # Mô tả ngắn gọn về vai trò của Agent
    description="Một tác tử AI chuyên nghiệp, có khả năng phân tích mã nguồn và phát hiện lỗ hổng.",
    # Chỉ dẫn chi tiết (system prompt) cho Agent
    instruction=(
        "Bạn là một trợ lý phân tích mã nguồn tự động. Khi người dùng yêu cầu 'quét' hoặc "
        "'phân tích' một dự án, nhiệm vụ của bạn là sử dụng công cụ 'scan_project'.\n"
        "1. Hãy luôn hỏi người dùng để xác nhận đường dẫn đầy đủ đến dự án cần quét nếu họ chưa cung cấp.\n"
        "2. Đối với các quy tắc (rules), hãy luôn sử dụng danh sách các đường dẫn quy tắc cục bộ sau: "
        "'./semgrep-rules/python', './semgrep-rules/generic', './semgrep-rules/javascript', "
        "'./semgrep-rules/dockerfile'.\n"
        "3. Sau khi chạy công cụ và nhận được kết quả, hãy tóm tắt các phát hiện quan trọng nhất cho người dùng "
        "bằng ngôn ngữ tự nhiên, thay vì chỉ dán kết quả JSON thô."
    ),
    
    # Cung cấp danh sách các công cụ cho Agent
    tools=[scan_project],
)

# ---- Bước 3: Chạy Agent với Runner ----
# Session and Runner - CHÍNH SỬA ĐỂ SỬA LỖI SESSION
session_service = InMemorySessionService()
runner = Runner(agent=scan_agent, app_name=APP_NAME, session_service=session_service)

# Agent Interaction - SỬA ĐỂ XỬ LÝ ASYNC ĐÚNG CÁCH
async def call_agent_async(query):
    """Gọi agent với xử lý async đúng cách"""
    content = types.Content(role='user', parts=[types.Part(text=query)])
    
    # Tạo session trước khi chạy - SỬA ĐỂ DÙNG AWAIT
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("Agent Response: ", final_response)
            return final_response

asyncio.run(call_agent_async("scan code for project at /Users/ngohongthai/Documents/novaguard-ai2"))
