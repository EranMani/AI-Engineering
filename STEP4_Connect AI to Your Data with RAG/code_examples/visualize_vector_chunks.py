"""
Visualize Vector Chunks - Understanding LangChain Document Processing & RAG Pipeline

This script demonstrates the complete RAG (Retrieval-Augmented Generation) workflow:
1. Loading documents from a knowledge base
2. Chunking documents into smaller pieces
3. Creating embeddings (vector representations) for each chunk
4. Storing chunks and embeddings in a vector database (Chroma)
5. Visualizing embeddings in 2D space using t-SNE

KEY CONCEPTS:

DOCUMENT LOADING:
- LangChain's DirectoryLoader loads files and converts them to Document objects
- Each Document has page_content (text) and metadata (file info, custom fields)

CHUNKING:
- Breaking large documents into smaller pieces that fit within LLM context windows
- RecursiveCharacterTextSplitter splits on paragraphs, sentences, then characters
- chunk_size: Maximum characters per chunk
- chunk_overlap: Characters to overlap between chunks (preserves context at boundaries)
- WHY? LLMs have token limits; chunking allows retrieving only relevant pieces

EMBEDDINGS:
- Vector representations of text that capture semantic meaning
- Similar text → similar vectors (close in vector space)
- Enables semantic search (finding meaning, not just keywords)
- HuggingFaceEmbeddings: Free, local embeddings (all-MiniLM-L6-v2 = 384 dimensions)
- OpenAIEmbeddings: Paid, cloud-based (text-embedding-3-large = 3072 dimensions)

VECTOR DATABASE (Chroma):
- Stores chunks + their embeddings + metadata
- Enables fast similarity search (find chunks similar to a query)
- Persists to disk for reuse across sessions

VISUALIZATION (t-SNE):
- Reduces high-dimensional vectors (384D) to 2D for human visualization
- Preserves local structure: similar chunks appear close together
- Colors represent document types to see clustering patterns
"""

import os
import glob
import tiktoken
import numpy as np
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sklearn.manifold import TSNE
import plotly.graph_objects as go
from pathlib import Path


# ============================================================================
# CONFIGURATION
# ============================================================================

MODEL = "gpt-4.1-nano"
db_name = "vector_db"


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


def analyze_knowledge_base_size(base_path: Path, model: str) -> tuple[int, int]:
    """
    Analyze the total size of the knowledge base in characters and tokens.
    
    This helps understand:
    - How much content we're working with
    - Whether chunking is necessary (if tokens exceed model limits)
    - The scale of the RAG system
    
    Args:
        base_path: Path to the knowledge base directory
        model: Model name for token counting (e.g., "gpt-4.1-nano")
    
    Returns:
        tuple: (total_characters, total_tokens)
    """
    # Find all markdown files recursively in the knowledge base
    # The "**" pattern means "search in all subdirectories"
    knowledge_base_path = base_path / "knowledge-base" / "**" / "*.md"
    print(f"\n📁 Knowledge base path: {knowledge_base_path}")
    
    files = glob.glob(str(knowledge_base_path), recursive=True)
    print(f"✓ Found {len(files)} files in the knowledge base")
    
    # Read all files and concatenate their content
    # This gives us the total raw text size
    entire_knowledge_base = ""
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            entire_knowledge_base += f.read()
            entire_knowledge_base += "\n\n"  # Add spacing between documents
    
    total_characters = len(entire_knowledge_base)
    print(f"✓ Total characters in knowledge base: {total_characters:,}")
    
    # Count tokens using tiktoken (OpenAI's tokenizer)
    # Tokens are what the model actually processes, not characters
    # 1 token ≈ 4 characters for English text, but varies
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(entire_knowledge_base)
    total_tokens = len(tokens)
    print(f"✓ Total tokens for {model}: {total_tokens:,}")
    
    return total_characters, total_tokens


