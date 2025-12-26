import streamlit as st
import time

# ページ設定
st.set_page_config(page_title="受験生専用：合格への3分集中", layout="centered")

# 離脱防止のJavaScriptを埋め込み
st.components.v1.html("""
<script>
    // タブを閉じようとした時の警告
    window.onbeforeunload = function() {
        return "集中を中断すると、合格が遠ざかります。本当にあきらめますか？";
    };

    // タブが切り替わった（サボった）ことを検知
    document.addEventListener("visibilitychange", function() {
        if (document.hidden) {
            console.log("サボり検知");
        } else {
            alert("⚠️ 警告：他のページを見ていましたね？その数分が合否を分けます。");
        }
    });
</script>
""", height=0)

# デザイン（CSS）
st.markdown("""
<style>
    .stApp { background-color: #0e1117 !important; color: #ffffff; }
    .status-card {
        background: #1e1e1e;
        border-left: 5px solid #ff4b4b;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .timer-font { font-size: 100px !important; font-weight: bold; text-align: center; color: #ff4b4b; }
</style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'input'

# --- 診断/入口画面 ---
if st.session_state.page == 'input':
    st.title("🎓 受験生用：時間損失計算機")
    usage = st.slider("1日のついつい見てしまうスマホ時間は？（時間）", 0, 10, 3)
    
    if st.button("現実を見る"):
        # 受験までの残り日数を仮に100日として計算
        days_left = 100
        total_loss = usage * days_left
        st.error(f"⚠️ 警告：入試までの残り100日で、あなたは合計 {total_loss} 時間をドブに捨てようとしています。")
        st.markdown(f"これは過去問 **{int(total_loss/2)}年分** を解く時間に相当します。")
        
        if st.button("今すぐスマホを置いて3分集中する"):
            st.session_state.page = 'timer'
            st.rerun()

# --- タイマー画面 ---
elif st.session_state.page == 'timer':
    st.markdown("<h2 style='text-align:center;'>🚨 精神統一中 🚨</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>このタブを閉じたり、別のページを見たら『不合格』が確定します。</p>", unsafe_allow_html=True)
    
    placeholder = st.empty()
    for t in range(180, -1, -1):
        m, s = divmod(t, 60)
        placeholder.markdown(f"<div class='timer-font'>{m:02d}:{s:02d}</div>", unsafe_allow_html=True)
        time.sleep(1)
        
    st.balloons()
    st.success("集中成功。この調子で机に向かいましょう！")
    if st.button("もう一度診断へ"):
        st.session_state.page = 'input'
        st.rerun()
