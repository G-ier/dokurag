import argparse
import sys
import os
import subprocess
import unittest
from pathlib import Path

# app imports
from core.chain import DokuragChain
from db.db import DokuragDB

# Prompt the LLM with the given text.
def prompt_llm(text: str) -> str:

    chain = DokuragChain()
    return chain.simple_invoke(text)

# Prompt the LLM with text and (future) relevant documents from the database.
def prompt_with_db_documents(text: str) -> str:

    chain = DokuragChain()
    # DB retrieval not wired yet; call invoke with no docs which uses the RAG template
    return chain.invoke(question=text, documents=None)

"""
Prompt the LLM with a question and user-provided docs.

The context provided to the chain contains only two fields: `question` and `docs`.
"""
def prompt_with_upload_documents(text: str, documents: list[str]) -> str:

    chain = DokuragChain()
    return chain.invoke(question=text, documents=documents)

# Store documents in the data folder in the database.
def store_documents() -> str:

    db = DokuragDB("/Users/gier/projects/dokurag/data/")
    try: 
        db.load_documents(uploaded_documents=None)
        return "Chunks stored in the database"
    except Exception as e:
        return f"Error storing documents: {e}"
    
def check_db() -> str:
    db = DokuragDB()
    try:
        count = len(db.db.get()['ids'])
        return f"Chunks stored in the database: {count}"
    except Exception as e:
        return f"Error checking documents: {e}"
    
def delete_db_entries() -> str:
    db = DokuragDB()
    try:
        db.db.delete()
        return "All entries deleted from the database"
    except Exception as e:
        return f"Error deleting entries: {e}"

"""
Run a specific test.

Args:
    testname: Name of the test to run
    
Returns:
    Test result
"""
def test_specific(testname: str) -> str:

    if testname.lower() == "openrouter":
        try:
            print("Running OpenRouter unit test via unittest loader...")
            suite = unittest.defaultTestLoader.loadTestsFromName(
                "tests.openrouter_test.TestOpenRouter.test_get_response_integration"
            )
            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)

            if result.wasSuccessful():
                return "openrouter unit test PASSED"
            if result.skipped:
                return "openrouter unit test SKIPPED"
            return "openrouter unit test FAILED"
        except Exception as import_run_error:
            return f"openrouter test FAILED to execute: {import_run_error}"
    elif testname.lower() == "simple_chain":
        try:
            print("Running simple_chain unit test via unittest loader...")
            suite = unittest.defaultTestLoader.loadTestsFromName(
                "tests.test_chain.TestDokuragChain.test_simple_chain"
            )
            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)

            if result.wasSuccessful():
                return "simple_chain unit test PASSED"
            if result.skipped:
                return "simple_chain unit test SKIPPED"
            return "simple_chain unit test FAILED"
        except Exception as import_run_error:
            return f"simple_chain test FAILED to execute: {import_run_error}"
    elif testname.lower() == "rag_chain":
        try:
            # Prefer running the unit test directly via unittest import
            print("Running rag_chain unit test via unittest loader...")

            # The unit test is decorated with @unittest.skip in tests/test_chain.py; this will report as skipped
            suite = unittest.defaultTestLoader.loadTestsFromName(
                "tests.test_chain.TestDokuragChain.test_rag_chain"
            )
            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)

            if result.wasSuccessful():
                return "rag_chain unit test PASSED"
            if result.skipped:
                return "rag_chain unit test SKIPPED"
            return "rag_chain unit test FAILED"
        except Exception as import_run_error:
            return f"rag_chain test FAILED to execute: {import_run_error}"
    elif testname.lower() == "rag_chain_quality":
        try:
            print("Running rag_chain_quality unit test via unittest loader...")
            suite = unittest.defaultTestLoader.loadTestsFromName(
                "tests.test_chain.TestDokuragChain.test_rag_chain_quality"
            )
            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)

            if result.wasSuccessful():
                return "rag_chain_quality unit test PASSED"
            if result.skipped:
                return "rag_chain_quality unit test SKIPPED"
            return "rag_chain_quality unit test FAILED"
        except Exception as import_run_error:
            return f"rag_chain_quality test FAILED to execute: {import_run_error}"
    else:
        return f"Unknown test: '{testname}'. Available tests: openrouter, simple_chain, rag_chain, rag_chain_quality"

