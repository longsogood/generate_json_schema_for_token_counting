#!/usr/bin/env python3
"""
Test để reproduce vấn đề với test_user_data.json
"""

import json
from countTokensSchema import parse_log_messages

def test_user_data_issue():
    """Test với data từ test_user_data.json"""
    
    # Đọc file test_user_data.json
    with open('test_user_data.json', 'r', encoding='utf-8') as f:
        log_data = json.load(f)
    
    print("=== PHÂN TÍCH LOG DATA ===")
    for i, item in enumerate(log_data):
        has_role = "role" in item
        has_additional_kwargs = "additional_kwargs" in item
        print(f"Item {i}: has_role={has_role}, has_additional_kwargs={has_additional_kwargs}")
        if has_role:
            print(f"  -> Role: {item['role']}")
        if has_additional_kwargs:
            print(f"  -> Additional kwargs: {list(item['additional_kwargs'].keys())}")
        if not has_role and not has_additional_kwargs:
            print(f"  -> Content preview: {str(item.get('content', ''))[:50]}...")
    
    print("\n=== TEST VỚI include_system=True ===")
    result_with_system = parse_log_messages(log_data, include_system=True)
    print(f"Số messages: {len(result_with_system['messages'])}")
    print(f"Số system prompts: {len(result_with_system.get('system', []))}")
    
    print("\nRoles trong messages:")
    for i, msg in enumerate(result_with_system['messages']):
        print(f"  {i+1}. {msg['role']}")
    
    print("\n=== TEST VỚI include_system=False ===")
    result_without_system = parse_log_messages(log_data, include_system=False)
    print(f"Số messages: {len(result_without_system['messages'])}")
    print(f"Có system prompts: {'system' in result_without_system}")
    
    print("\nRoles trong messages:")
    for i, msg in enumerate(result_without_system['messages']):
        print(f"  {i+1}. {msg['role']}")
    
    print("\n=== SO SÁNH KẾT QUẢ ===")
    roles_with_system = [msg['role'] for msg in result_with_system['messages']]
    roles_without_system = [msg['role'] for msg in result_without_system['messages']]
    
    print(f"Roles với system:    {roles_with_system}")
    print(f"Roles không system:  {roles_without_system}")
    
    # Kiểm tra xem có khác biệt không
    if roles_with_system == roles_without_system:
        print("✅ Roles giống nhau - logic đúng")
    else:
        print("❌ Roles khác nhau - có vấn đề!")
        print("Vấn đề: Item đầu tiên không có role/additional_kwargs:")
        print("- Với include_system=True: được coi là system prompt")
        print("- Với include_system=False: được coi là user message")
    
    # Kiểm tra content của message đầu tiên khi include_system=False
    if result_without_system['messages']:
        first_msg = result_without_system['messages'][0]
        print(f"\nMessage đầu tiên khi include_system=False:")
        print(f"Role: {first_msg['role']}")
        print(f"Content preview: {str(first_msg['content'][0])[:100]}...")

if __name__ == "__main__":
    test_user_data_issue()