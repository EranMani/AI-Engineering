import argparse
from src.analyzer import analyze_sentiment, analyze_summary, analyze_topics
from src.utils import read_text_file, validate_text
from src.config import setup_logger

def main():
    setup_logger(__name__)

    parser = argparse.ArgumentParser(description="AI Text Analyzer CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")  # Fixed: subparsers not subparses

    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze text")
    analyze_parser.add_argument("--file", type=str, help="Path to the text file")
    analyze_parser.add_argument("--text", type=str, help="Text to analyze")
    analyze_parser.add_argument("--type", choices=["sentiment", "summary", "topics"],
                                default="sentiment", help="Analysis type")  # Fixed: lowercase "sentiment"

    args = parser.parse_args()

    if not args.command:
        parser.error("Please provide a command. Use 'analyze' to analyze text.")

    if args.command == "analyze":
        # Get text from file or direct input
        if args.file:
            text = read_text_file(args.file)
        elif args.text:
            text = args.text
        else:
            parser.error("Either --file or --text must be provided!")

        validate_text(text)

        # Run analysis based on type
        if args.type == "sentiment":
            result = analyze_sentiment(text)
            print(f"Sentiment: {result.sentiment} (Score: {result.score})")
        elif args.type == "summary":
            result = analyze_summary(text)
            print(f"Summary: {result.summary}")
            print(f"Key points: {', '.join(result.key_points)}")
        elif args.type == "topics":
            result = analyze_topics(text)
            print(f"Topics: {', '.join(result.topics)}")
            print(f"Primary topic: {result.primary_topic}")

if __name__ == "__main__":
    main()