from types import SimpleNamespace
from chat_server import ChatServer
from config import Config

cfg = Config(max_content=2,keep_content=1,model="chat",url="url",api_key="key",llm_miss=1.5,llm_cache=0.05,llm_completion=4.5,system_prompt="",summary_prompt="")

def fake_response(content,cache,prompt,total,miss,**kwargs):
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))],
        usage = SimpleNamespace(
            total_tokens = total,
            prompt_tokens = prompt,
            prompt_cache_hit_tokens = cache,
            prompt_cache_miss_tokens = miss,
        ),
    )

def fake_create(model,messages,**kwargs):
    return fake_response(content="集成测试回复1",cache=10,prompt=10,total=20,miss=10)

def test_chat_create_saves_history_and_usage(monkeypatch):
    chat = ChatServer(cfg)
    monkeypatch.setattr(chat.client.chat.completions,"create",fake_create)
    chat.chat_create("测试1")
    assert chat.usage.cache == 10
    assert chat.usage.prompt == 10
    assert chat.usage.tokens ==20
    assert chat.usage.miss == 10
    assert len(chat.history) ==2
    assert chat.history[0]["role"] == "user" and chat.history[0]["content"] == "测试1"
    assert chat.usage.price() ==  ((0.5+15+45)/1000000)


def test_history_reorganize_summarizes(monkeypatch):
    chat = ChatServer(cfg)
    monkeypatch.setattr(chat.client.chat.completions,"create",fake_create)
    chat.chat_create("测试2")
    chat.chat_create("测试2—重复")
    chat.chat_create("测试2—重复")
    assert chat.usage.amount_price == ((0.5+15+45)/1000000)*4
    assert chat.usage.amount_tokens ==80
    assert len(chat.history) ==5
    assert chat.history[0]["role"] == "system" and chat.history[0]["content"]=="历史摘要：集成测试回复1"


def test_history_reorganize_with_large_limit(monkeypatch):
    cfg = Config(max_content=5,keep_content=3,model="chat",url="url",api_key="key",llm_miss=1.5,llm_cache=0.05,llm_completion=4.5,system_prompt="",summary_prompt="")
    chat = ChatServer(cfg)
    monkeypatch.setattr(chat.client.chat.completions,"create",fake_create)
    chat.chat_create("测试3")
    chat.chat_create("测试3—重复")
    chat.chat_create("测试3—重复")
    chat.chat_create("测试3—重复")
    chat.chat_create("测试3—重复")
    chat.chat_create("测试3—重复")
    assert chat.usage.amount_price == ((0.5+15+45)/1000000)*7
    assert chat.usage.amount_tokens ==140
    assert len(chat.history) ==9
    assert chat.history[0]["role"] == "system" and chat.history[0]["content"]=="历史摘要：集成测试回复1"

