from llm_api import ollama_api
from prompts.chapter_prompts import CHAPTER_PROMPT

class Chapters:
    @staticmethod
    def generate_chapters(world_setting, main_quest, characters, plot, user_input):
        prompt = CHAPTER_PROMPT.format(
            world_setting=world_setting,
            main_quest=main_quest,
            characters=characters,
            plot=plot,
            user_input=user_input
        )
        response = ollama_api.generate_text(prompt)
        return response

    @staticmethod
    def refine_chapters(current_chapters, user_input):
        # 可以添加一个用于优化章节的方法
        pass