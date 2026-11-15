import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'solution'))
from lab7 import agent

class ApiSafetyTests(unittest.TestCase):
    def test_rejects_missing_key_before_request(self):
        with patch.dict(os.environ, {}, clear=True), patch('lab7.defaults'):
            with self.assertRaisesRegex(ValueError, 'GEMINI_API_KEY missing'):
                agent('question', None)

    def test_rejects_without_free_tier_confirmation(self):
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'unit-test-placeholder'}, clear=True), patch('lab7.defaults'):
            with self.assertRaisesRegex(ValueError, 'Free Tier'):
                agent('question', None)
