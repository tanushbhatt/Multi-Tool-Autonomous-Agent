from agent import create_autonomous_agent, run_agent

def display_trace(trace):

    if not trace:
        print("\nNo tools were used for this request.")
        return

    print("\n========== EXECUTION TRACE ==========")

    for index, item in enumerate(trace, start=1):

        if item["type"] == "tool_call":

            print(f"\n[STEP {index}] ACTION")
            print(f"Tool: {item['tool']}")
            print(f"Input: {item['input']}")

        elif item["type"] == "observation":

            print(f"\n[STEP {index}] OBSERVATION")
            print(f"Tool: {item['tool']}")
            print(f"Output: {item['output']}")

    print("\n=====================================")



def main():

    print("\n======================================")
    print("       MULTI-TOOL AUTONOMOUS AGENT")
    print("======================================")

    print("\nAvailable tools:")
    print("1. Web Search")
    print("2. Python Calculator")
    print("3. Local File Reader")

    print("\nType 'exit' or 'quit' to stop.")

    try:
        print("\nInitializing AI Agent...")

        agent = create_autonomous_agent()

        print("AI Agent initialized successfully!")

    except Exception as error:
        print(f"\nAgent initialization failed: {error}")
        return

    while True:

        try:
            query = input("\nYou: ").strip()

            if query.lower() in ("exit", "quit"):
                print("\nAI Agent stopped. Goodbye!")
                break

            if not query:
                print("Please enter a question.")
                continue

            print("\nAI Agent is processing your request...")

            answer, trace = run_agent(agent, query)

            display_trace(trace)

            print("\n========== FINAL ANSWER ==========")
            print(answer)
            print("==================================")

        except KeyboardInterrupt:
            print("\n\nApplication interrupted. Goodbye!")
            break

        except Exception as error:
            print(
                f"\nRequest failed: {type(error).__name__}: {error}"
            )
            print("You can try submitting another request.")



if __name__ == "__main__":
    main()
