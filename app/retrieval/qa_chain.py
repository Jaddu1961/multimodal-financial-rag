# ============================================
# QA CHAIN
# Generates answers using retrieved context
# ============================================

from app.retrieval.retriever import retrieve
from app.retrieval.prompt_templates import (
    RAG_SYSTEM_PROMPT,
    RAG_USER_PROMPT,
    NO_CONTEXT_RESPONSE,
    format_context,
)
from app.llm.groq_client import generate_answer
from app.utils.logger import logger
from config.settings import settings


def answer_question(
    question:    str,
    n_results:   int  = None,
    filter_type: str  = None,
    filter_doc:  str  = None,
) -> dict:
    """Answer a question using RAG pipeline."""
    logger.info(f"💬 Processing: '{question[:60]}'")

    retrieval_result = retrieve(
        query       = question,
        n_results   = n_results,
        filter_type = filter_type,
        filter_doc  = filter_doc,
    )

    if not retrieval_result["chunks"]:
        return {
            "answer":            NO_CONTEXT_RESPONSE,
            "sources":           [],
            "types_used":        {},
            "total_chunks_used": 0,
            "question":          question,
        }

    user_prompt = RAG_USER_PROMPT.format(
        context  = retrieval_result["formatted_context"],
        question = question,
    )

    answer = generate_answer(
        system_prompt = RAG_SYSTEM_PROMPT,
        user_prompt   = user_prompt,
    )

    sources = []
    for chunk in retrieval_result["chunks"]:
        sources.append({
            "chunk_type":  chunk["metadata"].get("chunk_type"),
            "page_number": chunk["metadata"].get("page_number"),
            "source_file": chunk["metadata"].get("source_file"),
            "document_id": chunk["metadata"].get("document_id", ""),
            "relevance":   round(chunk.get("score", 0), 3),
            "preview":     chunk["text"][:150] + "..."
                           if len(chunk["text"]) > 150
                           else chunk["text"],
        })

    logger.info("✅ Answer generated successfully")

    return {
        "answer":            answer,
        "sources":           sources,
        "types_used":        retrieval_result["types_found"],
        "total_chunks_used": retrieval_result["total_found"],
        "question":          question,
    }


def compare_documents(
    question:   str,
    document_1: str,
    document_2: str,
    n_results:  int = 5,
) -> dict:
    """
    Compare two documents for the same question.

    Args:
        question:   What to compare
        document_1: First document filename
        document_2: Second document filename
        n_results:  Chunks per document

    Returns:
        Dict with answers from both docs + combined analysis
    """
    logger.info(f"🔄 Comparing: {document_1} vs {document_2}")

    # --- Get answer from Document 1 ---
    result_1 = _retrieve_by_filename(
        query     = question,
        filename  = document_1,
        n_results = n_results,
    )

    # --- Get answer from Document 2 ---
    result_2 = _retrieve_by_filename(
        query     = question,
        filename  = document_2,
        n_results = n_results,
    )

    # --- Generate answer for Document 1 ---
    if result_1["chunks"]:
        prompt_1 = f"""Answer this question using ONLY the context from {document_1}:

Context:
{result_1["formatted_context"]}

Question: {question}

Format your answer with:
- Bold key numbers
- Bullet points
- Be concise (max 150 words)"""

        answer_1 = generate_answer(
            system_prompt = RAG_SYSTEM_PROMPT,
            user_prompt   = prompt_1,
        )
    else:
        answer_1 = f"No relevant data found in {document_1}"

    # --- Generate answer for Document 2 ---
    if result_2["chunks"]:
        prompt_2 = f"""Answer this question using ONLY the context from {document_2}:

Context:
{result_2["formatted_context"]}

Question: {question}

Format your answer with:
- Bold key numbers
- Bullet points
- Be concise (max 150 words)"""

        answer_2 = generate_answer(
            system_prompt = RAG_SYSTEM_PROMPT,
            user_prompt   = prompt_2,
        )
    else:
        answer_2 = f"No relevant data found in {document_2}"

    # --- Generate combined analysis ---
    combined_prompt = f"""You are comparing two Tesla financial reports.

{document_1} findings:
{answer_1}

{document_2} findings:
{answer_2}

Question: {question}

Provide a brief comparative analysis:
- What changed between the two periods?
- Which period performed better and why?
- Key takeaways

Keep it under 150 words. Use bold for numbers."""

    combined_analysis = generate_answer(
        system_prompt = "You are a financial analyst comparing Tesla quarterly reports.",
        user_prompt   = combined_prompt,
    )

    logger.info("✅ Comparison complete")

    return {
        "answer_1":          answer_1,
        "answer_2":          answer_2,
        "combined_analysis": combined_analysis,
    }


def _retrieve_by_filename(
    query:     str,
    filename:  str,
    n_results: int = 5,
) -> dict:
    """
    Retrieve chunks filtered by source filename.
    Uses direct ChromaDB query with metadata filter.
    """
    from app.embeddings.embedder import embed_single
    from app.vectorstore.chroma_store import get_collection

    try:
        logger.info(f"🔍 Searching in: {filename}")

        # --- Embed query ---
        query_embedding = embed_single(query)

        # --- Query ChromaDB with filename filter ---
        collection = get_collection()
        results    = collection.query(
            query_embeddings = [query_embedding],
            n_results        = n_results,
            where            = {"source_file": {"$eq": filename}},
            include          = ["documents", "metadatas", "distances"],
        )

        # --- Format results ---
        chunks = []
        if results and results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                chunks.append({
                    "text":     doc,
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i],
                    "score":    1 - results["distances"][0][i],
                })

        if not chunks:
            logger.warning(f"⚠️  No chunks found for: {filename}")
            return {
                "chunks":            [],
                "formatted_context": "",
                "total_found":       0,
                "types_found":       {},
            }

        logger.info(f"✅ Found {len(chunks)} chunks in {filename}")

        formatted_context = format_context(chunks)

        return {
            "chunks":            chunks,
            "formatted_context": formatted_context,
            "total_found":       len(chunks),
            "types_found":       {},
        }

    except Exception as e:
        logger.error(f"❌ Filename filter failed for {filename}: {e}")
        return {
            "chunks":            [],
            "formatted_context": "",
            "total_found":       0,
            "types_found":       {},
        }