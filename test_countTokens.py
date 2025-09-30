#!/usr/bin/env python3
"""
Test script để demo cách sử dụng countTokens.py
"""

import json
import subprocess
import sys
import os

def test_countTokens_tool():
    """Test countTokens.py tool"""
    
    print("🧪 Testing countTokens.py tool...")
    print("=" * 60)
    
    # Test 1: Test với converted_schema.json
    print("\n📝 Test 1: Count tokens từ converted_schema.json")
    if os.path.exists('converted_schema.json'):
        try:
            # Chạy countTokens.py với file
            result = subprocess.run([
                sys.executable, 'countTokens.py', 
                '--file', 'converted_schema.json'
            ], capture_output=True, text=True, timeout=30)
            
            print("Command output:")
            print(result.stdout)
            
            if result.stderr:
                print("Errors:")
                print(result.stderr)
                
            print(f"Exit code: {result.returncode}")
            
        except subprocess.TimeoutExpired:
            print("❌ Command timed out (likely due to AWS credentials)")
        except Exception as e:
            print(f"❌ Error running command: {e}")
    else:
        print("❌ converted_schema.json not found")
    
    # Test 2: Test với converted_complex_schema.json
    print("\n📝 Test 2: Count tokens từ converted_complex_schema.json")
    if os.path.exists('converted_complex_schema.json'):
        try:
            # Chạy countTokens.py với file
            result = subprocess.run([
                sys.executable, 'countTokens.py', 
                '--file', 'converted_complex_schema.json'
            ], capture_output=True, text=True, timeout=30)
            
            print("Command output:")
            print(result.stdout)
            
            if result.stderr:
                print("Errors:")
                print(result.stderr)
                
            print(f"Exit code: {result.returncode}")
            
        except subprocess.TimeoutExpired:
            print("❌ Command timed out (likely due to AWS credentials)")
        except Exception as e:
            print(f"❌ Error running command: {e}")
    else:
        print("❌ converted_complex_schema.json not found")
    
    # Test 3: Test help command
    print("\n📝 Test 3: Show help")
    try:
        result = subprocess.run([
            sys.executable, 'countTokens.py', '--help'
        ], capture_output=True, text=True, timeout=10)
        
        print("Help output:")
        print(result.stdout)
        
    except Exception as e:
        print(f"❌ Error showing help: {e}")
    
    # Test 4: Test với inline input
    print("\n📝 Test 4: Count tokens với inline input")
    test_input = {
        "converse": {
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": "Hello, how are you?"}]
                }
            ]
        }
    }
    
    try:
        result = subprocess.run([
            sys.executable, 'countTokens.py',
            '--model', 'anthropic.claude-3-5-sonnet-20241022-v2:0',
            '--input', json.dumps(test_input)
        ], capture_output=True, text=True, timeout=30)
        
        print("Command output:")
        print(result.stdout)
        
        if result.stderr:
            print("Errors:")
            print(result.stderr)
            
        print(f"Exit code: {result.returncode}")
        
    except subprocess.TimeoutExpired:
        print("❌ Command timed out (likely due to AWS credentials)")
    except Exception as e:
        print(f"❌ Error running command: {e}")
    
    print("\n" + "=" * 60)
    print("ℹ️  Note: Để tool hoạt động, bạn cần:")
    print("   1. Cấu hình AWS credentials (aws configure)")
    print("   2. Có quyền truy cập AWS Bedrock")
    print("   3. Model được enable trong AWS Bedrock")
    print("🎉 countTokens.py tool test completed!")

if __name__ == "__main__":
    test_countTokens_tool()