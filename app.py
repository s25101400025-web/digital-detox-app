import streamlit as st
import time

# ページ設定
st.set_page_config(page_title="デジタルデトックス診断", layout="centered")

# デザイン（CSS）
st.markdown("""
<style>
    .stApp { background-color: #1b3c2c !important; color: #f2f2f2; }
    .card {
        background: linear-gradient(135deg, #223a2e 70%, #35564a 100%);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        border: 1px solid rgba(190,245,200,0.2);
    }
    .timer-display { font-size: 80px; text-align: center; color: #4CAF50; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 状態管理
if 'page' not in st.session_state:
    st.session_state.page = 'input'

# --- 診断画面 ---
if st.session_state.page == 'input':
    st.title("デジタルデトックス診断")
    usage = st.slider("1日のスマホ利用時間は？（時間）", 0, 24, 3)
    
    if st.button("診断する"):
        loss_30y = usage * 365 * 30
        money_30y = loss_30y * 1500
        st.session_state.result_text = f"30年で {loss_30y:,} 時間（約{money_30y:,}円）の損失です。"
        st.session_state.show_result = True

    if st.session_state.get('show_result'):
        st.markdown(f"<div class='card'><h2>衝撃の診断結果</h2><p>{st.session_state.result_text}</p></div>", unsafe_allow_html=True)
        # ここでボタンを押すとページが切り替わる
        if st.button("今この瞬間から、自分を取り戻す"):
            st.session_state.page = 'timer'
            st.rerun()

# --- タイマー画面 ---
elif st.session_state.page == 'timer':
    st.markdown("<h2 style='text-align:center;'>🧘 デトックス・タイム</h2>", unsafe_allow_html=True)
    placeholder = st.empty()
    for t in range(180, -1, -1):
        m, s = divmod(t, 60)
        placeholder.markdown(f"<div class='timer-display'>{m:02d}:{s:02d}</div>", unsafe_allow_html=True)
        time.sleep(1)
    st.balloons()
    st.success("素晴らしい！新しい一歩です。")
    if st.button("戻る"):
        st.session_state.page = 'input'
        st.session_state.show_result = False
        st.rerun()
