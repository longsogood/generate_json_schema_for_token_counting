#!/usr/bin/env python3
"""
Test logic đã sửa với nhiều test cases
"""

import json
from countTokensSchema import parse_log_messages

def test_fixed_logic():
    """Test logic đã sửa với các trường hợp khác nhau"""
    
    print("=== TEST CASE 1: Nhiều items không có role và additional_kwargs ===")
    log_data_1 = [
        {"content": "System prompt 1"},           # Lần 1 -> system (nếu include_system=True)
        {"role": "user", "content": "Hello"},
        {"content": "User message 1"},           # Lần 2 -> user
        {"role": "assistant", "content": "Hi"},
        {"content": "User message 2"},           # Lần 3 -> user
        {"content": "User message 3"},           # Lần 4 -> user
    ]
    
    print("Input:")
    for i, item in enumerate(log_data_1):
        has_role = "role" in item
        has_additional_kwargs = "additional_kwargs" in item
        print(f"  {i}: has_role={has_role}, has_kwargs={has_additional_kwargs}, content='{str(item.get('content', ''))[:30]}...'")
    
    # Test với include_system=True
    result_with_system = parse_log_messages(log_data_1, include_system=True)
    print(f"\nVới include_system=True:")
    print(f"  Messages: {len(result_with_system['messages'])}")
    print(f"  System: {len(result_with_system.get('system', []))}")
    print(f"  Roles: {[msg['role'] for msg in result_with_system['messages']]}")
    
    # Test với include_system=False
    result_without_system = parse_log_messages(log_data_1, include_system=False)
    print(f"\nVới include_system=False:")
    print(f"  Messages: {len(result_without_system['messages'])}")
    print(f"  System: {len(result_without_system.get('system', []))}")
    print(f"  Roles: {[msg['role'] for msg in result_without_system['messages']]}")
    
    # Kiểm tra kết quả
    # Logic: item 0 (System prompt 1) -> system nếu include_system=True, bỏ qua nếu False
    #        item 1 (Hello) -> user
    #        item 2 (User message 1) -> user (lần 2 không có role/kwargs)
    #        item 3 (Hi) -> assistant
    #        item 4 (User message 2) -> user (lần 3 không có role/kwargs)
    #        item 5 (User message 3) -> user (lần 4 không có role/kwargs)
    expected_roles_with_system = ['user', 'user', 'assistant', 'user', 'user']
    expected_roles_without_system = ['user', 'user', 'assistant', 'user', 'user']
    
    actual_roles_with_system = [msg['role'] for msg in result_with_system['messages']]
    actual_roles_without_system = [msg['role'] for msg in result_without_system['messages']]
    
    assert actual_roles_with_system == expected_roles_with_system, f"Expected {expected_roles_with_system}, got {actual_roles_with_system}"
    assert actual_roles_without_system == expected_roles_without_system, f"Expected {expected_roles_without_system}, got {actual_roles_without_system}"
    assert len(result_with_system.get('system', [])) == 1, "Should have 1 system message"
    assert len(result_without_system.get('system', [])) == 0, "Should have 0 system messages"
    
    print("✅ Test case 1 passed!")
    
    print("\n=== TEST CASE 2: Chỉ có items không có role và additional_kwargs ===")
    log_data_2 = [
        {"content": "System prompt"},     # Lần 1 -> system (nếu include_system=True)
        {"content": "User message 1"},   # Lần 2 -> user
        {"content": "User message 2"},   # Lần 3 -> user
        {"content": "User message 3"},   # Lần 4 -> user
    ]
    
    # Test với include_system=True
    result2_with_system = parse_log_messages(log_data_2, include_system=True)
    print(f"Với include_system=True:")
    print(f"  Messages: {len(result2_with_system['messages'])}")
    print(f"  System: {len(result2_with_system.get('system', []))}")
    print(f"  Roles: {[msg['role'] for msg in result2_with_system['messages']]}")
    
    # Test với include_system=False
    result2_without_system = parse_log_messages(log_data_2, include_system=False)
    print(f"\nVới include_system=False:")
    print(f"  Messages: {len(result2_without_system['messages'])}")
    print(f"  System: {len(result2_without_system.get('system', []))}")
    print(f"  Roles: {[msg['role'] for msg in result2_without_system['messages']]}")
    
    # Kiểm tra kết quả
    assert len(result2_with_system['messages']) == 3, "Should have 3 user messages"
    assert len(result2_with_system.get('system', [])) == 1, "Should have 1 system message"
    assert len(result2_without_system['messages']) == 3, "Should have 3 user messages"
    assert len(result2_without_system.get('system', [])) == 0, "Should have 0 system messages"
    
    print("✅ Test case 2 passed!")
    
    print("\n=== TEST CASE 3: Test với test_user_data.json ===")
    with open('test_user_data.json', 'r', encoding='utf-8') as f:
        test_user_data = json.load(f)
    
    result3_with_system = parse_log_messages(test_user_data, include_system=True)
    result3_without_system = parse_log_messages(test_user_data, include_system=False)
    
    print(f"test_user_data.json với include_system=True:")
    print(f"  Messages: {len(result3_with_system['messages'])}")
    print(f"  System: {len(result3_with_system.get('system', []))}")
    print(f"  Roles: {[msg['role'] for msg in result3_with_system['messages']]}")
    
    print(f"\ntest_user_data.json với include_system=False:")
    print(f"  Messages: {len(result3_without_system['messages'])}")
    print(f"  System: {len(result3_without_system.get('system', []))}")
    print(f"  Roles: {[msg['role'] for msg in result3_without_system['messages']]}")
    
    # Kiểm tra rằng roles giống nhau (vì item đầu tiên được bỏ qua khi include_system=False)
    roles_with_system = [msg['role'] for msg in result3_with_system['messages']]
    roles_without_system = [msg['role'] for msg in result3_without_system['messages']]
    
    assert roles_with_system == roles_without_system, f"Roles should be the same: {roles_with_system} vs {roles_without_system}"
    
    print("✅ Test case 3 passed!")
    
    print("\n🎉 Tất cả test cases đều passed! Logic đã được sửa đúng.")

if __name__ == "__main__":
    test_fixed_logic()