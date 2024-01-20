import os
import json
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utility.env_manager import get_env_manager
from openai import OpenAI
from math import exp
import numpy as np
from utility.env_manager import get_env_manager
from typing import List, Dict
from dotenv import load_dotenv
from prompts.context import KnowledgeAssistant

load_dotenv()
env_manager = get_env_manager()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class PromptGenerator:
    def __init__(self, num_test_output: str, objective: str, output: str):
        self.num_test_output = num_test_output
        self.objective = objective
        self.output = output
        self.env_manager = get_env_manager()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def get_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = env_manager['vectordb_keys']['VECTORDB_MODEL'],
        max_tokens=500,
        temperature=0,
        stop=None,
        seed=123,
        tools=None,
        logprobs=None,
        top_logprobs=None,
    ) -> str:
        """Return the completion of the prompt.
        @parameter messages: list of dictionaries with keys 'role' and 'content'.
        @parameter model: the model to use for completion. Defaults to 'davinci'.
        @parameter max_tokens: max tokens to use for each prompt completion.
        @parameter temperature: the higher the temperature, the crazier the text
        @parameter stop: token at which text generation is stopped
        @parameter seed: random seed for text generation
        @parameter tools: list of tools to use for post-processing the output.
        @parameter logprobs: whether to return log probabilities of the output tokens or not.
        @returns completion: the completion of the prompt.
        """

        params = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stop": stop,
            "seed": seed,
            "logprobs": logprobs,
            "top_logprobs": top_logprobs,
        }
        if tools:
            params["tools"] = tools

        completion = client.chat.completions.create(**params)
        return completion


    def file_reader(self, path: str) -> str:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        base_dir = os.path.dirname(script_dir)
        file_path = os.path.join(base_dir, path)
        with open(file_path, 'r', encoding='utf-8') as f:
            system_message = f.read()
        return system_message
                
                

    def generate_test_data(self, prompt: str, context: str) -> str:
        """Return the classification of the hallucination."""
        API_RESPONSE = self.get_completion(
            [
                {
                    "role": "user",
                    "content": prompt.replace("{context}", context).replace("{num_test_output}", self.num_test_output).replace("{output}", self.output)
                }
            ],
            model=self.env_manager['vectordb_keys']['VECTORDB_MODEL'],
            logprobs=True,
            top_logprobs=1,
        )

        system_msg = API_RESPONSE.choices[0].message.content
        return system_msg

    def save_json(self, test_data) -> None:
    # Get the directory of the current script
        script_dir = os.path.dirname(os.path.realpath(__file__))

        # Get the base directory (parent of the script directory)
        base_dir = os.path.dirname(script_dir)

        # Define the relative path to your JSON file
        path = "prompt-dataset/prompt-data.json"

        # Join the base directory with the relative path
        file_path = os.path.join(base_dir, path)
        json_object = json.loads(test_data)
        with open(file_path, 'w') as json_file:
            json.dump(json_object, json_file, indent=4)
            
        print(f"JSON data has been saved to {file_path}")

    def execute(self):
        assistant = KnowledgeAssistant()
        query = '"' + str(self.objective) + '"'
        augmented_prompt = assistant.augment_prompt(query)
        context_message = augmented_prompt
        prompt_message = self.file_reader("prompts/prompt-generation-prompt.txt")
        context = str(context_message)
        prompt = str(prompt_message)
        test_data = self.generate_test_data(prompt, context)
        self.save_json(test_data)

        print("===========")
        print("Prompt Data")
        print("===========")
        print(test_data)


if __name__ == "__main__":
    generator = PromptGenerator("4", "I want to know what are bages of this week", "WHAT ARE THE COMPANY NAMES?")
    generator.execute()