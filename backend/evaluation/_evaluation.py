import os
import json
import sys
from openai import OpenAI
from math import exp
import numpy as np
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utility.env_manager import get_env_manager
from evaluation._data_generation import get_completion
from evaluation._data_generation import file_reader
from prompts.context import KnowledgeAssistant

env_manager = get_env_manager()
client = OpenAI(api_key=env_manager['openai_keys']['OPENAI_API_KEY'])


class Evaluator:
    def __init__(self, env_manager, client):
        self.env_manager = env_manager
        self.client = client
        self.assistant = KnowledgeAssistant()

    def evaluate(self, prompt: str, user_message: str, context: str, use_test_data: bool = False) -> str:
        API_RESPONSE = get_completion(
            [
                {
                    "role": "system", 
                    "content": prompt.replace("{Context}", context).replace("{Question}", user_message)
                }
            ],
            model=self.env_manager['vectordb_keys']['VECTORDB_MODEL'],
            logprobs=True,
            top_logprobs=1,
        )

        system_msg = str(API_RESPONSE.choices[0].message.content)
        
        for i, logprob in enumerate(API_RESPONSE.choices[0].logprobs.content[0].top_logprobs, start=1):
            output = f'\nhas_sufficient_context_for_answer: {system_msg}, \nlogprobs: {logprob.logprob}, \naccuracy: {np.round(np.exp(logprob.logprob)*100,2)}%\n'
            print(output)
            if system_msg == 'false' and np.round(np.exp(logprob.logprob)*100,2) >= 55.00:
                classification = 'false'
            elif system_msg == 'true' and np.round(np.exp(logprob.logprob)*100,2) >= 55.00:
                classification = 'true'
            else:
                classification = 'false'
        accuracy = np.round(np.exp(logprob.logprob)*100,2)
        sufficent = system_msg
        return classification, accuracy, sufficent

    def run(self, query, user_message):
        augmented_prompt = self.assistant.augment_prompt(query)
        context_message = augmented_prompt
        prompt_message = file_reader("prompts/generic-evaluation-prompt.txt")
        context = str(context_message)
        prompt = str(prompt_message)
        return self.evaluate(prompt, user_message, context)


if __name__ == "__main__":
    env_manager = get_env_manager()
    client = OpenAI(api_key=env_manager['openai_keys']['OPENAI_API_KEY'])
    evaluator = Evaluator(env_manager, client)
    query = "I want to know about this week tasks."
    user_message = "What are my tasks for this week?"
    print(evaluator.run(query, user_message))