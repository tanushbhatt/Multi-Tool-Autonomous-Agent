import ast
import math
import operator
from pathlib import Path
from ddgs import DDGS
from langchain_core.tools import tool


@tool
def web_search(query: str, max_results: int = 5) -> str:
    """Search the internet for current information about a topic.
    
    Use this tool when the user needs online information,
    recent facts, news, or research.
    """

    if not query.strip():
        return "Error: Search query cannot be empty."

    max_results = max(1, min(max_results, 8))

    try:
        results = DDGS(timeout=10).text(
            query,
            max_results=max_results
        )

        if not results:
            return "No search results found."

        formatted_results = []

        for index, result in enumerate(results, start=1):
            title = result.get("title", "No title")
            url = result.get("href", "No URL")
            body = result.get("body", "No description")

            formatted_results.append(
                f"{index}. {title}\n"
                f"URL: {url}\n"
                f"Description: {body}"
            )

        return "\n\n".join(formatted_results)

    except Exception as error:
        return f"Web search failed: {error}"



ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def evaluate_expression(node):
    """Safely evaluate basic mathematical expressions."""

    if isinstance(node, ast.Expression):
        return evaluate_expression(node.body)

    if isinstance(node, ast.Constant):
        if type(node.value) in (int, float):
            return node.value

        raise ValueError("Only numeric values are allowed.")

    if isinstance(node, ast.BinOp):
        operator_type = type(node.op)

        if operator_type not in ALLOWED_OPERATORS:
            raise ValueError("Unsupported mathematical operation.")

        left = evaluate_expression(node.left)
        right = evaluate_expression(node.right)

        if isinstance(node.op, ast.Pow) and abs(right) > 10:
            raise ValueError("Exponent is too large.")

        result = ALLOWED_OPERATORS[operator_type](
            left, right
        )

        if isinstance(result, complex):
            raise ValueError("Complex numbers are not supported.")

        if isinstance(result, (int, float)):
            if not math.isfinite(result) or abs(result) > 1e100:
                raise ValueError("Result is outside the allowed range.")

        return result

    if isinstance(node, ast.UnaryOp):
        operator_type = type(node.op)

        if operator_type not in ALLOWED_UNARY_OPERATORS:
            raise ValueError("Unsupported unary operation.")

        return ALLOWED_UNARY_OPERATORS[operator_type](
            evaluate_expression(node.operand)
        )

    raise ValueError("Invalid mathematical expression.")


@tool
def calculator(expression: str) -> str:
    """Perform mathematical calculations.

    Use this tool for arithmetic, percentages,
    multiplication, division, powers and other
    basic mathematical operations.
    
    Examples: 25 * 4, 100 / 5, (50 + 20) * 2
    """

    try:
        if not expression.strip():
            return "Error: Mathematical expression cannot be empty."

        if len(expression) > 200:
            return "Error: Expression is too long."

        parsed_expression = ast.parse(
            expression,
            mode="eval"
        )

        result = evaluate_expression(parsed_expression)

        return f"Result: {result}"

    except ZeroDivisionError:
        return "Error: Cannot divide by zero."

    except (ValueError, SyntaxError, OverflowError) as error:
        return f"Calculation failed: {error}"


PROJECT_DIRECTORY = Path(__file__).resolve().parent

ALLOWED_EXTENSIONS = {
    ".txt",
    ".md",
    ".csv",
    ".json"
}

MAX_FILE_SIZE = 100_000


@tool
def read_local_file(file_path: str) -> str:
    """Read the contents of a local text, Markdown, CSV or JSON file.

    Use this tool when the user asks about information
    stored in a file inside the project directory.

    Provide the file path relative to the project directory.
    """

    try:
        path = Path(file_path).expanduser()

        if not path.is_absolute():
            path = PROJECT_DIRECTORY / path

        path = path.resolve()

        if not path.is_relative_to(PROJECT_DIRECTORY):
            return "Error: Access outside the project directory is not allowed."

        if path.suffix.lower() not in ALLOWED_EXTENSIONS:
            return "Error: Unsupported file type."

        if not path.is_file():
            return f"Error: File not found: {file_path}"

        if path.stat().st_size > MAX_FILE_SIZE:
            return "Error: File exceeds the 100 KB size limit."

        content = path.read_text(encoding="utf-8")

        if not content.strip():
            return "The file is empty."

        return content

    except UnicodeDecodeError:
        return "Error: File must contain UTF-8 encoded text."

    except OSError as error:
        return f"File reading failed: {error}"



TOOLS = [
    web_search,
    calculator,
    read_local_file
]