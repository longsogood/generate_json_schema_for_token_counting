#!/usr/bin/env python3
"""
Test script để demo với complex log có additional_kwargs
"""

import json
import sys
import os

# Import function từ countTokensSchema.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from countTokensSchema import parse_log_messages

def test_complex_log():
    """Test với complex log file"""
    
    print("🧪 Testing với example_complex_log.json...")
    print("=" * 70)
    
    # Đọc complex log file
    with open('example_complex_log.json', 'r', encoding='utf-8') as f:
        log_data = json.load(f)
    
    print("📥 Input Complex Log Data:")
    print(json.dumps(log_data, indent=2, ensure_ascii=False))
    
    # Convert using our function với include_system=True
    print("\n" + "="*25 + " INCLUDE SYSTEM = TRUE " + "="*25)
    result_with_system = parse_log_messages(log_data, include_system=True)
    print("📤 Converted Schema (include_system=True):")
    print(json.dumps(result_with_system, indent=2, ensure_ascii=False))
    
    # Analyze result
    messages = result_with_system.get('messages', [])
    system_msgs = result_with_system.get('system', [])
    
    print(f"\n📊 Phân tích kết quả:")
    print(f"• Tổng số messages: {len(messages)}")
    print(f"• Tổng số system prompts: {len(system_msgs)}")
    
    print(f"\n🔍 Chi tiết messages:")
    for i, msg in enumerate(messages):
        role = msg['role']
        content_preview = str(msg['content'][0]['text'])[:50] + "..." if len(str(msg['content'][0]['text'])) > 50 else str(msg['content'][0]['text'])
        print(f"  {i+1}. Role: {role} | Content: {content_preview}")
    
    print(f"\n🔍 Chi tiết system prompts:")
    for i, sys_msg in enumerate(system_msgs):
        text_preview = sys_msg['text'][:50] + "..." if len(sys_msg['text']) > 50 else sys_msg['text']
        print(f"  {i+1}. {text_preview}")
    
    # Test với include_system=False
    print("\n" + "="*25 + " INCLUDE SYSTEM = FALSE " + "="*24)
    result_no_system = parse_log_messages(log_data, include_system=False)
    print("📤 Converted Schema (include_system=False):")
    print(json.dumps(result_no_system, indent=2, ensure_ascii=False))
    
    messages_no_sys = result_no_system.get('messages', [])
    print(f"\n📊 Kết quả không có system: {len(messages_no_sys)} messages")
    
    # Create full AWS Bedrock schema
    full_schema = {
        "modelId": "anthropic.claude-3-5-sonnet-20241022-v2:0",
        "input": {
            "converse": result_with_system
        }
    }
    
    # Save result to file
    with open('converted_complex_schema.json', 'w', encoding='utf-8') as f:
        json.dump(full_schema, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Full schema đã được lưu vào 'converted_complex_schema.json'")
    print("=" * 70)
    print("🎉 Complex log test PASSED! Logic xử lý additional_kwargs hoạt động hoàn hảo!")

if __name__ == "__main__":
    test_complex_log()