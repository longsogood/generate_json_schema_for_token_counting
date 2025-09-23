#!/usr/bin/env python3
"""
Test script để validate logic mới với additional_kwargs
"""

import json
import sys
import os

# Import function từ countTokensSchema.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from countTokensSchema import parse_log_messages

def test_additional_kwargs():
    """Test các trường hợp với additional_kwargs"""
    
    print("🧪 Testing logic mới với additional_kwargs...")
    print("=" * 70)
    
    # Test case 1: Mixed messages với additional_kwargs
    print("\n📝 Test Case 1: Mixed messages với additional_kwargs")
    test_data_1 = [
        # Regular messages
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
        
        # System prompt (no role, no additional_kwargs)
        {"content": "You are a helpful assistant."},
        
        # Assistant message với tool_calls (no role, có additional_kwargs với tool_calls)
        {
            "content": "",
            "additional_kwargs": {
                "tool_calls": [
                    {
                        "id": "tooluse_7Z_JGRx1SNyAHdBLq3Ce4g",
                        "function": {
                            "arguments": {
                                "input": "nhân viên kinh doanh đi muộn số lần cho phép tháng"
                            },
                            "name": "CMCTSRetriever"
                        },
                        "type": "function",
                        "index": 0
                    }
                ]
            }
        },
        
        # User message với name (no role, có additional_kwargs với name)
        {
            "content": ["Some content here"],
            "additional_kwargs": {
                "name": "CMCTSRetriever"
            }
        }
    ]
    
    result_1 = parse_log_messages(test_data_1, include_system=True)
    print("Input:")
    print(json.dumps(test_data_1, indent=2, ensure_ascii=False))
    print("\nOutput:")
    print(json.dumps(result_1, indent=2, ensure_ascii=False))
    
    # Validate result
    assert "messages" in result_1
    assert "system" in result_1
    assert len(result_1["messages"]) == 4  # 2 regular + 1 assistant + 1 user
    assert len(result_1["system"]) == 1    # 1 system prompt
    
    # Check roles
    roles = [msg["role"] for msg in result_1["messages"]]
    expected_roles = ["user", "assistant", "assistant", "user"]
    assert roles == expected_roles, f"Expected roles {expected_roles}, got {roles}"
    
    print("✅ Test Case 1 PASSED")
    
    # Test case 2: Chỉ có additional_kwargs messages, không có system
    print("\n📝 Test Case 2: Chỉ có additional_kwargs messages")
    test_data_2 = [
        {
            "content": "",
            "additional_kwargs": {
                "tool_calls": [{"id": "test", "function": {"name": "test_func"}}]
            }
        },
        {
            "content": "Response content",
            "additional_kwargs": {
                "name": "TestTool"
            }
        }
    ]
    
    result_2 = parse_log_messages(test_data_2, include_system=True)
    print("Input:")
    print(json.dumps(test_data_2, indent=2, ensure_ascii=False))
    print("\nOutput:")
    print(json.dumps(result_2, indent=2, ensure_ascii=False))
    
    # Validate result
    assert "messages" in result_2
    assert "system" not in result_2  # No system prompts
    assert len(result_2["messages"]) == 2
    
    # Check roles
    roles = [msg["role"] for msg in result_2["messages"]]
    expected_roles = ["assistant", "user"]
    assert roles == expected_roles, f"Expected roles {expected_roles}, got {roles}"
    
    print("✅ Test Case 2 PASSED")
    
    # Test case 3: Test với include_system=False
    print("\n📝 Test Case 3: Test với include_system=False")
    result_3 = parse_log_messages(test_data_1, include_system=False)
    print("Output (include_system=False):")
    print(json.dumps(result_3, indent=2, ensure_ascii=False))
    
    # Validate result
    assert "messages" in result_3
    assert "system" not in result_3  # System prompts excluded
    assert len(result_3["messages"]) == 4  # Same messages, no system
    
    print("✅ Test Case 3 PASSED")
    
    print("\n" + "=" * 70)
    print("🎉 All additional_kwargs tests PASSED! Logic hoạt động đúng.")

if __name__ == "__main__":
    test_additional_kwargs()