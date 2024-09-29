CONTENT_PROMPT = """
基于以下信息,为指定的章节生成详细内容:

世界观设定: {world_setting}
主线任务: {main_quest}
角色设计: {characters}
剧情大纲: {plot}
章节列表: {chapters}
当前章节: {current_chapter}
用户输入: {user_input}

请生成约3000-5000字的当前章节内容,包括:
1. 生动的场景描述
2. 引人入胜的对话
3. 角色的内心活动
4. 情节的推进
5. 与整体故事的联系

请严格按照以下格式输出章节正文内容：
[章节标题]
[章节正文内容]
"""


# 其他相关的prompts...