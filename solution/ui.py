import os
import sys
from pathlib import Path
import streamlit as st
sys.path.insert(0,str(Path(__file__).parent))
from lab7 import ROOT,load,Retrieval,agent
st.set_page_config(page_title='Lab 7 Agentic RAG',layout='wide')
st.title('Lab 7 · Agentic RAG')
st.caption(f"Tìm kiếm thật trên dữ liệu Lab 6. Model: {os.getenv('GEMINI_MODEL', 'gemini-3.8-flash')}. Lỗi được hiển thị, không thay bằng dữ liệu giả.")
chunks=load(ROOT/'submission/data/chunks.json')
method=st.sidebar.selectbox('Phương pháp',['tfidf','dense','hybrid'])
budget=st.sidebar.slider('Context budget (ký tự)',800,6400,3200,400)
query=st.text_area('Câu hỏi')
@st.cache_resource
def retriever(method): return Retrieval(chunks,method)
if st.button('Tìm kiếm'):
 try:
  with st.spinner('Đang tìm...'): hits=retriever(method).search(query)
  for h in hits:
   with st.expander(f"{h['id']} · trang {h['page']} · {h['score']:.4f}",expanded=True): st.write(h['text']);st.json(h['metadata'])
 except Exception as e:st.error(f'{type(e).__name__}: kiểm tra database/model local. Không dùng fallback.')
allow=st.checkbox('Tôi xác nhận dự án Gemini là Free Tier, chưa liên kết thanh toán và cho phép gửi câu hỏi/evidence')
if st.button('Chạy agent',disabled=not allow):
 try:
  with st.spinner('Agent đang chạy...'): result=agent(query,retriever(method),budget)
  st.write(result['answer']);st.json(result)
 except Exception as e:st.error(f'{type(e).__name__}: kiểm tra .env, quyền API, quota và database; không có kết quả giả.')
