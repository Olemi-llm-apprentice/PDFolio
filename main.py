import streamlit as st  # Streamlitライブラリのインポート
import fitz  # PyMuPDFのインポート
from PIL import Image, ImageDraw  # PILライブラリからImageとImageDrawをインポート
import tempfile  # 一時ファイル作成用ライブラリ

# PDFを画像に変換する関数
def pdf_to_image(pdf_path, page_number):
    pdf = fitz.open(pdf_path)  # PDFを開く
    page = pdf.load_page(page_number)  # 指定されたページを読み込む
    pix = page.get_pixmap()  # ページから画像データを取得
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)  # 画像データからPIL Imageを作成
    pdf.close()  # PDFを閉じる
    return img  # PIL Imageを返す

# Streamlit UIの設定
st.title("PDF Thumbnail Generator")  # タイトルの設定

# ファイルアップローダーの設定
uploaded_files = st.file_uploader("PDFファイルをアップロード", type=["pdf"], accept_multiple_files=True)

# ファイルがアップロードされた場合の処理
if uploaded_files:
    for uploaded_file in uploaded_files:  # 複数のファイルを一つずつ処理
        
       
        # 一時ファイルを作成してそのパスを取得
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        pdf = fitz.open(temp_file_path)  # 一時ファイルからPDFを読み込む
        num_pages = len(pdf)  # PDFのページ数を取得

        # 8ページごとに処理
        for start_page in range(num_pages):
            
            # # A4サイズの白い画像を作成
            # a4_img = Image.new("RGB", (595 * 2, 842 * 4), color="white")
            # draw = ImageDraw.Draw(a4_img)  # 描画オブジェクトを作成

            # 各ページを処理
            for i in range(num_pages):
                current_page = start_page + i
                if current_page >= num_pages:  # 最後のページに達したら終了
                    break

                img = pdf_to_image(temp_file_path, current_page)  # PDFページを画像に変換
                img.thumbnail((300, 300))  
                # # 画像を貼り付ける位置を計算
                # x_offset = (i % 2) * 595
                # y_offset = (i // 2) * 421

                # # A4画像にページ画像を貼り付け
                # a4_img.paste(img.resize((595, 421)), (x_offset, y_offset))
                # ページ名を追加
                # draw.text((x_offset, y_offset + 405), uploaded_file.name, fill="black")

                # 生成されたA4画像を表示
                st.image(img, width=150, caption=f"{uploaded_file.name} (Pages {start_page + 1}-{current_page + 1})")
