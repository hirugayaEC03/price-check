# app.py
# Streamlit Cloud で動作・共有できる税込金額X計算アプリ
import streamlit as st

st.set_page_config(page_title="税込金額X 計算アプリ", layout="centered")
st.title("税込金額X 計算アプリ")

st.markdown("入力値 V と、税抜金額にかける割合を指定して、求める税込金額 X を計算します。")

# 入力: ユーザーが計算したい値 V
V = st.number_input(
    label="入力値 V（円）",
    min_value=0.0,
    format="%.2f"
)

# パラメータ: 税抜金額にかける割合（デフォルト 0.015）
ratio = st.number_input(
    label="税抜金額にかける割合",
    min_value=0.0,
    max_value=1.0,
    value=0.015,
    format="%.4f"
)

# 計算ボタン
if st.button("計算する"):
    # 定数 k = ratio / 1.1
    k = ratio / 1.1
    # 方程式: X - (X/1.1 * ratio) = V  →  X = V / (1 - k)
    try:
        X = V / (1 - k)
        st.success(f"税込金額 X: {X:.2f} 円")
    except ZeroDivisionError:
        st.error("設定された割合が不正です。1 - (ratio/1.1) が 0 にならないようにしてください。")

# デプロイ方法:
# 1. GitHub リポジトリに app.py を配置
# 2. requirements.txt に `streamlit` を追加
# 3. Streamlit Cloud (https://share.streamlit.io) でリポジトリを指定してデプロイ
