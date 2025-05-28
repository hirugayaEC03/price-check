# app.py
# Streamlit Cloud で動作・共有できる税込金額X計算アプリ（Enterキー対応フォーム版）
import streamlit as st
import re

# アプリ設定
st.set_page_config(page_title="税込金額X 計算アプリ", layout="centered")
st.title("税込金額X 計算アプリ")
st.markdown(
    "入力値 V（目標価格 円、カンマ区切り可）と、税抜金額にかける割合（％）を指定し、税込金額 X を計算します。"
)

# セッションステート初期化
if 'V_text' not in st.session_state:
    st.session_state.V_text = ''
if 'pct' not in st.session_state:
    st.session_state.pct = 1.5
if 'result' not in st.session_state:
    st.session_state.result = None
if 'error_msg' not in st.session_state:
    st.session_state.error_msg = None

# フォームを使用してEnterキーで送信を可能に
with st.form(key="calc_form", clear_on_submit=False):
    V_text = st.text_input(
        label="入力値 V（目標価格 円）",
        value=st.session_state.V_text,
        key='V_text',
        placeholder="例: 11,810"
    )
    pct = st.number_input(
        label="税抜金額にかける割合 (%)",
        min_value=0.0, max_value=100.0,
        format="%.2f",
        key='pct'
    )
    submitted = st.form_submit_button("計算する")
    if submitted:
        st.session_state.error_msg = None
        raw = st.session_state.V_text
        # 数字とピリオド以外を除去
        cleaned = re.sub(r"[^0-9.]", "", raw)
        try:
            V = float(cleaned)
            ratio = st.session_state.pct / 100
            k = ratio / 1.1
            X = V / (1 - k)
            st.session_state.result = (V, X)
            # 計算後に入力値をクリア
            st.session_state.V_text = ''
        except ValueError:
            st.session_state.error_msg = "有効な数値を入力してください（カンマ区切りやスペースは自動削除）。"
            st.session_state.result = None
        except ZeroDivisionError:
            st.session_state.error_msg = "設定された割合が不正です。1 - (pct/100/1.1) が 0 になります。"
            st.session_state.result = None

# エラーメッセージの表示
if st.session_state.error_msg:
    st.error(st.session_state.error_msg)

# 結果の表示
if st.session_state.result:
    V_val, X_val = st.session_state.result
    st.success(f"目標価格: {V_val:,.2f} 円 → 税込金額 X: {X_val:,.2f} 円")

# デプロイ手順:
# GitHub に app.py と requirements.txt を配置し、share.streamlit.io で指定してデプロイ