import os
import logging
import json
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Response

# [CẬP NHẬT] Import các thành phần từ đúng module
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

# Import agent đã được định nghĩa
from agents.orchestrator.agent import orchestrator_agent

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Tải các biến môi trường
load_dotenv()
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY chưa được thiết lập trong tệp .env")

# --- KIẾN TRÚC MỚI SỬ DỤNG FASTAPI ---

# 1. Tạo một ứng dụng FastAPI chính
app = FastAPI(
    title="Multi-Agent Code Reviewer System",
    description="Một hệ thống Multi-Agent để review mã nguồn và hỗ trợ phát triển.",
    version="1.0.0"
)

# 2. Tạo một route trên app chính để phục vụ Agent Card
@app.get("/agent_card.json", tags=["Discovery"])
async def serve_agent_card():
    """
    Đọc và trả về nội dung của file agent_card.json để các agent khác có thể khám phá.
    """
    logger.info("Request for Agent Card received. Serving card...")
    card_path = os.path.join("agents", "orchestrator", "agent_card.json")
    try:
        with open(card_path, "r", encoding="utf-8") as f:
            card_data = json.load(f)
        return Response(content=json.dumps(card_data, indent=2), media_type="application/json")
    except FileNotFoundError:
        logger.error(f"Agent card not found at path: {card_path}")
        return Response(content=json.dumps({"error": "Agent card not found"}), status_code=404, media_type="application/json")

# 3. Khởi tạo Runner của ADK
# Runner trong phiên bản này chính là một ứng dụng ASGI có thể được "mount"
adk_runner = Runner(
    agent=orchestrator_agent,
    app_name="multi-agent-code-reviewer",
    session_service=InMemorySessionService()
)

# 4. "Gắn" ứng dụng của Runner vào app FastAPI chính tại đường dẫn /a2a
# Điều này có nghĩa là tất cả các yêu cầu A2A sẽ được chuyển đến adk_runner để xử lý
app.mount("/a2a", adk_runner, name="a2a_api")
logger.info("A2A endpoint is mounted at /a2a")
logger.info("Agent card is available at http://localhost:8080/agent_card.json")

# 5. Cấu hình để chạy server bằng Uvicorn khi file này được thực thi
if __name__ == "__main__":
    logger.info("Starting the main FastAPI server with Uvicorn...")
    uvicorn.run(app, host="0.0.0.0", port=8080)