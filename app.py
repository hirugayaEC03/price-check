# app.py
# Streamlit Cloud で動作・共有できる税込金額X計算アプリ（入力履歴を残さない設定付き）
import streamlit as st
import re

# アプリ設定
st.set_page_config(page_title="税込金額X 計算アプリ", layout="centered")
st.title("税込金額X 計算アプリ")
st.markdown(
    "入力値 V（目標価格 円、カンマ区切り可）と、税抜金額にかける割合（％）を指定し、税込金額 X を計算します。"
)

# セッションステート初期化
for key, default in [('V_text', ''), ('pct', 1.5), ('result', None), ('error_msg', None)]:
    if key not in st.session_state:
        st.session_state[key] = default

# 計算処理コールバック
def on_submit():
    # エラーメッセージと結果を初期化
    st.session_state.error_msg = None
    st.session_state.result = None
    raw = st.session_state.V_text or ''
    # カンマ・スペースを除去し、数字とピリオドのみを抽出
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
        st.session_state.error_msg = (
            "有効な数値を入力してください（カンマ区切りやスペースは自動削除）。"
        )
    except ZeroDivisionError:
        st.session_state.error_msg = (
            "設定された割合が不正です。1 - (pct/100/1.1) が 0 になります。"
        )

# フォーム: Enterキーで計算を実行
with st.form(key="calc_form"):
    st.text_input(
        label="入力値 V（目標価格 円）", 
        key='V_text', 
        placeholder="例: 11,810",
        value=st.session_state.V_text,
        autocomplete="off"
    )
    st.number_input(
        label="税抜金額にかける割合 (%)", 
        min_value=0.0, max_value=100.0,
        format="%.2f", 
        key='pct'
    )
    st.form_submit_button("計算する", on_click=on_submit)

# エラーメッセージ表示
if st.session_state.error_msg:
    st.error(st.session_state.error_msg)

# 結果表示
if st.session_state.result:
    V_val, X_val = st.session_state.result
    st.success(f"目標価格: {V_val:,.2f} 円 → 税込金額 X: {X_val:,.2f} 円")

# デプロイ手順:
# 1. GitHub リポジトリに app.py と requirements.txt を配置
# 2. share.streamlit.io でリポジトリを指定してデプロイ