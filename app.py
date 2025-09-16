import streamlit as st
from PIL import Image
import io
import time

st.title("🖼️ 이미지 → PDF 변환기 (모바일 지원)")

# 세션 상태 초기화
if "uploads" not in st.session_state:
    st.session_state.uploads = []

# 여러 이미지 업로드
uploaded_files = st.file_uploader(
    "여러 장의 JPG/PNG 이미지를 업로드하세요",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    for f in uploaded_files:
        # 중복 파일 방지
        if f.name not in [x["name"] for x in st.session_state.uploads]:
            st.session_state.uploads.append({
                "name": f.name,
                "file": f,
                "ts": time.time()   # 업로드 시각 기록
            })

    # 업로드 순서대로 정렬
    files_sorted = sorted(st.session_state.uploads, key=lambda x: x["ts"])

    st.subheader("📂 병합 순서")
    st.write([f["name"] for f in files_sorted])

    if st.button("📌 PDF 만들기"):
        images = []
        for f in files_sorted:
            image = Image.open(f["file"]).convert("RGB")
            images.append(image)

        # 첫 번째 이미지를 기준으로 PDF 생성
        output_pdf = io.BytesIO()
        images[0].save(
            output_pdf, format="PDF", save_all=True, append_images=images[1:]
        )
        output_pdf.seek(0)

        # 다운로드 버튼 제공
        st.download_button(
            label="⬇️ PDF 다운로드",
            data=output_pdf,
            file_name="merged.pdf",
            mime="application/pdf"
        )
