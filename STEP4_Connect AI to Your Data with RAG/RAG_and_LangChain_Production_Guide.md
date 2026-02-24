# Production-Grade RAG & LangChain: Engineer’s Guide

**For:** Eran, Junior AI Engineer (and anyone building a first RAG app from zero)  
**From:** Todd, Senior AI Engineer & Team Lead  
**Purpose:** Turn you into a confident builder of RAG applications with LangChain  
**Assumptions:** No prior RAG, vector, or embedding knowledge  

---

## What You’ll Build (The Big Picture)

By the end of this guide you will have built an application that:

1. **Takes your own documents** (PDFs, text files, etc.).
2. **Chunks and embeds them** into a vector store (e.g. Chroma).
3. **Answers user questions** by retrieving relevant chunks and asking an LLM to answer using only that context.
4. **Shows where each answer came from** (source citations) so users and you can verify and debug.

You’ll understand *why* each step exists and *when* to choose one option over another—so you can ship and maintain a real RAG system, not just copy-paste a tutorial.

---

## Table of Contents

| Section | Purpose |
|--------|--------|
| [How to Use This Guide](#how-to-use-this-guide) | How to read and use the doc. |
| [Prerequisites](#prerequisites-before-you-start) | What you need before starting. |
| [Learning Path](#learning-path-where-you-are) | Map of phases and pipeline diagram. |
| [Build Order](#build-order-what-to-do-when) | Step-by-step what to build and when. |
| [Quick Start](#quick-start-your-first-rag-in-one-script) | One script to run RAG end-to-end. |
| [Scope](#scope-what-this-guide-covers-and-what-it-doesnt) | What’s in and out of scope. |
| [Troubleshooting](#troubleshooting-common-beginner-issues) | Fix common errors and confusion. |
| [Glossary](#glossary-quick-reference) | Term definitions. |
| **Part 1** | [Core Concepts — Vectors & Embeddings](#part-1-core-concepts--vectors--embeddings) |
| **Part 2** | [RAG Architecture](#part-2-rag-architecture--the-two-model-pipeline) |
| **Part 3** | [LangChain Ecosystem](#part-3-the-framework--langchain-ecosystem) |
| **Part 4** | [Chunking & Ingestion](#part-4-data-preparation--chunking--ingestion) |
| **Part 5** | [Encoders & Vector Stores](#part-5-infrastructure--encoders--vector-stores) |
| **Part 6** | [Visualization & Debugging](#part-6-visualization--debugging) |
| **Part 7** | [Production Operations](#part-7-production-operations--safety) |
| **Part 8** | [Engineering Decision Matrix](#part-8-engineering-decision-matrix) |
| **Lessons 9–13** | [Implementation Track](#implementation-track-lessons-913-query-pipeline-to-production) (query, temperature, stitching, modularization, failure modes) |
| **Reference** | [ingest.py & answer.py](#reference-implementation-ingestpy--answerpy) — full code structure and breakdown |
| **Part 9–11** | [Testing](#part-9-testing--quality), [Structure](#part-10-project-structure--boundaries), [Anti-Patterns](#part-11-anti-patterns-what-not-to-do) |
| [Summary](#summary-for-eran) | What you’ve learned and next steps. |

---

## How to Use This Guide

- **Read in order.** Parts 1–8 build the mental model and decisions; the Implementation Track (Lessons 9–13) turns that into a working pipeline. Skipping ahead will leave gaps.
- **Do the checkpoints.** Answer the **Check Your Understanding** questions before moving on. They’re there so you catch misunderstandings early.
- **Use the roadmaps.** The **Learning path** and **Build order** tell you what to do when. The **Milestone** tables show what you’ll have after each phase.
- **Run code early.** The **Quick start** gets you to a minimal “ask a question, get an answer” in one script. Then you can revisit the theory with something concrete in mind.
- **Engineering decisions** are called out so you know *why* we choose one option over another. Code examples are production-oriented, not throwaway scripts.

---

## Prerequisites (Before You Start)

| Requirement | What you need | Why |
|-------------|----------------|-----|
| **Python** | 3.10+ recommended | LangChain and common vector stores target modern Python. |
| **Environment** | Virtual env (e.g. `python -m venv .venv`) | Keeps dependencies isolated from other projects. |
| **API keys** | OpenAI API key (or another provider for embeddings + LLM) | Embedding and generation calls go to an API. Get keys from [OpenAI](https://platform.openai.com/api-keys) (or your provider); never commit them—use env vars (e.g. `OPENAI_API_KEY`). |
| **A few documents** | 1–3 PDFs or text files to “ask questions about” | You need something to chunk and embed. Start small (e.g. a single FAQ or short manual). |

**Optional but helpful:** Basic Python (functions, lists, dicts) and a vague idea of what an “API” is. No ML or math required—we explain vectors and similarity as we go.

---

## Learning Path (Where You Are)

Use this to see how the pieces fit and what you’ll have at each stage.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE          │  PARTS / LESSONS   │  YOU WILL HAVE…                      │
├─────────────────┼────────────────────┼──────────────────────────────────────┤
│  Theory         │  Part 1–2           │  Clear idea: RAG = retrieve by        │
│                 │                    │  meaning, then generate. Two models.   │
├─────────────────┼────────────────────┼──────────────────────────────────────┤
│  Framework &    │  Part 3–4           │  LangChain in mind; know how to       │
│  Data           │                    │  chunk and attach metadata.            │
├─────────────────┼────────────────────┼──────────────────────────────────────┤
│  Infrastructure │  Part 5–6           │  Encoder vs store choices; when to    │
│  & Debugging    │                    │  re-index; how to sanity-check data.  │
├─────────────────┼────────────────────┼──────────────────────────────────────┤
│  Operations &   │  Part 7–8           │  Dev vs prod ingestion; config;      │
│  Decisions      │                    │  decision matrix for “which store?”   │
├─────────────────┼────────────────────┼──────────────────────────────────────┤
│  Query &        │  Lessons 9–11       │  Retriever + LLM + prompt; working   │
│  Pipeline       │                    │  “ask a question → get an answer” flow.│
├─────────────────┼────────────────────┼──────────────────────────────────────┤
│  Production &   │  Lessons 12–13     │  Modular ingest/answer; history;       │
│  Failure Modes  │                    │  failure modes and evaluation.       │
└─────────────────┴────────────────────┴──────────────────────────────────────┘
```

**RAG pipeline at a glance (same flow you’ll implement):**

```
  User question
        │
        ▼
  ┌─────────────┐     query vector      ┌──────────────┐
  │  Embedding  │ ──────────────────►  │  Vector      │
  │  model      │                      │  store       │
  └─────────────┘                      │  (e.g. Chroma)│
        ▲                               └──────┬───────┘
        │                                      │
  "What are ticket                             │ returns
   prices to Heathrow?"                        │ text chunks
        │                                      ▼
        │                               ┌─────────────┐
        │                               │  Prompt:    │
        └───────────────────────────────│  context +  │
                                       │  question   │
                                       └──────┬──────┘
                                              │
                                              ▼
                                       ┌─────────────┐
                                       │  LLM        │
                                       │  (e.g. GPT) │
                                       └──────┬──────┘
                                              │
                                              ▼
                                       Answer + sources
```

---

## Build Order (What to Do When)

Follow this sequence so each step has a clear goal and you don’t block yourself.

| Step | What to do | By the end you’ll have… |
|------|------------|--------------------------|
| **1. Setup** | Create a project folder, venv, install `langchain-openai`, `langchain-chroma`, `langchain-text-splitters`. Set `OPENAI_API_KEY`. | Environment ready to run RAG code. |
| **2. Quick start** | Run the minimal script below (or your own one-file version): load 1 doc → chunk → embed → store → ask one question. | A single question answered from your doc; end-to-end loop working. |
| **3. Ingest properly** | Use Parts 4–5: recursive chunking, metadata, same embedding model you’ll use at query time. Persist to Chroma (or your chosen store). | A populated vector store you can query. |
| **4. Query from code** | Use Lesson 9–10: retriever with `similarity_score_threshold`, same embedding model, LLM with low temperature. Log retrieved docs. | A function that takes a question and returns answer + sources. |
| **5. Add a simple UI** | Wrap your query function in Gradio (or a minimal web endpoint) and **show source documents** next to the answer. | Something you can demo and debug visually. |
| **6. Harden** | Use Part 7 and Lessons 12–13: config/env, error handling, ingest vs answer separation, evaluation and failure-mode checklist. | A structure you can deploy and improve over time. |

---

## Quick Start (Your First RAG in One Script)

**Goal:** Run one script that loads a small piece of text, chunks it, embeds it, stores it in Chroma, and answers one question. No prior RAG knowledge required—this is to “see the loop” before diving into theory.

**When to do it:** Right after **Prerequisites**. You can do it before Part 1, or after Part 2. If you prefer theory first, skip to Part 1 and come back here when you want to run something.

**Setup (one-time):**

```bash
mkdir my-first-rag && cd my-first-rag
python -m venv .venv
# Windows: .venv\Scripts\activate   # macOS/Linux: source .venv/bin/activate
pip install langchain-openai langchain-chroma langchain-text-splitters python-dotenv
```

Create a `.env` file (and add `.env` to `.gitignore`):

```
OPENAI_API_KEY=sk-your-key-here
```

**Minimal script (`quick_rag.py`):**

```python
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma

# 1. Tiny "corpus" — in a real app you'd load PDFs or files
text = """
Our company refund policy: Refunds are allowed within 30 days of purchase.
Contact support@company.com with your order ID. No refunds after 30 days.
"""
docs = [Document(page_content=text.strip(), metadata={"source": "policy.txt"})]

# 2. Chunk (we use the same splitter we'll use in production)
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
chunks = splitter.split_documents(docs)

# 3. Embed and store — use one embedding model and stick to it
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
persist_dir = "./chroma_quickstart"
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=persist_dir,
)

# 4. Retriever + LLM (same embedding model as above; low temperature for RAG)
retriever = vectorstore.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 2, "score_threshold": 0.5})
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 5. Ask a question
question = "How do I get a refund?"
retrieved = retriever.invoke(question)
context = "\n\n".join([d.page_content for d in retrieved])
prompt = f"Answer only using this context. If the answer is not here, say so.\n\nContext:\n{context}\n\nQuestion: {question}"
answer = llm.invoke(prompt)

print("Question:", question)
print("Answer:", answer.content)
print("Sources:", [d.page_content[:80] + "..." for d in retrieved])
```

**Run:** `python quick_rag.py`

**What to notice:** The retriever returns *chunks* (text), and that text is passed into the LLM’s prompt. The LLM never sees vectors—only the retrieved text. If you change the question to something unrelated, you may get “I don’t have that in the context”—that’s correct behavior. Once this runs, continue with Part 1 for the concepts and then build out ingestion and UI following the Build order.

---

## Scope: What This Guide Covers (and What It Doesn’t)

| In scope | Not in scope (mentioned for context only) |
|----------|-------------------------------------------|
| End-to-end RAG: ingest → store → query → answer with citations | **Agents** (tool use, multi-step planning) — different architecture |
| LangChain 1.0 patterns: Retriever, ChatModel, chunking, Chroma | **Streaming** token-by-token — we focus on request/response |
| Embedding consistency, temperature, similarity threshold | **Multi-tenancy** or per-user isolation — same concepts, more infra |
| Production concerns: config, errors, logging, modularization | **Advanced RAG** (HyDE, re-ranking, query rewriting) — we introduce ideas; deep dives are elsewhere |
| Failure modes and evaluation (RAGAS, test sets) | **Brute-force RAG without LangChain** — referenced; not the main path here |

Staying in scope keeps the guide focused so you can go from zero to a working, maintainable RAG app. You can add streaming, agents, or advanced retrieval later.

---

## Troubleshooting: Common Beginner Issues

When something goes wrong, check this table first. Most “mysterious” RAG bugs come from a few repeated causes.

| What you see | Likely cause | What to do |
|--------------|--------------|------------|
| **`ValueError: dimension mismatch`** or similar from the vector store | You used a **different embedding model** at query time than at ingestion (e.g. OpenAI at ingest, HuggingFace at query). | Use the **exact same** embedding model and dimensions for both. Re-index if you already ingested with another model. |
| **Retriever returns no documents** (empty list) | `score_threshold` is too high, or the store is empty, or the question is unrelated to the corpus. | Lower the threshold (e.g. 0.5) for testing; confirm the store has documents (e.g. check Chroma collection count); try a question that clearly matches your docs. |
| **LLM gives a generic or wrong answer** (ignores your docs) | The **retrieved context was never passed** into the LLM prompt, or it’s in the wrong place. | Ensure you build the prompt with `context = "\n\n".join([d.page_content for d in docs])` and put `context` into the system/user message. Log the prompt to verify. |
| **LLM “hallucinates” details not in the docs** | Temperature too high, or no instruction to “answer only from context.” | Set **temperature to 0** (or &lt; 0.5) and add an explicit instruction:  “Answer only using the context below. If the answer is not in the context, say so.” |
| **Good answer but no way to check the source** | Sources not shown in the UI or logs. | Always **return and display** the list of `Document` objects (or their `page_content` / `metadata`) alongside the answer. Non-negotiable for trust and debugging. |
| **Different answer every time for the same question** | Expected at temperature &gt; 0. For temp 0, small differences can still happen (model/GPU non-determinism). | Use **temperature 0** for RAG when you want consistency. Don’t rely on exact string match in tests—use semantic or eval metrics. |
| **“No module named 'langchain_...'”** | Wrong or missing LangChain packages. | Use **LangChain 1.0** modular packages: `langchain-openai`, `langchain-chroma`, `langchain-text-splitters`, etc. Install what you need; avoid old monolithic `langchain` if starting fresh. |
| **API key errors** | Key not set or not visible to the process. | Set `OPENAI_API_KEY` (or your provider’s env var) in the same shell/process that runs the script, or in a `.env` file loaded with `python-dotenv`. Never hardcode keys. |

---

## Glossary (Quick Reference)

| Term | Meaning |
|------|--------|
| **RAG** | Retrieval-Augmented Generation: retrieve relevant text by vector similarity, then generate an answer with an LLM. |
| **Encoder / Embedding model** | Model that maps text → fixed-size vector. Used only for retrieval. |
| **Generator / LLM** | Model that maps text → text. Used for the final answer. |
| **Vector** | List of floats (e.g. 1536) representing semantic meaning of text. |
| **Chunk** | A piece of document text (and metadata) stored and retrieved as one unit. |
| **Vector store** | Database that stores vectors and runs similarity search (k-NN). |
| **Retriever** | Component that, given a query, returns a list of relevant chunks (LangChain: `invoke(query)` → list of `Document`). |
| **Cosine similarity** | Metric in [−1, 1]; 1 = same direction, 0 = unrelated. Used to rank retrieval results. |
| **Upsert** | Insert or update by ID; basis for incremental indexing. |
| **Re-index** | Re-embed all documents (required when changing embedding model). |
| **invoke** | LangChain pattern: call a component with `.invoke(input)`. Retriever, LLM, Tools use it for composability. |
| **Runnable** | LangChain interface for components that support `.invoke()` (and optionally `.stream()`, `.batch()`). |
| **Temperature** | LLM sampling parameter: 0 ≈ argmax (deterministic); higher = more variance. Use 0–0.5 for RAG. |
| **combine_question** | Heuristic: concatenate recent user messages into one string for retrieval. Fixes “she”/“it” reference; can cause topic drift. |
| **Parent-document retrieval** | Retrieve small chunks, then pass the parent document (or larger window) to the LLM for full context. |
| **Query rewriting** | Use an LLM to turn the latest user message into a stand-alone question using conversation history (e.g. “What did she do?” → “What did Avery Lancaster do?”). |

---

## Part 1: Core Concepts — Vectors & Embeddings

This part answers “what is RAG made of?” You don’t need to write code yet—focus on the ideas. They will make every later step (chunking, retrieval, prompting) easier to reason about.

### 1.1 Why “Search by Meaning” Exists

Classic search is **keyword-based**: you match exact or stemmed words. That breaks when users ask in different words than the document uses.  

**RAG (Retrieval-Augmented Generation)** adds a step: we turn both the user’s question and our documents into **vectors** (lists of numbers that encode *meaning*), then find the document chunks whose vectors are “closest” to the question. So we search by **semantic similarity**, not just keywords.

**Takeaway:** RAG = “find the right text pieces by meaning, then let an LLM answer using those pieces.”

---

### 1.2 Two Completely Different Kinds of Models

In production we treat two model types differently:

| Aspect | **Generator (LLM)** | **Encoder (Embedding model)** |
|--------|----------------------|--------------------------------|
| **Job** | Predict the next token → generate text | Turn full input into one fixed-size vector |
| **Input** | Text (tokens) | Text |
| **Output** | Text (tokens) | **Vector** (list of numbers, e.g. 1536 floats) |
| **Examples** | GPT-4, Claude, Gemini, Llama | text-embedding-3-large, all-MiniLM-L6-v2, BERT |
| **In RAG** | Produces the final answer | Produces vectors for search only |

**Critical:** The generator **never** sees vectors. It only sees text. Vectors are used only to *select* which text to pass into the generator.

---

### 1.3 Tokens vs Vectors (Don’t Confuse Them)

- **Tokens:** IDs for subword pieces (from a tokenizer). Input-side: “hello” → `[104, 101, 108, 108, 111]` (conceptually). Simple lookup.
- **Vectors:** Dense representations of *meaning*. Output of a neural network. Same sentence in two languages can be close in vector space; different meanings are far apart.

**Flow:**  
`Raw text → Tokenizer → Tokens → Embedding model → Vector`

So: tokens are *discrete IDs*; vectors are *continuous “meaning” coordinates*.

---

### 1.4 Vector Space and “Closeness”

A vector of dimension 1536 is a point in **1536-dimensional space**.  
Documents with similar meaning end up **close** in this space; unrelated ones are **far**.

We measure “closeness” with **cosine similarity**:

- **1.0** = same direction (very similar meaning)
- **0.0** = unrelated
- **-1.0** = opposite meaning

In practice, for RAG retrieval we often treat **0.75–0.85** as “strong match.” **1.0** everywhere usually means duplicates or overfitting; **0.0** threshold means no filtering and noisy results. Tuning this threshold is a core part of production RAG.

---

#### Check Your Understanding (Part 1)

1. In one sentence, what is RAG and why do we use it instead of only keyword search?
2. What is the **output** of an embedding model: text or a list of numbers? What uses that output in the RAG pipeline?
3. Why does the generator LLM never receive vectors?
4. If cosine similarity between a query and a chunk is 0.95, is that chunk a good candidate to pass to the LLM? What if it’s 0.4?

**Milestone:** You can explain what a vector is, why we use two kinds of models (encoder vs generator), and how “closeness” in vector space drives retrieval.

---

## Part 2: RAG Architecture — The Two-Model Pipeline

### 2.1 End-to-End Flow

1. **User query:** e.g. “What are ticket prices to Heathrow?”
2. **Encode:** Send the query to the **encoder** → get **query vector**.
3. **Vector search:** Search the **vector store** for the k nearest vectors to the query vector (e.g. top 5).
4. **Retrieve:** The store returns the **text chunks** (and optional metadata) attached to those vectors — *not* the vectors themselves for generation.
5. **Prompt assembly:** Build: `[System prompt] + [Retrieved chunks] + [User question]`.
6. **Generation:** Send that text to the **generator** LLM → final answer.

So: **Encoder** and **vector store** are for *retrieval*; **generator** is for *answer*. Clear separation.

**Beginner tip:** The LLM never sees vectors. It only ever sees *text* (the retrieved chunks plus the question). If you forget to pass the retrieved chunks into the prompt, the LLM will answer from its training data—and your RAG will look “broken.” Always wire context into the prompt.

---

### 2.2 Critical Boundaries

- **Vectors never go to the generator.** Only text (retrieved chunks + prompts) goes to the LLM. I’ve seen people try to feed vectors into the generator — that’s wrong. Vectors are for finding text; once text is found, vectors are not used in that step.
- **Encoder and generator are independent.** You can change the embedding model or the LLM separately (with care: same “language” of documents and queries, and re-index if you change the encoder).

---

### 2.3 RAG Is Heuristic, Not Closed-Form

RAG is not a solved math problem. It’s **empirical**: chunk size, overlap, model choice, threshold, and prompt design all interact. In production, expect to spend a lot of time on evals and tuning, not just wiring. Use evaluation frameworks (e.g. RAGAS, TruLens) and A/B tests before calling it “done.”

---

#### Check Your Understanding (Part 2)

1. List the six steps of the RAG pipeline in order. Where do vectors “stop” being used?
2. What exactly is passed into the generator LLM: raw vectors or text?
3. Why is it important to treat RAG as heuristic and invest in evaluation?

**Milestone:** You can draw or recite the full RAG flow (query → encode → search → retrieve text → prompt → generate) and explain why vectors never go to the LLM.

---

## Part 3: The Framework — LangChain Ecosystem

### 3.1 What LangChain Is

LangChain is an **abstraction layer** between your application and AI providers (OpenAI, Anthropic, etc.) and infrastructure (vector stores, loaders). It gives you:

- Standard interfaces for documents, retrievers, and chains
- Integrations for 50+ vector stores and many LLM providers
- Composability (e.g. “this retriever” + “this LLM” + “this prompt”)

**Versioning:** Pre-1.0 had breaking changes often. **Post-1.0 (langchain >= 1.0.0)** is the stable, modular line (e.g. `langchain_openai`, `langchain_chroma`). In production, pin `langchain>=1.0.0` and use the modular packages.

---

### 3.2 Why We Use LangChain (And When Not To)

**We use it when we need:**

- **Observability:** LangSmith traces (latency per step, token counts, retrieved doc IDs, similarity scores). Essential for debugging RAG.
- **Ecosystem:** Retries, fallbacks, many vector-store and loader integrations.
- **Consistency:** Same patterns across projects so the team can maintain and extend.

**We might not use it when:** We only need a thin proxy to one LLM API with no retrieval or tracing. Then raw API or a lightweight client can be enough.

**Trade-offs:** LangChain is powerful but heavy and has a learning curve. The abstraction can hide details. For production RAG and agents, the observability and integrations usually justify it.

---

### 3.3 Code Patterns (LangChain, Python)

**Chunking (ingestion):**

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,          # in chars; ~tokens depends on tokenizer
    chunk_overlap=50,        # 10–20% of chunk_size
    length_function=len,     # or a token counter for token-based sizing
    separators=["\n\n", "\n", ". ", " ", ""],
)
chunks = splitter.split_documents(docs)  # docs = list of Document with metadata
```

**Retriever with similarity threshold (query path):**

```python
# After you have a vector store (e.g. Chroma) with your embeddings:
retriever = store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 5, "score_threshold": 0.75},
)
# Returns only chunks with cosine similarity >= 0.75, up to 5
docs = retriever.invoke("What are ticket prices to Heathrow?")
```

**Why this matters:** If you use plain `search_type="similarity"` with no threshold, you get the top-k even when all scores are bad. With `similarity_score_threshold`, you can get zero results when nothing is good — then your code can fall back to keyword or “I don’t know.”

**RAG chain (high level):** Use `create_retrieval_chain` (or equivalent) to wire: retriever → prompt (with `context` + `question`) → LLM. The chain’s input is the user question; output includes `context` (retrieved docs) and `answer`. Log `context` and scores in production for debugging.

---

#### Check Your Understanding (Part 3)

1. In one sentence, what is LangChain’s role between your code and AI?
2. Why is LangSmith “non-negotiable” for debugging RAG in production?
3. When might you *not* choose LangChain for a project?

**Milestone:** You know what LangChain gives you (abstractions, observability) and you’ve seen the chunking and retriever code patterns you’ll use later.

---

## Part 4: Data Preparation — Chunking & Ingestion

### 4.1 Why We Chunk

- **Granularity:** We want to retrieve the *paragraph* about password reset, not the whole 200-page manual.
- **Context limits:** LLMs have token limits. We can’t stuff every document into one prompt.
- **Signal vs noise:** Too much context causes “lost in the middle” and dilutes the important bits. Smaller, focused chunks improve retrieval and answer quality.

---

### 4.2 How to Chunk: Recursive Character Splitting

**Production standard:** `RecursiveCharacterTextSplitter` (or equivalent in your stack).

It respects structure by splitting in this order:

1. `\n\n` (paragraphs)  
2. `\n` (lines)  
3. `. ` (sentences)  
4. Space  
5. Character  

So we avoid cutting in the middle of a sentence when we can.

**Overlap** is important: typically **10–20%** of chunk size (e.g. 50 tokens overlap for 500-token chunks). Overlap keeps context across boundaries and reduces “chopped concept” issues.

**Engineering choice:** Fixed token count alone is brittle. Recursive splitting + overlap is the default; then tune chunk size and overlap on your content and retrieval metrics. **Alternative:** Some implementations use an **LLM** to produce chunks (e.g. headline + summary + original text per chunk) for better semantic boundaries—see the [Reference Implementation: ingest.py](#reference-implementation-ingestpy--answerpy) for that pattern.

---

### 4.3 Metadata

**Metadata** = extra fields per chunk (e.g. `source`, `doc_type`, `last_modified`).

Use it for:

- **Filtering:** e.g. “only search in `doc_type='contracts'`” before or during vector search (hybrid search).
- **Attribution:** Showing “Source: X” in the UI.
- **Incremental indexing:** Using `last_modified` to decide what to re-embed.

Design metadata early; adding it later often means re-chunking and re-embedding.

---

### 4.4 Document & Retriever Contracts (For Implementers)

**Document (LangChain):** Each chunk is a `Document` with:

- `page_content`: str (the chunk text)
- `metadata`: dict (e.g. `source`, `doc_type`, `last_modified`)

**Retriever contract:** Given a query string, a retriever returns a list of `Document` (or equivalent). The vector store returns *text + metadata*; the generator only ever sees `page_content` (and whatever you put in the prompt from metadata). Your code should rely on this contract so you can swap store or encoder without changing the rest of the pipeline.

**Idempotency:** Use a stable `document_id` (e.g. hash of source path + chunk index, or DB primary key) for every chunk. Upsert by that ID so re-running ingestion doesn’t create duplicates and incremental updates are safe.

---

#### Check Your Understanding (Part 4)

1. Give two reasons we chunk documents instead of feeding whole docs to the LLM.
2. What is the split order used by RecursiveCharacterTextSplitter, and why does that order matter?
3. Why do we use overlap between chunks? What’s a typical overlap in % of chunk size?
4. Name two uses of metadata in a RAG system.

**Milestone:** You can implement ingestion: load docs → recursive split with overlap → attach metadata → produce a list of `Document` objects ready for embedding.

---

## Part 5: Infrastructure — Encoders & Vector Stores

### 5.1 Encoder (Embedding) Model — The Quality Lever

The encoder turns text into vectors. This choice **drives accuracy** more than the vector store in many cases.

**Options (examples):**

- **OpenAI** (e.g. text-embedding-3-large): High quality, paid API, 1536 dimensions.
- **HuggingFace** (e.g. all-MiniLM-L6-v2): Open source, local, cheaper, often 384 dimensions.

**Dimensions are model-specific.** You cannot mix dimensions in one index: every vector in a store must come from the same embedding model (same dimensions and same “space”).

**Decision:** Benchmark a few encoders on *your* data (accuracy, latency, cost). Often a smaller/cheaper model gets 90%+ of the benefit at half the cost. Start there unless you have proven need for the largest model.

**Beginner trap:** Using one embedding model at ingestion (e.g. OpenAI) and a different one at query time (e.g. HuggingFace) will cause a dimension error or meaningless results. Always use the *same* model for both. Write the model name in config or store metadata so you don’t forget.

---

### 5.2 Vector Store — The Scale & Ops Lever

The store holds vectors and runs similarity search (e.g. k-NN). This choice is mainly about **scale, ops, and existing stack**.

**Rough mapping:**

- **Local / dev:** Chroma, FAISS — simple, no extra services.
- **Managed:** Pinecone, Weaviate — scale and managed ops.
- **Existing DB:** Postgres (pgvector), Elasticsearch, MongoDB — reuse current infra and avoid new systems.

**Rule of thumb:** If you already have Postgres or Elastic, use them unless you need huge scale (e.g. 100M+ vectors) or very low latency SLA. Don’t add a new store “just because” for small/medium scale.

---

### 5.3 Re-Indexing When You Change the Encoder

If you **switch the embedding model**, you **must re-embed every document**. Vectors from model A live in a different space than model B; you can’t mix them in one index.

Re-indexing has cost: time and (if using paid embedding APIs) money. Plan for it. Use blue/green indexing where you build a new index and switch traffic instead of in-place replacement when possible.

---

#### Check Your Understanding (Part 5)

1. What is the main trade-off when choosing an encoder (e.g. OpenAI vs small open-source)?
2. Why can’t we mix vectors from two different embedding models in one vector store?
3. If we already run Postgres in production, when would we still consider Pinecone or Weaviate?

**Milestone:** You can choose an embedding model and a vector store for your context (dev vs prod, scale) and know you must re-index if you change the encoder.

---

## Part 6: Visualization & Debugging

### 6.1 t-SNE (and Similar) Projections

Vectors live in high dimensions (e.g. 384 or 1536). We can’t plot that. **t-SNE** (and UMAP, etc.) project them down to 2D or 3D so we can look at clusters and outliers.

**Use it to:**

- See if chunks cluster by topic (good) or are a blob (maybe bad chunking or model).
- Spot outliers (e.g. one “contract” chunk sitting in the “HR” cluster — worth inspecting).
- Sanity-check ingestion before wiring to the full RAG.

**Caveat:** 2D/3D is approximate. Two points close in 2D might not be close in 384D. Use visualization to form hypotheses; validate with actual retrieval tests and metrics.

---

#### Check Your Understanding (Part 6)

1. Why do we project vectors to 2D/3D? What can we learn from it?
2. Why shouldn’t we rely only on 2D proximity to decide if two chunks are “similar” for retrieval?

**Milestone:** You know how to sanity-check your ingested data (e.g. t-SNE) and that 2D is only a hypothesis—validate with real retrieval tests.

---

## Part 7: Production Operations & Safety

### 7.1 Dev vs Prod Ingestion

- **Dev:** Wiping the store (e.g. `shutil.rmtree` on a local Chroma path) for a clean slate is fine.
- **Prod:** **Never** full wipe. Use **incremental indexing (upsert)**:
  - Track `document_id` and `last_modified` (or hash).
  - Embed only new or changed documents; upsert into the store.
  - For big changes, use **blue/green**: build a new index in parallel, then switch traffic.

---

### 7.2 Observability & Safety

- **Logging:** Log each retrieval: query (or hash), top doc IDs, similarity scores, latency. Essential for debugging and tuning.
- **Fallbacks:** If top results are below a confidence threshold (e.g. max score < 0.7), fall back to keyword search or a safe “I don’t have enough information” answer.
- **Security:** Treat retrieved text as untrusted input. Sanitize and bound it to reduce prompt injection and context overflow.

---

### 7.4 Error Handling & Resilience

- **Timeouts:** Set timeouts on embedding and LLM calls (e.g. 30s). Fail fast rather than hang.
- **Retries:** Use bounded retries with backoff for transient failures (rate limits, network). Don’t retry forever.
- **Partial failure:** If 1 of 100 docs fails to embed, log and skip (or dead-letter); don’t fail the whole batch. Track failure counts for alerting.
- **Fallback path:** If the vector store or encoder is down, fall back to keyword search or a static “search unavailable” response instead of exposing raw errors.

**Performance (ingestion):** Use batch embedding APIs when available (e.g. OpenAI accepts lists of texts). Respect rate limits and backpressure. For the query path, consider caching repeated queries or embeddings only if you’ve measured a need and have a cache-invalidation story.

---

### 7.5 Configuration & Secrets

- **Config:** Keep chunk size, overlap, `k`, `similarity_score_threshold`, and model names in config (env or config file), not hardcoded. Same code can run in dev/staging/prod with different values.
- **Secrets:** Never commit API keys. Use env vars or a secrets manager. LangChain reads `OPENAI_API_KEY` etc. from the environment by default — use that.
- **Versioning:** Pin `langchain>=1.0.0,<2` and the exact embedding model name (e.g. `text-embedding-3-large`) so runs and re-indexes are reproducible.

---

### 7.6 Model Benchmarking

Before locking in an encoder:

1. Take a sample of your data and queries.
2. Measure: accuracy (e.g. NDCG, relevance ratings), latency (e.g. p95), cost ($/1k tokens or per query).
3. Choose the model that meets your SLA at the lowest cost. Re-evaluate when you change data or requirements.

---

#### Check Your Understanding (Part 7)

1. Why do we avoid wiping the vector store in production? What do we do instead?
2. What should we log for every retrieval call?
3. What is a simple fallback when vector search returns only low-similarity results?

**Milestone:** You know how to run ingestion safely (incremental, blue/green), what to log, and how to handle errors and config without hardcoding.

---

## Part 8: Engineering Decision Matrix

Use this as a quick reference when making design choices.

| Question | What to consider | Recommended direction |
|----------|------------------|------------------------|
| **Which vector store?** | Existing DB? Scale? | Use Postgres/Elastic unless you need &gt;100M vectors or special SLA; then consider Pinecone/Weaviate. |
| **Which embedding model?** | Accuracy vs cost vs data residency | Benchmark small vs large; if small is ~95% as good at ~50% cost, prefer small. |
| **Chunk size?** | Content type (code vs prose) | Start ~512 tokens, ~50 overlap; tune with retrieval evals. |
| **Low retrieval quality?** | Model vs chunks | 1) Inspect clusters (e.g. t-SNE). 2) Check overlap and boundaries. 3) Try better encoder. |
| **Changing embedding model?** | Re-index cost and downtime | Re-embed everything; dimensions must match; plan downtime/cost and prefer blue/green. |
| **Dev vs prod ingestion?** | Static vs changing data | Dev: wipe & reload. Prod: upsert + incremental; blue/green for big re-indexes. |
| **Vectors “overlapping” in 2D?** | Bug or normal? | Often normal semantic overlap; use metadata filters to narrow when needed. |
| **LangChain vs raw API?** | Need for observability and integrations | Use LangChain for RAG and observability; raw/lite for simple proxy-only use cases. |

**Milestone:** When you face a design choice (store, model, chunk size, etc.), you can open this matrix and pick a direction instead of guessing.

---

# Implementation Track: Lessons 9–13 (Query Pipeline to Production)

The following sections complete the loop from “static vector library” to “conversational product.” Each lesson is summarized with **how** (mechanics), **why** (engineering rationale), and **when** (when to apply or avoid).

**When to use this track:** After you have ingestion working (documents → chunks → embeddings → vector store). Lessons 9–11 get you to a working query path and UI; Lessons 12–13 cover production structure and failure modes so you can ship and improve systematically.

---

## Lesson 9: The Query Pipeline (Completing the Loop)

### 9.1 What Changes

**Before Lesson 9:** You have a populated vector store (e.g. Chroma). It does not answer questions.  
**After Lesson 9:** A user question flows through Retriever → LLM → answer, and the UI shows the answer plus source documents.

**Why this matters:** Ingestion is “write”; query is “read.” In production these are often **separate services**: ingestion runs on a schedule or webhook; query runs on every user request. Separating them lets you scale and secure each path independently.

### 9.2 The Flow (Recap)

1. **User question** → e.g. “What are ticket prices to Heathrow?”
2. **Retriever** → Embeds the question, queries the vector store, returns **text chunks** (as `Document` objects).
3. **LLM** → Receives question + retrieved chunks (as text in the prompt) → generates answer.
4. **UI** → Shows answer + **source documents**.

**Engineering note:** The Retriever does **two** things inside a single `invoke()`: (1) embed the query with the same embedding model used at ingestion, (2) run similarity search. You don’t call the vector store or the embedding API directly in your query code—the Retriever abstraction hides that. **When** you swap the vector store (e.g. Chroma → Pinecone), only the Retriever’s backing changes; your query logic stays the same.

### 9.3 LangChain Abstractions: Retriever & LLM

| Abstraction | What it is | What it does | Why use it |
|-------------|------------|--------------|------------|
| **Retriever** | Wrapper around Vector Store + Embedding Model | `retriever.invoke(question)` → list of `Document` | Hides embedding + DB lookup; same interface regardless of store. |
| **LLM / ChatModel** | Wrapper around Generator (GPT-4, Claude, etc.) | `llm.invoke(messages)` → response | Swap provider/model without rewriting chain logic. |

**Return type:** The Retriever returns **`Document` objects** (each with `page_content` and `metadata`), not raw strings. That gives you text for the prompt plus source attribution (e.g. `source`, `doc_type`) for the UI and for debugging.

### 9.4 The `invoke` Pattern (Runnable Interface)

**How:** In LangChain 1.0, Retriever, LLM, Tools, and many other components respond to **`.invoke(input)`**. The exact type of `input` and the return type vary by component, but the method name is consistent.

**Why:** **Composability.** You can build chains (e.g. Retriever → Prompt → LLM) and later add steps (e.g. summarizer, router) because every step has a predictable interface. This is the same idea as a shared interface in classic OOP—polymorphism so you can swap implementations without changing the pipeline.

**When:** Use `.invoke()` for synchronous calls. For streaming or batch, LangChain exposes other methods (e.g. `.stream()`, `.batch()`); the principle of a single “trigger” per component still holds.

### 9.5 User Interface: Show Sources (Trust & Debugging)

**How:** The UI (e.g. Gradio, or a React/Next.js frontend) displays (1) the generated answer and (2) the **source documents** (chunks) used to produce it.

**Why:**

- **Trust:** Users don’t trust a black box. Citations let them verify the answer against the source.
- **Debugging:** When a user reports “wrong answer,” you inspect the sources. If sources are irrelevant → **retrieval** problem (embeddings/chunking). If sources are relevant but the answer is wrong → **generation** problem (prompt/LLM).
- **Hallucination signal:** If the UI shows “No sources found,” the user knows the answer may be weak or unsupported.

**When:** Treat source citation as **non-negotiable** for any production RAG UI. Gradio is fine for demos and internal QA; production will typically use a proper frontend with collapsible source cards.

### 9.6 “LangChain Is Optional” Reality

**Reality:** You can build a RAG pipeline with raw API calls (embedding API + vector store client + LLM API) in only a few more lines than with LangChain.

**Why use LangChain anyway?**

- **Observability:** LangSmith gives traces (latency per step, token counts, retrieved doc IDs, similarity scores). Essential for debugging RAG.
- **Consistency:** Same patterns across the team; easier to maintain and swap components.
- **Integrations:** Many vector stores and loaders are pre-wired.

**When to skip LangChain:** If you need ultra-low latency and want to strip every abstraction and dependency, a minimal custom pipeline may be justified. For most enterprise RAG, observability and standardization outweigh the extra lines of code.

### Lessons 1–9 Unified (Status)

| Phase | Lessons | Component | Status |
|-------|---------|-----------|--------|
| Theory | 1–3 | Vectors, embeddings, architecture | ✅ |
| Framework | 4 | LangChain ecosystem | ✅ |
| Ingestion | 5–8 | Chunking, embedding, Chroma, viz | ✅ |
| Query | 9 | Retriever, LLM, UI, invoke | ✅ |

**Checkpoint (Lesson 9):** What does the Retriever do with the embedding model and vector store when you call `invoke(question)`? Why is it important to show source documents in the UI?

---

## Lesson 10: Pipeline Parameters & Temperature

### 10.1 Embedding Consistency Rule (Golden Rule)

**Rule:** The embedding model used at **query** time **must** be the same as the one used at **ingestion** time.

**Why (two layers of failure):**

1. **Dimension mismatch:** If ingestion used 1536-dim vectors (e.g. OpenAI) and query uses 384-dim (e.g. all-MiniLM-L6-v2), the vector store will raise a **ValueError** (dimension mismatch). The code fails at runtime.
2. **Semantic mismatch:** Even if two models had the same dimension (e.g. both 768), they map meaning to different coordinates. A vector from model A is meaningless in an index built with model B—retrieval quality collapses.

**When / how to enforce:**

- Store the **embedding model name/version** in the vector store’s metadata (or in config tied to that store) at ingestion time.
- At query time, check that the current embedding model matches. If not, **abort and alert** instead of running a broken search.

### 10.2 Retriever & ChatModel (Recap)

- **Retriever:** `vectorstore.as_retriever()` — wraps store + embeddings; `invoke(query)` returns list of `Document`.
- **ChatModel:** e.g. `ChatOpenAI(model="gpt-4o-mini", temperature=0)` — wraps the generator; `invoke(messages)` returns the reply. You can swap to `ChatAnthropic` or another provider with minimal code change.

### 10.3 Temperature: What It Is and How to Use It

**What it is (mechanism):** Temperature controls **probability sampling** for the next token, not “creativity” in the abstract.

- **Temp = 0:** Choose the token with **highest probability** (argmax). Mostly deterministic.
- **Temp = 1:** Sample according to the model’s probability distribution.
- **Temp > 1:** Flatten the distribution; lower-probability tokens become more likely → higher variance.

**Why it matters for RAG:** We want answers **grounded in retrieved context**, not creative variation. So for RAG we keep temperature **low (0–0.5)**; for medical/legal/financial bots, **0** is standard.

**When:** Use **temperature 0** (or low) for factual RAG. Use higher temperature only for clearly creative tasks (e.g. story generation).

### 10.4 Reproducibility: Don’t Rely on It

**Reality:** Even with temperature 0, the same query can yield slightly different answers over time.

**Why:**

- **Model drift:** Providers update models silently; “gpt-4” today may not equal “gpt-4” in six months.
- **Parallelism:** GPU execution order can vary; floating-point non-determinism can change which token is “max.”

**When / how:** Don’t write tests that depend on **exact string match**. Test for **semantic equivalence** (does the answer mean the same thing?) or use evaluation metrics (e.g. faithfulness, relevance). Pin model versions (e.g. `gpt-4-0613`) when you need more stability.

### Lessons 1–10 Unified

| Phase | Lessons | Component | Status |
|-------|---------|-----------|--------|
| Theory | 1–3 | Vectors, embeddings, architecture | ✅ |
| Framework | 4, 9 | LangChain, invoke | ✅ |
| Ingestion | 5–8 | Chunking, embedding, Chroma, viz | ✅ |
| Query | 9–10 | Retriever, LLM, temperature | ✅ |

**Checkpoint (Lesson 10):** Why must ingestion and query use the same embedding model? Why use low temperature for RAG? What are two reasons the same query can give different answers even at temperature 0?

---

## Lesson 11: Stitching Retrieval + Generation

### 11.1 The Stitching Problem (Retriever ≠ LLM)

**Critical point:** The LLM has **no** access to your vector store. If you call `llm.invoke("Who is Avery?")` with no context, you get a generic answer from training data, not from your documents.

**How we fix it:** We **orchestrate two steps** and pass the result of the first into the second:

1. **Retriever:** `retriever.invoke(question)` → get relevant chunks.
2. **Context string:** Build one string from chunk `page_content` (e.g. `"\n\n".join([d.page_content for d in docs])`).
3. **Prompt:** Inject that string into a **system prompt** (or equivalent) so the LLM is told to answer using only this context.
4. **LLM:** `llm.invoke([SystemMessage(prompt), HumanMessage(question)])` → answer.

**Why this is “two API calls”:** Embedding API (for the query vector) + LLM completion API. That doubles latency and cost per query compared to a raw LLM call. **When** optimizing, consider caching, smaller context, or fewer retrieved chunks.

### 11.2 Prompt Templates (The Glue)

**How:** Use a fixed **system prompt template** that includes placeholders for `{context}` and possibly `{question}`. Example: “Answer only using the following context. If the answer is not in the context, say so. Context: {context}”

**Why:**

- **Consistency:** Every query gets the same structure and instructions.
- **Safety:** Explicit “if you don’t know, say so” reduces hallucination.
- **Separation:** Prompt logic stays out of retrieval logic; easier to test and tune.

**When / security:** Treat `{context}` as **untrusted** (it came from retrieval). Sanitize or wrap it in delimiters (e.g. `<context>...</context>`) to reduce prompt injection via retrieved text.

### 11.3 The Minimal Chain (Manual Chaining)

A minimal “5-line” pattern:

```python
docs = retriever.invoke(question)
context = "\n\n".join([d.page_content for d in docs])
prompt = system_prompt.format(context=context)
response = llm.invoke([SystemMessage(prompt), HumanMessage(question)])
return response.content
```

**What’s often missing in production:** Error handling (Chroma down, empty `docs`), **logging** (which docs were retrieved, scores), and use of **history** (this version is stateless). For multi-turn, you need message history and a strategy for what to pass to the retriever (see Lesson 12).

### 11.4 Fuzzy Matching (Semantic Payoff)

**Why RAG handles typos and paraphrasing:** We match on **vectors** (meaning), not keywords. “Who is Avery?” vs “Who is Lancaster?” vs slight misspellings can all retrieve the right chunk because the embedding captures intent. This reduces friction: users don’t need the exact wording from your docs.

### Lessons 1–11 Unified

| Phase | Lessons | Component | Status |
|-------|---------|-----------|--------|
| Theory | 1–3 | Vectors, embeddings, architecture | ✅ |
| Framework | 4, 9 | LangChain, invoke | ✅ |
| Ingestion | 5–8 | Chunking, embedding, Chroma, viz | ✅ |
| Query | 9–10 | Retriever, LLM, temperature | ✅ |
| Pipeline | 11 | Prompting, chaining, UI | ✅ |

**Checkpoint (Lesson 11):** Why can’t the LLM answer from your docs if you don’t pass retrieved context? What two API calls does a single RAG query typically imply?

---

## Lesson 12: Production Modularization

### 12.1 From Notebooks to Modules

**Why modules over notebooks in production:**

| Notebooks | Modules |
|-----------|---------|
| Linear, stateful execution | Reusable functions, stateless |
| Hard to test, hard to deploy | Unit-testable, CI/CD-friendly |
| Fragile for long runs | Robust, clear boundaries |

**When:** Use notebooks for exploration and one-off analysis. Use **modules** for ingestion and query code that runs in cron jobs, webhooks, or API servers.

### 12.2 Package Structure (Strategy Pattern)

**How:** Split into an **implementation** package that exposes a small interface, e.g.:

- `fetch_context(question, history)` → retrieved chunks or context string.
- `answer_question(question, history)` → final answer (and optionally sources).

The **UI** (e.g. `app.py` or a FastAPI app) depends only on these two functions, not on Chroma or a specific embedding model. You can have `implementation_v1/`, `implementation_v2/`, and swap via config or env (e.g. `IMPLEMENTATION_PATH=implementation_v2`).

**Why:** **Dependency inversion.** The app depends on an interface, not concrete implementations. That enables A/B testing (different chunking, models, or retrieval strategies) and quick rollback without changing the UI.

### 12.3 ingest.py vs answer.py (Write vs Read)

- **ingest.py:** Loads documents → chunks → embeds → writes to vector store. **When:** Run on a schedule, webhook (e.g. new doc in S3), or CI. In prod, use **incremental** ingestion (upsert by `document_id`); avoid full wipe.
- **answer.py:** Loads retriever + LLM, implements `fetch_context` and `answer_question`. **When:** Called on every user request (e.g. FastAPI endpoint). Only **reads** from the vector store.

**Why separate:** Different scaling (ingestion can be CPU/heavy; query needs low latency), different permissions (query service should not be able to wipe the store), and independent deploy (fix answer logic without re-running ingestion).

### 12.4 History Handling (Multi-Turn)

**Problem:** The UI (e.g. Gradio) passes conversation history as a list of dicts (`role`, `content`). LangChain’s `ChatModel.invoke()` expects **LangChain message objects** (`HumanMessage`, `AIMessage`, etc.). Passing raw dicts can cause `TypeError` or wrong role handling.

**How:** Convert UI history to LangChain messages before calling the LLM. That preserves roles and ordering so the model sees a proper multi-turn conversation.

**combine_question for retrieval:** For retrieval, we need a **single query**. A naive approach is to use only the latest message (“What did she do before?”). The retriever doesn’t know “she” = Avery. So we **combine** recent user messages into one query string (e.g. “Who is Avery? What did she do before?”) and run retrieval on that. **When** this is wrong: when the user **changes topic** (e.g. “Who won the IIoT award?”); the combined query can still be dominated by “Avery” and return the wrong context (topic drift). Alternatives: **query rewriting** (LLM turns the last question into a stand-alone question using history), **sliding window** (only last N messages), or **topic detection** (reset context on subject change). A/B test these strategies.

### Lessons 1–12 Unified

| Phase | Lessons | Component | Status |
|-------|---------|-----------|--------|
| Theory | 1–3 | Vectors, embeddings, architecture | ✅ |
| Framework | 4, 9 | LangChain, invoke | ✅ |
| Ingestion | 5–8, 12 | Chunking, embedding, Chroma, modularization | ✅ |
| Query | 9–11, 12 | Retriever, LLM, history, interfaces | ✅ |
| Production | 12 | Modules, swappability, DevOps | ✅ |

**Checkpoint (Lesson 12):** Why separate ingest and answer into different modules? Why convert UI message history to LangChain message types? What is one downside of combining all user messages for retrieval?

---

## Lesson 13: Failure Modes & Empirical Tuning

### 13.1 Naive vs Proper Implementation

**Naive (broken):** No history; retrieval only on the latest question. Example: user asks “Who is Avery?” then “What is her salary?” — the retriever searches for “What is her salary?” and may return any doc about “salary” (e.g. another person). **Why it fails:** No link between “her” and Avery; wrong context.

**Proper (Lesson 12):** Convert history to LangChain messages; use **combine_question** (or similar) so retrieval sees “Who is Avery? What is her salary?” and returns Avery’s context. **But** this introduces **topic drift** when the user switches subject (e.g. “Who won the IIoT award?”) — the combined query still emphasizes “Avery” and can return the wrong chunks. So we iterate: query rewriting, sliding window, or topic detection, and **measure** impact.

### 13.2 Chunking Boundary Failures

**Example:** User asks “Who won the prestigious IIoT award?” Answer: “Maxine was recognized…” but not “Maxine Thompson.” **Why:** The chunk that contains “received the prestigious IIoT award” was split so that “Maxine Thompson” (full name) stayed in another chunk. Retrieval returned the right chunk for “award,” but the LLM never saw the full name.

**How to mitigate:**

- **Increase chunk overlap** so names and key facts are less likely to be split across boundaries.
- **Parent-document retrieval:** Store small chunks for retrieval, but when a chunk is retrieved, pass the **parent document** (or a larger window) to the LLM so it sees full names and surrounding context.
- **Metadata enrichment:** Attach `full_name`, `document_id`, etc., to chunks so the LLM can use metadata even when the exact phrase is in another chunk.

**When:** If the answer is “almost right” but missing an obvious detail (e.g. full name, date), inspect **chunk boundaries** first before blaming retrieval or the LLM.

### 13.3 RAG Is Empirical (Trial and Error)

**Reality:** RAG is heuristic. Many parameters interact: chunk size, overlap, embedding model, top_k, similarity threshold, and history/query strategy. There is no closed-form “correct” setting.

**How to improve systematically:**

| Practice | Purpose |
|----------|---------|
| **Evaluation harness** | Golden set of Q&A; run after every change; track metrics (e.g. context relevance, answer faithfulness). |
| **Logging & tracing** | Log every retrieval (query, doc IDs, scores); use LangSmith or equivalent for debugging. |
| **A/B testing** | Compare configurations (e.g. combine_question vs query rewriting) on real or synthetic traffic. |
| **Metrics dashboard** | Track accuracy, latency, cost over time so you see regressions. |

**When:** Don’t guess parameters. **Measure.** Build a test set of 50–100 representative queries, run the harness on each change, and block deploy if scores drop (or alert and investigate).

### 13.4 Manual Evaluation (LLM-as-Judge)

**How:** Curate a set of questions with expected answers (or criteria). Run the RAG pipeline on each; use another LLM to score relevance, faithfulness, or correctness (e.g. 1–10 or binary). Automate this in CI so regressions are caught before deploy.

**Why:** This is the core idea behind tools like RAGAS and TruLens—automated, repeatable evaluation so “it works on my examples” becomes “it meets a defined bar.”

### Lessons 1–13 Unified

| Phase | Lessons | Component | Status |
|-------|---------|-----------|--------|
| Theory | 1–3 | Vectors, embeddings, architecture | ✅ |
| Framework | 4, 9 | LangChain, invoke | ✅ |
| Ingestion | 5–8, 12 | Chunking, embedding, Chroma, modularization | ✅ |
| Query | 9–11, 12 | Retriever, LLM, history, interfaces | ✅ |
| Production | 12 | Modules, swappability | ✅ |
| Failure analysis | 13 | Topic drift, chunk boundaries, empirical tuning | ✅ |

**Checkpoint (Lesson 13):** What is one alternative to combining all user messages for retrieval? How can you mitigate “correct but incomplete” answers due to chunk boundaries? Name two practices to move from ad-hoc tuning to systematic improvement.

**Milestone (Lessons 9–13):** You have a full query path (Retriever → LLM), understand temperature and embedding consistency, can stitch prompt + context, and know how to modularize and debug failure modes. You’re ready to run evals and ship.

---

# Reference Implementation: ingest.py & answer.py

This section walks through a **production-style RAG implementation** split into two files: **ingest.py** (write path) and **answer.py** (read path). The code uses **raw OpenAI and Chroma** (no LangChain), so you see exactly what happens under the hood. The same architecture applies when you use LangChain: same separation of ingest vs query, same embedding consistency, same “context + question → LLM” stitch.

Use this to see how the concepts from Parts 1–8 and Lessons 9–13 map onto real scripts and to understand the **architecture** behind a two-file RAG build.

---

## Architecture Overview: How the Two Files Fit Together

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  INGESTION (ingest.py) — runs on schedule or when new docs arrive                │
├─────────────────────────────────────────────────────────────────────────────────┤
│  knowledge-base/                                                                  │
│    ├── *.md files                                                                 │
│         │                                                                         │
│         ▼                                                                         │
│  fetch_documents()  ──►  create_chunks()  ──►  create_embeddings()               │
│  (load by folder)        (LLM or splitter)    (OpenAI embed → Chroma add)         │
│                                                      │                            │
│                                                      ▼                            │
│                                              preprocessed_db/  (Chroma)           │
│                                              collection: "docs"                   │
│                                              embedding_model: text-embedding-3-*  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         │  shared: DB_NAME, collection_name,
                                         │          embedding_model (must match)
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│  QUERY (answer.py) — runs on every user question                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│  question + optional history                                                       │
│         │                                                                         │
│         ▼                                                                         │
│  fetch_context(question)  ──►  make_rag_messages(question, history, chunks)       │
│  (embed question, query Chroma, optionally rewrite query, rerank)                │
│         │                              │                                          │
│         │                              ▼                                          │
│         │                     completion(MODEL, messages)  ──►  answer             │
│         │                                                                         │
│         └──────────────────────────────► return (answer, chunks)  ──►  UI shows  │
│                                            (sources for citation)      answer +   │
│                                                                        sources   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**Design principles reflected here:**

- **Single vector store, single embedding model:** Both scripts use the same `DB_NAME`, `collection_name`, and `embedding_model`. That’s the Golden Rule (Lesson 10).
- **Ingest = write, Answer = read:** Ingestion creates/replaces the collection; the answer path only queries. In production they can run in different processes or services (e.g. cron vs API).
- **Answer returns chunks:** The API returns `(answer, chunks)` so the UI can show **source documents** (Lesson 9, Part 7).

---

## ingest.py: Breakdown and Mapping to the Guide

### Role of ingest.py

Turn documents on disk into **chunks**, then **embed** them and **write** them into the vector store. Nothing in this file answers user questions—it only prepares the knowledge base.

### 1. Config and shared constants (top of file)

```python
DB_NAME = str(Path(__file__).parent.parent / "preprocessed_db")
collection_name = "docs"
embedding_model = "text-embedding-3-large"
KNOWLEDGE_BASE_PATH = Path(__file__).parent.parent / "knowledge-base"
AVERAGE_CHUNK_SIZE = 100
WORKERS = 3
```

- **DB_NAME / collection_name:** Must match what **answer.py** uses so both talk to the same Chroma collection. (See Part 10: same store for ingest and query.)
- **embedding_model:** Must be **identical** in answer.py. If you change it here, you must re-run ingestion and use the same value at query time (Part 5, Lesson 10).
- **KNOWLEDGE_BASE_PATH:** Where raw documents live (e.g. `.md` per folder). In a larger system this could be S3, a CMS, etc.
- **AVERAGE_CHUNK_SIZE / WORKERS:** Tuning for chunking and parallel document processing (Part 4, Part 7).

**Guide link:** Part 7 (Configuration & Secrets) — config at top; in production these would come from env or a config module.

---

### 2. Document and chunk schema (Pydantic)

```python
class Result(BaseModel):
    page_content: str
    metadata: dict

class Chunk(BaseModel):
    headline: str = Field(description="A brief heading for this chunk ...")
    summary: str = Field(description="A few sentences summarizing the content ...")
    original_text: str = Field(description="The original text of this chunk ...")

    def as_result(self, document):
        metadata = {"source": document["source"], "type": document["type"]}
        return Result(
            page_content=self.headline + "\n\n" + self.summary + "\n\n" + self.original_text,
            metadata=metadata,
        )
```

- **Result:** Same idea as LangChain’s `Document`: `page_content` (text stored and retrieved) + `metadata` (source, type). Answer.py will receive chunks in this shape (Part 4.4 Document & Retriever contracts).
- **Chunk:** This implementation uses an **LLM** to produce structured chunks (headline, summary, original text) instead of a fixed-size splitter. That’s a valid production choice: semantic boundaries and summaries can improve retrieval. The important part is that each chunk becomes a **Result** with stable metadata for filtering and citation.

**Guide link:** Part 4 (metadata for attribution and filtering); Part 4.4 (Document contract).

---

### 3. Loading documents: fetch_documents()

```python
def fetch_documents():
    documents = []
    for folder in KNOWLEDGE_BASE_PATH.iterdir():
        doc_type = folder.name
        for file in folder.rglob("*.md"):
            with open(file, "r", encoding="utf-8") as f:
                documents.append({"type": doc_type, "source": file.as_posix(), "text": f.read()})
    return documents
```

- **Purpose:** Build a list of raw documents, each with `type` (e.g. folder name), `source` (path), and `text` (content). This is the “homemade DirectoryLoader” pattern.
- **Metadata early:** Attaching `type` and `source` here ensures every chunk later can carry them (Part 4.3).

**Guide link:** Part 4 (data preparation); Part 10 (ingestion pipeline).

---

### 4. Chunking via LLM: make_prompt(), process_document(), create_chunks()

The implementation **does not** use `RecursiveCharacterTextSplitter`. It uses an **LLM** with a structured prompt to split each document into overlapping chunks with headline and summary:

```python
def make_prompt(document):
    how_many = (len(document["text"]) // AVERAGE_CHUNK_SIZE) + 1
    return f"""
You take a document and you split the document into overlapping chunks ...
This document should probably be split into at least {how_many} chunks ...
There should be overlap between the chunks as appropriate; typically about 25% overlap ...
For each chunk, provide a headline, a summary, and the original text.
...
{document["text"]}
"""
```

- **Why LLM chunking:** Better semantic boundaries and built-in summaries (good for retrieval and display). Trade-off: cost and latency; you need a small/fast model and possibly rate-limit handling (WORKERS=1 if needed).
- **Overlap:** The prompt asks for ~25% overlap, matching the guide’s 10–20% overlap idea (Part 4.2).

```python
@retry(wait=wait)
def process_document(document):
    messages = make_messages(document)
    response = completion(model=MODEL, messages=messages, response_format=Chunks)
    reply = response.choices[0].message.content
    doc_as_chunks = Chunks.model_validate_json(reply).chunks
    return [chunk.as_result(document) for chunk in doc_as_chunks]

def create_chunks(documents):
    chunks = []
    with Pool(processes=WORKERS) as pool:
        for result in tqdm(pool.imap_unordered(process_document, documents), total=len(documents)):
            chunks.extend(result)
    return chunks
```

- **process_document:** One document → one LLM call → list of `Result` with `page_content` and metadata. `@retry` handles transient failures (Part 7.4).
- **create_chunks:** Parallel over documents. Output is a single flat list of chunks ready for embedding.

**Guide link:** Part 4 (why we chunk, overlap); Part 7.4 (retries); Lesson 12 (ingestion as a separate process).

---

### 5. Embedding and writing to Chroma: create_embeddings()

```python
def create_embeddings(chunks):
    chroma = PersistentClient(path=DB_NAME)
    if collection_name in [c.name for c in chroma.list_collections()]:
        chroma.delete_collection(collection_name)

    texts = [chunk.page_content for chunk in chunks]
    emb = openai.embeddings.create(model=embedding_model, input=texts).data
    vectors = [e.embedding for e in emb]

    collection = chroma.get_or_create_collection(collection_name)
    ids = [str(i) for i in range(len(chunks))]
    metas = [chunk.metadata for chunk in chunks]
    collection.add(ids=ids, embeddings=vectors, documents=texts, metadatas=metas)
```

- **Delete then recreate:** Acceptable for **dev** or a full re-index. In **production** you’d use incremental upsert (Part 7.1).
- **Batch embed:** `input=texts` sends all chunk texts in one API call (efficiency; Part 7.4 performance).
- **Same embedding model:** `embedding_model` is the one answer.py must use for queries (Lesson 10).
- **What gets stored:** For each chunk: `id`, **embedding** (vector), **documents** (text), **metadatas** (source, type). Chroma stores both the vector and the text so retrieval can return text + metadata without re-calling the embedding API.

**Guide link:** Part 5 (encoder, vector store); Part 7.1 (dev wipe vs prod incremental); Lesson 10 (embedding consistency).

---

### 6. Main flow

```python
if __name__ == "__main__":
    documents = fetch_documents()
    chunks = create_chunks(documents)
    create_embeddings(chunks)
```

**Order:** Load → Chunk → Embed → Write. This is the full ingestion pipeline; run it whenever the knowledge base changes (or on a schedule).

---

## answer.py: Breakdown and Mapping to the Guide

### Role of answer.py

Given a **question** (and optional **history**), **retrieve** relevant chunks from Chroma, then **build a prompt** (context + question) and call the **LLM** to produce an answer. Return **answer + chunks** so the UI can show sources.

### 1. Config and Chroma client (top of file)

```python
DB_NAME = str(Path(__file__).parent.parent / "preprocessed_db")
collection_name = "docs"
embedding_model = "text-embedding-3-large"
RETRIEVAL_K = 20
FINAL_K = 10
chroma = PersistentClient(path=DB_NAME)
collection = chroma.get_or_create_collection(collection_name)
```

- **DB_NAME, collection_name, embedding_model:** Must match ingest.py (Lesson 10). This is how the “read” side uses the same index the “write” side built.
- **RETRIEVAL_K / FINAL_K:** Retrieve 20 candidates, then rerank and keep 10. This is an **advanced** pattern (retrieve more, then rerank) to improve relevance; the guide’s basic pattern is “retrieve top-k with score_threshold” (Part 3.3, Lesson 9).

**Guide link:** Part 5 (vector store); Lesson 10 (embedding consistency).

---

### 2. System prompt (context injection)

```python
SYSTEM_PROMPT = """
You are a knowledgeable, friendly assistant representing the company Insurellm.
...
For context, here are specific extracts from the Knowledge Base that might be directly relevant to the user's question:
{context}

With this context, please answer the user's question. Be accurate, relevant and complete.
If you don't know the answer, say so.
"""
```

- **{context}:** Placeholder for the retrieved chunks. At runtime this is replaced by the concatenation of chunk texts (Lesson 11). The LLM **only** sees text—never vectors.
- **“If you don’t know, say so”:** Reduces hallucination (Lesson 11, Part 7.2). Treat `context` as untrusted (sanitize/delimit in high-security settings).

**Guide link:** Lesson 11 (prompt templates, stitching retrieval + generation).

---

### 3. Fetching context: embed query → query Chroma → (optional) rewrite + rerank

**Step A — Unranked retrieval (same as “Retriever” in spirit):**

```python
def fetch_context_unranked(question):
    query = openai.embeddings.create(model=embedding_model, input=[question]).data[0].embedding
    results = collection.query(query_embeddings=[query], n_results=RETRIEVAL_K)
    chunks = []
    for result in zip(results["documents"][0], results["metadatas"][0]):
        chunks.append(Result(page_content=result[0], metadata=result[1]))
    return chunks
```

- **Same embedding model:** `embedding_model` is the same as in ingest.py. Query vector is in the same space as stored vectors (Lesson 10).
- **Flow:** Question → one embedding API call → vector → Chroma `query` → list of (document, metadata). That’s exactly what a LangChain Retriever wraps (Lesson 9).
- **Return type:** List of `Result` (page_content + metadata) for building the prompt and for UI citations.

**Step B — Query rewriting (optional, improves retrieval):**

```python
def rewrite_query(question, history=[]):
    """Rewrite the user's question to be a more specific question that is more likely to surface relevant content."""
    # ... LLM call that returns a short, refined question ...
    return response.choices[0].message.content
```

- **Purpose:** Turn “What did she do before?” (with history) into a stand-alone, specific question so vector search gets better results (Lesson 12, Lesson 13: query rewriting vs combine_question).

**Step C — Merge and rerank:**

```python
def fetch_context(original_question):
    rewritten_question = rewrite_query(original_question)
    chunks1 = fetch_context_unranked(original_question)
    chunks2 = fetch_context_unranked(rewritten_question)
    chunks = merge_chunks(chunks1, chunks2)
    reranked = rerank(original_question, chunks)
    return reranked[:FINAL_K]
```

- **Dual retrieval:** Run retrieval on both the original and the rewritten question, then merge (dedupe). Then **rerank** with an LLM so the top FINAL_K chunks are the most relevant. This is an advanced pattern; the guide’s baseline is single retrieval + optional similarity_score_threshold (Lesson 9, Lesson 13).

**Guide link:** Lesson 9 (Retriever = embed + query); Lesson 10 (same embedding model); Lesson 12–13 (query rewriting, reranking).

---

### 4. Building RAG messages and calling the LLM

```python
def make_rag_messages(question, history, chunks):
    context = "\n\n".join(
        f"Extract from {chunk.metadata['source']}:\n{chunk.page_content}" for chunk in chunks
    )
    system_prompt = SYSTEM_PROMPT.format(context=context)
    return (
        [{"role": "system", "content": system_prompt}]
        + history
        + [{"role": "user", "content": question}]
    )

def answer_question(question: str, history: list[dict] = []) -> tuple[str, list]:
    chunks = fetch_context(question)
    messages = make_rag_messages(question, history, chunks)
    response = completion(model=MODEL, messages=messages)
    return response.choices[0].message.content, chunks
```

- **make_rag_messages:** Inject **context** (retrieved chunks, with source labels) into the system prompt; append **history** and the current **question**. This is the “stitch” in Lesson 11: retrieval output (text) + user input → LLM input.
- **answer_question:** Fetch context → build messages → one LLM call → return **(answer, chunks)**. The UI can show the answer and the list of chunks as sources (Lesson 9, Part 7.2).

**Guide link:** Lesson 11 (prompt assembly, two API calls per query); Lesson 9 (show sources).

---

## How This Maps to the Guide’s Concepts

| Concept in the guide | Where you see it in ingest.py / answer.py |
|----------------------|-------------------------------------------|
| **Two-model system (Part 2)** | Encoder (embedding_model) for retrieval; LLM (MODEL) for generation. Never send vectors to the LLM. |
| **Chunking & metadata (Part 4)** | Chunk schema (headline, summary, original_text); metadata (source, type); overlap in prompt. |
| **Encoder + vector store (Part 5)** | Same embedding_model; Chroma PersistentClient; batch embed and add. |
| **Embedding consistency (Lesson 10)** | Same `embedding_model` in both files; re-index if you change it. |
| **Retriever = embed + query (Lesson 9)** | fetch_context_unranked: embed question → collection.query → Result list. |
| **Prompt = context + question (Lesson 11)** | SYSTEM_PROMPT with {context}; make_rag_messages(question, history, chunks). |
| **Return answer + sources (Lesson 9, Part 7)** | answer_question returns (content, chunks) for UI citation. |
| **Config at top (Part 7)** | DB_NAME, collection_name, embedding_model, RETRIEVAL_K, etc. |
| **Retries (Part 7.4)** | @retry on process_document, rerank, rewrite_query, answer_question. |
| **Ingest vs query separation (Lesson 12)** | Two files; ingest writes, answer reads; same store and embedding model. |

---

## Takeaway for the Junior

- **ingest.py** = load docs → chunk (LLM or splitter) → embed with a **fixed** embedding model → write to Chroma. Run when the knowledge base changes.
- **answer.py** = embed the **question** with the **same** embedding model → query Chroma → (optionally) rewrite query, merge, rerank → build prompt (context + question + history) → LLM → return answer + chunks for citation.
- The **architecture** is the same whether you use LangChain or raw APIs: one store, one embedding model, clear split between “write” (ingest) and “read” (answer), and always pass **text** (not vectors) into the LLM and return **sources** to the UI.

---

## Part 9: Testing & Quality

### 9.1 What to Test

- **Chunking:** Unit tests that given a known document, the splitter produces expected number of chunks and preserves critical phrases (e.g. no cut mid-sentence at a boundary). Assert metadata is attached.
- **Retrieval shape:** Integration test that the retriever returns a list of objects with `page_content` and `metadata`, and that `similarity_score_threshold` actually filters (e.g. low-similarity query returns fewer or zero docs when threshold is high).
- **RAG pipeline:** Integration test: insert a known chunk, ask a question that should retrieve it, assert the chunk appears in the chain’s `context` and the answer is non-empty. Use a small in-memory store and deterministic seed if possible.
- **Eval harness:** Use RAGAS, TruLens, or custom metrics (e.g. relevance of retrieved docs, faithfulness of answer to context) on a golden set of Q&A. Run in CI when you change chunking, model, or prompt so regressions are visible.

### 9.2 Where Tests Live

- Unit tests next to the code (e.g. `tests/test_chunking.py`, `tests/test_retriever.py`).
- Integration tests that hit a real vector store (or test container) and optionally a real embedding API (with rate limits and cost in mind — or use mocks for daily CI).
- Eval suite as a separate script or job (e.g. `scripts/rag_eval.py`) with a fixed dataset and reported metrics.

---

## Part 10: Project Structure & Boundaries

A clean layout keeps ingestion and query paths obvious and makes swapping components easier:

```
project/
  config/           # or .env.example — chunk_size, overlap, score_threshold, model names
  src/
    ingestion/      # load docs → chunk → embed → upsert to store
    query/         # query → retriever → prompt → LLM → response
    shared/        # Document schema, retriever factory, env-based config
  tests/
    unit/
    integration/
  scripts/
    rag_eval.py    # Eval harness
```

**Ingestion vs query:** Ingestion runs on a schedule or event (e.g. new doc); it’s batch-oriented and can be heavy. Query path is latency-sensitive; keep it minimal (retrieve → prompt → generate). Don’t mix “re-index everything” logic in the request path.

---

## Part 11: Anti-Patterns (What Not to Do)

| Anti-pattern | Why it’s bad | Do this instead |
|--------------|--------------|------------------|
| Sending vectors into the generator LLM | LLMs expect tokens (text), not vectors. | Only pass retrieved *text* (and prompt) to the LLM. |
| Wiping the vector store in production | Data loss, downtime. | Incremental upsert; blue/green for full re-index. |
| No similarity threshold (`score_threshold`) | Bad retrievals still get passed to the LLM. | Use `similarity_score_threshold` and handle “no results” with a fallback. |
| Hardcoding API keys or chunk size | Security risk; can’t tune per env. | Config/env for keys and all tunables. |
| Ignoring retrieval in tests | Regressions in chunking or model hide until production. | Unit test chunking; integration test retrieval shape and RAG chain. |
| Mixing embedding dimensions in one store | Similarity math is wrong across different models. | One store = one embedding model; re-index when changing model. |
| Running full re-index in the request path | Blocks users and can timeout. | Run ingestion in a job; query path only reads. |

---

#### Check Your Understanding (Parts 9–11)

1. What should a unit test for chunking verify? What should an integration test for the retriever verify?
2. Why separate “ingestion” and “query” in project structure and runtime?
3. Name two anti-patterns from the table and what to do instead.

---

## References

- **LangChain:** [langchain.com/docs](https://python.langchain.com/docs/) — use the v1/modular packages (`langchain-openai`, `langchain-chroma`, etc.).
- **RAG evaluation:** RAGAS, TruLens — add to your eval harness.
- **LangSmith:** Tracing and debugging for LangChain runs; set `LANGCHAIN_TRACING_V2=true` and `LANGCHAIN_API_KEY` for production observability.

---

## Summary for Eran

You now have:

- **Big picture & path:** What you’ll build (documents → chunks → store → Q&A with citations), **prerequisites** (Python, env, API keys), **learning path** table, **pipeline diagram**, **build order** (setup → quick start → ingest → query → UI → harden), **quick start** script to run RAG in one file, **scope** (what’s in and out), and **troubleshooting** for common beginner issues.
- **Glossary:** RAG, encoder, retriever, chunk, vector store, cosine similarity, upsert, re-index, **invoke**, **Runnable**, **Temperature**, **combine_question**, **parent-document retrieval**, **query rewriting**.
- **Concepts:** Vectors vs tokens, encoders vs generators, cosine similarity, why RAG works.
- **Architecture:** The two-model RAG pipeline and where vectors are used (and where they are not).
- **Framework:** What LangChain is, why we use it, code patterns (chunking, retriever with `similarity_score_threshold`, RAG chain).
- **Data:** Why we chunk, how to chunk (recursive + overlap), metadata, and **contracts** (Document, retriever, idempotent document_id).
- **Infrastructure:** Encoder = quality/cost; store = scale/ops; re-index when you change the encoder; **ingestion model must equal query model**.
- **Implementation track (Lessons 9–13):** Query pipeline (Retriever + LLM, invoke, UI with sources), **temperature** (low for RAG, reproducibility caveats), **stitching** (prompt template, two API calls per query), **modularization** (ingest vs answer, history handling, combine_question trade-offs), **failure modes** (topic drift, chunk boundaries, parent-document retrieval, systematic evaluation).
- **Reference implementation (ingest.py & answer.py):** Full breakdown of a two-file RAG (raw OpenAI + Chroma): architecture diagram, ingest (load → chunk → embed → Chroma), answer (fetch_context → prompt → LLM → answer + chunks), and how each step maps to the guide’s concepts.
- **Debugging:** t-SNE and logging to form hypotheses and validate with retrieval tests; **source citations** for trust and debugging.
- **Operations:** Incremental indexing, logging, fallbacks, **error handling** (timeouts, retries, partial failure), **configuration & secrets**, and benchmarking.
- **Testing:** Unit tests (chunking), integration tests (retriever shape, RAG pipeline), and an eval harness (RAGAS/TruLens) in CI.
- **Structure:** Clear separation of ingestion vs query path, suggested project layout, **interface over implementation** for swappability.
- **Anti-patterns:** What not to do (vectors to LLM, wiping prod, no threshold, hardcoded config, mixing dimensions, re-index in request path).
- **References:** LangChain docs, RAGAS/TruLens, LangSmith.

Next step is to **build a minimal RAG pipeline** (one encoder, one vector store, one LLM) with LangChain, add logging and a similarity threshold, then run the checks in this guide on your own data. Work through the **Implementation Track (Lessons 9–13)** to complete the loop from ingestion to production-style modularization and failure analysis. If you can answer all the “Check Your Understanding” and checkpoint questions and explain the decision matrix, you’re ready to own a production RAG feature.

— Todd
