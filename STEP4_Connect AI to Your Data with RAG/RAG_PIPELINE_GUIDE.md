# Complete RAG Pipeline Guide: Step-by-Step Explanation

This guide walks through the `visualize_vector_chunks.py` script, explaining each step in detail with code examples, concepts, and best practices.

## Table of Contents

1. [Overview](#overview)
2. [Step 1: Setup Environment](#step-1-setup-environment)
3. [Step 2: Analyze Knowledge Base Size](#step-2-analyze-knowledge-base-size)
4. [Step 3: Load Documents with Metadata](#step-3-load-documents-with-metadata)
5. [Step 4: Chunk Documents](#step-4-chunk-documents)
6. [Step 5: Create Embeddings & Vectorstore](#step-5-create-embeddings--vectorstore)
7. [Step 6: Extract Vectors for Analysis](#step-6-extract-vectors-for-analysis)
8. [Step 7: Visualize Embeddings](#step-7-visualize-embeddings)
9. [Complete Flow Diagram](#complete-flow-diagram)
10. [Quick Reference](#quick-reference)

---

## Overview

### What is RAG?

**RAG (Retrieval-Augmented Generation)** combines:
- **Retrieval**: Finding relevant information from your documents
- **Augmented**: Adding that information to LLM prompts
- **Generation**: LLM generates answers using retrieved context

### The Complete Pipeline

```
📁 Files on Disk
    ↓
📄 Documents (LangChain Document objects with metadata)
    ↓
✂️  Chunks (Smaller Document pieces, still with metadata)
    ↓
🔢 Embeddings (Vectors: arrays of numbers representing meaning)
    ↓
💾 Vector Database (Chroma stores vectors + chunks + metadata)
    ↓
📊 Visualization (2D plot showing relationships)
```

### Why Each Step Matters

1. **Loading**: Convert files to a standard format LangChain understands
2. **Chunking**: Break large documents into manageable pieces
3. **Embeddings**: Convert text to numbers that capture meaning
4. **Vector Database**: Store embeddings for fast similarity search
5. **Visualization**: Understand how your documents relate to each other

---

## Step 1: Setup Environment

### What It Does

Loads environment variables from a `.env` file and verifies API key configuration.

### Code

```python
def setup_environment():
    """
    Load environment variables and verify API key configuration.
    
    Returns:
        str: The OpenAI API key if found, None otherwise
    """
    load_dotenv(override=True)
    openai_api_key = os.getenv('OPENAI_API_KEY')
    
    if openai_api_key:
        print(f"✓ OpenAI API Key exists and begins {openai_api_key[:8]}")
    else:
        print("⚠ OpenAI API Key not set")
    
    return openai_api_key
```

### Why Written This Way

- **`load_dotenv(override=True)`**: Reads secrets from `.env` file (keeps keys out of code)
- **`override=True`**: Ensures latest values are used
- **Early verification**: Checks if API key exists before proceeding

### What Happens

- Loads environment variables from `.env` file
- Checks if `OPENAI_API_KEY` exists
- Prints status message
- Returns the key (or `None`) for later use

### Key Concepts

- **Environment Variables**: Store secrets outside code
- **`.env` file**: Contains `OPENAI_API_KEY=sk-...`
- **Security**: Never commit `.env` to version control

### Quick Reference

```python
# Standard usage
openai_api_key = setup_environment()

# Check if key exists
if openai_api_key:
    print("Ready to use OpenAI")
else:
    print("Need to set API key")
```

---

## Step 2: Analyze Knowledge Base Size

### What It Does

Finds all markdown files in the knowledge base and counts total characters and tokens.

### Code

```python
def analyze_knowledge_base_size(base_path: Path, model: str) -> tuple[int, int]:
    """
    Analyze the total size of the knowledge base in characters and tokens.
    
    Args:
        base_path: Path to the knowledge base directory
        model: Model name for token counting (e.g., "gpt-4.1-nano")
    
    Returns:
        tuple: (total_characters, total_tokens)
    """
    # Find all markdown files recursively
    knowledge_base_path = base_path / "knowledge-base" / "**" / "*.md"
    files = glob.glob(str(knowledge_base_path), recursive=True)
    
    # Read all files and concatenate
    entire_knowledge_base = ""
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            entire_knowledge_base += f.read()
            entire_knowledge_base += "\n\n"
    
    total_characters = len(entire_knowledge_base)
    
    # Count tokens using tiktoken
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(entire_knowledge_base)
    total_tokens = len(tokens)
    
    return total_characters, total_tokens
```

### Why Written This Way

- **`Path` objects**: Cross-platform path handling
- **`**` pattern**: Recursive search in all subdirectories
- **`glob.glob()`**: Finds all matching files
- **`tiktoken`**: OpenAI's tokenizer for accurate token counting

### Key Concepts

#### Characters vs Tokens

- **Characters**: Raw text length (what you see)
- **Tokens**: What the model actually processes
- **Conversion**: 1 token ≈ 4 characters (varies by language)

#### Why Count Tokens?

- LLMs have token limits (e.g., GPT-4: 8K-32K tokens)
- Helps decide if chunking is necessary
- Understands the scale of your RAG system

### What Happens

1. Finds all `.md` files recursively
2. Reads and concatenates all file contents
3. Counts total characters
4. Counts total tokens using `tiktoken`
5. Returns both counts

### Quick Reference

```python
# Analyze knowledge base
total_chars, total_tokens = analyze_knowledge_base_size(
    current_directory, 
    MODEL
)

# Check if chunking is needed
if total_tokens > 8000:
    print("Chunking recommended!")
```

---

## Step 3: Load Documents with Metadata

### What It Does

Loads files using LangChain's `DirectoryLoader`, converts them to Document objects, and adds metadata.

### Code

```python
def load_documents_with_metadata(base_path: Path) -> list:
    """
    Load documents from the knowledge base using LangChain's DirectoryLoader.
    
    Returns:
        list: List of LangChain Document objects with metadata
    """
    # Find all subdirectories
    folders_path = str(base_path / "knowledge-base") + "/*"
    folders = glob.glob(folders_path)
    
    documents = []
    
    # Process each folder separately
    for folder in folders:
        doc_type = os.path.basename(folder)  # Get folder name
        
        # Create loader
        loader = DirectoryLoader(
            folder,
            glob="**/*.md",  # Recursive pattern
            loader_cls=TextLoader,  # Use TextLoader for .md files
            loader_kwargs={'encoding': 'utf-8'}  # Ensure proper encoding
        )
        
        folder_docs = loader.load()  # Actually load the files
        
        # Add custom metadata
        for doc in folder_docs:
            doc.metadata["doc_type"] = doc_type
            documents.append(doc)
    
    return documents
```

### Key Questions Answered

#### When Should I Use DirectoryLoader?

**Use `DirectoryLoader` when:**
- Loading multiple files from a directory
- Files are in subdirectories (recursive search)
- Files are the same type (e.g., all `.md` or all `.pdf`)
- You want automatic file discovery

**Don't use it when:**
- Loading a single file → use specific loader directly
- Loading from URL → use `WebBaseLoader`
- Loading from database → use `SQLDatabaseLoader`

**Example alternatives:**
```python
# Single file
from langchain_community.document_loaders import TextLoader
loader = TextLoader("file.md")

# PDF file
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader("document.pdf")

# Web page
from langchain_community.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://example.com")
```

#### What Does `loader_cls` Mean?

`loader_cls` = **loader class**. It tells `DirectoryLoader` which loader to use for each file.

**Why needed:**
- `DirectoryLoader` finds files but doesn't know how to read them
- Different file types need different loaders:
  - `.md` → `TextLoader`
  - `.pdf` → `PyPDFLoader`
  - `.docx` → `Docx2txtLoader`

**Example:**
```python
# For markdown files
loader = DirectoryLoader(
    folder,
    glob="**/*.md",
    loader_cls=TextLoader  # "Use TextLoader for each .md file"
)

# For PDF files
loader = DirectoryLoader(
    folder,
    glob="**/*.pdf",
    loader_cls=PyPDFLoader  # "Use PyPDFLoader for each .pdf file"
)
```

#### What Does `loader_kwargs` Mean?

`loader_kwargs` = **keyword arguments** passed to the loader class.

**Why a dictionary:**
- Different loaders accept different parameters
- Flexible: pass any arguments the loader needs

**Example:**
```python
loader = DirectoryLoader(
    folder,
    glob="**/*.md",
    loader_cls=TextLoader,
    loader_kwargs={'encoding': 'utf-8'}  # Passed to TextLoader
)
```

#### Why Do We Need `.load()`?

**No, `.load()` triggers the actual loading.** This is **lazy loading**.

**What happens:**
```python
loader = DirectoryLoader(...)  # Just creates the loader object
# At this point, NO files have been read yet!

folder_docs = loader.load()  # NOW it actually reads all the files
```

**Why lazy loading:**
- Efficiency: Don't load until needed
- Flexibility: Configure loader before loading
- Error handling: Catch errors during `.load()`

**What `.load()` does:**
1. Finds all matching files (using `glob` pattern)
2. For each file, creates the loader (`TextLoader`, etc.)
3. Reads the file content
4. Converts to `Document` objects
5. Returns list of `Document` objects

#### Why "page_content"?

**Historical naming:** LangChain started with PDFs, where each page was a separate `Document`.

**How it works:**
- **One file → one Document** (for text files like `.md`)
- **One PDF page → one Document** (for PDFs)
- **One row → one Document** (for CSVs)

**Example with PDF:**
```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("document.pdf")
docs = loader.load()  # Returns MULTIPLE Document objects

# If PDF has 10 pages, you get 10 Document objects:
# docs[0] = Document(page_content="Page 1 text", metadata={'page': 0})
# docs[1] = Document(page_content="Page 2 text", metadata={'page': 1})
```

**For markdown files:**
- One `.md` file = one `Document`
- `page_content` contains the entire file's text
- The name is just convention (it's not really "pages")

#### What Metadata Can We Add?

**You can add ANY keys to `metadata`.** It's a dictionary!

**What's already there:**
```python
# Automatically added by DirectoryLoader:
doc.metadata = {
    'source': '/full/path/to/file.md',  # File path
}
```

**What you can add:**
```python
# Add document type
doc.metadata["doc_type"] = "products"

# Add author
doc.metadata["author"] = "John Doe"

# Add creation date
doc.metadata["created_date"] = "2024-01-15"

# Add category
doc.metadata["category"] = "technical"

# Add tags
doc.metadata["tags"] = ["important", "reference"]

# Add custom fields
doc.metadata["department"] = "Engineering"
doc.metadata["priority"] = "high"
doc.metadata["version"] = "2.0"
```

**Common metadata keys:**
- `source`: File path (usually auto-added)
- `doc_type`: Document category/type
- `author`: Document author
- `created_date` / `modified_date`: Timestamps
- `title`: Document title
- `tags`: List of tags
- `category`: Category classification
- `language`: Document language
- `page`: Page number (for PDFs)

**Why metadata matters:**
- **Filtering**: `vectorstore.similarity_search(..., filter={"doc_type": "products"})`
- **Organization**: Group and categorize documents
- **Tracking**: Know where chunks came from
- **Inheritance**: Chunks inherit parent document metadata

### LangChain Document Structure

A LangChain `Document` has:
- **`page_content`**: The actual text content
- **`metadata`**: Dictionary with file path, source, and custom fields

**Example:**
```python
Document(
    page_content="The actual text content here...",
    metadata={
        'source': '/path/to/file.md',
        'doc_type': 'products',
        'author': 'John Doe'
    }
)
```

### Quick Reference

```python
# Load documents
documents = load_documents_with_metadata(current_directory)

# Access document content
text = documents[0].page_content

# Access metadata
doc_type = documents[0].metadata['doc_type']
source = documents[0].metadata['source']

# Add custom metadata
documents[0].metadata["custom_key"] = "custom_value"
```

---

## Step 4: Chunk Documents

### What It Does

Splits large documents into smaller chunks using `RecursiveCharacterTextSplitter` with overlap to preserve context.

### Code

```python
def chunk_documents(documents: list, chunk_size: int = 1000, chunk_overlap: int = 200) -> list:
    """
    Split documents into smaller chunks using RecursiveCharacterTextSplitter.
    
    Args:
        documents: List of Document objects to chunk
        chunk_size: Maximum characters per chunk (default: 1000)
        chunk_overlap: Characters to overlap between chunks (default: 200)
    
    Returns:
        list: List of Document chunks (each chunk is a Document object with metadata)
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    chunks = text_splitter.split_documents(documents)
    
    return chunks
```

### Why Chunking?

**Problem:**
- Documents can be huge (thousands of tokens)
- LLMs have context limits (e.g., GPT-4: 8K-32K tokens)
- Can't send entire documents to LLM every time

**Solution:**
- Split documents into smaller pieces
- Retrieve only relevant chunks
- Send only those chunks to LLM

### How RecursiveCharacterTextSplitter Works

It tries to split text intelligently by attempting separators in order:

**Step 1: Try splitting on `\n\n` (double newline = paragraphs)**
```
Text: "Paragraph 1\n\nParagraph 2\n\nParagraph 3..."
↓
Try: Split at \n\n
Result: ["Paragraph 1", "Paragraph 2", "Paragraph 3..."]
```

**Step 2: If chunks still too large, try `\n` (single newline = sentences)**
```
Chunk: "Sentence 1\nSentence 2\nSentence 3..."
↓
Try: Split at \n
Result: ["Sentence 1", "Sentence 2", "Sentence 3..."]
```

**Step 3: If still too large, try ` ` (spaces = words)**
```
Chunk: "Word1 Word2 Word3 Word4..."
↓
Try: Split at spaces
Result: ["Word1 Word2", "Word3 Word4..."]
```

**Step 4: Last resort: Split on characters**
```
Chunk: "abcdefghijklmnop..."
↓
Split every 1000 characters
Result: ["abcdefghij...", "klmnopqrst..."]
```

**Why this order?**
- Preserves structure (paragraphs → sentences → words)
- Avoids breaking words when possible
- Falls back gracefully if needed

### Understanding `chunk_size`

**What it means:**
- `chunk_size=1000` = **maximum** characters per chunk
- **Not exact**: Chunks can be slightly smaller (if split at natural boundary)
- **Not guaranteed**: If single paragraph is 2000 chars, it may exceed limit

**How to choose:**

| Use Case | Recommended chunk_size | Why |
|----------|----------------------|-----|
| Code documentation | 500-800 | Code blocks need context |
| Long articles | 1000-1500 | Standard for most text |
| Technical docs | 800-1200 | Preserve code examples |
| Chat/conversation | 500-1000 | Preserve message context |
| Legal documents | 1500-2000 | Longer sentences |

**Rule of thumb:**
- 1 token ≈ 4 characters (English)
- `chunk_size=1000` ≈ 250 tokens
- GPT-4 context: 8K tokens = ~32K characters
- So 1000-char chunks fit comfortably

### Understanding `chunk_overlap`

**What it does:**
- Overlap = characters shared between adjacent chunks
- Prevents losing context at boundaries

**Visual example:**
```
Original text (2000 characters):
[========================================]
0                                    2000

Without overlap (chunk_size=1000):
[============][============]
0           1000          2000
            ↑
        Context lost here!

With overlap=200:
[============][====][============]
0           1000 1200          2000
            ↑    ↑
        Split    Overlap preserves context
```

**Why overlap matters:**

**Example 1: Mid-sentence split**
```
Chunk 1 ends: "...the company's revenue increased significantly"
Chunk 2 starts: "in Q4 2023, reaching $10 million..."

Without overlap: Context lost! "in Q4 2023" seems disconnected.
With overlap: Chunk 2 includes "...significantly in Q4 2023..."
```

**Example 2: Code example split**
```
Chunk 1 ends: "def calculate_total(items):"
Chunk 2 starts: "    return sum(items)"

Without overlap: Missing the function definition context!
With overlap: Chunk 2 includes "def calculate_total(items):\n    return..."
```

**How much overlap?**

| Overlap | Result |
|---------|--------|
| Too little (0-50) | Context loss |
| **Good (100-300)** | **Balances context and efficiency** |
| Too much (500+) | Redundant, wastes tokens |

**Recommendation:**
- `chunk_overlap = chunk_size * 0.1` to `chunk_size * 0.2`
- For `chunk_size=1000`: `overlap=100` to `200` (10-20%)

### What Happens to Metadata?

**Metadata is inherited:** Each chunk gets the parent document's metadata.

**Example:**
```python
# Original document
doc = Document(
    page_content="Long text here...",
    metadata={
        'source': '/path/to/file.md',
        'doc_type': 'products',
        'author': 'John Doe'
    }
)

# After chunking
chunks = text_splitter.split_documents([doc])

# Each chunk has the SAME metadata:
chunks[0].metadata = {
    'source': '/path/to/file.md',  # Same!
    'doc_type': 'products',         # Same!
    'author': 'John Doe'            # Same!
}
```

**Additional metadata you can add:**
```python
# After chunking, you can add chunk-specific metadata
for i, chunk in enumerate(chunks):
    chunk.metadata["chunk_index"] = i  # Which chunk number
    chunk.metadata["total_chunks"] = len(chunks)  # How many chunks total
    chunk.metadata["chunk_size"] = len(chunk.page_content)  # Size of this chunk
```

### Alternative Chunking Strategies

**1. CharacterTextSplitter**
- Simple: splits on characters only
- No intelligence, just cuts text
```python
from langchain_text_splitters import CharacterTextSplitter
splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
```

**2. TokenTextSplitter**
- Splits by tokens (not characters)
- More accurate for LLM context limits
```python
from langchain_text_splitters import TokenTextSplitter
splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=200)
```

**3. MarkdownHeaderTextSplitter**
- Splits markdown by headers
- Preserves header hierarchy
```python
from langchain_text_splitters import MarkdownHeaderTextSplitter
headers_to_split_on = [("#", "Header 1"), ("##", "Header 2")]
splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
```

**4. PythonCodeTextSplitter**
- For Python code
- Splits by functions/classes
```python
from langchain_text_splitters import PythonCodeTextSplitter
splitter = PythonCodeTextSplitter(chunk_size=1000)
```

**Why RecursiveCharacterTextSplitter?**
- Works for most text types
- Preserves structure intelligently
- Good default choice

### Common Chunking Mistakes

**Mistake 1: Chunks too large**
```python
# BAD: Too large
chunk_size=5000  # Won't fit in many LLM contexts!

# GOOD: Reasonable size
chunk_size=1000
```

**Mistake 2: No overlap**
```python
# BAD: No overlap
chunk_overlap=0  # Loses context at boundaries!

# GOOD: Some overlap
chunk_overlap=200
```

**Mistake 3: Overlap too large**
```python
# BAD: Too much overlap
chunk_size=1000
chunk_overlap=800  # 80% overlap = mostly redundant!

# GOOD: Reasonable overlap
chunk_size=1000
chunk_overlap=200  # 20% overlap
```

**Mistake 4: Wrong splitter for content**
```python
# BAD: Using CharacterTextSplitter for code
splitter = CharacterTextSplitter(...)  # Breaks code structure!

# GOOD: Use code-specific splitter
splitter = PythonCodeTextSplitter(...)
```

### Quick Reference

```python
# Standard chunking setup
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # ~250 tokens, fits most LLMs
    chunk_overlap=200     # 20% overlap, preserves context
)

chunks = text_splitter.split_documents(documents)
# Result: List of Document objects, each with inherited metadata
```

---

## Step 5: Create Embeddings & Vectorstore

### What It Does

Converts text chunks into numerical vectors (embeddings) and stores them in Chroma vector database.

### Code

```python
def create_vectorstore(chunks: list, embeddings, db_name: str, reset: bool = True):
    """
    Create a Chroma vector database from document chunks.
    
    Args:
        chunks: List of Document chunks to embed and store
        embeddings: Embedding model (HuggingFaceEmbeddings or OpenAIEmbeddings)
        db_name: Name/path of the vector database directory
        reset: If True, delete existing database before creating new one
    
    Returns:
        Chroma: The vectorstore object for querying
    """
    # Delete existing database if reset is True
    if reset and os.path.exists(db_name):
        Chroma(persist_directory=db_name, embedding_function=embeddings).delete_collection()
    
    # Create embeddings for all chunks and store in Chroma
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_name
    )
    
    return vectorstore
```

### Understanding Embeddings

**What are embeddings?**

Embeddings convert text into numerical vectors that capture meaning.

**Analogy:**
- **Text**: "The cat sat on the mat"
- **Embedding**: `[0.23, -0.45, 0.67, ..., 0.12]` (384 numbers)
- **Similar text → similar vectors** (close in vector space)

**Why embeddings?**
- Enables semantic search (meaning, not keywords)
- Allows mathematical operations (distance, similarity)
- Works with vector databases for fast retrieval

### HuggingFaceEmbeddings

**What it is:**
- LangChain wrapper around HuggingFace's sentence-transformers
- Runs locally (free, no API calls)
- Good for development and production

**How it works:**
```python
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
```

**What happens:**
1. Downloads the model (first time only)
2. Loads it into memory
3. Converts text → vectors when called

**The model: `all-MiniLM-L6-v2`**
- **384 dimensions**
- Fast and efficient
- Good quality for most use cases
- ~80MB download

**How to use it:**
```python
# Create the embedding model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Embed a single text
text = "Hello world"
vector = embeddings.embed_query(text)
# Returns: [0.23, -0.45, 0.67, ..., 0.12] (384 numbers)

# Embed multiple texts (batch)
texts = ["Hello", "World", "Python"]
vectors = embeddings.embed_documents(texts)
# Returns: [[...], [...], [...]] (list of 384-dim vectors)
```

### Other HuggingFace Models

| Model Name | Dimensions | Speed | Quality | Use Case |
|------------|------------|-------|---------|----------|
| `all-MiniLM-L6-v2` | 384 | ⚡⚡⚡ Fast | ⭐⭐⭐ Good | **Default choice** |
| `all-mpnet-base-v2` | 768 | ⚡⚡ Medium | ⭐⭐⭐⭐ Better | Higher quality needed |
| `all-MiniLM-L12-v2` | 384 | ⚡⚡ Medium | ⭐⭐⭐⭐ Better | Better than L6 |
| `paraphrase-multilingual-MiniLM-L12-v2` | 384 | ⚡⚡ Medium | ⭐⭐⭐⭐ | **Multilingual** |

**Example with different model:**
```python
# Higher quality (but slower)
embeddings = HuggingFaceEmbeddings(
    model_name="all-mpnet-base-v2"  # 768 dimensions, better quality
)

# Multilingual support
embeddings = HuggingFaceEmbeddings(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)
```

**Advanced configuration:**
```python
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={
        'device': 'cuda',  # Use GPU if available (faster)
        # 'device': 'cpu'   # Use CPU (default)
    },
    encode_kwargs={
        'normalize_embeddings': True,  # Normalize vectors (often improves results)
        'batch_size': 32  # Process multiple texts at once
    }
)
```

### Understanding Chroma (Vector Database)

**What is Chroma?**

Chroma is a vector database that stores:
- **Embeddings** (vectors)
- **Original text**
- **Metadata**

**Why use a vector database?**
- Fast similarity search
- Persistence (saves to disk)
- Metadata filtering
- Scalable to millions of vectors

**How it works:**
```
Chunk Text → Embedding Model → Vector → Chroma Storage
"The cat..." → [0.23, -0.45, ...] → Stored with metadata
```

**What gets stored:**
```python
# For each chunk, Chroma stores:
{
    'id': 'unique-id-123',
    'embedding': [0.23, -0.45, 0.67, ..., 0.12],  # 384 numbers
    'document': "The cat sat on the mat...",       # Original text
    'metadata': {                                  # Your metadata
        'source': '/path/to/file.md',
        'doc_type': 'products',
        'chunk_index': 0
    }
}
```

### The Embedding Process

**Visual example:**

**Input chunk:**
```python
chunk = Document(
    page_content="RAG systems combine retrieval with generation...",
    metadata={'source': 'rag.md', 'doc_type': 'tutorial'}
)
```

**Step 1: Extract text**
```python
text = chunk.page_content
# "RAG systems combine retrieval with generation..."
```

**Step 2: Convert to embedding**
```python
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector = embeddings.embed_documents([text])[0]
# Returns: [0.234, -0.456, 0.789, ..., 0.123] (384 numbers)
```

**Step 3: Store in Chroma**
```python
Chroma stores:
- Vector: [0.234, -0.456, 0.789, ..., 0.123]
- Text: "RAG systems combine retrieval with generation..."
- Metadata: {'source': 'rag.md', 'doc_type': 'tutorial'}
```

**Result:**
- Searchable by meaning
- Can find similar chunks
- Metadata available for filtering

### Understanding Dimensions

**What are dimensions?**
- Each embedding is a vector of numbers
- Dimensions = how many numbers in the vector
- More dimensions = more information (but slower)

**Example:**
```python
# all-MiniLM-L6-v2: 384 dimensions
vector = [0.23, -0.45, 0.67, ..., 0.12]  # 384 numbers

# all-mpnet-base-v2: 768 dimensions
vector = [0.23, -0.45, 0.67, ..., 0.12]  # 768 numbers (more detailed)
```

**Trade-offs:**

| Dimensions | Pros | Cons |
|------------|------|------|
| 384 (MiniLM) | Fast, efficient, good quality | Less detail than larger models |
| 768 (mpnet) | Better quality, more detail | Slower, more storage |
| 3072 (OpenAI) | Best quality | Requires API, costs money |

**For most use cases:** 384 dimensions is a good balance.

### Persistence: Saving to Disk

**Why persist?**
- Embeddings are expensive to create (time + compute)
- Save once, reuse many times
- Database survives script restarts

**How it works:**
```python
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="vector_db"  # Folder name
)
```

**What gets saved:**
```
vector_db/
├── chroma.sqlite3          # Database file
├── index/                  # Search index
└── ...                     # Other files
```

**Reloading later:**
```python
# Instead of recreating, just load from disk:
vectorstore = Chroma(
    persist_directory="vector_db",
    embedding_function=embeddings
)
# Now you can query immediately - no re-embedding needed!
```

**When to reset:**
```python
# Reset = True: Delete and recreate (use when documents changed)
vectorstore = create_vectorstore(..., reset=True)

# Reset = False: Reuse existing (use when nothing changed)
vectorstore = create_vectorstore(..., reset=False)
```

### Alternative: OpenAIEmbeddings

**When to use:**
- Need highest quality
- Don't mind API costs
- Want cloud-based (no local model)

**How it works:**
```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
# Requires: OPENAI_API_KEY in environment

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=db_name
)
```

**Comparison:**

| Feature | HuggingFace | OpenAI |
|---------|-------------|--------|
| Cost | Free | ~$0.13 per 1M tokens |
| Speed | Fast (local) | Slower (API calls) |
| Quality | Good | Excellent |
| Dimensions | 384-768 | 1536-3072 |
| Internet | Not needed | Required |
| Best for | Development, production | Production (if budget allows) |

### What Happens During `Chroma.from_documents()`

**Detailed process:**

1. **Initialize Chroma**
   - Creates database structure
   - Sets up embedding function

2. **Process each chunk:**
   ```python
   for chunk in chunks:
       # Get text
       text = chunk.page_content
       
       # Create embedding
       vector = embeddings.embed_documents([text])[0]
       
       # Store in Chroma
       chroma.add(
           embeddings=[vector],
           documents=[text],
           metadatas=[chunk.metadata]
       )
   ```

3. **Build index:**
   - Creates similarity search index
   - Enables fast retrieval

4. **Save to disk:**
   - Writes all data to `persist_directory`
   - Can be reloaded later

**Time estimate:**
- 100 chunks: ~5-10 seconds
- 1000 chunks: ~30-60 seconds
- 10000 chunks: ~5-10 minutes

### Common Issues and Solutions

**Issue 1: Model download slow**
```python
# First run downloads model (~80MB)
# Solution: Be patient, or download manually
```

**Issue 2: Out of memory**
```python
# Solution: Use smaller model or process in batches
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",  # Smaller model
    encode_kwargs={'batch_size': 16}  # Smaller batches
)
```

**Issue 3: Database locked**
```python
# Solution: Make sure only one process uses it, or use reset=True
```

**Issue 4: Embeddings inconsistent**
```python
# Solution: Use normalize_embeddings=True
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    encode_kwargs={'normalize_embeddings': True}
)
```

### Quick Reference

```python
# Standard setup
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="vector_db"
)

# Later: reload from disk
vectorstore = Chroma(
    persist_directory="vector_db",
    embedding_function=embeddings
)

# Query it
results = vectorstore.similarity_search("your query", k=5)
```

---

## Step 6: Extract Vectors for Analysis

### What It Does

Retrieves all vectors, documents, and metadata from Chroma for visualization and analysis.

### Code

```python
def extract_vectors_and_metadata(vectorstore) -> tuple[np.ndarray, list, list, list]:
    """
    Extract vectors, documents, and metadata from the vectorstore for analysis.
    
    Returns:
        tuple: (vectors_array, documents_list, metadatas_list, doc_types_list)
    """
    collection = vectorstore._collection
    count = collection.count()
    
    # Get a sample embedding to check dimensions
    sample_embedding = collection.get(limit=1, include=["embeddings"])["embeddings"][0]
    dimensions = len(sample_embedding)
    
    # Retrieve all embeddings, documents, and metadata
    result = collection.get(include=['embeddings', 'documents', 'metadatas'])
    
    # Convert to numpy array for easier manipulation
    vectors = np.array(result['embeddings'])
    documents = result['documents']
    metadatas = result['metadatas']
    
    # Extract document types from metadata for coloring visualization
    doc_types = [metadata['doc_type'] for metadata in metadatas]
    
    return vectors, documents, metadatas, doc_types
```

### Key Concepts

**What gets extracted:**
- **Vectors**: NumPy array of shape `[n_chunks, embedding_dim]`
- **Documents**: List of chunk texts
- **Metadatas**: List of metadata dictionaries
- **Doc types**: List of document type strings (for coloring)

**Why extract?**
- Analyze embedding dimensions
- Visualize vector relationships
- Understand chunk distribution
- Prepare for visualization

### Quick Reference

```python
# Extract all data
vectors, chunk_texts, metadatas, doc_types = extract_vectors_and_metadata(vectorstore)

# Check dimensions
print(f"Vectors shape: {vectors.shape}")  # (n_chunks, embedding_dim)
print(f"Number of chunks: {len(chunk_texts)}")
print(f"Embedding dimensions: {vectors.shape[1]}")
```

---

## Step 7: Visualize Embeddings

### What It Does

Reduces high-dimensional vectors (384D) to 2D using t-SNE and creates an interactive visualization.

### Code

```python
def visualize_embeddings(vectors: np.ndarray, documents: list, doc_types: list, 
                         color_map: dict = None):
    """
    Visualize high-dimensional embeddings in 2D using t-SNE.
    
    Args:
        vectors: numpy array of embeddings (n_chunks, embedding_dim)
        documents: List of chunk texts for hover tooltips
        doc_types: List of document type strings for coloring
        color_map: Optional dict mapping doc_type to color
    """
    # Default color mapping if not provided
    if color_map is None:
        unique_types = list(set(doc_types))
        default_colors = ['blue', 'green', 'red', 'orange', 'purple', 'cyan', 'magenta', 'yellow']
        color_map = {doc_type: default_colors[i % len(default_colors)] 
                     for i, doc_type in enumerate(unique_types)}
    
    # Map document types to colors
    colors = [color_map.get(doc_type, 'gray') for doc_type in doc_types]
    
    # Apply t-SNE dimensionality reduction
    tsne = TSNE(n_components=2, random_state=42)
    reduced_vectors = tsne.fit_transform(vectors)
    
    # Create interactive Plotly scatter plot
    fig = go.Figure(data=[go.Scatter(
        x=reduced_vectors[:, 0],
        y=reduced_vectors[:, 1],
        mode='markers',
        marker=dict(size=5, color=colors, opacity=0.8),
        text=[f"Type: {t}<br>Text: {d[:100]}..." for t, d in zip(doc_types, documents)],
        hoverinfo='text'
    )])
    
    fig.update_layout(
        title='2D Vector Embeddings Visualization (t-SNE)',
        xaxis_title='t-SNE Dimension 1',
        yaxis_title='t-SNE Dimension 2',
        width=1000,
        height=700
    )
    
    fig.show()
    return fig
```

### Understanding t-SNE

**What is t-SNE?**

- **t-Distributed Stochastic Neighbor Embedding**
- Reduces high-dimensional vectors (e.g., 384D) to 2D for visualization
- Preserves local structure: similar chunks appear close together
- Non-linear: captures complex relationships that PCA cannot

**Why visualize?**
- See if similar document types cluster together
- Identify outliers or unusual chunks
- Understand semantic structure of knowledge base
- Verify embeddings capture meaningful relationships

**How it works:**
1. Takes high-dimensional vectors (384D)
2. Reduces to 2D coordinates
3. Preserves local relationships (similar = close)
4. Creates scatter plot

### Quick Reference

```python
# Visualize embeddings
color_map = {
    'products': 'blue',
    'employees': 'green',
    'contracts': 'red',
    'company': 'orange'
}

visualize_embeddings(
    vectors=vectors,
    documents=chunk_texts,
    doc_types=doc_types,
    color_map=color_map
)
```

---

## Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    RAG PIPELINE FLOW                        │
└─────────────────────────────────────────────────────────────┘

1. SETUP ENVIRONMENT
   ├─ Load .env file
   ├─ Verify API keys
   └─ Return configuration
   
2. ANALYZE KNOWLEDGE BASE
   ├─ Find all .md files recursively
   ├─ Count total characters
   ├─ Count total tokens
   └─ Return size metrics
   
3. LOAD DOCUMENTS
   ├─ Use DirectoryLoader for each folder
   ├─ Convert files → Document objects
   ├─ Add metadata (doc_type, source, etc.)
   └─ Return list of Documents
   
4. CHUNK DOCUMENTS
   ├─ Use RecursiveCharacterTextSplitter
   ├─ Split on paragraphs → sentences → words → characters
   ├─ Apply chunk_size and chunk_overlap
   ├─ Preserve metadata in each chunk
   └─ Return list of chunk Documents
   
5. CREATE EMBEDDINGS & VECTORSTORE
   ├─ Initialize HuggingFaceEmbeddings
   ├─ Convert each chunk text → vector (384D)
   ├─ Store in Chroma: vector + text + metadata
   ├─ Build similarity search index
   ├─ Save to disk (persist_directory)
   └─ Return vectorstore object
   
6. EXTRACT VECTORS
   ├─ Retrieve all vectors from Chroma
   ├─ Extract documents and metadata
   ├─ Get doc_types for coloring
   └─ Return vectors, documents, metadatas, doc_types
   
7. VISUALIZE
   ├─ Apply t-SNE: 384D → 2D
   ├─ Create Plotly scatter plot
   ├─ Color by document type
   ├─ Add hover tooltips
   └─ Display interactive plot
```

---

## Quick Reference

### Complete Pipeline

```python
# 1. Setup
openai_api_key = setup_environment()

# 2. Analyze
total_chars, total_tokens = analyze_knowledge_base_size(current_directory, MODEL)

# 3. Load
documents = load_documents_with_metadata(current_directory)

# 4. Chunk
chunks = chunk_documents(documents, chunk_size=1000, chunk_overlap=200)

# 5. Embed & Store
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = create_vectorstore(chunks, embeddings, "vector_db", reset=True)

# 6. Extract
vectors, chunk_texts, metadatas, doc_types = extract_vectors_and_metadata(vectorstore)

# 7. Visualize
visualize_embeddings(vectors, chunk_texts, doc_types, color_map)
```

### Common Configurations

**Standard RAG Setup:**
```python
# Chunking
chunk_size = 1000
chunk_overlap = 200

# Embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Vectorstore
db_name = "vector_db"
reset = True  # Set False to reuse existing
```

**High-Quality Setup:**
```python
# Chunking
chunk_size = 1500
chunk_overlap = 300

# Embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")

# Vectorstore
db_name = "vector_db"
reset = True
```

**Production Setup:**
```python
# Chunking
chunk_size = 1000
chunk_overlap = 200

# Embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# Vectorstore
db_name = "vector_db"
reset = False  # Reuse existing
```

### Querying the Vectorstore

```python
# Basic similarity search
results = vectorstore.similarity_search("your query", k=5)

# With metadata filtering
results = vectorstore.similarity_search(
    "your query",
    k=5,
    filter={"doc_type": "products"}
)

# With score (similarity distance)
results = vectorstore.similarity_search_with_score("your query", k=5)
```

---

## Key Takeaways

1. **Documents**: LangChain's standard format (`page_content` + `metadata`)
2. **Chunking**: Split large documents into manageable pieces with overlap
3. **Embeddings**: Convert text to vectors that capture semantic meaning
4. **Vector Database**: Store embeddings for fast similarity search
5. **Visualization**: Understand relationships between chunks

### Best Practices

- **Chunk size**: 1000 characters (~250 tokens) is a good default
- **Chunk overlap**: 10-20% of chunk size preserves context
- **Embeddings**: HuggingFace for development, OpenAI for production
- **Persistence**: Save to disk, reload when possible
- **Metadata**: Add as much as needed for filtering and organization

---

## Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Chroma Documentation](https://docs.trychroma.com/)
- [HuggingFace Sentence Transformers](https://www.sbert.net/)
- [t-SNE Explanation](https://distill.pub/2016/misread-tsne/)

---

*This guide was created to help understand the RAG pipeline step-by-step. For questions or clarifications, refer to the script comments or LangChain documentation.*
