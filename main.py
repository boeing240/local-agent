try:
    import readline  # enables up-arrow history in the REPL (Unix)
except ImportError:
    pass  # not available on Windows, that's fine

from agent import Agent


def main():
    print("Local Agent (llama3:8b)")
    print("Type 'exit' or press Ctrl+C to quit.\n")

    agent = Agent()

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye.")
            break

        try:
            agent.chat(user_input)
        except Exception as e:
            print(f"[error] {e}\n")


if __name__ == "__main__":
    main()
