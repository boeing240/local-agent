from ollama_client import OllamaClient
from tool_registry import ToolRegistry

SYSTEM_PROMPT = (
    "You are a helpful local assistant. You have access to tools for "
    "web search, file operations, task management, and running shell commands. "
    "Use tools when needed. Be concise."
)


class Agent:
    def __init__(self):
        self.client = OllamaClient()
        self.registry = ToolRegistry()
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    def chat(self, user_input: str) -> None:
        self.messages.append({"role": "user", "content": user_input})

        try:
            response = self.client.chat(self.messages, self.registry.get_tool_definitions())
        except Exception as e:
            print(f"[error] {e}\n")
            self.messages.pop()  # убираем сообщение пользователя из истории
            return

        # Resolve tool calls in a loop (model may chain multiple tool calls)
        while response.get("tool_calls"):
            self.messages.append({"role": "assistant", **response})

            for tool_call in response["tool_calls"]:
                name = tool_call["function"]["name"]
                args = tool_call["function"]["arguments"]
                result = self.registry.call(name, args)
                preview = str(result)[:120].replace("\n", " ")
                print(f"  [tool: {name}] -> {preview}")
                self.messages.append({
                    "role": "tool",
                    "name": name,
                    "content": str(result),
                })

            try:
                response = self.client.chat(self.messages, self.registry.get_tool_definitions())
            except Exception as e:
                print(f"[error] {e}\n")
                return

        final = response.get("content", "")
        print(f"Agent: {final}\n")
        self.messages.append({"role": "assistant", "content": final})
