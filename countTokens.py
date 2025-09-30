#!/usr/bin/env python3
"""
AWS Bedrock Count Tokens Tool
Tool để đếm tokens cho các messages sử dụng AWS Bedrock count_tokens API
"""

import json
import boto3
import argparse
import sys
from typing import Dict, Any, List, Optional
from botocore.exceptions import ClientError, BotoCoreError

class BedrockTokenCounter:
    """Class để đếm tokens sử dụng AWS Bedrock"""
    
    def __init__(self, region_name: str = 'us-east-1', aws_access_key_id: str = None, aws_secret_access_key: str = None):
        """
        Initialize Bedrock client
        
        Args:
            region_name: AWS region name
        """
        try:
            self.bedrock_client = boto3.client('bedrock-runtime', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        except Exception as e:
            print(f"❌ Error initializing Bedrock client: {e}")
            sys.exit(1)
    
    def count_tokens(self, model_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Đếm tokens cho input data
        
        Args:
            model_id: Model ID (e.g., anthropic.claude-3-5-sonnet-20241022-v2:0)
            input_data: Input data theo format AWS Bedrock
            
        Returns:
            Response từ count_tokens API
        """
        try:
            request_body = {
                "modelId": model_id,
                "input": input_data
            }
            
            print(f"🔍 Counting tokens for model: {model_id}")
            print(f"📊 Input data: {json.dumps(input_data, indent=2, ensure_ascii=False)}")
            
            response = self.bedrock_client.count_tokens(**request_body)
            
            return response
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            print(f"❌ AWS Client Error [{error_code}]: {error_message}")
            return None
            
        except BotoCoreError as e:
            print(f"❌ BotoCore Error: {e}")
            return None
            
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    def count_tokens_from_file(self, file_path: str) -> Dict[str, Any]:
        """
        Đếm tokens từ file JSON
        
        Args:
            file_path: Path to JSON file chứa schema
            
        Returns:
            Response từ count_tokens API
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                schema = json.load(f)
            
            model_id = schema.get('modelId')
            input_data = schema.get('input')
            
            if not model_id:
                print("❌ Missing 'modelId' in schema")
                return None
                
            if not input_data:
                print("❌ Missing 'input' in schema")
                return None
            
            return self.count_tokens(model_id, input_data)
            
        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
            return None
            
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in file: {e}")
            return None
            
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return None
    
    def print_token_count_result(self, result: Dict[str, Any]):
        """
        In kết quả đếm tokens một cách đẹp mắt
        
        Args:
            result: Response từ count_tokens API
        """
        if not result:
            return
            
        print("\n" + "="*50)
        print("📊 TOKEN COUNT RESULTS")
        print("="*50)
        
        # Input tokens
        input_tokens = result.get('inputTokens', 0)
        print(f"📥 Input Tokens: {input_tokens:,}")
        
        # Output tokens (nếu có)
        output_tokens = result.get('outputTokens', 0)
        if output_tokens > 0:
            print(f"📤 Output Tokens: {output_tokens:,}")
        
        # Total tokens
        total_tokens = input_tokens + output_tokens
        print(f"🔢 Total Tokens: {total_tokens:,}")
        
        # Token breakdown (nếu có)
        if 'tokenBreakdown' in result:
            breakdown = result['tokenBreakdown']
            print(f"\n🔍 Token Breakdown:")
            for key, value in breakdown.items():
                print(f"  • {key}: {value:,}")
        
        print("="*50)
        return result

def main():
    """Main function"""
#     parser = argparse.ArgumentParser(
#         description="AWS Bedrock Count Tokens Tool",
#         formatter_class=argparse.RawDescriptionHelpFormatter,
#         epilog="""
# Examples:
#   python countTokens.py --file schema.json
#   python countTokens.py --model anthropic.claude-3-5-sonnet-20241022-v2:0 --input '{"converse": {"messages": [{"role": "user", "content": [{"text": "Hello"}]}]}}'
#   python countTokens.py --file converted_schema.json --region us-west-2
#         """
#     )
    
#     parser.add_argument(
#         '--file', '-f',
#         type=str,
#         help='Path to JSON file chứa schema'
#     )
    
#     parser.add_argument(
#         '--model', '-m',
#         type=str,
#         help='Model ID (e.g., anthropic.claude-3-5-sonnet-20241022-v2:0)'
#     )
    
#     parser.add_argument(
#         '--input', '-i',
#         type=str,
#         help='Input data as JSON string'
#     )
    
#     parser.add_argument(
#         '--region', '-r',
#         type=str,
#         default='us-east-1',
#         help='AWS region (default: us-east-1)'
#     )
    
#     args = parser.parse_args()
    
#     # Validate arguments
#     if not args.file and not (args.model and args.input):
#         parser.error("Either --file or both --model and --input are required")
    from dotenv import load_dotenv
    import os

    # Load environment variables from .env file
    load_dotenv(".env")

    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION")

    # Initialize counter
    counter = BedrockTokenCounter(region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    
    # # Count tokens
    # if args.file:
    #     print(f"📁 Reading schema from file: {args.file}")
    #     result = counter.count_tokens_from_file(args.file)
    # else:
    #     try:
    #         input_data = json.loads(args.input)
    #         result = counter.count_tokens(args.model, input_data)
    #     except json.JSONDecodeError as e:
    #         print(f"❌ Invalid JSON in --input: {e}")
    #         sys.exit(1)

    with open("test_user_data.json", "r") as f:
        user_data = json.load(f)

    result = counter.count_tokens("anthropic.claude-sonnet-4-20250514-v1:0", {"converse": user_data})
    
    # Print results
    if result:
        counter.print_token_count_result(result)
        print("✅ Token counting completed successfully!")
    else:
        print("❌ Token counting failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()