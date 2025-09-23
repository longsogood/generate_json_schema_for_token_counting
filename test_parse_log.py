#!/usr/bin/env python3
"""
Test script để validate function parse_log_messages()
"""

import json
import sys
import os

# Import function từ countTokensSchema.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from countTokensSchema import parse_log_messages

def test_parse_log_messages():
    """Test các trường hợp khác nhau của parse_log_messages"""
    
    print("🧪 Testing parse_log_messages function...")
    print("=" * 50)
    
    # Test case 1: Basic messages với system prompt
    print("\n📝 Test Case 1: Basic messages với system prompt")
    test_data_1 = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm doing well, thank you!"},
        {"content": "You are a helpful AI assistant."}  # System prompt
    ]
    
    result_1 = parse_log_messages(test_data_1)
    print("Input:")
    print(json.dumps(test_data_1, indent=2, ensure_ascii=False))
    print("\nOutput:")
    print(json.dumps(result_1, indent=2, ensure_ascii=False))
    
    # Validate result
    assert "messages" in result_1
    assert "system" in result_1
    assert len(result_1["messages"]) == 2
    assert len(result_1["system"]) == 1
    assert result_1["messages"][0]["role"] == "user"
    assert result_1["messages"][0]["content"][0]["text"] == "Hello, how are you?"
    assert result_1["system"][0]["text"] == "You are a helpful AI assistant."
    print("✅ Test Case 1 PASSED")
    
    # Test case 2: Chỉ có messages, không có system prompt
    print("\n📝 Test Case 2: Chỉ có messages, không có system prompt")
    test_data_2 = [
        {"role": "user", "content": "What's the weather like?"},
        {"role": "assistant", "content": "I don't have access to current weather data."}
    ]
    
    result_2 = parse_log_messages(test_data_2)
    print("Input:")
    print(json.dumps(test_data_2, indent=2, ensure_ascii=False))
    print("\nOutput:")
    print(json.dumps(result_2, indent=2, ensure_ascii=False))
    
    # Validate result
    assert "messages" in result_2
    assert "system" not in result_2
    assert len(result_2["messages"]) == 2
    print("✅ Test Case 2 PASSED")
    
    # Test case 3: Multiple system prompts
    print("\n📝 Test Case 3: Multiple system prompts")
    test_data_3 = [
        {"content": "You are a helpful assistant."},
        {"content": "Always be polite and professional."},
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]
    
    result_3 = parse_log_messages(test_data_3)
    print("Input:")
    print(json.dumps(test_data_3, indent=2, ensure_ascii=False))
    print("\nOutput:")
    print(json.dumps(result_3, indent=2, ensure_ascii=False))
    
    # Validate result
    assert "messages" in result_3
    assert "system" in result_3
    assert len(result_3["messages"]) == 2
    assert len(result_3["system"]) == 2
    print("✅ Test Case 3 PASSED")
    
    # Test case 4: Content dạng list
    print("\n📝 Test Case 4: Content dạng list")
    test_data_4 = [
        {"role": "user", "content": [{"text": "Hello"}, {"text": "How are you?"}]},
        {"role": "assistant", "content": [{"text": "I'm fine, thanks!"}]}
    ]
    
    result_4 = parse_log_messages(test_data_4)
    print("Input:")
    print(json.dumps(test_data_4, indent=2, ensure_ascii=False))
    print("\nOutput:")
    print(json.dumps(result_4, indent=2, ensure_ascii=False))
    
    # Validate result
    assert "messages" in result_4
    assert len(result_4["messages"]) == 2
    assert isinstance(result_4["messages"][0]["content"], list)
    assert len(result_4["messages"][0]["content"]) == 2
    print("✅ Test Case 4 PASSED")
    
    # Test case 5: Empty input
    print("\n📝 Test Case 5: Empty input")
    test_data_5 = []
    
    result_5 = parse_log_messages(test_data_5)
    print("Input:")
    print(json.dumps(test_data_5, indent=2, ensure_ascii=False))
    print("\nOutput:")
    print(json.dumps(result_5, indent=2, ensure_ascii=False))
    
    # Validate result
    assert "messages" in result_5
    assert len(result_5["messages"]) == 0
    assert "system" not in result_5
    print("✅ Test Case 5 PASSED")
    
    # Test case 6: Test với include_system=False
    print("\n📝 Test Case 6: Test với include_system=False")
    test_data_6 = [
        {"role": "user", "content": "Hello"},
        {"content": "You are helpful"}, # System prompt sẽ bị bỏ qua
        {"role": "assistant", "content": "Hi there!"}
    ]
    
    result_6 = parse_log_messages(test_data_6, include_system=False)
    print("Input:")
    print(json.dumps(test_data_6, indent=2, ensure_ascii=False))
    print("\nOutput (include_system=False):")
    print(json.dumps(result_6, indent=2, ensure_ascii=False))
    
    # Validate result
    assert "messages" in result_6
    assert "system" not in result_6  # System prompts should be excluded
    assert len(result_6["messages"]) == 2
    print("✅ Test Case 6 PASSED")
    
    # Test case 7: Test với include_system=True (default)
    print("\n📝 Test Case 7: Test với include_system=True (default)")
    result_7 = parse_log_messages(test_data_6, include_system=True)
    print("Output (include_system=True):")
    print(json.dumps(result_7, indent=2, ensure_ascii=False))
    
    # Validate result
    assert "messages" in result_7
    assert "system" in result_7  # System prompts should be included
    assert len(result_7["messages"]) == 2
    assert len(result_7["system"]) == 1
    print("✅ Test Case 7 PASSED")

    print("\n" + "=" * 50)
    print("🎉 All tests PASSED! Function works correctly with include_system option.")

if __name__ == "__main__":
    test_parse_log_messages()