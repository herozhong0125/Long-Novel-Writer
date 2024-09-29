from llm_api import ollama_api
from prompts.character_prompts import CHARACTER_PROMPT

class Characters:
    @staticmethod
    def generate_characters(world_setting, main_quest, user_input):
        prompt = CHARACTER_PROMPT.format(
            world_setting=world_setting,
            main_quest=main_quest,
            user_input=user_input
        )
        response = ollama_api.generate_text(prompt)
        return response

    @staticmethod
    def refine_characters(current_characters, user_input):
        # 可以添加一个用于优化角色的方法
        pass