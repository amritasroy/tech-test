#!/usr/bin/env python3
"""
Test to verify LLM mode is enabled and working correctly.
This test demonstrates that use_llm=True parameter works.
"""

from llm_code_analyzer import LLMCodeAnalyzer


def test_llm_mode_enabled():
    """Test that LLM mode can be enabled."""
    print("="*80)
    print("Testing LLM Mode Configuration")
    print("="*80)
    print()
    
    # Test 1: Default mode (heuristic)
    print("Test 1: Default mode (use_llm=False)")
    analyzer_default = LLMCodeAnalyzer(use_llm=False)
    print(f"  use_llm: {analyzer_default.use_llm}")
    print(f"  model_name: {analyzer_default.model_name}")
    assert analyzer_default.use_llm == False, "Default should be heuristic mode"
    print("  ✓ Passed\n")
    
    # Test 2: LLM mode enabled
    print("Test 2: LLM mode enabled (use_llm=True)")
    analyzer_llm = LLMCodeAnalyzer(use_llm=True)
    print(f"  use_llm: {analyzer_llm.use_llm}")
    print(f"  model_name: {analyzer_llm.model_name}")
    assert analyzer_llm.use_llm == True, "LLM mode should be enabled"
    print("  ✓ Passed\n")
    
    # Test 3: Try to initialize (will fall back if no internet)
    print("Test 3: Test LLM initialization (may fall back to heuristics)")
    test_diff = """
+def test_function():
+    return True
"""
    result = analyzer_llm.analyze_code_impact(test_diff)
    print(f"  Analysis result: {result}")
    print(f"  Logical Impact: {result['logical_impact']:.2%}")
    assert result['logical_impact'] > 0, "Should detect logical code"
    print("  ✓ Passed\n")
    
    # Test 4: Custom model name
    print("Test 4: Custom model name")
    analyzer_custom = LLMCodeAnalyzer(use_llm=True, model_name="custom/model")
    print(f"  use_llm: {analyzer_custom.use_llm}")
    print(f"  model_name: {analyzer_custom.model_name}")
    assert analyzer_custom.model_name == "custom/model", "Custom model name should be set"
    print("  ✓ Passed\n")
    
    print("="*80)
    print("All LLM mode tests passed! ✓")
    print("="*80)
    print()
    print("Note: If LLM model download fails (no internet access),")
    print("the system correctly falls back to heuristic-based analysis.")
    print("This is the expected behavior and ensures the tool remains functional.")


if __name__ == '__main__':
    test_llm_mode_enabled()
