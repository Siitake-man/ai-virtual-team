import sys
import os
# プロジェクトルートディレクトリをPython検索パスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from dotenv import load_dotenv
from app.api_client import APIClient

# 環境変数の読み込み
load_dotenv()

# ページレイアウトの設定
st.set_page_config(
    page_title="AI Virtual Team Builder",
    layout="wide",
    initial_sidebar_state="expanded"
)

# プレミアムデザイン用CSSインジェクション
st.markdown("""
<style>
    .gradient-text {
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 0.2rem;
    }
    .subtitle-text {
        color: #9ca3af;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
    .employee-card {
        background: rgba(31, 41, 55, 0.45);
        border: 1px solid rgba(75, 85, 99, 0.3);
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(8px);
    }
    .card-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #f3f4f6;
        margin-bottom: 0.5rem;
    }
    .card-meta {
        font-size: 0.85rem;
        color: #a78bfa;
        margin-bottom: 0.5rem;
    }
    .card-detail {
        font-size: 0.9rem;
        color: #d1d5db;
        line-height: 1.4;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if "selected_project_id" not in st.session_state:
    st.session_state.selected_project_id = None
if "editing_employee_id" not in st.session_state:
    st.session_state.editing_employee_id = None

# プロジェクト一覧のロード
projects = APIClient.list_projects()
project_options = {p["name"]: p["id"] for p in projects}

# ----------------- サイドバー領域 -----------------
with st.sidebar:
    st.header("⚙️ プロジェクト設定")
    
    # 1. プロジェクト切り替え
    if project_options:
        project_names = list(project_options.keys())
        
        # セッション状態とセレクトボックスの同期
        default_index = 0
        if st.session_state.selected_project_id in project_options.values():
            default_index = list(project_options.values()).index(st.session_state.selected_project_id)
            
        selected_name = st.selectbox("アクティブなプロジェクト", project_names, index=default_index)
        st.session_state.selected_project_id = project_options[selected_name]
    else:
        st.info("プロジェクトがありません。新規作成してください。")
        st.session_state.selected_project_id = None

    st.markdown("---")
    
    # 2. 新規プロジェクト作成フォーム
    with st.expander("📁 新規プロジェクト作成"):
        new_id = st.text_input("プロジェクトID", placeholder="例: npo-trust-platform", key="create_proj_id")
        new_name = st.text_input("プロジェクト名", placeholder="例: NPO Trust Platform", key="create_proj_name")
        submit_proj = st.button("作成", key="create_proj_submit", use_container_width=True)
        
        if submit_proj:
            if not new_id or not new_name:
                st.error("すべてのフィールドを入力してください。")
            else:
                safe_id = "".join(c for c in new_id if c.isalnum() or c in ("-", "_")).lower()
                res = APIClient.create_project(safe_id, new_name)
                if res:
                    st.success(f"プロジェクト '{new_name}' を作成しました！")
                    st.session_state.selected_project_id = safe_id
                    st.rerun()
                else:
                    st.error("作成に失敗しました。IDが重複している可能性があります。")

    st.markdown("---")

    # 3. プロジェクト削除
    if st.session_state.selected_project_id:
        current_id = st.session_state.selected_project_id
        if st.button("🗑️ プロジェクトを削除", use_container_width=True):
            if APIClient.delete_project(current_id):
                st.toast("プロジェクトを削除しました。")
                st.session_state.selected_project_id = None
                st.rerun()
            else:
                st.error("プロジェクトの削除に失敗しました。")

# ----------------- メインエリア -----------------
st.markdown('<div class="gradient-text">🤖 AIバーチャルチームビルダー</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">プロジェクト固有の「魂」と「人格」を持つ仮想従業員チームの構築</div>', unsafe_allow_html=True)

# プロジェクト未選択時の表示
if not st.session_state.selected_project_id:
    st.warning("サイドバーからプロジェクトを選択するか、新しく作成してください。")
    st.stop()

# 選択中プロジェクトのデータ取得
project = APIClient.get_project(st.session_state.selected_project_id)
if not project:
    st.error("プロジェクトデータの読み込みに失敗しました。")
    st.stop()

# メンバー一覧とアクティブ数
active_employees = [e for e in project.get("employees", []) if e.get("is_active", True)]
st.sidebar.markdown(f"**アクティブ従業員数**: {len(active_employees)} / {len(project.get('employees', []))}名")

# メインタブの構成
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👥 従業員管理", 
    "💬 個別チャット", 
    "🔍 全員同時レビュー",
    "📚 知識ストック", 
    "📥 エクスポート"
])

# ----------------- タブ1: 従業員管理 -----------------
with tab1:
    st.subheader("👥 仮想従業員チーム")
    
    # オーナー設定セクション
    with st.expander("👤 オーナー設定（従業員への共通注入コンテキスト）", expanded=False):
        owner_ctx = project.get("owner_context", {})
        with st.form("owner_context_form"):
            motivation = st.text_area("1. プロジェクトの動機・背景 (Why)", value=owner_ctx.get("motivation", ""))
            vision = st.text_area("2. ビジョン（5年後の目標）", value=owner_ctx.get("vision", ""))
            values = st.text_area("3. 大切にしている価値観・判断基準", value=owner_ctx.get("values", ""))
            ng_items = st.text_area("4. 絶対にやってはいけないこと (NG項目)", value=owner_ctx.get("ng_items", ""))
            current_phase = st.text_input("5. 現在の開発フェーズ", value=owner_ctx.get("current_phase", ""))
            
            save_owner = st.form_submit_button("オーナー設定を保存")
            if save_owner:
                new_owner_context = {
                    "motivation": motivation,
                    "vision": vision,
                    "values": values,
                    "ng_items": ng_items,
                    "current_phase": current_phase
                }
                res = APIClient.update_owner_context(project["id"], new_owner_context)
                if res:
                    st.success("オーナー設定を更新しました！")
                    st.rerun()
                else:
                    st.error("更新に失敗しました。")

    col_list, col_form = st.columns([3, 2])
    
    # 従業員一覧 (左カラム)
    with col_list:
        st.markdown("### 従業員メンバーリスト")
        employees = project.get("employees", [])
        
        if not employees:
            st.info("このプロジェクトにはまだ従業員が登録されていません。右のフォームから追加してください。")
        else:
            for emp in employees:
                # 従業員カードのレンダリング
                status_label = "🟢 アクティブ" if emp.get("is_active", True) else "🔴 非アクティブ"
                
                st.markdown(f"""
                <div class="employee-card">
                    <div class="card-title">{emp['display_name']}</div>
                    <div class="card-meta">専門領域: {emp['specialty']} | モデル: {emp['llm_model']} | 状態: {status_label}</div>
                    <div class="card-detail"><strong>人格プロンプト:</strong><br>{emp['personality_prompt'][:100]}...</div>
                </div>
                """, unsafe_allow_html=True)
                
                # アクション用ミニカラム
                btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 3])
                
                # 1. 編集ボタン
                if btn_col1.button("✍️ 編集", key=f"edit_btn_{emp['id']}"):
                    st.session_state.editing_employee_id = emp["id"]
                    st.rerun()
                
                # 2. 削除ボタン
                if btn_col2.button("🗑️ 削除", key=f"del_btn_{emp['id']}"):
                    if APIClient.delete_employee(project["id"], emp["id"]):
                        st.toast(f"従業員 {emp['name']} を削除しました。")
                        st.rerun()
                    else:
                        st.error("削除に失敗しました。")
                        
                # 3. アクティブ状態切替トグル
                is_active = emp.get("is_active", True)
                toggle_label = "アクティブ状態を無効化" if is_active else "アクティブ状態を有効化"
                if btn_col3.button(toggle_label, key=f"toggle_btn_{emp['id']}"):
                    APIClient.update_employee(project["id"], emp["id"], {"is_active": not is_active})
                    st.rerun()

    # 追加・編集フォーム (右カラム)
    with col_form:
        if st.session_state.editing_employee_id:
            st.markdown("### ✍️ 従業員情報の編集")
            editing_id = st.session_state.editing_employee_id
            # 現在のデータを取得
            emp_data = next((e for e in project.get("employees", []) if e["id"] == editing_id), None)
            
            if emp_data:
                with st.form("edit_employee_form"):
                    edit_name = st.text_input("名前", value=emp_data["name"])
                    edit_attr = st.selectbox(
                        "属性", 
                        ["クリティカル", "ドリーマー", "リアリスト", "専門家", "カスタム"],
                        index=["クリティカル", "ドリーマー", "リアリスト", "専門家", "カスタム"].index(
                            emp_data["attribute"] if emp_data["attribute"] in ["クリティカル", "ドリーマー", "リアリスト", "専門家", "カスタム"] else "カスタム"
                        )
                    )
                    edit_spec = st.text_input("専門領域", value=emp_data["specialty"])
                    edit_model = st.selectbox("使用LLMモデル", ["gemini-2.0-flash", "claude-3-5-sonnet", "gpt-4o"], index=["gemini-2.0-flash", "claude-3-5-sonnet", "gpt-4o"].index(emp_data["llm_model"]) if emp_data["llm_model"] in ["gemini-2.0-flash", "claude-3-5-sonnet", "gpt-4o"] else 0)
                    edit_prompt = st.text_area("人格プロンプト", value=emp_data["personality_prompt"], height=200)
                    edit_active = st.checkbox("アクティブにする", value=emp_data.get("is_active", True))
                    
                    col_form_btns = st.columns([1, 1])
                    submitted = col_form_btns[0].form_submit_button("保存")
                    canceled = col_form_btns[1].form_submit_button("キャンセル")
                    
                    if submitted:
                        update_payload = {
                            "name": edit_name,
                            "attribute": edit_attr,
                            "specialty": edit_spec,
                            "llm_model": edit_model,
                            "personality_prompt": edit_prompt,
                            "is_active": edit_active
                        }
                        res = APIClient.update_employee(project["id"], editing_id, update_payload)
                        if res:
                            st.success(f"{edit_name} の情報を更新しました！")
                            st.session_state.editing_employee_id = None
                            st.rerun()
                        else:
                            st.error("更新に失敗しました。")
                    if canceled:
                        st.session_state.editing_employee_id = None
                        st.rerun()
            else:
                st.session_state.editing_employee_id = None
                st.rerun()
        else:
            st.markdown("### ➕ 従業員の追加")
            with st.form("add_employee_form", clear_on_submit=True):
                add_name = st.text_input("名前", placeholder="例: 鋭子")
                add_attr = st.selectbox("属性", ["クリティカル", "ドリーマー", "リアリスト", "専門家", "カスタム"])
                add_spec = st.text_input("専門領域", placeholder="例: リスク洗い出し・デバッグ")
                add_model = st.selectbox("使用LLMモデル", ["gemini-2.0-flash", "claude-3-5-sonnet", "gpt-4o"])
                add_prompt = st.text_area("人格プロンプト (自由記述、または後で自動生成)", placeholder="例: あなたは批判的な思考を持つアドバイザーです。最悪のシナリオを考慮した設計チェックを行います。")
                
                submit_emp = st.form_submit_button("従業員をチームに追加")
                if submit_emp:
                    if not add_name or not add_spec:
                        st.error("名前と専門領域を入力してください。")
                    else:
                        payload = {
                            "name": add_name,
                            "attribute": add_attr,
                            "specialty": add_spec,
                            "personality_prompt": add_prompt,
                            "llm_model": add_model,
                            "is_active": True
                        }
                        res = APIClient.add_employee(project["id"], payload)
                        if res:
                            st.success(f"{add_name} がチームに加わりました！")
                            st.rerun()
                        else:
                            st.error("従業員の追加に失敗しました。")

# ----------------- タブ2: 個別チャット -----------------
with tab2:
    st.subheader("💬 仮想従業員との個別対話")
    
    # 登録されている従業員リストを取得
    employees = project.get("employees", [])
    active_emp_options = {e["display_name"]: e["id"] for e in employees if e.get("is_active", True)}
    
    if not active_emp_options:
        st.info("アクティブな従業員がいません。従業員管理タブで従業員を追加・有効化してください。")
    else:
        # 従業員選択
        selected_emp_name = st.selectbox("対話する従業員を選択", list(active_emp_options.keys()), key="chat_emp_select")
        selected_emp_id = active_emp_options[selected_emp_name]
        selected_emp = next((e for e in employees if e["id"] == selected_emp_id), None)
        
        if selected_emp:
            st.caption(f"🎯 専門領域: {selected_emp['specialty']} | 🤖 使用モデル: {selected_emp['llm_model']}")
            
            # 対話履歴クリアボタン
            if st.button("🗑️ 対話履歴をクリア", key="clear_chat_history_btn", use_container_width=True):
                if APIClient.clear_chat_history(project["id"], selected_emp_id):
                    st.toast("対話履歴をクリアしました。")
                    st.rerun()
            
            st.markdown("---")
            
            # 会話履歴の取得と表示
            chat_history = APIClient.get_chat_history(project["id"], selected_emp_id)
            
            # チャット履歴コンテナの描画
            for msg in chat_history:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
            
            # ユーザーからのメッセージ入力
            if prompt := st.chat_input(f"{selected_emp['name']} に相談する..."):
                # 画面上にユーザーメッセージを即座に表示
                with st.chat_message("user"):
                    st.write(prompt)
                
                # APIを呼び出してGeminiの応答を取得
                with st.spinner(f"{selected_emp['name']} が回答を生成中..."):
                    res = APIClient.send_chat_message(project["id"], selected_emp_id, prompt)
                    if res:
                        # 画面上にAI応答を表示
                        with st.chat_message("assistant"):
                            st.write(res["content"])
                        st.rerun()
                    else:
                        st.error("メッセージの送信または応答の取得に失敗しました。.envファイルに「GEMINI_API_KEY」が正しく設定されているか確認してください。")

# ----------------- タブ3: 全員同時レビュー (スケルトン) -----------------
with tab3:
    st.subheader("🔍 全員同時レビュー")
    st.info("全員同時レビュー機能は Phase 2 で実装予定です。")

# ----------------- タブ4: 知識ストック (スケルトン) -----------------
with tab4:
    st.subheader("📚 知識ストック")
    st.info("知識ストック管理機能は Phase 2 で実装予定です。")

# ----------------- タブ5: エクスポート (スケルトン) -----------------
with tab5:
    st.subheader("📥 エクスポート")
    st.info("エクスポート機能は Phase 3 で実装予定です。")
