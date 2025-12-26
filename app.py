import streamlit as st
import time

# ページ設定
st.set_page_config(page_title="受験生専用：合格への3分集中")

# デザイン
st.markdown("""
<style>
    .stApp { background-color: #0e1117 !important; color: #ffffff; }
    h1, h2, p { text-align: center; }
</style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'input'

# --- 1. 診断画面 ---
if st.session_state.page == 'input':
    st.title("🎓 受験生用：時間損失計算機")
    usage = st.slider("1日のついつい見てしまうスマホ時間は？（時間）", 0, 10, 3)
    
    if st.button("現実を見る"):
        total_loss = usage * 100
        st.error(f"⚠️ 入試までの残り100日で、あなたは合計 {total_loss} 時間を失う可能性があります。")
        st.write(f"これは過去問 {int(total_loss/2)} 年分に相当します。")
        
    if st.button("今すぐ3分集中を開始する"):
        st.session_state.page = 'timer'
        st.rerun()

# --- 2. タイマー画面 ---
elif st.session_state.page == 'timer':
    st.header("🚨 精神統一中 🚨")
    st.write("この画面を開いたまま、机に向かってください。")
    
    # シンプルなタイマー表示
    timer_display = st.empty()
    
    for t in range(180, -1, -1):
        m, s = divmod(t, 60)
        # 文字サイズを大きく表示
        timer_display.markdown(f"<h1 style='font-size: 100px;'>{m:02d}:{s:02d}</h1>", unsafe_allow_html=True)
        time.sleep(1)
        
    st.balloons()
    st.success("3分間の集中、お見事です！そのまま勉強を続けましょう。")
    if st.button("最初に戻る"):
        st.session_state.page = 'input'
        st.rerun()

# --- 最後に警告機能を配置（干渉防止） ---
st.components.v1.html("""
<script>
    document.addEventListener("visibilitychange", function() {
        if (!document.hidden) {
            alert("⚠️ 警告：他のページを見ていましたね？その数分が合否を分けます。");
        }
    });
</script>
""", height=0)
