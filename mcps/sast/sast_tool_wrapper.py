# file: sast_tool_wrapper.py

import subprocess
import json
from typing import List, Dict, Any

def run_semgrep_scan(source_path: str, rule_paths: List[str]) -> Dict[str, Any]:
    """
    Thực thi Semgrep trên một thư mục mã nguồn với một danh sách các đường dẫn
    quy tắc cục bộ và trả về kết quả dưới dạng dictionary.

    Args:
        source_path (str): Đường dẫn đến thư mục hoặc tệp mã nguồn cần quét.
        rule_paths (List[str]): Một danh sách các đường dẫn đến thư mục hoặc file 
                                 quy tắc của Semgrep.

    Returns:
        Dict[str, Any]: Một dictionary chứa kết quả phân tích từ Semgrep.
    """
    # Xây dựng câu lệnh cơ bản
    command: List[str] = [
        "semgrep", "scan", 
        "--verbose", 
        "--json"
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
            check=True
        )
        results: Dict[str, Any] = json.loads(process.stdout)
        print("✅ Quét thành công!")
        return results

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

# --- Ví dụ sử dụng ---
if __name__ == "__main__":
    # Đường dẫn đến dự án thực tế của bạn
    project_to_scan = "/Users/ngohongthai/Documents/novaguard-ai2"
    
    # Danh sách các thư mục quy tắc bạn muốn áp dụng.
    # Cách làm này sẽ không đọc phải các file YAML không hợp lệ.
    local_semgrep_rules = [
        "./semgrep-rules/python",
        "./semgrep-rules/generic",
        "./semgrep-rules/javascript",
        "./semgrep-rules/dockerfile",
        # Thêm các thư mục khác nếu dự án của bạn có Java, Go, Terraform...
        # ví dụ: "./semgrep-rules/java"
    ]

    scan_results = run_semgrep_scan(project_to_scan, local_semgrep_rules)

    print("\n--- KẾT QUẢ PHÂN TÍCH ---")
    
    # Kiểm tra xem có lỗi từ Semgrep không (dựa trên JSON output)
    semgrep_errors = scan_results.get("errors", [])
    if scan_results.get("error"): # Lỗi từ script của chúng ta
        print(f"Đã xảy ra lỗi thực thi: {scan_results['error']}")
        # In chi tiết lỗi từ stderr nếu có
        if scan_results.get('stderr'):
            print("\n--- Stderr: ---")
            print(scan_results['stderr'])
        # In chi tiết lỗi từ stdout (JSON) nếu có
        if scan_results.get('stdout'):
            print("\n--- Stdout (chứa lỗi JSON): ---")
            print(scan_results['stdout'])
            
    elif semgrep_errors:
        print("❌ Semgrep đã chạy nhưng báo cáo lỗi cấu hình:")
        for err in semgrep_errors:
            print(f"  - [{err.get('type')}] {err.get('message')}")
    else:
        found_issues = scan_results.get("results", [])
        if not found_issues:
            print("✅ Không tìm thấy vấn đề nào.")
        else:
            print(f"🚨🚨🚨 THÀNH CÔNG! Tìm thấy {len(found_issues)} vấn đề.")
            # In ra 5 vấn đề đầu tiên để xem trước
            for issue in found_issues[:5]:
                check_id = issue['check_id']
                path = issue['path']
                line = issue['start']['line']
                message = issue['extra']['message']
                print(f"  - [{check_id}] tại {path}:{line}")
                print(f"    -> {message.strip()}")
            if len(found_issues) > 5:
                print(f"    ... và {len(found_issues) - 5} vấn đề khác.")