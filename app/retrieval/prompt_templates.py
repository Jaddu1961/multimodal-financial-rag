# ============================================
# PROMPT TEMPLATES
# All LLM prompts defined in one place
# ============================================


# --- Main RAG System Prompt ---
RAG_SYSTEM_PROMPT = """You are a professional financial analyst assistant \
specialized in analyzing Tesla's financial reports.

You will be given relevant context retrieved from Tesla's financial documents.
This context may include:
- 📝 Text excerpts from the report
- 📊 Table data with financial figures
- 📈 Chart/graph descriptions showing trends

Your job is to answer the user's question accurately based ONLY on the provided context.

Rules:
1. Answer ONLY using the provided context — never use outside knowledge
2. Always cite which type of source supports your answer (text, table, or chart)
3. Be precise with numbers, percentages, and dates
4. If the context doesn't contain enough information, say so clearly
5. Keep answers clear, concise, and professional
6. If multiple sources support the answer, mention all of them"""


# --- RAG User Prompt Template ---
RAG_USER_PROMPT = """Here is the relevant context retrieved from Tesla's financial documents:

{context}

---

Based on the context above, please answer this question:
{question}"""


# --- Context Formatter ---
def format_context(retrieved_chunks: list[dict]) -> str:
    """
    Format retrieved chunks into a readable context string.

    Args:
        retrieved_chunks: List of dicts from store_manager.search()

    Returns:
        Formatted context string for the LLM prompt
    """
    if not retrieved_chunks:
        return "No relevant context found."

    context_parts = []

    for i, chunk in enumerate(retrieved_chunks, 1):
        chunk_type = chunk["metadata"].get("chunk_type", "text")
        page_num   = chunk["metadata"].get("page_number", "?")
        source     = chunk["metadata"].get("source_file", "unknown")
        score      = chunk.get("score", 0)

        # --- Type emoji ---
        type_emoji = {
            "text":  "📝",
            "table": "📊",
            "graph": "📈",
        }.get(chunk_type, "📄")

        # --- Format each chunk ---
        context_parts.append(
            f"[Source {i}] {type_emoji} {chunk_type.upper()} "
            f"| Page {page_num} | {source} | Relevance: {score:.2f}\n"
            f"{chunk['text']}"
        )

    return "\n\n---\n\n".join(context_parts)


# --- Standalone Question Prompt ---
# Used to rephrase follow-up questions into standalone ones
CONDENSE_QUESTION_PROMPT = """Given the following conversation history and \
a follow-up question, rephrase the follow-up question to be a standalone \
question that contains all necessary context.

Conversation History:
{chat_history}

Follow-up Question: {question}

Standalone Question:"""


# --- No Context Response ---
NO_CONTEXT_RESPONSE = """I couldn't find relevant information in the \
Tesla financial documents to answer your question.

This could mean:
- The information is not in the ingested documents
- Try rephrasing your question
- Make sure the relevant Tesla report has been uploaded

Please try a different question or upload more documents."""