import streamlit as st
from PIL import Image
import io
import os

st.title("📸 JPG → PDF 변환기")

st.write("여러 장의 JPG/PNG 이미지를 업로드하면 하나의 PDF로 합쳐드립니다.")

# 여러 이미지 업로드 가능
uploaded_files = st.file_uploader(
    "이미지 파일을 업로드하세요", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

if uploaded_files:
    # 파일을 업로드 순서대로 정렬 (원하면 촬영일/EXIF 기준 정렬도 가능)
    images = []
    for file in uploaded_files:
        img = Image.open(file)
        images.append(img.convert("RGB"))

    # PDF 생성
    pdf_bytes = io.BytesIO()
    images[0].save(
        pdf_bytes, format="PDF", save_all=True, append_images=images[1:]
    )
    pdf_bytes.seek(0)

    st.success("✅ 변환 완료! 아래 버튼으로 다운로드하세요.")

    # 다운로드 버튼 제공
    st.download_button(
        label="📥 PDF 다운로드",
        data=pdf_bytes,
        file_name="merged.pdf",
        mime="application/pdf"
    )
