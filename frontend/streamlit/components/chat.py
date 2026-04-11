# ============================================
# CHAT COMPONENT
# ============================================

import streamlit as st
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from frontend.streamlit.api_client import ask_question
from frontend.streamlit.components.sources import render_sources
from frontend.streamlit.config import COLORS


def render_chat():
    """Render the main chat interface"""

    # --- Chat Header ---
    st.markdown("""
        <div style='padding: 1rem 0;'>
            <h2 style='color: white; margin: 0;'>
                💬 Financial Q&A
            </h2>
            <p style='color: #888; margin: 0; font-size: 0.9rem;'>
                Ask anything about Tesla's financial reports
            </p>
        </div>
    """, unsafe_allow_html=True)

    # --- Initialize chat history ---
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        st.session_state.messages.append({
            "role":    "assistant",
            "content": "👋 Hello! I'm your Tesla Financial Intelligence assistant. Ask me anything about Tesla's Q3 2023 financial report — revenue, margins, deliveries, and more!",
            "sources": [],
            "metadata": {},
        })

    # --- Display chat messages ---
    chat_container = st.container()

    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                _render_user_message(message["content"])
            else:
                _render_assistant_message(
                    content  = message["content"],
                    sources  = message.get("sources", []),
                    metadata = message.get("metadata", {}),
                )

    # --- Handle sample question selection ---
    if "selected_question" in st.session_state:
        question = st.session_state.selected_question
        del st.session_state.selected_question
        _process_question(question)
        st.rerun()

    # --- Chat Input ---
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([5, 1])

    with col1:
        question = st.chat_input(
            placeholder="Ask about Tesla's financials...",
        )

    if question:
        _process_question(question)
        st.rerun()

    # --- Clear Chat Button ---
    if len(st.session_state.messages) > 1:
        if st.button("🗑️ Clear Chat", use_container_width=False):
            st.session_state.messages = []
            st.rerun()


def _render_user_message(content: str):
    """Render a user message bubble"""
    with st.chat_message("user"):
        st.markdown(f"""
            <div style='
                background: #E31937;
                color: white;
                padding: 0.8rem 1rem;
                border-radius: 12px 12px 2px 12px;
                display: inline-block;
                max-width: 80%;
            '>
                {content}
            </div>
        """, unsafe_allow_html=True)


def _render_assistant_message(
    content:  str,
    sources:  list,
    metadata: dict,
):
    """Render an assistant message with sources"""
    with st.chat_message("assistant"):

        # --- Answer ---
        st.markdown(content.replace("📝", " 📝").replace("📊", " 📊").replace("📈", " 📈"))

        # --- Metadata bar ---
        if metadata:
            chunks = metadata.get("total_chunks_used", 0)
            time_  = metadata.get("processing_time_seconds", 0)
            types  = metadata.get("types_used", {})

            type_str = " | ".join([
                f"{'📝' if k=='text' else '📊' if k=='table' else '📈'} {k}: {v}"
                for k, v in types.items()
            ])

            st.markdown(f"""
                <div style='
                    background: #1E1E1E;
                    border-radius: 8px;
                    padding: 0.4rem 0.8rem;
                    margin-top: 0.5rem;
                    font-size: 0.75rem;
                    color: #888;
                '>
                    ⚡ {time_}s | 🔍 {chunks} chunks | {type_str}
                </div>
            """, unsafe_allow_html=True)

        # --- Sources ---
        if sources:
            render_sources(sources)


def _process_question(question: str):
    """Process a question and get answer from backend"""

    # Add user message
    st.session_state.messages.append({
        "role":    "user",
        "content": question,
        "sources": [],
        "metadata": {},
    })

    # Get settings
    n_results   = st.session_state.get("n_results", 5)
    filter_type = st.session_state.get("filter_type", None)

    # Call API
    with st.spinner("🤔 Thinking..."):
        result = ask_question(
            question    = question,
            n_results   = n_results,
            filter_type = filter_type,
        )

    if result["success"]:
        data = result["data"]
        st.session_state.messages.append({
            "role":    "assistant",
            "content": data["answer"],
            "sources": data.get("sources", []),
            "metadata": {
                "total_chunks_used":      data.get("total_chunks_used", 0),
                "processing_time_seconds": data.get("processing_time_seconds", 0),
                "types_used":             data.get("types_used", {}),
            },
        })
    else:
        st.session_state.messages.append({
            "role":    "assistant",
            "content": f"❌ Error: {result['error']}",
            "sources": [],
            "metadata": {},
        })