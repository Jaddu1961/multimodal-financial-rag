# ============================================
# SIDEBAR COMPONENT
# ============================================

import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from frontend.streamlit.api_client import check_health, get_documents, get_stats
from frontend.streamlit.config import SAMPLE_QUESTIONS, APP_VERSION, COLORS


def render_sidebar():
    """Render the left sidebar with system info and controls"""

    with st.sidebar:

        # --- Logo & Title ---
        st.markdown("""
            <div style='text-align: center; padding: 1.2rem 0 0.5rem 0;'>
                <div style='
                    background: linear-gradient(135deg, #2563EB, #B01228);
                    width: 65px;
                    height: 65px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0 auto 0.8rem auto;
                    font-size: 1.8rem;
                    box-shadow: 0 4px 15px rgba(227,25,55,0.35);
                '>🚗</div>
                <h3 style='
                    color: #1A1A1A;
                    margin: 0;
                    font-weight: 700;
                    font-size: 1.1rem;
                '>Tesla RAG</h3>
                <p style='
                    color: #999999;
                    font-size: 0.75rem;
                    margin: 0.2rem 0 0 0;
                    letter-spacing: 1px;
                '>FINANCIAL INTELLIGENCE</p>
            </div>
        """, unsafe_allow_html=True)

        st.divider()

        # --- System Status ---
        st.markdown("""
            <p style='
                color: #666666;
                font-size: 0.7rem;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                font-weight: 600;
                margin-bottom: 0.5rem;
            '>🔌 System Status</p>
        """, unsafe_allow_html=True)

        health = check_health()

        if health["status"] == "online":
            st.success("✅ Backend Online")
            data = health["data"]
            st.caption(f"Model: `{data.get('llm_model', 'N/A')}`")
            st.caption(f"Embeddings: `{data.get('embedding_model', 'N/A')}`")
        elif health["status"] == "offline":
            st.error("❌ Backend Offline")
            st.caption("Start the FastAPI server:")
            st.code("uvicorn app.api.main:app --reload", language="bash")
        else:
            st.warning("⚠️ Status Unknown")

        st.divider()

        # --- Knowledge Base Stats ---
        st.markdown("""
            <p style='
                color: #666666;
                font-size: 0.7rem;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                font-weight: 600;
                margin-bottom: 0.5rem;
            '>📊 Knowledge Base</p>
        """, unsafe_allow_html=True)

        stats = get_stats()

        if stats["success"]:
            data = stats["data"]
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Chunks", data.get("total_chunks", 0))
            with col2:
                st.metric("Docs", "1")

            # --- Chunk type breakdown ---
            total = data.get("total_chunks", 0)
            if total > 0:
                st.markdown(f"""
                    <div style='
                        background: #FFF0F2;
                        border-radius: 8px;
                        padding: 0.6rem;
                        margin-top: 0.5rem;
                        font-size: 0.75rem;
                        color: #666;
                    '>
                        📝 Text &nbsp;|&nbsp;
                        📊 Tables &nbsp;|&nbsp;
                        📈 Graphs
                        <br>
                        <span style='color: #2563EB; font-weight: 600;'>
                            Multimodal RAG Active ✓
                        </span>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("No documents ingested yet")

        st.divider()

        # --- Documents ---
        st.markdown("""
            <p style='
                color: #666666;
                font-size: 0.7rem;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                font-weight: 600;
                margin-bottom: 0.5rem;
            '>📄 Documents</p>
        """, unsafe_allow_html=True)

        docs = get_documents()

        if docs["success"] and docs["data"]["total_documents"] > 0:
            for doc in docs["data"]["documents"]:
                st.markdown(f"""
                    <div style='
                        background: #FFFFFF;
                        border-left: 3px solid #2563EB;
                        padding: 0.6rem 0.8rem;
                        border-radius: 0 8px 8px 0;
                        margin-bottom: 0.5rem;
                        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
                    '>
                        <p style='
                            color: #1A1A1A;
                            margin: 0;
                            font-size: 0.82rem;
                            font-weight: 600;
                        '>
                            📄 {doc['filename']}
                        </p>
                        <p style='
                            color: #999999;
                            margin: 0.2rem 0 0 0;
                            font-size: 0.72rem;
                        '>
                            🕐 {doc['ingested_at']}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("No documents ingested yet")

        st.divider()

        # --- Sample Questions ---
        st.markdown("""
            <p style='
                color: #666666;
                font-size: 0.7rem;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                font-weight: 600;
                margin-bottom: 0.5rem;
            '>💡 Try These Questions</p>
        """, unsafe_allow_html=True)

        for question in SAMPLE_QUESTIONS:
            if st.button(
                question[:42] + "..." if len(question) > 42 else question,
                key                 = f"sample_{question[:20]}",
                use_container_width = True,
            ):
                st.session_state.selected_question = question

        st.divider()

        # --- Settings ---
        st.markdown("""
            <p style='
                color: #666666;
                font-size: 0.7rem;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                font-weight: 600;
                margin-bottom: 0.5rem;
            '>⚙️ Settings</p>
        """, unsafe_allow_html=True)

        st.session_state.n_results = st.slider(
            "Results to retrieve",
            min_value = 3,
            max_value = 10,
            value     = 5,
            help      = "More results = better context but slower",
        )

        st.session_state.filter_type = st.selectbox(
            "Filter by source type",
            options      = [None, "text", "table", "graph"],
            format_func  = lambda x: "🔍 All Sources" if x is None
                           else f"{'📝' if x=='text' else '📊' if x=='table' else '📈'} {x.capitalize()}",
        )

        st.divider()

        # --- Footer ---
        st.markdown(f"""
            <div style='
                text-align: center;
                padding: 0.5rem 0;
            '>
                <p style='
                    color: #CCCCCC;
                    font-size: 0.7rem;
                    margin: 0;
                '>v{APP_VERSION} · Built with ❤️</p>
                <p style='
                    color: #2563EB;
                    font-size: 0.65rem;
                    margin: 0.2rem 0 0 0;
                    font-weight: 600;
                    letter-spacing: 1px;
                '>MULTIMODAL RAG</p>
            </div>
        """, unsafe_allow_html=True)