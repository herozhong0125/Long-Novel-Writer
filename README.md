# Long-Novel Writer

Long-Novel Writer 是一个基于人工智能的小说创作辅助工具，旨在帮助作者从构思到完成长篇小说的整个创作过程。

## 功能特点

1. **小说管理**：创建、加载和删除小说项目。
2. **故事核心设计**：
   - 世界观设定
   - 主线任务生成
3. **角色设计**：根据世界观和主线任务生成丰富的角色。
4. **剧情设计**：基于前期设定生成整体剧情架构。
5. **章节设计**：自动规划小说章节结构。
6. **正文撰写**：为每个章节生成详细内容。
7. **润色调整**：对已生成的内容进行优化和润色。
8. **多模型支持**：支持 Ollama 和 OpenAI 的多种语言模型。

## 安装说明

1. 克隆此仓库：
   ```
   git clone https://github.com/herozhong0125/Long-Novel-Writer
   cd long-novel-writer
   ```

2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

3. 配置 API：
   - 对于 Ollama，确保本地服务正在运行。
   - 对于 OpenAI，在设置页面中填入您的 API 密钥。

## 使用方法

1. 运行应用：
   ```
   streamlit run novel_generator.py
   ```

2. 在浏览器中打开显示的本地地址（通常是 http://localhost:8501）。

3. 按照界面提示，从"选择小说"开始，逐步完成小说创作的各个环节。

## 注意事项

- 请确保在使用 OpenAI API 时遵守其使用条款。
- 生成的内容仅供参考，最终创作成果仍需作者的创意和修改。

## 贡献

欢迎提交问题报告和改进建议。如果您想为项目做出贡献，请遵循以下步骤：

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 联系方式

项目维护者：[您的姓名] - [您的邮箱]

项目链接：[https://github.com/herozhong0125/Long-Novel-Writer](https://github.com/herozhong0125/Long-Novel-Writer)
# Long-Novel-Writer
