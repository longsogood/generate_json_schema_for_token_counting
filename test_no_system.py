#!/usr/bin/env python3
"""
Test script để demo tính năng include_system=False
"""

import json
import sys
import os

# Import function từ countTokensSchema.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from countTokensSchema import parse_log_messages

def test_no_system():
    """Test với include_system=False"""
    
    print("🧪 Demo tính năng include_system=False...")
    print("=" * 60)
    
    # Test data với system prompts
    test_data = [
        {"role": "user", "content": "Xin chào!"},
        {"content": "Bạn là AI assistant hữu ích."},  # System prompt 1
        {"role": "assistant", "content": "Chào bạn! Tôi có thể giúp gì?"},
        {"content": "Luôn trả lời bằng tiếng Việt."},  # System prompt 2
        {"role": "user", "content": "Cảm ơn bạn!"}
    ]
    
    print("📥 Input Data:")
    print(json.dumps(test_data, indent=2, ensure_ascii=False))
    
    print("\n" + "="*30 + " INCLUDE SYSTEM = TRUE " + "="*30)
    result_with_system = parse_log_messages(test_data, include_system=True)
    print("📤 Output (include_system=True):")
    print(json.dumps(result_with_system, indent=2, ensure_ascii=False))
    print(f"📊 Kết quả: {len(result_with_system['messages'])} messages, {len(result_with_system.get('system', []))} system prompts")
    
    print("\n" + "="*30 + " INCLUDE SYSTEM = FALSE " + "="*29)
    result_no_system = parse_log_messages(test_data, include_system=False)
    print("📤 Output (include_system=False):")
    print(json.dumps(result_no_system, indent=2, ensure_ascii=False))
    print(f"📊 Kết quả: {len(result_no_system['messages'])} messages, {len(result_no_system.get('system', []))} system prompts")
    
    print("\n" + "="*60)
    print("✅ Demo hoàn thành! Người dùng có thể chọn có lấy system prompts hay không.")

if __name__ == "__main__":
    test_no_system()