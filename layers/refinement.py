from llm_api import ollama_api
from prompts.refinement_prompts import REFINEMENT_PROMPT

class Refinement:
    @staticmethod
    def polish_content(original_content, user_input):
        prompt = REFINEMENT_PROMPT.format(
            original_content=original_content,
            user_input=user_input
        )
        response = ollama_api.generate_text(prompt)
        return response