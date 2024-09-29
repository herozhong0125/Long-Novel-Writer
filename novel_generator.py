import streamlit as st
from llm_api import ollama_api
from llm_api import openai_api
from layers.world_setting import WorldSetting
from layers.main_quest import MainQuest
from layers.characters import Characters
from layers.plot import Plot
from layers.chapters import Chapters
from layers.content import Content
from layers.refinement import Refinement
import json
import os
import re
import openai

def load_novels():
    if not os.path.exists("novels"):
        os.makedirs("novels")
    novels = [f for f in os.listdir("novels") if f.endswith(".json")]
    return novels

def save_novel(novel_data):
    try:
        with open(f"novels/{novel_data['name']}.json", "w") as f:
            json.dump(novel_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"保存小说时出现错误: {str(e)}")

def load_novel(novel_name):
    try:
        with open(f"novels/{novel_name}", "r") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        st.error(f"加载小说 '{novel_name}' 时出现错误。尝试恢复数据...")
        with open(f"novels/{novel_name}", "r") as f:
            content = f.read()
        
        # 尝试找到最后一个有效的 JSON 对象
        last_brace = content.rfind('}')
        if last_brace != -1:
            try:
                recovered_data = json.loads(content[:last_brace+1])
                st.warning(f"已恢复部分数据。某些信息可能丢失。")
                return recovered_data
            except json.JSONDecodeError:
                st.error(f"无法恢复数据。请检查文件 '{novel_name}' 的内容。")
        
        # 如果无法恢复，返回一个空的小说数据结构
        return {
            "name": novel_name.replace(".json", ""),
            "description": "",
            "world_setting": "",
            "main_quest": "",
            "characters": "",
            "plot": "",
            "chapters": [],
            "content": {}
        }

def delete_novel(novel_name):
    os.remove(f"novels/{novel_name}")

def parse_chapters(text):
    chapters = []
    pattern = r'\*(.*?)\*'
    matches = re.findall(pattern, text)
    return matches

def parse_content(text):
    content = {}
    pattern = r'\#(.*?)\#'
    matches = re.findall(pattern, text)
    return matches

