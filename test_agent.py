import unittest
from types import SimpleNamespace
from agent import run_agent

class FakeAgent:
    """Simulates an agent without calling Gemini."""

    def __init__(self, response):
        self.response = response

    def invoke(self, payload):
        return self.response


class TestAgentExecution(unittest.TestCase):

    def test_execution_trace(self):

        action_message = SimpleNamespace(
            type="ai",
            tool_calls=[
                {
                    "name": "calculator",
                    "args": {
                        "expression": "250 * 40"
                    }
                }
            ],
            content=""
        )

        observation_message = SimpleNamespace(
            type="tool",
            name="calculator",
            content="Result: 10000"
        )

        final_message = SimpleNamespace(
            type="ai",
            tool_calls=[],
            content="The answer is 10000."
        )

        fake_agent = FakeAgent({
            "messages": [
                action_message,
                observation_message,
                final_message
            ]
        })

        answer, trace = run_agent(
            fake_agent,
            "Calculate 250 * 40"
        )

        self.assertEqual(answer, "The answer is 10000.")

        self.assertEqual(len(trace), 2)

        self.assertEqual(trace[0]["tool"], "calculator")
        self.assertEqual(trace[0]["type"], "tool_call")

        self.assertEqual(trace[1]["type"], "observation")
        self.assertEqual(trace[1]["output"], "Result: 10000")

    def test_empty_query(self):

        fake_agent = FakeAgent({"messages": []})

        with self.assertRaises(ValueError):
            run_agent(fake_agent, "")




    
    # Test 3: Verify multiple tool calls and observations
    def test_multiple_tool_executions(self):

        action_message = SimpleNamespace(
            type="ai",
            tool_calls=[
                {
                    "name": "web_search",
                    "args": {"query": "Python programming"}
                },
                {
                    "name": "calculator",
                    "args": {"expression": "250 * 40"}
                }
            ],
            content=""
        )

        search_observation = SimpleNamespace(
            type="tool",
            name="web_search",
            content="Python is a programming language."
        )

        calculator_observation = SimpleNamespace(
            type="tool",
            name="calculator",
            content="Result: 10000"
        )

        final_message = SimpleNamespace(
            type="ai",
            tool_calls=[],
            content="Python search completed. The calculation is 10000."
        )

        fake_agent = FakeAgent({
            "messages": [
                action_message,
                search_observation,
                calculator_observation,
                final_message
            ]
        })

        answer, trace = run_agent(
            fake_agent,
            "Search for Python and calculate 250 * 40."
        )

        self.assertEqual(len(trace), 4)

        self.assertEqual(trace[0]["tool"], "web_search")
        self.assertEqual(trace[1]["tool"], "calculator")

        self.assertEqual(trace[2]["type"], "observation")
        self.assertEqual(trace[3]["type"], "observation")

        self.assertIn("10000", answer)



if __name__ == "__main__":
    unittest.main()
