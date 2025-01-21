import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.environ['SERPAPI_API_KEY'] = ''

import streamlit as st
from streamlit import logger

from components import get_response, side_bar, theme, upload_and_process_document
from docGPT import create_doc_gpt

OPENAI_API_KEY = ''
SERPAPI_API_KEY = ''
model = None

st.session_state.openai_api_key = None
st.session_state.serpapi_api_key = None
st.session_state.g4f_provider = None
st.session_state.button_clicked = None

if 'response' not in st.session_state:
    st.session_state['response'] = ['我该如何帮助您？']

if 'query' not in st.session_state:
    st.session_state['query'] = ['你好']

app_logger = logger.get_logger(__name__)

# 定义需要高亮的关键词及其解释
HIGHLIGHT_KEYWORDS = {
    "Text-to-SQL": "一种将自然语言问题转换为结构化查询语言（SQL）的技术。",
    "自然语言处理（NLP）": "计算机科学和人工智能领域的一个分支，专注于计算机与人类语言之间的交互。",
    "SQL生成": "根据自然语言理解的结果生成结构化查询语言（SQL）的过程。",
    "数据库模式理解": "理解数据库的结构（如表、列、关系等），以确保生成的SQL查询有效。",
    "语义解析": "将自然语言输入解析为计算机可理解的结构化表示的过程。",
    "复杂查询处理": "处理嵌套查询、聚合函数等复杂的SQL结构。",
    "歧义消除": "解决自然语言中的歧义，确保生成的SQL查询准确。",
    "智能助手": "如Alexa、Siri等，允许用户通过语音查询数据库。",
    "商业智能": "帮助非技术人员通过自然语言生成报表和数据分析。",
    "数据探索": "使用户能够通过简单提问探索数据集。",
    "客户支持": "自动生成SQL查询以回答客户问题，提升效率。",
    "基于规则的方法": "使用预定义规则将自然语言转换为SQL，适用于简单场景。",
    "基于机器学习的方法": "使用序列到序列（Seq2Seq）模型等机器学习技术，适合复杂查询。",
    "基于深度学习的方法": "使用Transformer、BERT等模型，提升语义理解和生成准确性。"
}

# 高亮标注函数
def highlight_keywords(text, keywords):
    """
    在文本中高亮标注关键词，并为关键词添加点击事件
    :param text: 原始文本
    :param keywords: 需要高亮的关键词及其解释（字典形式）
    :return: 高亮后的文本（HTML格式）
    """
    for keyword, explanation in keywords.items():
        # 使用 HTML 标签包裹关键词，并添加点击事件
        text = text.replace(
            keyword,
            f"<span style='background-color: yellow; cursor: pointer;' onclick='showExplanation(\"{keyword}\", \"{explanation}\")'>{keyword}</span>"
        )
    return text

# 添加 JavaScript 代码以显示解释
def add_javascript():
    """
    在页面中添加 JavaScript 代码，用于显示关键词的解释
    """
    js_code = """
    <script>
    function showExplanation(keyword, explanation) {
        alert(keyword + ": " + explanation);
    }
    </script>
    """
    st.components.v1.html(js_code, height=0)

def main():
    global model
    theme()
    side_bar()

    # 添加 JavaScript 代码
    add_javascript()

    doc_container = st.container()
    with doc_container:
        docs = upload_and_process_document()

        if docs:
            model = create_doc_gpt(
                docs,
                {k: v for k, v in docs[0].metadata.items() if k not in ['source', 'file_path']},
                st.session_state.g4f_provider
            )
            app_logger.info(f'{__file__}: Created model: {model}')
            del docs
        st.write('---')

    user_container = st.container()
    response_container = st.container()
    with user_container:
        query = st.text_input(
            "#### 问题:",
            placeholder='请输入您的问题'
        )

        if model and query and query != '' and not st.session_state.button_clicked:
            response = get_response(query, model)
            # 对响应文本进行高亮标注
            highlighted_response = highlight_keywords(response, HIGHLIGHT_KEYWORDS)
            st.session_state.query.append(query)
            st.session_state.response.append(highlighted_response)  # 存储高亮后的响应

    with response_container:
        if st.session_state['response']:
            for i in range(len(st.session_state['response'])-1, -1, -1):
                # 使用 st.markdown 显示高亮后的文本
                st.markdown(
                    f"**聊天机器人:** {st.session_state['response'][i]}",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"**您:** {st.session_state['query'][i]}",
                    unsafe_allow_html=True
                )

if __name__ == "__main__":
    main()



