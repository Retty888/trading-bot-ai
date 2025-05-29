
import openai

def get_openai_usage(api_key: str):
    try:
        openai.api_key = api_key
        usage_data = openai.Usage.retrieve()
        total_tokens = usage_data.get("total_tokens", 0)
        return {"total_tokens": total_tokens}
    except Exception as e:
        print(f"❌ Failed to retrieve OpenAI usage: {e}")
        return None
