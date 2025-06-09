# file: sast_tool_wrapper.py

import subprocess
import json
from typing import List, Dict, Any
from pathlib import Path

def semgrep_scan_project(source_path: str) -> Dict[str, Any]:
    """
    Thực thi Semgrep trên một thư mục mã nguồn và trả về kết quả dưới dạng dictionary.

    Args:
        source_path (str): Đường dẫn đến thư mục hoặc tệp mã nguồn cần quét.
        
    Returns:
        Dict[str, Any]: Một dictionary chứa kết quả phân tích từ Semgrep.
    """
    # Xây dựng câu lệnh cơ bản
    command: List[str] = [
        "semgrep", "scan", 
        "--verbose", 
        "--json",
        "--timeout", "40"  # Thêm timeout để tránh quá trình scan quá lâu
    ]
    
    HERE = str((Path(__file__).parent).resolve())
    
    rule_paths: List[str] = [
        f"{HERE}/semgrep-rules/python",
        f"{HERE}/semgrep-rules/generic",
    ]

    # Thêm từng đường dẫn quy tắc vào câu lệnh với cờ --config
    for path in rule_paths:
        command.extend(["--config", path])

    # Thêm đường dẫn mã nguồn cần quét vào cuối
    command.append(source_path)

    print(f"🔹 Đang thực thi lệnh: {' '.join(command)}")

    try:
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            timeout=50  # Thêm timeout cho subprocess
        )
        results: Dict[str, Any] = json.loads(process.stdout)
        print("✅ Quét thành công!")
        return results

    except subprocess.TimeoutExpired:
        print("❌ LỖI: Semgrep scan timed out.")
        return {
            "error": "Semgrep scan timeout",
            "details": "Quá trình scan vượt quá thời gian cho phép (50 giây). Hãy thử quét thư mục nhỏ hơn."
        }
    except FileNotFoundError:
        print("❌ LỖI: Lệnh 'semgrep' không được tìm thấy.")
        return {
            "error": "Command not found: semgrep",
            "details": "Hãy đảm bảo Semgrep đã được cài đặt và có trong biến môi trường PATH."
        }
    except subprocess.CalledProcessError as e:
        print(f"❌ LỖI: Semgrep thực thi thất bại với exit code {e.returncode}.")
        # Cố gắng parse JSON từ stdout ngay cả khi có lỗi, vì Semgrep thường trả về lỗi trong JSON
        try:
            error_json = json.loads(e.stdout)
        except json.JSONDecodeError:
            error_json = {}
            
        return {
            "error": "Semgrep execution failed",
            "exit_code": e.returncode,
            "stdout": e.stdout, # Giữ lại stdout để xem chi tiết lỗi JSON
            "stderr": e.stderr,
            "parsed_error": error_json 
        }
    except json.JSONDecodeError:
        print("❌ LỖI: Không thể phân giải output JSON từ Semgrep.")
        return {
            "error": "JSON decoding failed",
            "raw_output": process.stdout if 'process' in locals() else "N/A"
        }

