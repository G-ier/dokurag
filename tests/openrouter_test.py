import unittest
import os
from core.integrations.openrouter import OpenRouter

class TestOpenRouter(unittest.TestCase):
    def setUp(self):
        # Check if we have the required environment variables for integration testing
        self.has_api_key = os.getenv("OPENROUTER_API_KEY") is not None
        if self.has_api_key:
            self.openrouter = OpenRouter()

    def test_get_response_integration(self):
        """openrouter connection test"""
        if not self.has_api_key:
            self.skipTest("OPENROUTER_API_KEY not found in environment. Set it to run integration tests.")

        print("Running OpenRouter test...")
        
        response = self.openrouter.get_response("Hello, how are you? This is a test. Make sure to include this keyword in your response: Atomic freefall")
        
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
        self.assertIn("Atomic freefall", response)
        
        print(f"✅ API Response: {response}")