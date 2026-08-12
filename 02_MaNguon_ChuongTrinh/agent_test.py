import os
import asyncio
from dotenv import load_dotenv
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.hooks.policy import allow, deny

# Load .env to get GEMINI_API_KEY
load_dotenv()

# 1. Định nghĩa danh sách chính sách (Được duyệt từ trên xuống dưới)
custom_policies = [
    # Ưu tiên 1: Luôn chặn các hành vi nguy hiểm
    deny("command(sudo*)"),
    deny("command(rm -rf*)"),
    deny("write_file(/etc/*)"),
    
    # Ưu tiên 2: Tự động cho phép các thao tác an toàn trong thư mục dự án
    allow("read_file(./**)"),
    allow("write_file(./**)"),
    allow("command(pytest*)"),
    allow("command(git status)"),
    
    # Ưu tiên 3: Cho phép mọi lệnh python cục bộ
    allow("command(python *)")
]

# 2. Khởi tạo LocalAgentConfig với danh sách quy tắc
config = LocalAgentConfig(
    model="gemini-3.5-flash",
    policies=custom_policies,
    api_key=os.getenv("GEMINI_API_KEY")
)

# 3. Khởi tạo Agent
agent = Agent(config=config)

# 4. Thực thi tác vụ
async def main():
    async with agent:
        response = await agent.chat("Kiểm tra file test_main.py và chạy pytest để xác nhận.")
        text = await response.text()
        print(text)

if __name__ == "__main__":
    asyncio.run(main())
