!python text_sanitizer.py input.txt --target output.json
import argparse
import string
import json

class TextSanitizer:
    def __init__(self, source: str, target: str = None):
        self.source = source
        self.target = target
        self.text = ""
        self.sanitized_text = ""
        self.statistics = {}

    def read_input(self):
        """Read input text from a file."""
        if not self.source:
            print("Error: No source file provided.")
            exit(1)
        try:
            with open(self.source, 'r', encoding='utf-8') as file:
                self.text = file.read()
        except FileNotFoundError:
            print(f"Error: File '{self.source}' not found.")
            exit(1)

    def sanitize(self):
        """Sanitize the input text (convert to lowercase, replace tabs)."""
        self.sanitized_text = self.text.lower().replace('\t', '____')

    def generate_statistics(self):
        """Count occurrences of each alphabet."""
        self.statistics = {char: self.sanitized_text.count(char) for char in string.ascii_lowercase}

    def output_result(self):
        """Print sanitized text and statistics or write to a file if target is specified."""
        output_data = {
            "sanitized_text": self.sanitized_text,
            "statistics": self.statistics
        }

        if self.target:
            with open(self.target, 'w', encoding='utf-8') as file:
                json.dump(output_data, file, indent=4)
            print(f"Output written to '{self.target}'")
        else:
            print("\nSanitized Text:")
            print(self.sanitized_text)
            print("\nCharacter Frequency:")
            for char, count in self.statistics.items():
                print(f"{char}: {count}")

    def process(self):
        """Run the full text sanitization process."""
        self.read_input()
        self.sanitize()
        self.generate_statistics()
        self.output_result()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Text Sanitizer Application")
    parser.add_argument("source", nargs="?", help="Path to the source text file", default=None)
    parser.add_argument("--target", help="Path to the target output file (optional)", default=None)
    
    args, _ = parser.parse_known_args()
    sanitizer = TextSanitizer(args.source, args.target)
    sanitizer.process()