"""
Run all tests.

Args:
    None
    
Returns:
    Test results
"""
def test_all() -> str:

    print("Running all tests...")
    
    # List of all available tests
    tests = ["openrouter", "simple_chain", "rag_chain"]
    results = []
    
    for test in tests:
        print(f"\n--- Running {test} test ---")
        result = test_specific(test)
        results.append(f"{test}: {result}")
    
    print("\n--- Test Summary ---")
    for result in results:
        print(result)
    
    passed_count = sum(1 for result in results if "PASSED" in result)
    total_count = len(results)
    
    if passed_count == total_count:
        return f"All tests passed ({passed_count}/{total_count})"
    else:
        return f"Some tests failed ({passed_count}/{total_count} passed)"


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="dokurag",
        description="Document RAG (Retrieval-Augmented Generation) CLI tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -p "What is machine learning?"     # Prompt LLM
  %(prog)s -pd "Explain this concept"         # Prompt with retrieval form docs from db
  %(prog)s -pdm "your question" file1.pdf file2.pdf  # Prompt with docs you provide
  %(prog)s -s                                 # Store all documents from the data folder in the database
  %(prog)s -c                                 # Check how many documents are stored in the database
  %(prog)s -t  testname                       # Run specific test
  %(prog)s -ta                                # Run all tests
  %(prog)s -h                                 # Show help
        """
    )
    
    # Create mutually exclusive group for the main operations
    group = parser.add_mutually_exclusive_group(required=True)
    
    group.add_argument(
        "-p", "--prompt",
        type=str,
        metavar="QUESTION",
        help="Prompt the LLM with the given text"
    )
    
    group.add_argument(
        "-pd", "--prompt-docs",
        type=str,
        metavar="QUESTION",
        help="Prompt the LLM with text and relevant documents from the database"
    )

    group.add_argument(
        "-pdm", "--prompt-docs-multiple",
        nargs="+",
        metavar=("QUESTION", "DOCS"),
        help="Prompt the LLM with a question followed by one or more doc paths"
    )

    group.add_argument(
        "-s", "--store-documents",
        action="store_true",
        help="Store all documents from the data folder in the database"
    )

    group.add_argument(
        "-c", "--check-db",
        action="store_true",
        help="Check how many documents are stored in the database"
    )

    group.add_argument(
        "-d", "--delete-db-entries",
        action="store_true",
        help="Delete all entries from the database"
    )

    group.add_argument(
        "-t", "--test",
        type=str,
        metavar="TEST_NAME",
        help="Run a specific test"
    )
    
    group.add_argument(
        "-ta", "--test-all",
        action="store_true",
        help="Run all tests"
    )
    
    return parser


def validate_file_path(file_path: str) -> bool:
    """Validate that the file path exists and is a PDF."""
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File '{file_path}' does not exist.")
        return False
    if not path.is_file():
        print(f"Error: '{file_path}' is not a file.")
        return False
    if path.suffix.lower() != '.pdf':
        print(f"Error: '{file_path}' is not a PDF file.")
        return False
    return True


def validate_folder_path(folder_path: str) -> bool:
    """Validate that the folder path exists and contains PDF files."""
    path = Path(folder_path)
    if not path.exists():
        print(f"Error: Folder '{folder_path}' does not exist.")
        return False
    if not path.is_dir():
        print(f"Error: '{folder_path}' is not a directory.")
        return False
    
    # Check if folder contains any PDF files
    pdf_files = list(path.glob("*.pdf"))
    if not pdf_files:
        print(f"Warning: No PDF files found in '{folder_path}'.")
    
    return True


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        
        if args.prompt:
            result = prompt_llm(args.prompt)
            print(result)
        
        elif args.prompt_docs:
            result = prompt_with_db_documents(args.prompt_docs)
            print(result)

        elif args.prompt_docs_multiple:
            # First argument is the question; remaining are doc paths
            question = args.prompt_docs_multiple[0]
            docs = args.prompt_docs_multiple[1:] if len(args.prompt_docs_multiple) > 1 else []
            result = prompt_with_upload_documents(question, docs)
            print(result)
        
        elif args.store_documents:
            result = store_documents()
            print(result)
        
        elif args.check_db:
            result = check_db()
            print(result)
        
        elif args.delete_db_entries:
            result = delete_db_entries()
            print(result)
        
        elif args.test:
            result = test_specific(args.test)
            print(result)
        
        elif args.test_all:
            result = test_all()
            print(result)
    
    except NotImplementedError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
