import streamlit as st
from PyPDF2 import PdfMerger
import time
import io

st.title("📑 PDF 병합기 (모바일 지원 버전)")

# 세션 상태에 업로드 기록 저장
if "uploads" not in st.session_state:
    st.session_state.uploads = []

# 여러 파일 업로드 가능
uploaded_files = st.file_uploader("여러 PDF 파일을 업로드하세요", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    for f in uploaded_files:
        # 동일 파일명이 중복 저장되지 않도록 체크
        if f.name not in [x["name"] for x in st.session_state.uploads]:
            st.session_state.uploads.append({
                "name": f.name,
                "file": f,
                "ts": time.time()   # 업로드 시각 기록
            })

    # 업로드된 시간(ts) 기준으로 정렬
    files_sorted = sorted(st.session_state.uploads, key=lambda x: x["ts"])

    st.subheader("📂 병합 순서")
    st.write([f["name"] for f in files_sorted])

    if st.button("📌 병합하기"):
        merger = PdfMerger()
        for f in files_sorted:
            merger.append(f["file"])

        # 병합된 결과를 메모리 버퍼에 저장
        output_pdf = io.BytesIO()
        merger.write(output_pdf)
        merger.close()
        output_pdf.seek(0)

        # 다운로드 버튼 제공
        st.download_button(
            label="⬇️ 병합된 PDF 다운로드",
            data=output_pdf,
            file_name="merged.pdf",
            mime="application/pdf"
        )
