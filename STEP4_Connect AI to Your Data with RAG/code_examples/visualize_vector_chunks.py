"""
Visualize Vector Chunks - Understanding LangChain Document Processing

This script demonstrates the complete workflow for processing documents in a RAG (Retrieval-Augmented Generation) system:
1. Loading documents from a knowledge base
2. Understanding document structure and token counts
3. Preparing documents for chunking and vectorization

KEY CONCEPTS:
- Document Loading: LangChain's DirectoryLoader loads files and converts them to Document objects
- Chunking: Breaking large documents into smaller pieces that fit within LLM context windows
- Metadata: Adding context to chunks (like document type) helps with retrieval and filtering
- Vectorization: Converting text chunks to embeddings for semantic search (not shown here, but prepared for)

WHY CHUNKING?
- LLMs have token limits (e.g., GPT-4 has ~8K-32K tokens)
- Large documents won't fit in a single prompt
- Chunking allows us to retrieve only relevant pieces of information
- Smaller chunks improve search precision and reduce costs
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


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main execution flow:
    1. Setup environment and verify configuration
    2. Analyze knowledge base size (characters and tokens)
    3. Load documents with metadata using LangChain loaders
    4. Display document structure for understanding
    """
    # Get the project root directory (parent of code_examples folder)
    current_directory = Path(__file__).parent.parent
    print("=" * 60)
    print("🔍 VECTOR CHUNKS VISUALIZATION")
    print("=" * 60)
    print(f"\n📁 Current Working Directory: {current_directory}")
    
    # Step 1: Setup and verify environment
    openai_api_key = setup_environment()
    
    # Step 2: Analyze the size of our knowledge base
    # This helps us understand if chunking is necessary
    total_chars, total_tokens = analyze_knowledge_base_size(current_directory, MODEL)
    
    # Step 3: Load documents using LangChain's DirectoryLoader
    # This converts files to Document objects with metadata
    documents = load_documents_with_metadata(current_directory)
    
    # Step 4: Show what a Document object looks like
    display_document_structure(documents)

    # Divide into chunks using the RecursiveCharacterTextSplitter

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)

    print(f"Divided into {len(chunks)} chunks")
    print(f"First chunk:\n\n{chunks[0]}")

    # Pick an embedding model
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    #embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    if os.path.exists(db_name):
        Chroma(persist_directory=db_name, embedding_function=embeddings).delete_collection()

    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=db_name)
    print(f"Vectorstore created with {vectorstore._collection.count()} documents")

    # Let's investigate the vectors

    collection = vectorstore._collection
    count = collection.count()

    sample_embedding = collection.get(limit=1, include=["embeddings"])["embeddings"][0]
    dimensions = len(sample_embedding)
    print(f"There are {count:,} vectors with {dimensions:,} dimensions in the vector store")

    result = collection.get(include=['embeddings', 'documents', 'metadatas'])
    vectors = np.array(result['embeddings'])
    documents = result['documents']
    metadatas = result['metadatas']
    doc_types = [metadata['doc_type'] for metadata in metadatas]
    colors = [['blue', 'green', 'red', 'orange'][['products', 'employees', 'contracts', 'company'].index(t)] for t in doc_types]

    # We humans find it easier to visalize things in 2D!
    # Reduce the dimensionality of the vectors to 2D using t-SNE
    # (t-distributed stochastic neighbor embedding)

    tsne = TSNE(n_components=2, random_state=42)
    reduced_vectors = tsne.fit_transform(vectors)

    # Create the 2D scatter plot
    fig = go.Figure(data=[go.Scatter(
        x=reduced_vectors[:, 0],
        y=reduced_vectors[:, 1],
        mode='markers',
        marker=dict(size=5, color=colors, opacity=0.8),
        text=[f"Type: {t}<br>Text: {d[:100]}..." for t, d in zip(doc_types, documents)],
        hoverinfo='text'
    )])

    fig.update_layout(title='2D Chroma Vector Store Visualization',
        scene=dict(xaxis_title='x',yaxis_title='y'),
        width=800,
        height=600,
        margin=dict(r=20, b=10, l=10, t=40)
    )

    fig.show()
    
    # print("\n" + "=" * 60)
    # print("✅ Document loading complete!")
    # print("=" * 60)
    # print("\nNext steps would be:")
    # print("  1. Use RecursiveCharacterTextSplitter to chunk documents")
    # print("  2. Create embeddings for each chunk")
    # print("  3. Store chunks and embeddings in a vector database")
    # print("  4. Visualize chunk relationships and embeddings")


if __name__ == "__main__":
    main()