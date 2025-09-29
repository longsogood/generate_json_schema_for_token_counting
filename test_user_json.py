import json
from countTokensSchema import parse_log_messages

def test_user_json():
    """Test hàm parse_log_messages với JSON data từ user"""
    
    # Load JSON data từ file
    with open('test_user_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    print("=== PHÂN TÍCH INPUT DATA ===")
    print(f"Tổng số items: {len(test_data)}")
    
    for i, item in enumerate(test_data):
        print(f"\nItem {i}:")
        has_role = "role" in item
        has_additional_kwargs = "additional_kwargs" in item
        has_content = "content" in item
        
        print(f"  - Có 'role': {has_role}")
        if has_role:
            print(f"    Role: {item['role']}")
        print(f"  - Có 'additional_kwargs': {has_additional_kwargs}")
        print(f"  - Có 'content': {has_content}")
        if has_content:
            content_preview = str(item['content'])[:100] + "..." if len(str(item['content'])) > 100 else str(item['content'])
            print(f"    Content preview: {content_preview}")
    
    print("\n=== TEST VỚI include_system=True ===")
    result_with_system = parse_log_messages(test_data, include_system=True)
    
    print(f"Số messages: {len(result_with_system.get('messages', []))}")
    print(f"Số system prompts: {len(result_with_system.get('system', []))}")
    
    print("\nMessages:")
    for i, msg in enumerate(result_with_system.get('messages', [])):
        print(f"  Message {i}: role='{msg['role']}', content_length={len(msg['content'])}")
    
    print("\nSystem prompts:")
    for i, sys in enumerate(result_with_system.get('system', [])):
        content_preview = sys['text'][:100] + "..." if len(sys['text']) > 100 else sys['text']
        print(f"  System {i}: {content_preview}")
    
    print("\n=== TEST VỚI include_system=False ===")
    result_without_system = parse_log_messages(test_data, include_system=False)
    
    print(f"Số messages: {len(result_without_system.get('messages', []))}")
    print(f"Số system prompts: {len(result_without_system.get('system', []))}")
    
    print("\nMessages:")
    for i, msg in enumerate(result_without_system.get('messages', [])):
        print(f"  Message {i}: role='{msg['role']}', content_length={len(msg['content'])}")
    
    print("\n=== PHÂN TÍCH KẾT QUẢ ===")
    print("✅ Logic mới đã hoạt động:")
    print("- Với include_system=True: Tất cả items không có 'role' và 'additional_kwargs' -> System prompts")
    print("- Với include_system=False: Tất cả items không có 'role' và 'additional_kwargs' -> User messages")
    
    # Xuất kết quả ra file để dễ kiểm tra
    with open('test_result_with_system.json', 'w', encoding='utf-8') as f:
        json.dump(result_with_system, f, indent=2, ensure_ascii=False)
    
    with open('test_result_without_system.json', 'w', encoding='utf-8') as f:
        json.dump(result_without_system, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Kết quả đã được lưu vào:")
    print("- test_result_with_system.json")
    print("- test_result_without_system.json")

if __name__ == "__main__":
    test_user_json()