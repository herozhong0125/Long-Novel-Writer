from llm_api import ollama_api
from llm_api import openai_api
from prompts.content_prompts import CONTENT_PROMPT

class Content:
    @staticmethod
    def generate_content(world_setting, main_quest, characters, plot, chapters, current_chapter, user_input):
        prompt = CONTENT_PROMPT.format(
            world_setting=world_setting,
            main_quest=main_quest,
            characters=characters,
            plot=plot,
            chapters=chapters,
            current_chapter=current_chapter,
            user_input=user_input
        )
        response = ollama_api.generate_text(prompt)
        #response = openai_api.call_openai_api(prompt,model="gpt-4o",temperature=0.7,max_tokens=4096)
        return response

    @staticmethod
    def refine_content(current_content, user_input):
        # 可以添加一个用于优化内容的方法
        pass