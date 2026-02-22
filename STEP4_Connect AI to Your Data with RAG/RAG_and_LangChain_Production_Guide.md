# Production-Grade RAG & LangChain: Engineer’s Guide

**For:** Eran, Junior AI Engineer  
**From:** Todd, Senior AI Engineer & Team Lead  
**Purpose:** Turn you into a confident builder of RAG applications with LangChain  
**Assumptions:** No prior RAG, vector, or embedding knowledge  

---

## How to Use This Guide

- Read section by section. Each builds on the previous.
- Answer the **Check Your Understanding** questions before moving on.
- **Engineering decisions** are called out so you know *why* we choose one option over another.
- Code and config examples are production-oriented, not throwaway scripts.

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

---

## Part 1: Core Concepts — Vectors & Embeddings

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

**Engineering choice:** Fixed token count alone is brittle. Recursive splitting + overlap is the default; then tune chunk size and overlap on your content and retrieval metrics.

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

---

## Part 5: Infrastructure — Encoders & Vector Stores

### 5.1 Encoder (Embedding) Model — The Quality Lever

The encoder turns text into vectors. This choice **drives accuracy** more than the vector store in many cases.

**Options (examples):**

- **OpenAI** (e.g. text-embedding-3-large): High quality, paid API, 1536 dimensions.
- **HuggingFace** (e.g. all-MiniLM-L6-v2): Open source, local, cheaper, often 384 dimensions.

**Dimensions are model-specific.** You cannot mix dimensions in one index: every vector in a store must come from the same embedding model (same dimensions and same “space”).

**Decision:** Benchmark a few encoders on *your* data (accuracy, latency, cost). Often a smaller/cheaper model gets 90%+ of the benefit at half the cost. Start there unless you have proven need for the largest model.

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

- **Glossary:** Quick reference for RAG, encoder, retriever, chunk, vector store, cosine similarity, upsert, re-index.
- **Concepts:** Vectors vs tokens, encoders vs generators, cosine similarity, why RAG works.
- **Architecture:** The two-model RAG pipeline and where vectors are used (and where they are not).
- **Framework:** What LangChain is, why we use it, code patterns (chunking, retriever with `similarity_score_threshold`, RAG chain).
- **Data:** Why we chunk, how to chunk (recursive + overlap), metadata, and **contracts** (Document, retriever, idempotent document_id).
- **Infrastructure:** Encoder = quality/cost; store = scale/ops; re-index when you change the encoder.
- **Debugging:** t-SNE and logging to form hypotheses and validate with retrieval tests.
- **Operations:** Incremental indexing, logging, fallbacks, **error handling** (timeouts, retries, partial failure), **configuration & secrets**, and benchmarking.
- **Testing:** Unit tests (chunking), integration tests (retriever shape, RAG pipeline), and an eval harness (RAGAS/TruLens) in CI.
- **Structure:** Clear separation of ingestion vs query path and a suggested project layout.
- **Anti-patterns:** What not to do (vectors to LLM, wiping prod, no threshold, hardcoded config, mixing dimensions, re-index in request path).
- **References:** LangChain docs, RAGAS/TruLens, LangSmith.

Next step is to **build a minimal RAG pipeline** (one encoder, one vector store, one LLM) with LangChain, add logging and a similarity threshold, then run the checks in this guide on your own data. If you can answer all the “Check Your Understanding” questions and explain the decision matrix, you’re ready to own a production RAG feature.

— Todd
