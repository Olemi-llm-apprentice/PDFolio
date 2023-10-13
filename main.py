import streamlit as st
import PyPDF2
from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont

# StreamlitアプリのUI
st.title("PDF Thumbnail Generator")

uploaded_files = st.file_uploader("PDFファイルをアップロード", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        pdf_reader = PyPDF2.PdfFileReader(uploaded_file)
        num_pages = pdf_reader.getNumPages()

        for start_page in range(0, num_pages, 8):  # A4には最大8ページ分のサムネイルを配置
            a4_img = Image.new("RGB", (595 * 2, 842 * 4), color="white")
            draw = ImageDraw.Draw(a4_img)

            for i in range(8):
                current_page = start_page + i
                if current_page >= num_pages:
                    break

                images = convert_from_path(uploaded_file, first_page=current_page + 1, last_page=current_page + 1)
                img = images[0]

                x_offset = (i % 2) * 595
                y_offset = (i // 2) * 421

                a4_img.paste(img.resize((595, 421)), (x_offset, y_offset))
                draw.text((x_offset, y_offset + 405), uploaded_file.name, fill="black")

            st.image(a4_img, caption=f"{uploaded_file.name} (Pages {start_page + 1}-{current_page + 1})")