def load_documents_with_metadata(base_path: Path) -> list:
    """
    Load documents from the knowledge base using LangChain's DirectoryLoader.
    
    WHY USE DirectoryLoader?
    - Automatically handles file reading and encoding
    - Converts files to LangChain Document objects (standard format)
    - Supports recursive directory traversal
    - Handles errors gracefully
    
    WHY ADD METADATA?
    - Metadata helps filter and organize chunks later
    - doc_type allows filtering by document category
    - Other useful metadata: source file, creation date, author, etc.
    - Metadata is preserved when chunks are created (each chunk inherits parent doc metadata)
    
    Args:
        base_path: Path to the project root directory
    
    Returns:
        list: List of LangChain Document objects with metadata
    """
    # Find all subdirectories in the knowledge-base folder
    # Each subdirectory represents a document type/category
    folders_path = str(base_path / "knowledge-base") + "/*"
    print(f"\n📂 Folders path: {folders_path}")
    
    folders = glob.glob(folders_path)
    print(f"✓ Found {len(folders)} document folders: {folders}")
    
    documents = []
    
    # Process each folder separately to add category metadata
    for folder in folders:
        print(f"\n📄 Loading documents from folder: {folder}")
        
        # Extract folder name as document type (e.g., "tutorials", "docs", etc.)
        doc_type = os.path.basename(folder)
        
        # DirectoryLoader automatically:
        # - Finds all matching files (**.md = recursive search)
        # - Reads each file using TextLoader
        # - Converts to Document objects with page_content and metadata
        loader = DirectoryLoader(
            folder,
            glob="**/*.md",  # Recursive pattern: find .md files in all subdirectories
            loader_cls=TextLoader,  # Use TextLoader for .md files
            loader_kwargs={'encoding': 'utf-8'}  # Ensure proper encoding
        )
        
        folder_docs = loader.load()
        print(f"  ✓ Loaded {len(folder_docs)} documents from {doc_type}")
        
        # Add custom metadata to each document
        # This metadata will be preserved when we chunk the documents later
        for doc in folder_docs:
            doc.metadata["doc_type"] = doc_type
            documents.append(doc)
    
    print(f"\n✓ Total documents loaded: {len(documents)}")
    return documents


def display_document_structure(documents: list, sample_index: int = 1):
    """
    Display the structure of a sample document to understand LangChain's Document format.
    
    A LangChain Document has:
    - page_content: The actual text content
    - metadata: Dictionary with file path, source, and custom fields
    
    Args:
        documents: List of Document objects
        sample_index: Index of document to display
    """
    if len(documents) > sample_index:
        print(f"\n📋 Sample Document Structure (index {sample_index}):")
        print("=" * 60)
        print(documents[sample_index])
        print("=" * 60)
        print("\nDocument components:")
        print(f"  - page_content length: {len(documents[sample_index].page_content)} chars")
        print(f"  - metadata keys: {list(documents[sample_index].metadata.keys())}")
        print(f"  - metadata values: {documents[sample_index].metadata}")


def chunk_documents(documents: list, chunk_size: int = 1000, chunk_overlap: int = 200) -> list:
    """
    Split documents into smaller chunks using RecursiveCharacterTextSplitter.
    
    HOW IT WORKS:
    RecursiveCharacterTextSplitter tries to split text intelligently:
    1. First tries to split on double newlines (paragraphs)
    2. Then tries single newlines (sentences)
    3. Then tries spaces (words)
    4. Finally splits on characters (last resort)
    
    WHY CHUNK OVERLAP?
    - Prevents losing context at chunk boundaries
    - Example: If chunk ends mid-sentence, overlap ensures next chunk includes that sentence
    - 200 characters overlap = ~50 words, enough to preserve context
    
    Args:
        documents: List of Document objects to chunk
        chunk_size: Maximum characters per chunk (default: 1000)
        chunk_overlap: Characters to overlap between chunks (default: 200)
    
    Returns:
        list: List of Document chunks (each chunk is a Document object with metadata)
    """
    print(f"\n✂️  Chunking {len(documents)} documents...")
    print(f"   Chunk size: {chunk_size} characters")
    print(f"   Chunk overlap: {chunk_overlap} characters")
    
    # Create the text splitter with specified parameters
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    # Split all documents into chunks
    # Each chunk is still a Document object with:
    # - page_content: The chunk text
    # - metadata: Inherited from parent document (source, doc_type, etc.)
    chunks = text_splitter.split_documents(documents)
    
    print(f"✓ Created {len(chunks)} chunks from {len(documents)} documents")
    print(f"  Average chunks per document: {len(chunks) / len(documents):.1f}")
    
    # Show a sample chunk
    if len(chunks) > 0:
        print(f"\n📄 Sample chunk (first chunk):")
        print("-" * 60)
        print(chunks[0])
        print("-" * 60)
    
    return chunks


