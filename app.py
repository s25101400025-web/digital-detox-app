import streamlit as st
import time
import pandas as pd

# ページ設定
st.set_page_config(page_title="受験生専用：合格への集中タイマー", layout="centered")

# セッション状態の初期化
if 'page' not in st.session_state:
    st.session_state.page = 'input'
if 'sabori_count' not in st.session_state:
    st.session_state.sabori_count = 0
if 'history' not in st.session_state:
    st.session_state.history = []
if 'target_minutes' not in st.session_state:
    st.session_state.target_minutes = 3

# --- JavaScriptでサボり検知 ---
st.components.v1.html(f"""
<script>
    document.addEventListener("visibilitychange", function() {{
        if (!document.hidden) {{
            alert("⚠️ 警告：他のページを見ていましたね？その数分が合否を分けます。");
            window.parent.postMessage({{type: 'sabori'}}, '*');
        }}
    }});
</script>
""", height=0)

# デザイン
st.markdown("""
<style>
    .stApp { background-color: #0e1117 !important; color: #ffffff; }
    .sabori-text { color: #ff4b4b; font-size: 24px; font-weight: bold; text-align: center; }
    .timer-font { font-size: 100px !important; font-weight: bold; text-align: center; color: #ff4b4b; }
    .stButton>button { width: 100%; border-radius: 20px; }
</style>
""", unsafe_allow_html=True)

# --- 1. 設定・診断画面 ---
if st.session_state.page == 'input':
    st.title("🎓 受験生用：時間損失計算機")
    
    usage = st.slider("1日のついつい見てしまうスマホ時間は？（時間）", 0, 10, 3)
    if st.button("現実を見る"):
        total_loss = usage * 100
        st.error(f"⚠️ 警告：入試までの残り100日で、合計 {total_loss} 時間を失う可能性があります。")
    
    st.markdown("---")
    st.subheader("⏱ 集中タイマー設定")
    st.session_state.target_minutes = st.select_slider(
        "何分間集中しますか？",
        options=[1, 3, 5, 10, 15, 20, 25, 30, 45, 60, 90, 120, 150, 180],
        value=3
    )
    
    if st.button(f"{st.session_state.target_minutes}分間の集中を開始する"):
        st.session_state.sabori_count = 0 # カウントをリセット
        st.session_state.page = 'timer'
        st.rerun()

# --- 2. タイマー画面 ---
elif st.session_state.page == 'timer':
    st.header("🚨 精神統一中 🚨")
    st.markdown(f"<p class='sabori-text'>現在の誘惑に負けた回数: {st.session_state.sabori_count} 回</p>", unsafe_allow_html=True)
    
    timer_placeholder = st.empty()
    
    # 中断ボタン
    if st.button("集中を中断してホームに戻る"):
        st.session_state.page = 'input'
        st.rerun()

    total_seconds = st.session_state.target_minutes * 60
    for t in range(total_seconds, -1, -1):
        m, s = divmod(t, 60)
        h, m = divmod(m, 60)
        time_str = f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"
        timer_placeholder.markdown(f"<div class='timer-font'>{time_str}</div>", unsafe_allow_html=True)
        time.sleep(1)
        
    st.session_state.history.append(st.session_state.sabori_count)
    st.session_state.page = 'result'
    st.rerun()

# --- 3. 結果・グラフ画面 ---
elif st.session_state.page == 'result':
    st.balloons()
    st.title("🎉 集中終了！")
    
    st.subheader("📊 集中レポート")
    st.write(f"今回のサボり回数: {st.session_state.sabori_count}回")
    
    if st.session_state.history:
        chart_data = pd.DataFrame({
            '回数': range(1, len(st.session_state.history) + 1),
            'サボり': st.session_state.history
        })
        st.bar_chart(data=chart_data, x='回数', y='サボり')

    # ホームに戻るボタン
    if st.button("🏠 ホーム（設定）に戻る"):
        st.session_state.sabori_count = 0
        st.session_state.page = 'input'
        st.rerun()
