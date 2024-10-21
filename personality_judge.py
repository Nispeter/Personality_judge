import openai
from config import OPENAI_API_KEY
import json

def load_personalities(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def generate_agent_response(agent_name, personality_description, input_data):
    prompt = f"""
    You are {agent_name}, {personality_description}. Here is some information: {input_data}.
    Based on your personality, provide your brief analysis or opinion on this information.
    """
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are {agent_name}, {personality_description}."},
            {"role": "user", "content": input_data}
        ]
    )
    return response.choices[0].message.content


def combine_responses(agent_responses):
    combined_prompt = "Here are the opinions of different experts:\n"

    for agent_name, response in agent_responses.items():
        combined_prompt += f"{agent_name}: {response}\n"

    combined_prompt += "Now, combine these insights into a final, cohesive analysis."

    final_response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a highly skilled mediator capable of synthesizing multiple expert opinions."},
            {"role": "user", "content": combined_prompt}
        ]
    )
    return final_response.choices[0].message.content


def main():

    personalities = load_personalities('personalities.json')
    input_data = "Briefly Discuss the impact of AI on modern education and its ethical implications."

    agent_responses = {}

    for _, personality in personalities.items():
        agent_name = personality["name"]
        personality_description = personality["description"]
        agent_responses[agent_name] = generate_agent_response(agent_name, personality_description, input_data)


    final_response = combine_responses(agent_responses)
    for agent, response in agent_responses.items():
        print(f"\n################### {agent}'s opinion:\n{response}\n")

    print(f"\n################### Final combined response:\n{final_response}")

if __name__ == "__main__":
    main()
