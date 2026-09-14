from chat_server import ChatServer
from config import load_config
def main():
    cfg = load_config()
    sessions = {}
    while True:
        chat_name = input("选择对话：")
        if chat_name == "exit":
            break
        if chat_name not in sessions:
            chat = ChatServer(cfg)
            sessions[chat_name] = chat
        chat = sessions[chat_name]
        while True:
            user_msg = input("开始对话>： ")
            if user_msg == "exit":
                break
            assistant = chat.chat_create(user_msg)
            print("entp:"+assistant.assistant)
            print(f"成本：{assistant.usage_rep.once.price:.4f}元，用量：{assistant.usage_rep.once.tokens}tokens,命中率{assistant.usage_rep.once.hit_rate:.2f}%,提示词：{assistant.usage_rep.once.prompt}tokens")
            print(f"总成本：{assistant.usage_rep.total.price:.2f}元，总用量：{assistant.usage_rep.total.tokens}tokens,总命中率{assistant.usage_rep.total.hit_rate:.2f}%")
if __name__ == "__main__":
    main()