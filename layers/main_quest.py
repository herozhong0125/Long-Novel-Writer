from llm_api import ollama_api
from prompts.main_quest_prompts import MAIN_QUEST_PROMPT

class MainQuest:
    @staticmethod
    def generate_main_quest(novel_data, user_input):
        prompt = MAIN_QUEST_PROMPT.format(
            novel_description=novel_data.get("description", ""),
            user_input=user_input,
            novel_name=novel_data.get("name", ""),
            word_count=novel_data.get("word_count", ""),
            novel_type=novel_data.get("type", ""),
            novel_tone=novel_data.get("tone", ""),
            world_setting=novel_data.get("world_setting", ""),
            writing_style=novel_data.get("writing_style", "")
        )
        response = ollama_api.generate_text(prompt)
        return response

    @staticmethod
    def refine_main_quest(current_quest, user_input):
        # 可以添加一个用于优化主线任务的方法
        pass