import asyncio
import os

import streamlit as st

from docGPT import GPT4Free


def side_bar() -> None:
    with st.sidebar:
        with st.expander(':orange[如何使用？]'):
            st.markdown(
                """
                1. 输入您的 API 密钥：（您可以使用 `gpt4free` 免费模型 **无需 API 密钥**）
                    * `OpenAI API 密钥`：确保您还有剩余的使用额度
                    * `SERPAPI API 密钥`：可选。如果您想询问不在 PDF 文档中的内容，需要此密钥。
                2. **上传文档** 文件（选择一种方法）：
                    * 方法1：从本地计算机浏览并上传自己的文档文件。
                    * 方法2：直接输入文档的 URL 链接。
                    
                    （**支持的文档类型**：`.pdf`, `.docx`, `.csv`, `.txt`）
                3. 开始提问！
                4. 更多详情。（https://github.com/Lin-jun-xiang/docGPT-streamlit）
                5. 如果有任何问题，请随时留言并参与讨论。（https://github.com/Lin-jun-xiang/docGPT-streamlit/issues）
                """
            )

    with st.sidebar:
        if st.session_state.openai_api_key:
            OPENAI_API_KEY = st.session_state.openai_api_key
            st.sidebar.success('API 密钥已从之前的输入加载')
        else:
            OPENAI_API_KEY = st.sidebar.text_input(
                label='#### 您的 OpenAI API 密钥 👇',
                placeholder="sk-...",
                type="password",
                key='OPENAI_API_KEY'
            )
            st.session_state.openai_api_key = OPENAI_API_KEY

        os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

    with st.sidebar:
        if st.session_state.serpapi_api_key:
            SERPAPI_API_KEY = st.session_state.serpapi_api_key
            st.sidebar.success('API 密钥已从之前的输入加载')
        else:
            SERPAPI_API_KEY = st.sidebar.text_input(
                label='#### 您的 SERPAPI API 密钥 👇',
                placeholder="...",
                type="password",
                key='SERPAPI_API_KEY'
            )
            st.session_state.serpapi_api_key = SERPAPI_API_KEY

        os.environ['SERPAPI_API_KEY'] = SERPAPI_API_KEY

    with st.sidebar:
        gpt4free = GPT4Free()
        st.session_state.g4f_provider = st.selectbox(
            (
                "#### 如果要使用免费模型，请选择提供商. "
                "([详细信息](https://github.com/xtekky/gpt4free#models))"
            ),
            (['BestProvider'] + list(gpt4free.providers_table.keys()))
        )

        st.session_state.button_clicked = st.button(
            '显示可用的提供商',
            help='点击以测试当前哪些提供商可用。',
            type='primary'
        )
        if st.session_state.button_clicked:
            available_providers = asyncio.run(gpt4free.show_available_providers())
            st.session_state.query.append('当前有哪些可用的提供商？')
            st.session_state.response.append(
                '当前可用的提供商有：\n'
                f'{available_providers}'
            )



