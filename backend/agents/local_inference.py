import os
from langchain_core.language_models.chat_models import BaseChatModel

# In production, we use vLLM for high-throughput local serving
# from langchain_community.llms import VLLMOpenAI

def get_local_financial_llm() -> BaseChatModel:
    """
    Returns an instance of the locally hosted, fine-tuned Llama-3-8B Financial model.
    Connects to a vLLM server running on the GPU instance.
    """
    vllm_url = os.getenv("VLLM_API_BASE", "http://localhost:8000/v1")
    
    # For LangChain compatibility, we can use ChatOpenAI pointing to vLLM
    from langchain_openai import ChatOpenAI
    
    llm = ChatOpenAI(
        model="finance-llama3-8b-lora",
        openai_api_key="EMPTY", # vLLM doesn't require an actual OpenAI key
        openai_api_base=vllm_url,
        max_tokens=4096,
        temperature=0.1
    )
    
    return llm