def main():
    st.set_page_config(layout="wide")
    st.title("Long-Novel Writer")

    with st.expander("使用指南", expanded=False):
        st.markdown("""
        1. 请在设置标签页中配置Ollama API。
        2. 按照标签页顺序，逐步完成小说作的各个环节。
        3. 如果遇到任何问题，请尝试刷新页面或重启程序。
        """)

    tabs = st.tabs(["选择小说", "故事核心", "角色设计", "剧情设计", "章节设计", "撰写正文", "润色调整", "设置"])

    with tabs[0]:
        st.header("选择小说")
        operation = st.radio("选择操作", ["新建小说", "加载小说", "删除小说"])
        
        if operation == "新建小说":
            novel_name = st.text_input("输入新小说名称")
            word_count = st.number_input("目标字数", min_value=1000, max_value=1000000, step=1000)
            
            novel_types = ["奇幻", "科幻", "言情", "悬疑", "历史", "武侠", "都市", "青春", "军事", "同人"]
            novel_type = st.selectbox("小说类型", novel_types)
            
            novel_tones = ["轻松", "严肃", "黑暗", "幽默", "温馨", "悲伤", "激烈", "平和"]
            novel_tone = st.selectbox("小说基调", novel_tones)
            
            writing_styles = ["华丽", "简洁", "幽默", "严肃", "抒情", "写实", "讽刺", "浪漫"]
            writing_style = st.selectbox("写作风格", writing_styles)
            
            novel_description = st.text_area("这是一部什么样的小说?", placeholder="可以选择在这里输入更多细节")
            if st.button("创建新小说"):
                if novel_name:
                    novel_data = {
                        "name": novel_name,
                        "word_count": word_count,
                        "type": novel_type,
                        "tone": novel_tone,
                        "writing_style": writing_style,
                        "description": novel_description,
                        "world_setting": "",
                        "main_quest": "",
                        "characters": "",
                        "plot": "",
                        "chapters": [],
                        "content": {}
                    }
                    save_novel(novel_data)
                    st.session_state.current_novel = novel_data
                    st.success(f"小说 '{novel_name}' 创建成功!")
                else:
                    st.error("请输入小说名称")
        
        elif operation == "加载小说":
            novels = load_novels()
            if novels:
                novel_name = st.selectbox("选择已有小说", novels)
                if st.button("加载小说"):
                    st.session_state.current_novel = load_novel(novel_name)
                    st.success(f"小说 '{novel_name}' 加载成功!")
            else:
                st.warning("没有可加载的小说")
        
        elif operation == "删除小说":
            novels = load_novels()
            if novels:
                novel_to_delete = st.selectbox("选择要删除的小说", novels)
                if st.button("删除小说"):
                    delete_novel(novel_to_delete)
                    st.success(f"小说 '{novel_to_delete}' 已删除")
                    if 'current_novel' in st.session_state and st.session_state.current_novel['name'] == novel_to_delete:
                        del st.session_state.current_novel
            else:
                st.warning("没有可删除的小说")

    with tabs[1]:
        st.header("故事核心")
        if 'current_novel' in st.session_state:
            st.subheader("步骤1：确定世界观")
            if st.session_state.current_novel.get("world_setting"):
                st.write("当前世界观设定:")
                st.text_area("世界观", st.session_state.current_novel["world_setting"], height=300, key="existing_world_setting")
            
            user_world_input = st.text_area("")
            
            if st.button("生成/更新世界观"):
                world_setting = ""
                progress_bar = st.progress(0)
                world_setting_area = st.empty()
                try:
                    response = WorldSetting.generate_world_setting(st.session_state.current_novel, user_world_input)
                    for i, chunk in enumerate(response):
                        world_setting += chunk
                        world_setting_area.text_area(f"世界观生成中...", world_setting, height=300, key=f"world_setting_{i}")
                        progress_bar.progress(min(1.0, (i + 1) / 100))
                    
                    st.session_state.current_novel["world_setting"] = world_setting
                    save_novel(st.session_state.current_novel)
                    st.success("世界观生成完成!")
                    st.text_area("新的世界观设定", world_setting, height=300, key="final_world_setting")
                except Exception as e:
                    st.error(f"生成世界观时出错：{str(e)}")

            st.subheader("步骤2：明确主线任务")
            if st.session_state.current_novel.get("main_quest"):
                st.write("当前主线任务:")
                st.text_area("主线任务", st.session_state.current_novel["main_quest"], height=300, key="existing_main_quest")
            
            user_quest_input = st.text_area("输入您对主线任务的想法", placeholder="例如：拯救世界免于魔法污染")
            
            if st.button("生成/更新主线任务"):
                if st.session_state.current_novel.get("world_setting"):
                    main_quest = ""
                    progress_bar = st.progress(0)
                    main_quest_area = st.empty()
                    response = MainQuest.generate_main_quest(st.session_state.current_novel, user_quest_input)
                    for i, chunk in enumerate(response):
                        main_quest += chunk
                        main_quest_area.text_area(f"主线任务生成中...", main_quest, height=300, key=f"main_quest_{i}")
                        progress_bar.progress(min(1.0, (i + 1) / 100))  # 假设大约有100个块
                    
                    st.session_state.current_novel["main_quest"] = main_quest
                    save_novel(st.session_state.current_novel)
                    st.write("新的主线任务:")
                    st.write(main_quest)
                else:
                    st.error("请先生成世界观设定")
        else:
            st.warning("请先选择或创建一个小说")

    with tabs[2]:
        st.header("角色设计")
        if 'current_novel' in st.session_state and st.session_state.current_novel.get("main_quest"):
            if st.session_state.current_novel.get("characters"):
                st.write("当前角色设计:")
                st.text_area("角色", st.session_state.current_novel["characters"], height=300, key="existing_characters")
            
            user_character_input = st.text_area("输入您对角色的想法", placeholder="例如：希望有一个反角色")
            
            if st.button("生成/更新角色设计"):
                characters = ""
                progress_bar = st.progress(0)
                characters_area = st.empty()
                response = Characters.generate_characters(st.session_state.current_novel["world_setting"],
                                                st.session_state.current_novel["main_quest"],
                                                user_character_input)
                for i, chunk in enumerate(response):
                    characters += chunk
                    characters_area.text_area(f"角色生成中...", characters, height=300, key=f"characters_{i}")
                    progress_bar.progress(min(1.0, (i + 1) / 100))  # 假设大约有100个块
                
                st.session_state.current_novel["characters"] = characters
                save_novel(st.session_state.current_novel)
                st.write("新的角色设计:")
                st.write(characters)
        else:
            st.warning("请先完成故事核心")

    with tabs[3]:
        st.header("剧情设计")
        if 'current_novel' in st.session_state and st.session_state.current_novel.get("characters"):
            if st.session_state.current_novel.get("plot"):
                st.write("当前剧情设计:")
                st.text_area("剧情", st.session_state.current_novel["plot"], height=300, key="existing_plot")
            
            user_plot_input = st.text_area("输入您对剧情的想法", placeholder="例如：希望有一个意想不到的转折")
            
            if st.button("生成/更新剧情设计"):
                plot = ""
                progress_bar = st.progress(0)
                plot_container = st.empty()
                for i, chunk in enumerate(Plot.generate_plot(st.session_state.current_novel["world_setting"],
                                     st.session_state.current_novel["main_quest"],
                                     st.session_state.current_novel["characters"],
                                     user_plot_input)):
                    plot += chunk
                    plot_container.markdown(f"""
                        <div style="white-space: pre-wrap; word-wrap: break-word; font-family: monospace;">
                        {plot}
                        </div>
                        """, unsafe_allow_html=True)
                    progress_bar.progress(min(1.0, (i + 1) / 100))  # 假设大约有100个块
                
                st.session_state.current_novel["plot"] = plot
                save_novel(st.session_state.current_novel)
                st.success("新的剧情设计已生成并保存!")
        else:
            st.warning("请先完成角色设计")

    with tabs[4]:
        st.header("章节设计")
        if 'current_novel' in st.session_state and st.session_state.current_novel.get("plot"):
            if st.session_state.current_novel.get("chapters"):
                st.write("当前章节设计:")
                chapters = st.session_state.current_novel["chapters"]
                st.text_area("章节", chapters, height=300, key="existing_chapters")
            
            user_chapter_input = st.text_area("输入您对章节的想法", placeholder="例如：希望有20个章节")
            
            if st.button("生成/更新章节设计"):
                chapters = ""   
                progress_bar = st.progress(0)
                chapters_area = st.empty()
                response = Chapters.generate_chapters(st.session_state.current_novel["world_setting"],
                                             st.session_state.current_novel["main_quest"],
                                             st.session_state.current_novel["characters"],
                                             st.session_state.current_novel["plot"],
                                             user_chapter_input)
                for i, chunk in enumerate(response):
                    chapters += chunk
                    chapters_area.text_area(f"章节生成中...", chapters, height=300, key=f"chapters_{i}")
                    progress_bar.progress(min(1.0, (i + 1) / 100))
                
                st.session_state.current_novel["chapters"] = chapters
                save_novel(st.session_state.current_novel)
                st.success("新的章节设计已生成并保存!")
        else:
            st.warning("请先完成剧情设计")

    with tabs[5]:
        st.header("撰写正文")
        if 'current_novel' in st.session_state and st.session_state.current_novel.get("chapters"):
            chapters = st.session_state.current_novel["chapters"]
            chapter_titles = parse_chapters(chapters)
            
            if chapter_titles:
                selected_chapter = st.selectbox("选择章节", chapter_titles)
                chapter_index = chapter_titles.index(selected_chapter)
                
                if st.session_state.current_novel.get("content") and st.session_state.current_novel["content"].get(str(chapter_index + 1)):
                    st.write("当前章节内容:")
                    st.text_area("章节内容", st.session_state.current_novel["content"][str(chapter_index + 1)], height=300, key=f"existing_content_{chapter_index}")
                else:
                    st.write("当前章节概述:")
                    #chapter_description = chapters.split('\n', 1)[1] if len(chapters.split('\n', 1)) > 1 else ""
                    chapter_descriptions = parse_content(chapters)
                    chapter_description = chapter_descriptions[chapter_index]
                    st.text_area("章节概述", chapter_description, height=100, key=f"chapter_summary_{chapter_index}")
                
                user_content_input = st.text_area("输入您对本章内容的建议", placeholder="例如：希望加入更多描写")
                
                if st.button("生成/更新章节内容"):
                    chapter_content = ""
                    progress_bar = st.progress(0)
                    content_area = st.empty()
                    response = Content.generate_content(st.session_state.current_novel["world_setting"],
                                                       st.session_state.current_novel["main_quest"],
                                                       st.session_state.current_novel["characters"],
                                                       st.session_state.current_novel["plot"],
                                                       chapters,
                                                       chapter_index + 1,
                                                       user_content_input)
                    for i, chunk in enumerate(response):
                        chapter_content += chunk
                        content_area.text_area(f"章节内容生成中...", chapter_content, height=300, key=f"content_{i}")
                        progress_bar.progress(min(1.0, (i + 1) / 100))
                    
                    if "content" not in st.session_state.current_novel:
                        st.session_state.current_novel["content"] = {}

                    st.session_state.current_novel["content"][str(chapter_index + 1)] = chapter_content
                    save_novel(st.session_state.current_novel)
                    st.write("新生成的章节内容:")
                    st.write(chapter_content)
            else:
                st.warning("没有找到章节标题")
        else:
            st.warning("请先完成章节设计")

    with tabs[6]:
        st.header("润色调整")
        if 'current_novel' in st.session_state and st.session_state.current_novel.get("content"):
            chapter_index = st.selectbox("选择要润色的章节", range(1, len(st.session_state.current_novel["chapters"])+1))
            
            if st.session_state.current_novel["content"].get(str(chapter_index)):
                st.write("当前章节内容:")
                st.text_area("待润色内容", st.session_state.current_novel["content"][str(chapter_index)], height=300, key=f"existing_content_to_polish_{chapter_index}")
            
            user_polish_input = st.text_area("输入您的润色建议", placeholder="例如：希望语言更加优美")
            
            if st.button("润色章节"):
                polished_content = Refinement.polish_content(st.session_state.current_novel["content"][str(chapter_index)],
                                                          user_polish_input)
                st.session_state.current_novel["content"][str(chapter_index)] = polished_content
                save_novel(st.session_state.current_novel)
                st.write("润色后的章节内容:")
                st.write(polished_content)
        else:
            st.warning("请先完成正文撰写")

    with tabs[7]:
        st.header("设置")
        
        # Ollama 设置
        st.subheader("Ollama 设置")
        ollama_api.OLLAMA_API_URL = st.text_input("Ollama API URL", value="http://localhost:11434/api/generate")
        ollama_model = st.selectbox("选择 Ollama 模型", ["qwen2.5:14b-instruct-q4_0", "llama2", "mistral"])
        
        # OpenAI 设置
        st.subheader("OpenAI 设置")
        openai_api_key = st.text_input("OpenAI API Key", type="password")
        openai_base_url = st.text_input("OpenAI Base URL (可选)", value="https://api.openai.com/v1")
        openai_model = st.selectbox("选择 OpenAI 模型", ["gpt-3.5-turbo", "gpt-4"])
        openai_proxy = st.text_input("OpenAI 代理地址 (可选)")
        
        # LLM 选择
        llm_choice = st.radio("选择使用的 LLM", ["Ollama", "OpenAI"])
        
        if st.button("保存设置"):
            # 保存 Ollama 设置
            ollama_api.MODEL = ollama_model
            
            # 保存 OpenAI 设置
            if openai_api_key:
                openai.api_key = openai_api_key
            if openai_base_url:
                openai.api_base = openai_base_url
            
            # 保存 LLM 选择
            st.session_state.llm_choice = llm_choice
            
            st.success("设置已保存")

if __name__ == "__main__":
    main()