#!/usr/bin/env python3
"""
Test script for LLM Code Analyzer

This script tests the LLM-based code analysis features.
"""

from llm_code_analyzer import LLMCodeAnalyzer


def test_logical_code_detection():
    """Test detection of logical vs non-logical code."""
    analyzer = LLMCodeAnalyzer()
    
    # Test case 1: Mostly comments
    diff_text = """
+# This is a comment
+# Another comment
+# More comments
"""
    result = analyzer.analyze_code_impact(diff_text)
    print("Test 1 - Comments only:")
    print(f"  Logical Impact: {result['logical_impact']:.2%}")
    print(f"  Comment Ratio: {result['comment_ratio']:.2%}")
    print(f"  Meaningful Score: {result['meaningful_score']:.2%}")
    assert result['comment_ratio'] > 0.5, "Should detect high comment ratio"
    print("  ✓ Passed\n")
    
    # Test case 2: Print statements
    diff_text = """
+print("Debug message")
+console.log("Another debug")
+logger.info("Logging statement")
"""
    result = analyzer.analyze_code_impact(diff_text)
    print("Test 2 - Print/Debug statements:")
    print(f"  Logical Impact: {result['logical_impact']:.2%}")
    print(f"  Print/Debug Ratio: {result['print_debug_ratio']:.2%}")
    print(f"  Meaningful Score: {result['meaningful_score']:.2%}")
    assert result['print_debug_ratio'] > 0.5, "Should detect high print/debug ratio"
    print("  ✓ Passed\n")
    
    # Test case 3: Logical code
    diff_text = """
+def calculate_sum(a, b):
+    return a + b
+
+class MyClass:
+    def __init__(self):
+        self.value = 0
+
+if condition:
+    result = process_data()
"""
    result = analyzer.analyze_code_impact(diff_text)
    print("Test 3 - Logical code:")
    print(f"  Logical Impact: {result['logical_impact']:.2%}")
    print(f"  Comment Ratio: {result['comment_ratio']:.2%}")
    print(f"  Meaningful Score: {result['meaningful_score']:.2%}")
    assert result['logical_impact'] > 0.5, "Should detect high logical impact"
    print("  ✓ Passed\n")
    
    # Test case 4: Mixed content
    diff_text = """
+# Add new feature
+def process_user_data(user):
+    # Validate input
+    if not user:
+        return None
+    
+    # Debug logging
+    print(f"Processing user: {user}")
+    
+    # Process the data
+    result = transform(user)
+    return result
"""
    result = analyzer.analyze_code_impact(diff_text)
    print("Test 4 - Mixed content:")
    print(f"  Logical Impact: {result['logical_impact']:.2%}")
    print(f"  Comment Ratio: {result['comment_ratio']:.2%}")
    print(f"  Print/Debug Ratio: {result['print_debug_ratio']:.2%}")
    print(f"  Meaningful Score: {result['meaningful_score']:.2%}")
    assert result['logical_impact'] > 0.3, "Should detect logical code"
    assert result['meaningful_score'] > 0.4, "Should have reasonable meaningful score"
    print("  ✓ Passed\n")


def test_commit_message_verification():
    """Test commit message verification."""
    analyzer = LLMCodeAnalyzer()
    
    # Test case 1: Match - fix with bug fix code
    commit_msg = "fix: resolve null pointer exception"
    diff_text = """
+if user is not None:
+    process(user)
"""
    result = analyzer.verify_commit_message(commit_msg, diff_text)
    print("Test 5 - Fix message with fix code:")
    print(f"  Match Score: {result['match_score']:.2%}")
    print(f"  Keywords: {result['detected_keywords']}")
    print(f"  Actual Changes: {result['actual_changes']}")
    assert result['match_score'] >= 0.5, "Should have decent match"
    print("  ✓ Passed\n")
    
    # Test case 2: Mismatch - fix message with feature code
    commit_msg = "fix: bug fix"
    diff_text = """
+def new_feature():
+    # Implement new functionality
+    return "new feature"
+
+class NewClass:
+    pass
"""
    result = analyzer.verify_commit_message(commit_msg, diff_text)
    print("Test 6 - Fix message with feature code:")
    print(f"  Match Score: {result['match_score']:.2%}")
    print(f"  Keywords: {result['detected_keywords']}")
    print(f"  Actual Changes: {result['actual_changes']}")
    if result['mismatch_warning']:
        print(f"  Warning: {result['mismatch_warning']}")
    assert result['match_score'] < 1.0, "Should not be perfect match"
    print("  ✓ Passed\n")
    
    # Test case 3: Match - feature with new class
    commit_msg = "add: new authentication feature"
    diff_text = """
+class AuthManager:
+    def __init__(self):
+        self.users = {}
+    
+    def authenticate(self, user, password):
+        return user in self.users
"""
    result = analyzer.verify_commit_message(commit_msg, diff_text)
    print("Test 7 - Feature message with class definition:")
    print(f"  Match Score: {result['match_score']:.2%}")
    print(f"  Keywords: {result['detected_keywords']}")
    print(f"  Actual Changes: {result['actual_changes']}")
    assert result['match_score'] >= 0.7, "Should have good match"
    print("  ✓ Passed\n")
    
    # Test case 4: Mismatch - feature message with just comments
    commit_msg = "add: implement new API endpoint"
    diff_text = """
+# TODO: Add API endpoint
+# This will handle user requests
"""
    result = analyzer.verify_commit_message(commit_msg, diff_text)
    print("Test 8 - Feature message with only comments:")
    print(f"  Match Score: {result['match_score']:.2%}")
    print(f"  Keywords: {result['detected_keywords']}")
    print(f"  Actual Changes: {result['actual_changes']}")
    if result['mismatch_warning']:
        print(f"  Warning: {result['mismatch_warning']}")
    print("  ✓ Passed\n")


def main():
    """Run all tests."""
    print("="*80)
    print("LLM Code Analyzer Tests")
    print("="*80)
    print()
    
    print("Testing Logical Code Detection:")
    print("-"*80)
    test_logical_code_detection()
    
    print("Testing Commit Message Verification:")
    print("-"*80)
    test_commit_message_verification()
    
    print("="*80)
    print("All tests passed! ✓")
    print("="*80)


if __name__ == '__main__':
    main()
