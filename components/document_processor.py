import os
import tempfile

import streamlit as st

from model import DocumentLoader


def upload_and_process_document() -> list:
    st.write('#### 上传文档文件')
    browse, url_link = st.tabs(
        ['拖拽文件到此处 (浏览本地文件)', '进入文件URL链接']
    )
    with browse:
        upload_file = st.file_uploader(
            '浏览本地文件 (.pdf, .docx, .csv, `.txt`)',
            type=['pdf', 'docx', 'csv', 'txt'],
            label_visibility='hidden'
        )
        filetype = os.path.splitext(upload_file.name)[1].lower() if upload_file else None
        upload_file = upload_file.read() if upload_file else None

    with url_link:
        doc_url = st.text_input(
            "进入文件URL链接 (.pdf, .docx, .csv, .txt)",
            placeholder='https://www.xxx/uploads/file.pdf',
            label_visibility='hidden'
        )
        if doc_url:
            upload_file, filetype = DocumentLoader.crawl_file(doc_url)

    if upload_file and filetype:
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(upload_file)
        temp_file_path = temp_file.name

        docs = DocumentLoader.load_documents(temp_file_path, filetype)
        docs = DocumentLoader.split_documents(
            docs, chunk_size=2000,
            chunk_overlap=200
        )

        temp_file.close()
        if temp_file_path:
            os.remove(temp_file_path)

        return docs
