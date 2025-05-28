import streamlit as st

st.set_page_config(page_title="税込金額X 計算アプリ", layout="centered")
st.title("税込金額X 計算アプリ")
st.markdown("入力値 V を指定して、求める税込金額 X を計算します。")

V = st.number_input("入力値 V（円）", min_value=0.0, format="%.2f")
if st.button("計算する"):
    k = 0.015 / 1.1
    X = V / (1 - k)
    st.success(f"税込金額 X: {X:.2f} 円")