# app.py
# Streamlit Cloud で動作・共有できる税込金額X計算アプリ（カンマ対応＆テキスト入力確実化）
import streamlit as st
import re

st.set_page_config(page_title="税込金額X 計算アプリ", layout="centered")
st.title("税込金額X 計算アプリ")
st.markdown(
    "入力値 V（目標価格 円、カンマ区切り可）と、税抜金額にかける割合（％）を指定し、税込金額 X を計算します。"
)

# セッションステート初期化
if 'pct' not in st.session_state:
    st.session_state.pct = 1.5
if 'V_text' not in st.session_state:
    st.session_state.V_text = ''
if 'result' not in st.session_state:
    st.session_state.result = None
if 'error_msg' not in st.session_state:
    st.session_state.error_msg = None

# コールバック関数定義
def on_calculate():
    st.session_state.error_msg = None
    # テキスト入力から数値を抽出（数字とピリオドのみ残す）
    raw = st.session_state.V_text
    cleaned = re.sub(r"[^0-9.]", "", raw)
    try:
        V = float(cleaned)
        ratio = st.session_state.pct / 100
        k = ratio / 1.1
        X = V / (1 - k)
        st.session_state.result = (V, X)
        # 入力欄クリア
        st.session_state.V_text = ''
    except ValueError:
        st.session_state.error_msg = "有効な数値を入力してください（カンマ区切りやスペースは自動削除）。"
    except ZeroDivisionError:
        st.session_state.error_msg = "設定された割合が不正です。1 - (pct/100/1.1) が 0 になります。"

# クリア用コールバック
def on_clear():
    st.session_state.V_text = ''
    st.session_state.result = None
    st.session_state.error_msg = None

# 入力フォーム（value 指定でテキスト入力を確実に反映）
st.text_input(
    label="入力値 V（目標価格 円）", 
    value=st.session_state.V_text,
    key='V_text',
    placeholder="例: 1,234,567"
)
st.number_input(
    label="税抜金額にかける割合 (%)", 
    min_value=0.0, max_value=100.0,
    format="%.2f", 
    key='pct'
)

# ボタン配置
col1, col2 = st.columns(2)
with col1:
    st.button("計算する", on_click=on_calculate)
with col2:
    st.button("クリア", on_click=on_clear)

# エラーメッセージ表示
if st.session_state.error_msg:
    st.error(st.session_state.error_msg)

# 結果表示
if st.session_state.result:
    V_val, X_val = st.session_state.result
    # 結果は千位区切りで表示
    st.success(f"目標価格: {V_val:,.2f} 円 → 税込金額 X: {X_val:,.2f} 円")

# デプロイメモ:
# GitHub に app.py と requirements.txt を配置し、share.streamlit.io で指定してデプロイ