def create_vectorstore(chunks: list, embeddings, db_name: str, reset: bool = True):
    """
    Create a Chroma vector database from document chunks.
    
    WHAT IS A VECTORSTORE?
    - Stores chunks + their embeddings + metadata together
    - Enables semantic search: find chunks similar to a query
    - Persists to disk so you don't need to recreate embeddings every time
    
    EMBEDDING MODELS:
    - HuggingFaceEmbeddings: Free, runs locally, good for development
      * all-MiniLM-L6-v2: 384 dimensions, fast, good quality
    - OpenAIEmbeddings: Paid, cloud-based, higher quality
      * text-embedding-3-large: 3072 dimensions, best quality
    
    Args:
        chunks: List of Document chunks to embed and store
        embeddings: Embedding model (HuggingFaceEmbeddings or OpenAIEmbeddings)
        db_name: Name/path of the vector database directory
        reset: If True, delete existing database before creating new one
    
    Returns:
        Chroma: The vectorstore object for querying
    """
    print(f"\n🔢 Creating embeddings and vectorstore...")
    
    # Delete existing database if reset is True
    if reset and os.path.exists(db_name):
        print(f"   Deleting existing database: {db_name}")
        Chroma(persist_directory=db_name, embedding_function=embeddings).delete_collection()
    
    # Create embeddings for all chunks and store in Chroma
    # This process:
    # 1. Converts each chunk's text to an embedding vector
    # 2. Stores the vector + chunk text + metadata in Chroma
    # 3. Creates an index for fast similarity search
    # 4. Saves everything to disk (persist_directory)
    print(f"   Embedding {len(chunks)} chunks...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_name
    )
    
    # Verify the vectorstore was created successfully
    count = vectorstore._collection.count()
    print(f"✓ Vectorstore created with {count:,} chunks")
    
    return vectorstore


def extract_vectors_and_metadata(vectorstore) -> tuple[np.ndarray, list, list, list]:
    """
    Extract vectors, documents, and metadata from the vectorstore for analysis.
    
    This function retrieves all stored data so we can:
    - Analyze embedding dimensions
    - Visualize vector relationships
    - Understand how chunks are distributed
    
    Args:
        vectorstore: Chroma vectorstore object
    
    Returns:
        tuple: (vectors_array, documents_list, metadatas_list, doc_types_list)
            - vectors_array: numpy array of shape (n_chunks, embedding_dim)
            - documents_list: List of chunk texts
            - metadatas_list: List of metadata dictionaries
            - doc_types_list: List of document type strings
    """
    print(f"\n📊 Extracting vectors and metadata from vectorstore...")
    
    collection = vectorstore._collection
    count = collection.count()
    
    # Get a sample embedding to check dimensions
    sample_embedding = collection.get(limit=1, include=["embeddings"])["embeddings"][0]
    dimensions = len(sample_embedding)
    print(f"✓ Found {count:,} vectors with {dimensions:,} dimensions")
    
    # Retrieve all embeddings, documents, and metadata
    result = collection.get(include=['embeddings', 'documents', 'metadatas'])
    
    # Convert to numpy array for easier manipulation
    vectors = np.array(result['embeddings'])
    documents = result['documents']
    metadatas = result['metadatas']
    
    # Extract document types from metadata for coloring visualization
    doc_types = [metadata['doc_type'] for metadata in metadatas]
    
    print(f"✓ Extracted {len(vectors)} vectors, {len(documents)} documents, {len(metadatas)} metadata entries")
    
    return vectors, documents, metadatas, doc_types


