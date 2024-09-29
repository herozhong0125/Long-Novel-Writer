from prompts.world_setting_prompts import WORLD_SETTING_PROMPT
from llm_api import ollama_api

class WorldSetting:
    @staticmethod
    def generate_world_setting(novel_data, user_input):
        prompt = WORLD_SETTING_PROMPT.format(
            novel_description=novel_data.get("description", ""),
            user_input=user_input,
            novel_name=novel_data.get("name", ""),
            word_count=novel_data.get("word_count", ""),
            novel_type=novel_data.get("type", ""),
            novel_tone=novel_data.get("tone", ""),
            writing_style=novel_data.get("writing_style", "")
        )
        
        return ollama_api.generate_text(prompt)