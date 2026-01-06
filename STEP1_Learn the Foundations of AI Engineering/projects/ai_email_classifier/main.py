import argparse
from src.classifier import classify_priority, classify_category, extract_email_info
from src.utils import read_email_file, validate_email_content
from src.config import setup_logger

def main():
    setup_logger(__name__)

    parser = argparse.ArgumentParser(description="AI Email Classifier CLI")
    subprasers = parser.add_subparsers(dest="command", help="Available commands")

    classify_parser = subprasers.add_parser("classify", help="Classify an email")
    classify_parser.add_argument("--file", type=str, help="Path to the email file")
    classify_parser.add_argument("--text", type=str, help="Email content as text")
    classify_parser.add_argument("--type", choices=["priority", "category", "info"], default="priority", help="Classifiction type (default: priority)")

    args = parser.parse_args()

    if not args.command:
        parser.error("Please provide a command. Use 'classify' to classify an email.")

    if args.command == "classify":
        # get email content from file or direct input
        if args.file:
            email_content = read_email_file(args.file)
        elif args.text:
            email_content = args.text
        else:
            parser.error("Either --file or --text must be provided!")

        validate_email_content(email_content)

        # Run classifiction based on type
        if args.type == "priority":
            result = classify_priority(email_content)
            print(f"Priority: {result.priority} (Confidence: {result.confidence:.2f})")
        elif args.type == "category":
            result = classify_category(email_content)
            print(f"Category: {result.category} (Confidence: {result.confidence:.2f})")
        elif args.type == "info":
            result = extract_email_info(email_content)
            print(f"Sender Intent: {result.sender_intent}")
            print(f"Action Required: {result.action_required}")
            print(f"Urgency Indicators: {', '.join(result.urgency_indicators) if result.urgency_indicators else 'None'}")
            print(f"Key Phrases: {', '.join(result.key_phrases) if result.key_phrases else 'None'}")

if __name__ == "__main__":
    main()
