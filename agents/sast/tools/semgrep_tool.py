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
    # Xây dựng câu lệnh cơ bản với các tối ưu hóa
    command: List[str] = [
        "semgrep", "scan", 
        "--verbose", 
        "--json",
        "--timeout", "30",  # Giảm timeout xuống 30 giây
        "--max-target-bytes", "1000000",  # Giới hạn kích thước file (1MB)
        "--jobs", "2",  # Sử dụng 2 jobs song song
        "--no-git-ignore",  # Không skip files trong .gitignore để scan nhanh hơn
        "--optimizations", "all"  # Bật tất cả optimizations
    ]
    
    HERE = str((Path(__file__).parent).resolve())
    
    # Chỉ sử dụng một subset rules quan trọng để tăng tốc
    rule_paths: List[str] = [
        f"{HERE}/semgrep-rules/python/requests/security",  # Chỉ security rules quan trọng
        f"{HERE}/semgrep-rules/generic/secrets",  # Secrets detection
    ]

    # Thêm từng đường dẫn quy tắc vào câu lệnh với cờ --config
    for path in rule_paths:
        if Path(path).exists():  # Kiểm tra path tồn tại
            command.extend(["--config", path])

    # Thêm đường dẫn mã nguồn cần quét vào cuối
    command.append(source_path)

    print(f"🔹 Đang thực thi lệnh (optimized): {' '.join(command)}")

    try:
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            timeout=45  # Giảm timeout subprocess xuống 45 giây
        )
        results: Dict[str, Any] = json.loads(process.stdout)
        
        # Thêm thông tin tối ưu hóa
        results["scan_info"] = {
            "optimization": "enabled",
            "rules_used": rule_paths,
            "timeout_seconds": 45
        }
        
        print("✅ Quét thành công (optimized)!")
        return results

    except subprocess.TimeoutExpired:
        print("❌ LỖI: Semgrep scan timed out.")
        return {
            "error": "Semgrep scan timeout", 
            "details": "Quá trình scan vượt quá thời gian cho phép (45 giây). Đã tối ưu hóa nhưng dự án vẫn quá lớn.",
            "suggestion": "Thử quét thư mục con hoặc file cụ thể thay vì toàn bộ dự án."
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

