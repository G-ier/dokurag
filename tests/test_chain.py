"""unittest-based tests for DokuragChain."""

import os
import sys
import dotenv
import unittest
from pathlib import Path

# import core
sys.path.append(str(Path(__file__).parent.parent))
from core.chain import DokuragChain

class TestDokuragChain(unittest.TestCase):
    def setUp(self):
        # Integration tests require an API key
        dotenv.load_dotenv()
        self.has_api_key = os.getenv("OPENROUTER_API_KEY") is not None
        if self.has_api_key:
            self.chain = DokuragChain("/Users/gier/projects/dokurag/data/")

    # Simple chain should not return the answer
    def test_simple_chain(self):
        
        if not self.has_api_key:
            self.skipTest(
                "OPENROUTER_API_KEY not found in environment. Set it to run integration tests."
            )

        prompt = (
            "What is the STK number of product with Product code 4050300006741? Say 'No data' if you don't know or cannot find it."
        )
        response = self.chain.simple_invoke(prompt)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
        self.assertIn("No data", response)

    # final test for RAG chain
    def test_rag_chain(self):

        if not self.has_api_key:
            self.skipTest(
                "OPENROUTER_API_KEY not found in environment. Set it to run integration tests."
            )

        files = ["/Users/gier/projects/dokurag/data/ZMP_56131.pdf"]
        question = (
            "What is the STK number of product with Product code 4050300006741?"
        )
        response = self.chain.invoke(question=question, documents=files)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
        self.assertIn("4739434", response)

    # second final test lol
    def test_rag_chain_quality(self):
        if not self.has_api_key:
            self.skipTest(
                "OPENROUTER_API_KEY not found in environment. Set it to run integration tests."
            )
        
        files = ["/Users/gier/projects/dokurag/data/ZMP_1006715.pdf"]
        question = (
            "What is the Family brand of product with Product code 54250?"
        )
        response = self.chain.invoke(question=question, documents=files)

        print(response)

        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
        self.assertIn("XENOPHOT", response)


if __name__ == "__main__":
    unittest.main()