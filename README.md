#丹砂

允许用户与上传的文件 (`.pdf`, `.docx`, `.csv`, `.txt`) 进行对话

项目架构图:
```python
根目录/
├── .git/
├── .github/
├── .idea/
├── .streamlit/
├── components/
├── docGPT/
├── model/
├── static/
├── .gitignore
├── app/
├── docker-compose
├── Dockerfile
├── LICENSE
├── README
└── requirements
```

* 主要开发软件与套件:
    * `Python 3.10.11`
    * `Langchain 0.0.218`
    * `Streamlit 1.22.0`
    * [more](./requirements.txt)

### 介绍

* 上传来自本地的 Document 链接 (`.pdf`, `.docx`, `.csv`, `.txt`)，并且向大模型询问有关 Document 内容。
* 提供两种模型选择:
  * `gpt4free`
    * **允许使用者在无需输入 API 密钥或付款的情况下使用该应用程序**
    * 需选择 Provider
  * `openai`
    * **需要有** `openai_api_key`
    * 如果有 `serpapi_key`，AI 的回应可以包括 Google 搜索结果


---

### 功能

- gpt4free 整合：任何人都可以免费使用 GPT4，无需输入 OpenAI API 密钥
- 支持 docx, pdf, csv, txt 文件: 可以上传 PDF, Word, CSV, txt 文件
- 直接输入 Document 网址：使用者可以直接输入 Document URL 进行解析，无需从本地上传文件
- Langchain Agent：AI 能够回答当前问题，实现类似 Google 搜索功能
- 简易操作环境：界面简洁，操作简便

---

### 部署

首先 `git clone https://github.com/OpenEduTech/CloudComputer2024/tree/006`

方法有如下几种方法:

* 本地不使用docker:
    * 下载开发需求套件
        ```
        pip install -r requirements.txt
        ```

    * 于项目根目录启动服务
        ```
        streamlit run ./app.py
        ```

* 本地使用docker:
    * 使用 Docker Compose 启动服务
        ```
        docker-compose up
        ```
    
    * 停止服务运行
        ```
        docker-compose down
        ```

---

