#!/usr/bin/env python3
"""
Generate test results cho test_user_data.json
"""

import json
from countTokensSchema import parse_log_messages

def generate_test_results():
    """Generate kết quả test với test_user_data.json"""
    
    # Đọc test data
    with open('test_user_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    print("=== GENERATING TEST RESULTS ===")
    
    # Test với include_system=True
    result_with_system = parse_log_messages(test_data, include_system=True)
    
    # Test với include_system=False  
    result_without_system = parse_log_messages(test_data, include_system=False)
    
    # Lưu kết quả
    with open('test_result_with_system.json', 'w', encoding='utf-8') as f:
        json.dump(result_with_system, f, indent=2, ensure_ascii=False)
    
    with open('test_result_without_system.json', 'w', encoding='utf-8') as f:
        json.dump(result_without_system, f, indent=2, ensure_ascii=False)
    
    print("✅ Đã tạo test_result_with_system.json")
    print("✅ Đã tạo test_result_without_system.json")
    
    # So sánh kết quả
    print(f"\n=== SO SÁNH KẾT QUẢ ===")
    print(f"Với include_system=True:")
    print(f"  Messages: {len(result_with_system['messages'])}")
    print(f"  System: {len(result_with_system.get('system', []))}")
    print(f"  Roles: {[msg['role'] for msg in result_with_system['messages']]}")
    
    print(f"\nVới include_system=False:")
    print(f"  Messages: {len(result_without_system['messages'])}")
    print(f"  System: {len(result_without_system.get('system', []))}")
    print(f"  Roles: {[msg['role'] for msg in result_without_system['messages']]}")
    
    # Kiểm tra logic
    roles_with_system = [msg['role'] for msg in result_with_system['messages']]
    roles_without_system = [msg['role'] for msg in result_without_system['messages']]
    
    if roles_with_system == roles_without_system:
        print("\n✅ Logic đúng: Roles giống nhau khi bỏ chọn system prompt")
        print("   Item đầu tiên không có role/additional_kwargs được xử lý đúng:")
        print("   - include_system=True: thành system prompt")
        print("   - include_system=False: bị bỏ qua")
    else:
        print("\n❌ Logic sai: Roles khác nhau")
        print(f"   With system: {roles_with_system}")
        print(f"   Without system: {roles_without_system}")

if __name__ == "__main__":
    generate_test_results()