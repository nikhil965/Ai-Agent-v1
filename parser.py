import json


def parse_tool_call(response: str):
    try:
        tool_request = json.loads(response)
        if(
            isinstance(tool_request, dict)
            and "tool" in tool_request
        ):
            return tool_request
    
    except Exception:
        pass
    
    return None

if __name__ == "__main__":
    test_response = '{"tool": "calculator", "input": "2 + 2"}'
    tool_request = parse_tool_call(test_response)
    if tool_request:
        print(f"Tool: {tool_request['tool']}, Input: {tool_request['input']}")
    else:
        print("No tool call found.")