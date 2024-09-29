from llm_api import ollama_api
from prompts.plot_prompts import PLOT_PROMPT

class Plot:
    @staticmethod
    def generate_plot(world_setting, main_quest, characters, user_input):
        prompt = PLOT_PROMPT.format(
            world_setting=world_setting,
            main_quest=main_quest,
            characters=characters,
            user_input=user_input
        )
        response = ollama_api.generate_text(prompt)
        return response

    @staticmethod
    def refine_plot(current_plot, user_input):
        # 可以添加一个用于优化剧情的方法
        pass