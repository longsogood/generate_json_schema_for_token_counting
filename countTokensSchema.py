import streamlit as st
import json
import base64
from typing import Dict, Any, List, Optional

def parse_log_messages(log_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Convert log messages format to AWS Bedrock schema format
    
    Input format:
    [
        0: {"role": "user", "content": "..."},
        1: {"role": "assistant", "content": "..."},
        2: {"content": "..."} # system prompt (no role)
    ]
    
    Output format:
    {
        "messages": [...],
        "system": [...] # if any system prompts exist
    }
    """
    messages = []
    system_messages = []
    
    for item in log_data:
        if isinstance(item, dict):
            # Check if it's a system prompt (no role, only content)
            if "role" not in item and "content" in item:
                # System prompt
                system_messages.append({
                    "text": str(item["content"])
                })
            elif "role" in item and "content" in item:
                # Regular message with role
                role = item["role"]
                content = item["content"]
                
                # Convert content to proper format
                if isinstance(content, str):
                    # Simple text content
                    formatted_content = [{"text": content}]
                elif isinstance(content, list):
                    # Already in list format, keep as is
                    formatted_content = content
                elif isinstance(content, dict):
                    # Single content object, wrap in list
                    formatted_content = [content]
                else:
                    # Fallback: convert to text
                    formatted_content = [{"text": str(content)}]
                
                messages.append({
                    "role": role,
                    "content": formatted_content
                })
    
    # Build result
    result = {"messages": messages}
    if system_messages:
        result["system"] = system_messages
    
    return result

def main():
    st.set_page_config(page_title="AWS Bedrock Count Tokens Schema Generator", layout="wide")

    st.title("🔧 AWS Bedrock Count Tokens Schema Generator")
    st.markdown("**Tạo JSON schema đầy đủ cho Langfuse logging với AWS Bedrock count_tokens API**")

    # Initialize session state
    if 'schema_data' not in st.session_state:
        st.session_state.schema_data = {'modelId': '', 'input': {}}

    col1, col2 = st.columns([1.2, 0.8])

    with col1:
        st.header("📝 Input Configuration")

        # Model ID với suggestions
        model_suggestions = [
            "anthropic.claude-3-5-sonnet-20241022-v2:0",
            "anthropic.claude-3-5-haiku-20241022-v1:0", 
            "anthropic.claude-3-opus-20240229-v1:0",
            "anthropic.claude-3-sonnet-20240229-v1:0"
        ]

        st.session_state.schema_data['modelId'] = st.selectbox(
            "**Model ID**", 
            options=[""] + model_suggestions + ["Custom..."],
            index=0
        )

        if st.session_state.schema_data['modelId'] == "Custom...":
            st.session_state.schema_data['modelId'] = st.text_input("Custom Model ID")

        # Choose input type
        input_type = st.radio("**Chọn loại input:**", ["converse", "invokeModel", "importLog"])

        if input_type == "converse":
            st.subheader("🗨️ Converse Configuration")

            # Messages
            st.markdown("**Messages:**")
            num_messages = st.number_input("Số lượng messages", min_value=1, max_value=10, value=1)

            messages = []
            for i in range(num_messages):
                with st.expander(f"📨 Message {i+1}", expanded=True):
                    role = st.selectbox(f"Role", ["user", "assistant"], key=f"role_{i}")

                    # Content types với description
                    content_options = {
                        "text": "📝 Text content",
                        "image": "🖼️ Image content", 
                        "document": "📄 Document content",
                        "video": "🎥 Video content",
                        "toolUse": "🔧 Tool use request",
                        "toolResult": "⚙️ Tool result response",
                        "guardContent": "🛡️ Guard content assessment",
                        "cachePoint": "💾 Cache point marker",
                        "reasoningContent": "🧠 Reasoning content (CoT)",
                        "citationsContent": "📚 Citations content"
                    }

                    content_types = st.multiselect(
                        f"Content types cho message {i+1}",
                        list(content_options.keys()),
                        format_func=lambda x: content_options[x],
                        key=f"content_types_{i}"
                    )

                    content = []
                    for content_type in content_types:
                        st.markdown(f"**{content_options[content_type]}**")

                        if content_type == "text":
                            text_content = st.text_area(
                                f"Text content", 
                                key=f"text_{i}",
                                height=100,
                                placeholder="Enter your text message here..."
                            )
                            if text_content:
                                content.append({"text": text_content})

                        elif content_type == "image":
                            col_img1, col_img2 = st.columns(2)
                            with col_img1:
                                img_format = st.selectbox(
                                    f"Image format", 
                                    ["png", "jpeg", "gif", "webp"],
                                    key=f"img_format_{i}"
                                )
                            with col_img2:
                                img_source_type = st.selectbox(
                                    f"Image source",
                                    ["bytes", "s3Location"],
                                    key=f"img_source_{i}"
                                )

                            if img_source_type == "bytes":
                                uploaded_file = st.file_uploader(
                                    f"Upload image",
                                    type=['png', 'jpg', 'jpeg', 'gif', 'webp'],
                                    key=f"img_upload_{i}"
                                )
                                if uploaded_file:
                                    img_bytes = uploaded_file.read()
                                    content.append({
                                        "image": {
                                            "format": img_format,
                                            "source": {"bytes": base64.b64encode(img_bytes).decode()}
                                        }
                                    })
                            else:
                                s3_uri = st.text_input(f"S3 URI", key=f"s3_uri_{i}", placeholder="s3://bucket-name/path/to/image.jpg")
                                bucket_owner = st.text_input(f"Bucket Owner (optional)", key=f"bucket_owner_{i}")
                                if s3_uri:
                                    s3_source = {"uri": s3_uri}
                                    if bucket_owner:
                                        s3_source["bucketOwner"] = bucket_owner
                                    content.append({
                                        "image": {
                                            "format": img_format,
                                            "source": {"s3Location": s3_source}
                                        }
                                    })

                        elif content_type == "document":
                            doc_col1, doc_col2 = st.columns(2)
                            with doc_col1:
                                doc_format = st.selectbox(
                                    f"Document format",
                                    ["pdf", "csv", "doc", "docx", "xls", "xlsx", "html", "txt", "md"],
                                    key=f"doc_format_{i}"
                                )
                            with doc_col2:
                                doc_name = st.text_input(f"Document name", key=f"doc_name_{i}", placeholder="document.pdf")

                            doc_source_type = st.selectbox(
                                f"Document source",
                                ["text", "bytes", "s3Location", "content"],
                                key=f"doc_source_type_{i}"
                            )

                            doc_context = st.text_input(f"Document context (optional)", key=f"doc_context_{i}")
                            enable_citations = st.checkbox(f"Enable citations", key=f"doc_citations_{i}")

                            doc_source = {}
                            if doc_source_type == "text":
                                doc_text = st.text_area(f"Document text", key=f"doc_text_{i}", height=100)
                                if doc_text:
                                    doc_source["text"] = doc_text
                            elif doc_source_type == "bytes":
                                doc_file = st.file_uploader(f"Upload document", type=['pdf', 'csv', 'doc', 'docx', 'xls', 'xlsx', 'html', 'txt', 'md'], key=f"doc_upload_{i}")
                                if doc_file:
                                    doc_bytes = doc_file.read()
                                    doc_source["bytes"] = base64.b64encode(doc_bytes).decode()
                            elif doc_source_type == "s3Location":
                                s3_uri = st.text_input(f"S3 URI", key=f"doc_s3_uri_{i}")
                                bucket_owner = st.text_input(f"Bucket Owner (optional)", key=f"doc_bucket_owner_{i}")
                                if s3_uri:
                                    s3_loc = {"uri": s3_uri}
                                    if bucket_owner:
                                        s3_loc["bucketOwner"] = bucket_owner
                                    doc_source["s3Location"] = s3_loc
                            elif doc_source_type == "content":
                                content_text = st.text_area(f"Content text", key=f"doc_content_{i}")
                                if content_text:
                                    doc_source["content"] = [{"text": content_text}]

                            if doc_name and doc_source:
                                doc_obj = {
                                    "format": doc_format,
                                    "name": doc_name,
                                    "source": doc_source
                                }
                                if doc_context:
                                    doc_obj["context"] = doc_context
                                if enable_citations:
                                    doc_obj["citations"] = {"enabled": True}
                                content.append({"document": doc_obj})

                        elif content_type == "video":
                            vid_col1, vid_col2 = st.columns(2)
                            with vid_col1:
                                vid_format = st.selectbox(
                                    f"Video format",
                                    ["mkv", "mov", "mp4", "webm", "flv", "mpeg", "mpg", "wmv", "three_gp"],
                                    key=f"vid_format_{i}"
                                )
                            with vid_col2:
                                vid_source_type = st.selectbox(
                                    f"Video source",
                                    ["bytes", "s3Location"],
                                    key=f"vid_source_{i}"
                                )

                            if vid_source_type == "bytes":
                                vid_file = st.file_uploader(f"Upload video", type=['mkv', 'mov', 'mp4', 'webm', 'flv', 'mpeg', 'mpg', 'wmv', '3gp'], key=f"vid_upload_{i}")
                                if vid_file:
                                    vid_bytes = vid_file.read()
                                    content.append({
                                        "video": {
                                            "format": vid_format,
                                            "source": {"bytes": base64.b64encode(vid_bytes).decode()}
                                        }
                                    })
                            else:
                                s3_uri = st.text_input(f"S3 URI", key=f"vid_s3_uri_{i}")
                                bucket_owner = st.text_input(f"Bucket Owner (optional)", key=f"vid_bucket_owner_{i}")
                                if s3_uri:
                                    s3_source = {"uri": s3_uri}
                                    if bucket_owner:
                                        s3_source["bucketOwner"] = bucket_owner
                                    content.append({
                                        "video": {
                                            "format": vid_format,
                                            "source": {"s3Location": s3_source}
                                        }
                                    })

                        elif content_type == "toolUse":
                            tool_use_id = st.text_input(f"Tool Use ID", key=f"tool_use_id_{i}", placeholder="tooluse_abc123")
                            tool_name = st.text_input(f"Tool Name", key=f"tool_name_{i}", placeholder="get_weather")
                            tool_input = st.text_area(f"Tool Input (JSON)", key=f"tool_input_{i}", placeholder='{"location": "New York", "unit": "celsius"}')

                            if tool_use_id and tool_name and tool_input:
                                try:
                                    parsed_input = json.loads(tool_input)
                                    content.append({
                                        "toolUse": {
                                            "toolUseId": tool_use_id,
                                            "name": tool_name,
                                            "input": parsed_input
                                        }
                                    })
                                except json.JSONDecodeError:
                                    st.error("❌ Invalid JSON format in tool input")

                        elif content_type == "toolResult":
                            tool_result_id = st.text_input(f"Tool Use ID", key=f"tool_result_id_{i}")
                            tool_status = st.selectbox(f"Status", ["success", "error"], key=f"tool_status_{i}")

                            # Tool result content
                            result_content_types = st.multiselect(
                                f"Result content types",
                                ["json", "text", "image", "document", "video"],
                                key=f"tool_result_content_{i}"
                            )

                            result_content = []
                            for result_type in result_content_types:
                                if result_type == "json":
                                    json_content = st.text_area(f"JSON result", key=f"tool_json_{i}")
                                    if json_content:
                                        try:
                                            parsed_json = json.loads(json_content)
                                            result_content.append({"json": parsed_json})
                                        except json.JSONDecodeError:
                                            st.error("❌ Invalid JSON format")
                                elif result_type == "text":
                                    text_result = st.text_area(f"Text result", key=f"tool_text_{i}")
                                    if text_result:
                                        result_content.append({"text": text_result})

                            if tool_result_id and result_content:
                                content.append({
                                    "toolResult": {
                                        "toolUseId": tool_result_id,
                                        "content": result_content,
                                        "status": tool_status
                                    }
                                })

                        elif content_type == "guardContent":
                            guard_type = st.selectbox(f"Guard content type", ["text", "image"], key=f"guard_type_{i}")

                            if guard_type == "text":
                                guard_text = st.text_area(f"Guard text", key=f"guard_text_{i}")
                                guard_qualifiers = st.multiselect(
                                    f"Qualifiers",
                                    ["grounding_source", "query", "guard_content"],
                                    key=f"guard_qualifiers_{i}"
                                )

                                if guard_text:
                                    guard_obj = {"text": {"text": guard_text}}
                                    if guard_qualifiers:
                                        guard_obj["text"]["qualifiers"] = guard_qualifiers
                                    content.append({"guardContent": guard_obj})

                            elif guard_type == "image":
                                guard_img_format = st.selectbox(f"Guard image format", ["png", "jpeg"], key=f"guard_img_format_{i}")
                                guard_img_file = st.file_uploader(f"Upload guard image", type=['png', 'jpg', 'jpeg'], key=f"guard_img_{i}")

                                if guard_img_file:
                                    img_bytes = guard_img_file.read()
                                    content.append({
                                        "guardContent": {
                                            "image": {
                                                "format": guard_img_format,
                                                "source": {"bytes": base64.b64encode(img_bytes).decode()}
                                            }
                                        }
                                    })

                        elif content_type == "cachePoint":
                            cache_type = st.selectbox(f"Cache point type", ["default"], key=f"cache_type_{i}")
                            content.append({"cachePoint": {"type": cache_type}})

                        elif content_type == "reasoningContent":
                            reasoning_text = st.text_area(f"Reasoning text", key=f"reasoning_text_{i}", height=100)
                            reasoning_signature = st.text_input(f"Reasoning signature (optional)", key=f"reasoning_sig_{i}")
                            redacted_content = st.text_area(f"Redacted content (optional)", key=f"redacted_{i}")

                            reasoning_obj = {}
                            if reasoning_text:
                                reasoning_text_obj = {"text": reasoning_text}
                                if reasoning_signature:
                                    reasoning_text_obj["signature"] = reasoning_signature
                                reasoning_obj["reasoningText"] = reasoning_text_obj

                            if redacted_content:
                                reasoning_obj["redactedContent"] = redacted_content.encode()

                            if reasoning_obj:
                                content.append({"reasoningContent": reasoning_obj})

                        elif content_type == "citationsContent":
                            citations_text = st.text_area(f"Citations content text", key=f"citations_text_{i}")
                            citation_title = st.text_input(f"Citation title", key=f"citation_title_{i}")
                            citation_source = st.text_area(f"Citation source content", key=f"citation_source_{i}")

                            if citations_text and citation_title:
                                citations_obj = {
                                    "content": [{"text": citations_text}],
                                    "citations": [{
                                        "title": citation_title,
                                        "sourceContent": [{"text": citation_source}] if citation_source else []
                                    }]
                                }
                                content.append({"citationsContent": citations_obj})

                    if content:
                        messages.append({"role": role, "content": content})

            # System messages
            system_messages = []
            if st.checkbox("**Thêm system messages**"):
                with st.expander("System Messages Configuration"):
                    system_text = st.text_area("System message text", height=100)

                    # System guard content
                    if st.checkbox("Add guard content to system"):
                        sys_guard_type = st.selectbox("System guard type", ["text", "image"])
                        if sys_guard_type == "text":
                            sys_guard_text = st.text_area("System guard text")
                            sys_guard_qualifiers = st.multiselect("System guard qualifiers", ["grounding_source", "query", "guard_content"])

                    # System cache point
                    sys_cache_point = st.checkbox("Add cache point to system")

                    if system_text:
                        sys_msg = {"text": system_text}
                        if 'sys_guard_text' in locals() and sys_guard_text:
                            guard_obj = {"text": {"text": sys_guard_text}}
                            if 'sys_guard_qualifiers' in locals() and sys_guard_qualifiers:
                                guard_obj["text"]["qualifiers"] = sys_guard_qualifiers
                            sys_msg["guardContent"] = guard_obj
                        if sys_cache_point:
                            sys_msg["cachePoint"] = {"type": "default"}
                        system_messages.append(sys_msg)

            # Build converse input
            converse_input = {"messages": messages}
            if system_messages:
                converse_input["system"] = system_messages

            st.session_state.schema_data['input'] = {"converse": converse_input}

        elif input_type == "importLog":
            st.subheader("📥 Import Log Messages")
            st.markdown("**Import và convert log messages từ format cũ sang schema chuẩn**")
            
            # Log input area
            log_content = st.text_area(
                "**Paste Log JSON:**",
                height=300,
                placeholder='''[
    {
        "role": "user",
        "content": "Hello, how are you?"
    },
    {
        "role": "assistant",
        "content": "I'm doing well, thank you!"
    },
    {
        "content": "You are a helpful assistant."
    }
]''',
                help="Paste log messages ở đây. Dict không có 'role' sẽ được coi là system prompt."
            )
            
            if log_content:
                try:
                    # Parse and validate JSON
                    log_data = json.loads(log_content)
                    
                    if not isinstance(log_data, list):
                        st.error("❌ Log data phải là một array/list")
                    else:
                        # Convert using our parse function
                        converted_data = parse_log_messages(log_data)
                        
                        # Update session state
                        st.session_state.schema_data['input'] = {"converse": converted_data}
                        
                        # Show preview
                        st.success("✅ Log đã được convert thành công!")
                        
                        with st.expander("👀 Preview Converted Data", expanded=True):
                            st.json(converted_data)
                        
                        # Option to append to existing messages
                        if st.button("📝 Append to Current Schema", type="secondary"):
                            current_input = st.session_state.schema_data.get('input', {})
                            if 'converse' in current_input:
                                # Merge messages
                                existing_messages = current_input['converse'].get('messages', [])
                                existing_system = current_input['converse'].get('system', [])
                                
                                new_messages = converted_data.get('messages', [])
                                new_system = converted_data.get('system', [])
                                
                                merged_converse = {
                                    'messages': existing_messages + new_messages
                                }
                                
                                if existing_system or new_system:
                                    merged_converse['system'] = existing_system + new_system
                                
                                st.session_state.schema_data['input'] = {"converse": merged_converse}
                                st.success("✅ Đã append log vào schema hiện tại!")
                                st.rerun()
                            else:
                                st.info("ℹ️ Không có schema hiện tại để append. Sử dụng log làm schema chính.")
                        
                except json.JSONDecodeError as e:
                    st.error(f"❌ Invalid JSON format: {str(e)}")
                except Exception as e:
                    st.error(f"❌ Error processing log: {str(e)}")

        else:  # invokeModel
            st.subheader("🤖 Invoke Model Configuration")
            body_content = st.text_area(
                "**Request Body (JSON)**",
                height=200,
                placeholder='{"messages": [{"role": "user", "content": "Hello"}], "max_tokens": 1000}'
            )

            if body_content:
                try:
                    # Validate JSON
                    json.loads(body_content)
                    st.session_state.schema_data['input'] = {
                        "invokeModel": {"body": body_content.encode()}
                    }
                    st.success("✅ Valid JSON format")
                except json.JSONDecodeError:
                    st.error("❌ Invalid JSON format")

    with col2:
        st.header("📋 Generated Schema")

        if st.button("🚀 **Generate Schema**", type="primary", use_container_width=True):
            # Clean empty values
            schema = clean_empty_values(st.session_state.schema_data)

            # Display formatted JSON
            st.code(json.dumps(schema, indent=2, ensure_ascii=False, default=str), language="json")

            # Copy button
            st.download_button(
                label="💾 Download JSON Schema",
                data=json.dumps(schema, indent=2, ensure_ascii=False, default=str),
                file_name="bedrock_count_tokens_schema.json",
                mime="application/json"
            )

            st.success("✅ Schema generated successfully!")

        # Quick templates
        st.subheader("⚡ Quick Templates")
        if st.button("📝 Simple Text Message"):
            st.session_state.schema_data = {
                'modelId': 'anthropic.claude-3-5-sonnet-20241022-v2:0',
                'input': {
                    'converse': {
                        'messages': [{
                            'role': 'user',
                            'content': [{'text': 'Hello, how are you?'}]
                        }]
                    }
                }
            }
            st.rerun()

        if st.button("🔧 Tool Use Example"):
            st.session_state.schema_data = {
                'modelId': 'anthropic.claude-3-5-sonnet-20241022-v2:0',
                'input': {
                    'converse': {
                        'messages': [{
                            'role': 'user',
                            'content': [{
                                'toolUse': {
                                    'toolUseId': 'tooluse_example_123',
                                    'name': 'get_weather',
                                    'input': {'location': 'New York', 'unit': 'celsius'}
                                }
                            }]
                        }]
                    }
                }
            }
            st.rerun()

        if st.button("📥 Import Log Example"):
            # Example log data that will be converted
            example_log = [
                {"role": "user", "content": "Hello, how are you?"},
                {"role": "assistant", "content": "I'm doing well, thank you! How can I help you today?"},
                {"content": "You are a helpful AI assistant."}  # System prompt
            ]
            
            # Convert using our function
            converted_data = parse_log_messages(example_log)
            
            st.session_state.schema_data = {
                'modelId': 'anthropic.claude-3-5-sonnet-20241022-v2:0',
                'input': {'converse': converted_data}
            }
            st.rerun()

        # Preview current data
        if st.session_state.schema_data.get('input'):
            st.subheader("👀 Current Data Preview")
            preview_data = clean_empty_values(st.session_state.schema_data)
            st.json(preview_data)

def clean_empty_values(data: Any) -> Any:
    """Remove empty values from nested dictionary/list"""
    if isinstance(data, dict):
        cleaned = {}
        for key, value in data.items():
            cleaned_value = clean_empty_values(value)
            if cleaned_value not in [None, "", [], {}]:
                cleaned[key] = cleaned_value
        return cleaned
    elif isinstance(data, list):
        return [clean_empty_values(item) for item in data if clean_empty_values(item) not in [None, "", [], {}]]
    else:
        return data

if __name__ == "__main__":
    main()