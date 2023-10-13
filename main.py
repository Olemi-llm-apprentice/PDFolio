import streamlit as st
import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont
import tempfile

# StreamlitアプリのUI
st.title("PDF Thumbnail Generator")

def pdf_to_image(pdf_path, page_number):
    pdf = fitz.open(pdf_path)
    page = pdf.load_page(page_number)
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return img

uploaded_files = st.file_uploader("PDFファイルをアップロード", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        # 一時ファイルを作成
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        pdf_reader = fitz.open(temp_file_path)
        num_pages = len(pdf_reader)

        for start_page in range(0, num_pages, 8):  # A4には最大8ページ分のサムネイルを配置
            a4_img = Image.new("RGB", (595 * 2, 842 * 4), color="white")
            draw = ImageDraw.Draw(a4_img)

            for i in range(8):
                current_page = start_page + i
                if current_page >= num_pages:
                    break

                img = pdf_to_image(temp_file_path, current_page)

                x_offset = (i % 2) * 595
                y_offset = (i // 2) * 421

                a4_img.paste(img.resize((595, 421)), (x_offset, y_offset))
                draw.text((x_offset, y_offset + 405), uploaded_file.name, fill="black")

            st.image(a4_img, caption=f"{uploaded_file.name} (Pages {start_page + 1}-{current_page + 1})")
