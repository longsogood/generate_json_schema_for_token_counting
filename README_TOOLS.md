# AWS Bedrock Count Tokens Tools

Bộ công cụ để tạo schema và đếm tokens cho AWS Bedrock count_tokens API.

## 📁 Files

### 1. `countTokensSchema.py` - Schema Generator (Streamlit UI)
Tool với giao diện web để tạo JSON schema cho AWS Bedrock count_tokens API.

**Tính năng:**
- ✅ Tạo schema cho `converse` và `invokeModel` 
- ✅ Hỗ trợ nhiều loại content: text, image, document, video, tool use, etc.
- ✅ **Import Log Messages** - Convert log từ format cũ sang schema chuẩn
- ✅ Xử lý `additional_kwargs` cho tool calls
- ✅ Tùy chọn bao gồm system prompts hay không
- ✅ Quick templates và preview

**Chạy:**
```bash
streamlit run countTokensSchema.py
```

### 2. `countTokens.py` - Token Counter (CLI Tool)
Command-line tool để đếm tokens sử dụng AWS Bedrock API.

**Tính năng:**
- ✅ Đếm tokens từ file JSON schema
- ✅ Đếm tokens từ inline input
- ✅ Hỗ trợ nhiều AWS regions
- ✅ Hiển thị kết quả chi tiết

**Chạy:**
```bash
# Từ file schema
python countTokens.py --file converted_schema.json

# Từ inline input
python countTokens.py --model anthropic.claude-3-5-sonnet-20241022-v2:0 --input '{"converse": {"messages": [{"role": "user", "content": [{"text": "Hello"}]}]}}'

# Với region khác
python countTokens.py --file schema.json --region us-west-2
```

## 🔄 Workflow

### Bước 1: Tạo Schema
1. Chạy `streamlit run countTokensSchema.py`
2. Chọn loại input:
   - **converse**: Tạo schema thủ công
   - **invokeModel**: Paste JSON body
   - **importLog**: Convert log cũ sang schema mới ⭐

### Bước 2: Import Log (Tính năng mới)
Nếu bạn có log messages từ hệ thống cũ:

```json
[
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"},
    {"content": "You are helpful"}, // System prompt
    {
        "content": "",
        "additional_kwargs": {
            "tool_calls": [{"id": "tool1", "function": {"name": "search"}}]
        }
    }, // Assistant với tool call
    {
        "content": ["Result data"],
        "additional_kwargs": {"name": "SearchTool"}
    } // User với tool result
]
```

**Logic xử lý:**
- Dict có `role` → message thông thường
- Dict không có `role` và không có `additional_kwargs` → system prompt
- Dict không có `role` nhưng có `additional_kwargs.tool_calls` → assistant message
- Dict không có `role` nhưng có `additional_kwargs.name` → user message

### Bước 3: Đếm Tokens
```bash
python countTokens.py --file converted_schema.json
```

## 📋 Requirements

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `streamlit` - Cho UI tool
- `boto3` - Cho AWS Bedrock API

## ⚙️ AWS Setup

1. **Cài đặt AWS CLI:**
```bash
pip install awscli
aws configure
```

2. **Cấu hình credentials:**
```bash
AWS Access Key ID: your-access-key
AWS Secret Access Key: your-secret-key
Default region: us-east-1
```

3. **Enable Bedrock Models:**
- Vào AWS Console → Bedrock → Model access
- Request access cho các models cần dùng

## 🧪 Testing

Chạy các test scripts:

```bash
# Test schema generator function
python test_parse_log.py
python test_additional_kwargs.py
python test_complex_log.py

# Test CLI tool
python test_countTokens.py
```

## 📊 Supported Models

- `anthropic.claude-3-5-sonnet-20241022-v2:0`
- `anthropic.claude-3-5-haiku-20241022-v1:0`
- `anthropic.claude-3-opus-20240229-v1:0`
- `anthropic.claude-3-sonnet-20240229-v1:0`

## 🔍 Examples

### Example 1: Simple Text
```json
{
  "modelId": "anthropic.claude-3-5-sonnet-20241022-v2:0",
  "input": {
    "converse": {
      "messages": [
        {
          "role": "user",
          "content": [{"text": "Hello, how are you?"}]
        }
      ]
    }
  }
}
```

### Example 2: With System Prompt
```json
{
  "modelId": "anthropic.claude-3-5-sonnet-20241022-v2:0",
  "input": {
    "converse": {
      "messages": [
        {
          "role": "user", 
          "content": [{"text": "What's the weather?"}]
        }
      ],
      "system": [
        {"text": "You are a helpful weather assistant."}
      ]
    }
  }
}
```

### Example 3: Tool Use
```json
{
  "modelId": "anthropic.claude-3-5-sonnet-20241022-v2:0",
  "input": {
    "converse": {
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "toolUse": {
                "toolUseId": "tool_123",
                "name": "get_weather",
                "input": {"location": "New York"}
              }
            }
          ]
        }
      ]
    }
  }
}
```

## 🚀 Quick Start

1. **Tạo schema từ log cũ:**
```bash
streamlit run countTokensSchema.py
# → Chọn "importLog" → Paste log → Generate schema
```

2. **Đếm tokens:**
```bash
python countTokens.py --file converted_schema.json
```

3. **Kết quả:**
```
📊 TOKEN COUNT RESULTS
==================================================
📥 Input Tokens: 25
📤 Output Tokens: 0  
🔢 Total Tokens: 25
==================================================
```

## 🎯 Use Cases

- **Migration**: Convert log messages từ hệ thống cũ sang AWS Bedrock format
- **Cost Estimation**: Tính toán chi phí trước khi gọi API
- **Optimization**: Tối ưu hóa prompts để giảm token count
- **Testing**: Validate schema trước khi deploy production

---

**Created by:** Kilo Code  
**Version:** 1.0.0  
**Last Updated:** 2025-01-23