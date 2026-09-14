from dataclasses import dataclass
@dataclass
class OncePrice:
    price: float
    tokens: int
    prompt: int
    hit_rate: float
@dataclass
class TotalPrice:
    price: float
    tokens: int
    hit_rate: float
class UsageTokens:
    def __init__(self,cache_price,miss_price,completion_price):
        self.amount_cache = self.amount_tokens = self.amount_prompt = self.amount_price =0
        self.cache_price = cache_price
        self.miss_price = miss_price
        self.completion_price = completion_price

    def usage_create(self,response):
        usage = response.usage
        self.cache = usage.prompt_cache_hit_tokens
        self.tokens = usage.total_tokens
        self.prompt = usage.prompt_tokens
        self.miss = usage.prompt_cache_miss_tokens
        self.completion = self.tokens - self.prompt

    def record(self,price):
        self.amount_cache += self.cache
        self.amount_tokens += self.tokens
        self.amount_prompt += self.prompt
        self.amount_price += price

    def price(self):
        price = float(self.cache*self.cache_price+self.miss*self.miss_price+self.completion*self.completion_price)/1000000
        return price

    def hit_rate(self,cache,prompt):
        hit_rate = cache/prompt*100
        return hit_rate

    def once_price(self):
        price = self.price()
        hit_rate = self.hit_rate(cache=self.cache,prompt=self.prompt)
        return OncePrice(price=price,hit_rate=hit_rate,tokens=self.tokens,prompt=self.prompt)

    def total_price(self):
        hit_rate = self.hit_rate(cache=self.amount_cache,prompt=self.amount_prompt)
        return TotalPrice(price=self.amount_price,tokens=self.amount_tokens,hit_rate=hit_rate)
