import os
from dotenv import load_dotenv
from dataclasses import dataclass
@dataclass(frozen=True)
class Config:
    url: str
    model: str
    api_key: str
    system_prompt: str
    llm_cache: float
    llm_completion: float
    llm_miss: float
    summary_prompt: str
    max_content:int
    keep_content:int

def load_config(env_file:str | None=None) -> Config:
    load_dotenv(env_file)
    return Config(
        url=os.getenv("DEEPSEEK_URL",""),
        model=os.getenv("DEEPSEEK_MODEL",""),
        api_key=os.getenv("DEEPSEEK_API_KEY",""),
        llm_miss=float(os.getenv("LLM_MISS","1.5")),
        llm_cache=float(os.getenv("LLM_CACHE","0.05")),
        llm_completion=float(os.getenv("LLM_COMPLETION","4.5")),
        max_content=int(os.getenv("MAX_CONTENT","10")),
        keep_content=int(os.getenv("KEEP_CONTENT","3")),
        summary_prompt=os.getenv("SUMMARY_PROMPT","简化用户信息，用简短的方式进行简要，保留语义压缩字数，你的输出将作为后续交互的历史摘要信息"),
        system_prompt=os.getenv("SYSTEM_PROMPT","你是一个AI助手，当用户问你问题时，请为用户提供可靠的回答，禁止编造。"),
    )