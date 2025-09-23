#!/usr/bin/env python3
"""
Test script để validate tính năng với example log file
"""

import json
import sys
import os

# Import function từ countTokensSchema.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from countTokensSchema import parse_log_messages

def test_example_log():
    """Test với example log file"""
    
    print("🧪 Testing với example_log.json...")
    print("=" * 60)
    
    # Đọc example log file
    with open('example_log.json', 'r', encoding='utf-8') as f:
        log_data = json.load(f)
    
    print("📥 Input Log Data:")
    print(json.dumps(log_data, indent=2, ensure_ascii=False))
    
    # Convert using our function
    result = parse_log_messages(log_data)
    
    print("\n📤 Converted Schema:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Validate result structure
    print("\n🔍 Validation:")
    assert "messages" in result, "❌ Missing 'messages' key"
    print("✅ Has 'messages' key")
    
    assert "system" in result, "❌ Missing 'system' key"
    print("✅ Has 'system' key")
    
    assert len(result["messages"]) == 4, f"❌ Expected 4 messages, got {len(result['messages'])}"
    print("✅ Correct number of messages (4)")
    
    assert len(result["system"]) == 2, f"❌ Expected 2 system messages, got {len(result['system'])}"
    print("✅ Correct number of system messages (2)")
    
    # Check message structure
    for i, msg in enumerate(result["messages"]):
        assert "role" in msg, f"❌ Message {i} missing 'role'"
        assert "content" in msg, f"❌ Message {i} missing 'content'"
        assert isinstance(msg["content"], list), f"❌ Message {i} content is not a list"
        assert len(msg["content"]) > 0, f"❌ Message {i} content is empty"
        assert "text" in msg["content"][0], f"❌ Message {i} content[0] missing 'text'"
    print("✅ All messages have correct structure")
    
    # Check system message structure
    for i, sys_msg in enumerate(result["system"]):
        assert "text" in sys_msg, f"❌ System message {i} missing 'text'"
        assert isinstance(sys_msg["text"], str), f"❌ System message {i} text is not string"
    print("✅ All system messages have correct structure")
    
    # Create full AWS Bedrock schema
    full_schema = {
        "modelId": "anthropic.claude-3-5-sonnet-20241022-v2:0",
        "input": {
            "converse": result
        }
    }
    
    print("\n🚀 Full AWS Bedrock Schema:")
    print(json.dumps(full_schema, indent=2, ensure_ascii=False))
    
    # Save result to file
    with open('converted_schema.json', 'w', encoding='utf-8') as f:
        json.dump(full_schema, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Schema đã được lưu vào 'converted_schema.json'")
    print("=" * 60)
    print("🎉 Test PASSED! Tính năng hoạt động hoàn hảo!")

if __name__ == "__main__":
    test_example_log()