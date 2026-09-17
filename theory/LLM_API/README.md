# LLM API（API 调用的基础理论）

> 本篇记录我对「调用大模型 API」这条链路的基础理解：从基础概念，到请求 / 响应结构，再到多轮对话与工程实践。

## 一、基础概念

**1. API（Application Programming Interface）**：即应用程序接口，是软件开发时对外提供的一组调用约定。通过 API，外部程序可以使用程序内部功能。调用方程序根据约定好的地址、格式、参数，发起 API 调用请求，程序根据请求内容处理并按约定格式返回结果。

**2. 模块**：Python 中.py文件就是一个模块，模块化就是指将程序按功能职责拆分成多个模块的设计，通常来说，模块应该是一组目标一致、功能相关、共同完成一个功能的代码文件。一个模块遵守四个原则——单一职责、单向依赖、通过接口交互、可单独测试。

**3. OOP**：面向对象编程，现代编程的常用方式。其核心思想是「一切事物皆可看作对象」（类：class），每个 class 都是一个模板，模板中定义了这个类的属性和方法，可以据此创建无数个实例（instance）。核心概念有封装、抽象、继承、多态。举例：能把「人类」这种对象批量造出来的模板，就是一个类。而所有人共有、由类统一定义的属性叫**类属性**，如种类、人类发展史(所有人共同拥有的属性)；每个人各自不同的属性叫**实例属性**，如姓名、身高、体重、腰围。而 OOP 中的方法可以看作是为这个类编写的技能，如直立行走、语言能力、开车、编程、建筑等。这里仅作简单了解，在 API 调用实践中不会深入。

## 二、大模型与调用协议

**4. OpenAI API**：OpenAI 公司规定的大语言模型（Large Language Model）调用接口，是OpenAI制定的标准化LLM调用接口，Deepseek等各大厂商都提供与之兼容的接口，通过 OpenAI 接口，所有程序都可以调用 LLM 并使用其提供的语言交流、逻辑推理等功能，在此基础上，通过编程就能实现 AI 的交互功能，并延伸出更多 AI 应用技术。

**5. LLM（Large Language Model）**：这里简述一下工作原理。LLM 是基于 Transformer 架构开发的模型，在实际的工作过程中，LLM 会将输入的语句切分成单独的 token 进行计算，基于当前所有 tokens 的计算结果预测下一个 token，通过多次计算直到出现结束标识时结束计算。在这个过程中，LLM 会同时（并行）处理所有 token，再按顺序逐个输出 token。

## 三、请求与响应

**6. JSON（JavaScript Object Notation）**：一种纯文本格式的结构化文本数据，不是数据类型，跨语言通用，所以常被用作跨系统、跨语言的数据传输载体。API 中的请求体和响应体都是 JSON 格式的文本。

**7. 请求体 JSON 结构(示例)**：

```json
{
    "model": "deepseek-v4-flash",
    "messages": [
        { "role": "system", "content": "你是一个AI助手！" },
        { "role": "user", "content": "Hello!" }
    ]
}
```

**8. model**：调用 OpenAI 接口时，需要在请求体的 model 字段里写明模型名称，用来指定访问哪个模型。

**9. messages**：LLM 本身不具备记忆功能，它只会对请求体中 messages 字段里的内容进行处理并根据最终的结果进行回复。它是上下文窗口的一部分，也是大家常说的AI记忆，模型能记住多少东西，取决于 messages 中数据的多寡。

**10. 响应体 JSON 结构(示例)**：

```json
{
    "id": "17879906-de....",
    "object": "chat.completion",
    "created": 1789361976,
    "model": "deepseek-flash",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Hello! How can I help you today?",
                "reasoning_content": "The user just said \"Hello!\" — a simple greeting."
            },
            "logprobs": null,
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 32,
        "completion_tokens": 51,
        "total_tokens": 83,
        "prompt_tokens_details": { "cached_tokens": 0 },
        "completion_tokens_details": { "reasoning_tokens": 41 },
        "prompt_cache_hit_tokens": 0,
        "prompt_cache_miss_tokens": 32
    },
    "system_fingerprint": "aeb56401ca74..."
}
```

**11. choices**：在实际的交互过程中，LLM 会将结果通过响应体返回，结构如上，LLM 的回复内容通常放在 choices 字段中，如回复的消息 message，以及调用时的一些参数设置。

**12. message**：LLM 的回复和思考内容都在 message 中：role 标记这条消息的角色，content 是回复内容，reasoning_content 是思考过程。

**13. usage 用量**：LLM 会将每次调用消耗的用量数据放在 usage 中，获取到用量信息可以实现对调用用量的监控和成本控制，其中 prompt_tokens 是提示词用量、total_tokens 是总用量、prompt_cache_hit_tokens 是命中用量、prompt_cache_miss_tokens 是未命中用量。

## 四、多轮对话与上下文管理

**14. 多轮对话**：要实现多轮对话，就需要对 messages 字段的内容进行组装，通过向 messages 中添加 {"role":"user","content":"message"} 实现。其中 role 常见的有三种——system、user、assistant，分别表示 content 中的内容是属于哪种类型的数据：system 是提示词数据、user 是用户问题、assistant 是 LLM 系统回复内容。

**15. 历史摘要**：为了避免历史消息超出模型的上下文窗口限制或自定义的用量成本限制，可以通过额外调用 LLM、本地小模型或程序裁剪的方式实现对信息的压缩，以达到减少tokens数量的目的。

## 五、工程实践

**16. 测试**：可以通过编写单元测试 / 集成测试来验证程序：后续改动时能快速判断是否破坏了原有逻辑，便于定位问题。

**17. dataclass**：dataclass 是一种数据载体。在 Python 中，用 @dataclass 只需定义「字段名 + 类型」，就能完成一个数据类的定义——本质上它是「无行为数据类」的定义模板。定义成类之后，参数使用起来更方便,在类定义时需在上方添加@dataclass，同时可以通过frozen=True使得其具备只读属性，创建后实例字段不会被更改。

**18. monkeypatch**：可在测试中**临时替换**代码里的对象、属性、字典项、环境变量……通过打桩，测试时不必真的调用 API 或改动真实数据，就能验证逻辑。
