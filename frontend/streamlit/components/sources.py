# ============================================
# SOURCES COMPONENT
# Renders source citations for answers
# ============================================

import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from frontend.streamlit.config import SOURCE_ICONS, SOURCE_COLORS


def render_sources(sources: list):
    """
    Render source citations in expandable section.

    Args:
        sources: List of source dicts from API response
    """
    if not sources:
        return

    with st.expander(f"📚 View Sources ({len(sources)} chunks used)"):
        for i, source in enumerate(sources, 1):
            chunk_type  = source.get("chunk_type", "text")
            page_num    = source.get("page_number", "?")
            source_file = source.get("source_file", "unknown")
            relevance   = source.get("relevance", 0)
            preview     = source.get("preview", "")

            icon  = SOURCE_ICONS.get(chunk_type, "📄")
            color = SOURCE_COLORS.get(chunk_type, "#888888")

            # --- Relevance bar width ---
            bar_width = int(relevance * 100)

            st.markdown(f"""
                <div style='
                    background: #FFFFFF;
                    border: 1px solid #E9ECEF;
                    border-left: 4px solid {color};
                    border-radius: 8px;
                    padding: 0.8rem;
                    margin-bottom: 0.8rem;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
                '>
                    border-radius: 8px;
                    padding: 0.8rem;
                    margin-bottom: 0.8rem;
                '>
                    <div style='
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-bottom: 0.4rem;
                    '>
                        <span style='color: {color}; font-weight: bold;'>
                            {icon} Source {i} — {chunk_type.upper()}
                        </span>
                        <span style='color: #888; font-size: 0.75rem;'>
                            Page {page_num} | {source_file}
                        </span>
                    </div>

                    <div style='
                        background: #333;
                        border-radius: 4px;
                        height: 4px;
                        margin-bottom: 0.6rem;
                    '>
                        <div style='
                            background: {color};
                            width: {bar_width}%;
                            height: 100%;
                            border-radius: 4px;
                        '></div>
                    </div>

                    <p style='
                        color: #888;
                        font-size: 0.7rem;
                        margin-bottom: 0.4rem;
                    '>
                        Relevance: {relevance:.1%}
                    </p>

                    <p style='
                        color: #495057;
                        font-size: 0.8rem;
                        font-family: monospace;
                        background: #F8F9FA;
                        padding: 0.5rem;
                        border-radius: 4px;
                        margin: 0;
                        white-space: pre-wrap;
                    '>
                        {preview[:200]}...
                    </p>
                </div>
            """, unsafe_allow_html=True)