import streamlit as st
import time
import pandas as pd

# ページ設定
st.set_page_config(page_title="受験生専用：合格への3分集中", layout="centered")

# セッション状態の初期化
if 'page' not in st.session_state:
    st.session_state.page = 'input'
if 'sabori_count' not in st.session_state:
    st.session_state.sabori_count = 0
if 'history' not in st.session_state:
    st.session_state.history = []

# --- JavaScriptでサボりを検知してStreamlitに伝える ---
# ボタンを押して隠し要素をクリックさせることで、JSからPythonへデータを渡します
st.components.v1.html(f"""
<script>
    document.addEventListener("visibilitychange", function() {{
        if (!document.hidden) {{
            // タブに戻ってきたときに警告を出し、親ウィンドウのカウントを増やすリクエストを送る
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
</style>
""", unsafe_allow_html=True)

# --- 1. 診断画面 ---
if st.session_state.page == 'input':
    st.title("🎓 受験生用：時間損失計算機")
    usage = st.slider("1日のついつい見てしまうスマホ時間は？（時間）", 0, 10, 3)
    
    if st.button("現実を見る"):
        total_loss = usage * 100
        st.error(f"⚠️ 入試までの残り100日で、合計 {total_loss} 時間を失う可能性があります。")
        
    if st.button("今すぐ3分集中を開始する"):
        st.session_state.page = 'timer'
        st.rerun()

# --- 2. タイマー画面 ---
elif st.session_state.page == 'timer':
    st.header("🚨 精神統一中 🚨")
    
    # サボり回数の表示
    st.markdown(f"<p class='sabori-text'>現在の誘惑に負けた回数: {st.session_state.sabori_count} 回</p>", unsafe_allow_html=True)
    
    timer_placeholder = st.empty()
    
    # 簡易タイマー（デモ用に180秒）
    for t in range(180, -1, -1):
        m, s = divmod(t, 60)
        timer_placeholder.markdown(f"<h1 style='text-align:center; font-size:100px;'>{m:02d}:{s:02d}</h1>", unsafe_allow_html=True)
        
        # 途中でページが切り替わった際のサボり検知処理（擬似）
        # 実際にはJSからのメッセージを受け取る仕組みが必要ですが、
        # ここではシンプルに表示を維持します。
        time.sleep(1)
        
    # 終了後の処理
    st.session_state.history.append(st.session_state.sabori_count)
    st.session_state.page = 'result'
    st.rerun()

# --- 3. 結果・グラフ画面 ---
elif st.session_state.page == 'result':
    st.balloons()
    st.title("🎉 集中終了！")
    st.success("3分間の儀式が完了しました。")
    
    st.subheader("📊 今回の集中レポート")
    st.write(f"今回のサボり回数: {st.session_state.sabori_count}回")
    
    if st.session_state.history:
        st.write("これまでのサボり回数の推移:")
        chart_data = pd.DataFrame({
            '集中回数': range(1, len(st.session_state.history) + 1),
            'サボり回数': st.session_state.history
        })
        st.bar_chart(data=chart_data, x='集中回数', y='サボり回数')
        

    if st.button("もう一度挑戦してサボりゼロを目指す"):
        st.session_state.sabori_count = 0
        st.session_state.page = 'input'
        st.rerun()
