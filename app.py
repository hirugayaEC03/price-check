# app.py
# Streamlit Cloud で動作・共有できる税込金額X計算アプリ（目標価格表示＆V欄リセット対応）
import streamlit as st

st.set_page_config(page_title="税込金額X 計算アプリ", layout="centered")
st.title("税込金額X 計算アプリ")
st.markdown("入力値 V（目標価格）と、税抜金額にかける割合（％）を指定して、求める税込金額 X を表示します。計算後は V 欄が空欄になります。％は保持されます。")

# セッションステート初期化
if 'V_text' not in st.session_state:
    st.session_state.V_text = ''
if 'pct' not in st.session_state:
    st.session_state.pct = 1.5
if 'result' not in st.session_state:
    st.session_state.result = None

# 入力フィールド
V_text = st.text_input(
    label="入力値 V（目標価格 円）", value=st.session_state.V_text, key='V_text'
)
pct = st.number_input(
    label="税抜金額にかける割合 (%)", min_value=0.0, max_value=100.0,
    format="%.2f", key='pct'
)

# ボタン配置
col1, col2 = st.columns(2)
with col1:
    if st.button("計算する"):
        # V_text から float に変換
        try:
            V = float(st.session_state.V_text)
        except ValueError:
            st.error("有効な数値を入力してください。")
        else:
            ratio = st.session_state.pct / 100
            k = ratio / 1.1
            try:
                X = V / (1 - k)
                # 結果をセッションに保存
                st.session_state.result = (V, X)
                # V欄を空に
                st.session_state.V_text = ''
                st.experimental_rerun()
            except ZeroDivisionError:
                st.error("設定された割合が不正です。1 - (pct/100/1.1) が 0 にならないようにしてください。")
with col2:
    if st.button("クリア"):
        # V欄と結果をリセット（％は保持）
        st.session_state.V_text = ''
        st.session_state.result = None
        st.experimental_rerun()

# 計算結果の表示
if st.session_state.result:
    V_val, X_val = st.session_state.result
    st.success(f"目標価格: {V_val:.2f} 円 → 税込金額 X: {X_val:.2f} 円")

# デプロイ方法:
# 1. GitHub リポジトリに app.py を配置
# 2. requirements.txt に `streamlit` を追加
# 3. Streamlit Cloud (https://share.streamlit.io) でリポジトリを指定してデプロイ