def visualize_embeddings(vectors: np.ndarray, documents: list, doc_types: list, 
                         color_map: dict = None):
    """
    Visualize high-dimensional embeddings in 2D using t-SNE.
    
    WHAT IS t-SNE?
    - t-Distributed Stochastic Neighbor Embedding
    - Reduces high-dimensional vectors (e.g., 384D) to 2D for visualization
    - Preserves local structure: similar chunks appear close together
    - Non-linear: captures complex relationships that PCA cannot
    
    WHY VISUALIZE?
    - See if similar document types cluster together
    - Identify outliers or unusual chunks
    - Understand the semantic structure of your knowledge base
    - Verify that embeddings capture meaningful relationships
    
    Args:
        vectors: numpy array of embeddings (n_chunks, embedding_dim)
        documents: List of chunk texts for hover tooltips
        doc_types: List of document type strings for coloring
        color_map: Optional dict mapping doc_type to color (default: auto-assigns colors)
    """
    print(f"\n🎨 Creating 2D visualization using t-SNE...")
    print(f"   Reducing {vectors.shape[1]}D vectors to 2D...")
    
    # Default color mapping if not provided
    if color_map is None:
        unique_types = list(set(doc_types))
        default_colors = ['blue', 'green', 'red', 'orange', 'purple', 'cyan', 'magenta', 'yellow']
        color_map = {doc_type: default_colors[i % len(default_colors)] 
                     for i, doc_type in enumerate(unique_types)}
    
    # Map document types to colors
    colors = [color_map.get(doc_type, 'gray') for doc_type in doc_types]
    
    # Apply t-SNE dimensionality reduction
    # n_components=2: Reduce to 2D for plotting
    # random_state=42: Reproducible results
    tsne = TSNE(n_components=2, random_state=42)
    reduced_vectors = tsne.fit_transform(vectors)
    
    print(f"✓ Reduced to 2D coordinates")
    
    # Create interactive Plotly scatter plot
    # Each point represents one chunk
    # Color = document type
    # Hover = shows document type and first 100 chars of text
    fig = go.Figure(data=[go.Scatter(
        x=reduced_vectors[:, 0],
        y=reduced_vectors[:, 1],
        mode='markers',
        marker=dict(
            size=5,
            color=colors,
            opacity=0.8
        ),
        text=[f"Type: {t}<br>Text: {d[:100]}..." for t, d in zip(doc_types, documents)],
        hoverinfo='text'
    )])
    
    # Configure plot layout
    fig.update_layout(
        title='2D Vector Embeddings Visualization (t-SNE)',
        xaxis_title='t-SNE Dimension 1',
        yaxis_title='t-SNE Dimension 2',
        width=1000,
        height=700,
        margin=dict(r=20, b=10, l=10, t=40)
    )
    
    print(f"✓ Visualization ready! Opening in browser...")
    fig.show()
    
    return fig


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main execution flow for the complete RAG pipeline:
    
    1. Setup environment and verify configuration
    2. Analyze knowledge base size (characters and tokens)
    3. Load documents with metadata using LangChain loaders
    4. Chunk documents into smaller pieces
    5. Create embeddings and store in vector database
    6. Extract vectors for analysis
    7. Visualize embeddings in 2D space
    """
    # Get the project root directory (parent of code_examples folder)
    current_directory = Path(__file__).parent.parent
    
    print("=" * 70)
    print("🔍 VECTOR CHUNKS VISUALIZATION - Complete RAG Pipeline")
    print("=" * 70)
    print(f"\n📁 Current Working Directory: {current_directory}")
    
    # ========================================================================
    # STEP 1: Setup and Configuration
    # ========================================================================
    print("\n" + "=" * 70)
    print("STEP 1: Environment Setup")
    print("=" * 70)
    openai_api_key = setup_environment()
    
    # ========================================================================
    # STEP 2: Analyze Knowledge Base
    # ========================================================================
    print("\n" + "=" * 70)
    print("STEP 2: Knowledge Base Analysis")
    print("=" * 70)
    total_chars, total_tokens = analyze_knowledge_base_size(current_directory, MODEL)
    
    # ========================================================================
    # STEP 3: Load Documents
    # ========================================================================
    print("\n" + "=" * 70)
    print("STEP 3: Document Loading")
    print("=" * 70)
    documents = load_documents_with_metadata(current_directory)
    display_document_structure(documents)
    
    # ========================================================================
    # STEP 4: Chunk Documents
    # ========================================================================
    print("\n" + "=" * 70)
    print("STEP 4: Document Chunking")
    print("=" * 70)
    chunks = chunk_documents(
        documents,
        chunk_size=1000,      # Maximum characters per chunk
        chunk_overlap=200     # Characters to overlap between chunks
    )
    
    # ========================================================================
    # STEP 5: Create Embeddings and Vectorstore
    # ========================================================================
    print("\n" + "=" * 70)
    print("STEP 5: Creating Embeddings & Vector Database")
    print("=" * 70)
    
    # Choose embedding model:
    # Option 1: HuggingFace (free, local, good for development)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Option 2: OpenAI (paid, cloud-based, higher quality)
    # embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    
    vectorstore = create_vectorstore(
        chunks=chunks,
        embeddings=embeddings,
        db_name=db_name,
        reset=True  # Set to False to reuse existing database
    )
    
    # ========================================================================
    # STEP 6: Extract Vectors for Analysis
    # ========================================================================
    print("\n" + "=" * 70)
    print("STEP 6: Extracting Vectors & Metadata")
    print("=" * 70)
    vectors, chunk_texts, metadatas, doc_types = extract_vectors_and_metadata(vectorstore)
    
    # ========================================================================
    # STEP 7: Visualize Embeddings
    # ========================================================================
    print("\n" + "=" * 70)
    print("STEP 7: Visualization")
    print("=" * 70)
    
    # Define color mapping for document types
    # Adjust these colors based on your document types
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
    
    # ========================================================================
    # Summary
    # ========================================================================
    print("\n" + "=" * 70)
    print("✅ RAG Pipeline Complete!")
    print("=" * 70)
    print(f"\n📊 Summary:")
    print(f"   - Documents loaded: {len(documents)}")
    print(f"   - Chunks created: {len(chunks)}")
    print(f"   - Vectors stored: {len(vectors)}")
    print(f"   - Embedding dimensions: {vectors.shape[1]}")
    print(f"   - Vector database: {db_name}/")
    print(f"\n💡 Next steps:")
    print(f"   - Query the vectorstore: vectorstore.similarity_search('your query')")
    print(f"   - Use in RAG: Retrieve relevant chunks → Add to LLM prompt → Generate answer")


if __name__ == "__main__":
    main()