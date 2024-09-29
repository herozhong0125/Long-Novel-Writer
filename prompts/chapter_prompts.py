CHAPTER_PROMPT = """
基于以下世界观设定、主线任务、角色设计、剧情大纲和用户输入,创建一个详细的章节列表:

世界观设定: {world_setting}
主线任务: {main_quest}
角色设计: {characters}
剧情大纲: {plot}
用户输入: {user_input}

请创建一个包含15-25章的章节列表。每个章节应包括:
1. 章节标题
2. 简短的章节概要(2-3句话)

确保章节列表:
1. 按照剧情大纲的结构展开
2. 每个章节都推动主线任务的发展
3. 为主要角色提供足够的出场和发展机会
4. 包含适当的起伏和节奏变化
5. 在关键点设置悬念或转折

请严格按照以下格式输出章节列表：
*第1章：[章节标题]*
#[章节概述]#

*第2章：[章节标题]*
#[章节概述]#

...

*第N章：[章节标题]*）
#[章节概述]#
"""

# 其他相关的prompts...
