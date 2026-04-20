from typing import List

import requests
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, ToolMessage
from langchain.tools import tool, BaseTool
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from callbacks import AgentCallbackHandler

load_dotenv()

@tool("get_text_length", description="Returns the length of a text by characters") #from langchain.tools
def get_text_length(text: str) -> int:
    """Returns the length of a text by characters"""
    print(f"get_text_length enter with {text=}")
    text = text.strip("'\n").strip(
        '"'
    )  # stripping away non alphabetic characters

    return len(text)

@tool
def get_city_temperature(city: str) -> str:
    """Returns the current temperature in Fahrenheit for a US city"""
    print(f"get_city_temperature enter with {city=}")
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_resp = requests.get(geo_url, params={"name": city, "count": 1, "country": "US", "language": "en", "format": "json"})
    geo_resp.raise_for_status()
    results = geo_resp.json().get("results")
    if not results:
        return f"Could not find US city: {city}"
    lat, lon = results[0]["latitude"], results[0]["longitude"]
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_resp = requests.get(weather_url, params={
        "latitude": lat, "longitude": lon,
        "current_weather": True,
        "temperature_unit": "fahrenheit",
    })
    weather_resp.raise_for_status()
    temp = weather_resp.json()["current_weather"]["temperature"]
    return f"The current temperature in {city} is {temp}°F"


def find_tool_by_name(tools: List[BaseTool], tool_name: str) -> BaseTool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool wtih name {tool_name} not found")


if __name__ == "__main__":
    print("Hello LangChain Tools (.bind_tools)!")
    tools = [get_text_length, get_city_temperature] 

    '''llm = ChatOllama(temperature=0, model="gemma3:1b-it-qat",
        callbacks=[AgentCallbackHandler()],
    )'''
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",
        callbacks=[AgentCallbackHandler()],
    )

    llm_with_tools = llm.bind_tools(tools) #allows LLM to call tools

    # Start conversation
    user_input = input("Enter your message: ")
    messages = [HumanMessage(content=user_input)]

    while True:
        ai_message = llm_with_tools.invoke(messages)

        # If the model decides to call tools, execute them and return results
        tool_calls = getattr(ai_message, "tool_calls", None) or []
        if len(tool_calls) > 0:
            messages.append(ai_message)
            for tool_call in tool_calls:
                # tool_call is typically a dict with keys: id, type, name, args
                tool_name = tool_call.get("name")
                tool_args = tool_call.get("args", {})
                tool_call_id = tool_call.get("id")

                tool_to_use = find_tool_by_name(tools, tool_name)
                observation = tool_to_use.invoke(tool_args)
                print(f"observation={observation}")

                messages.append(
                    ToolMessage(content=str(observation), tool_call_id=tool_call_id)
                )
            # Continue loop to allow the model to use the observations
            continue

        # No tool calls -> final answer
        print(ai_message.content)
        break
