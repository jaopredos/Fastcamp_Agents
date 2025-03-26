def calculate(operation: str) -> str:
    try:
        result = eval(operation)
        return f"The result of '{operation}' is: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

calculator_tool = {
    "name": "Make a calculation",
    "description": "Performs basic math operations like +, -, *, /",
    "func": calculate
}