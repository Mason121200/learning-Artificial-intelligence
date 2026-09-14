from openai import OpenAI
from config import Config
from usage import UsageTokens, TotalPrice, OncePrice
from dataclasses import dataclass

@dataclass
class UsageRep:
    once :OncePrice
    total :TotalPrice
@dataclass
class Response:
    assistant :str
    usage_rep :UsageRep
class ChatServer:
    def __init__(self,cfg:Config):
        self.history = []
        self.client = OpenAI(api_key=cfg.api_key,base_url=cfg.url)
        self.model = cfg.model
        self.system_prompt = cfg.system_prompt
        self.usage = UsageTokens(cache_price=cfg.llm_cache,completion_price = cfg.llm_completion,miss_price = cfg.llm_miss)
        self.keep_content =cfg.keep_content
        self.max_content =cfg.max_content
        self.summary_prompt = cfg.summary_prompt

    def response_create(self,system_prompt:str):
        messages = [{"role": "system", "content":system_prompt}]+self.history
        response = self.client.chat.completions.create(model=self.model,messages=messages)
        usage_rep = self.usage_price(response=response)
        assistant = response.choices[0].message.content
        return Response(assistant=assistant,usage_rep=usage_rep)

    def usage_price(self,response):
        self.usage.usage_create(response=response)
        once = self.usage.once_price()
        price = once.price
        self.usage.record(price)
        total = self.usage.total_price()
        return UsageRep(once=once,total=total)

    def chat_create(self,message:str):
        self.history_reorganize()
        self.save_history(role="user", message=message)
        assistant = self.response_create(self.system_prompt)
        self.save_history(role="assistant",message=assistant.assistant)
        return assistant

    def save_history(self, role,message):
        self.history.append({"role":role,"content":message})

    def history_reorganize(self):
        limit = self.max_content*2
        keep = self.keep_content*2
        if len(self.history)>=limit:
            history_cope = []
            for i in self.history[-keep:]:
                history_cope.append(i)
            for i in range(len(history_cope)):
                self.history.pop()
            summary_rep = self.response_create(self.summary_prompt)
            self.history =[]
            self.history.append({"role":"system","content":"历史摘要："+summary_rep.assistant})
            self.history+=history_cope
