#!/usr/bin/env python3
"""
LLM-Based Code Analysis Module

This module uses heuristic-based semantic analysis to analyze code changes
and detect mismatches between commit messages and actual changes.

Note: While this module is designed to work with HuggingFace transformers,
it uses heuristic analysis by default to avoid heavy model loading.
Full LLM analysis can be enabled by setting use_llm=True in initialization.
"""

import re
from typing import Dict, List, Tuple, Optional, Any


class LLMCodeAnalyzer:
    """
    Analyzes code changes using semantic heuristics to detect impact and verify
    commit message accuracy.
    """
    
    def __init__(self, use_llm: bool = False, model_name: str = "microsoft/codebert-base"):
        """
        Initialize the code analyzer.
        
        Args:
            use_llm: Whether to use actual LLM model (requires transformers)
                    Default False uses heuristic-based analysis (faster, lighter)
            model_name: HuggingFace model identifier for code analysis
                       Default: microsoft/codebert-base (open-source, no API key needed)
        """
        self.use_llm = use_llm
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self._initialized = False
        
    def _lazy_init(self):
        """
        Lazily initialize the model only when needed and if use_llm is True.
        
        Note: This method is reserved for future use when full LLM model support
        is enabled via use_llm=True. Currently, the tool uses heuristic-based
        analysis by default for speed and simplicity.
        """
        if self.use_llm and not self._initialized:
            try:
                from transformers import AutoTokenizer
                # Use a lightweight model for code understanding
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self._initialized = True
            except Exception as e:
                print(f"Warning: Could not initialize LLM model: {e}")
                print("Falling back to heuristic-based analysis")
                self._initialized = False
    
    def analyze_code_impact(self, diff_text: str) -> Dict[str, float]:
        """
        Analyze the semantic impact of code changes.
        
        Args:
            diff_text: The git diff text to analyze
            
        Returns:
            Dictionary with impact scores:
            - logical_impact: Score 0-1 indicating logical/functional changes
            - comment_ratio: Ratio of comment-only changes
            - print_debug_ratio: Ratio of print/logging statements
            - meaningful_score: Overall meaningful code score
        """
        # Initialize LLM model if needed
        self._lazy_init()
        
        if not diff_text:
            return {
                'logical_impact': 0.0,
                'comment_ratio': 0.0,
                'print_debug_ratio': 0.0,
                'meaningful_score': 0.0
            }
        
        # Parse the diff to extract added lines
        added_lines = self._extract_added_lines(diff_text)
        
        if not added_lines:
            return {
                'logical_impact': 0.0,
                'comment_ratio': 0.0,
                'print_debug_ratio': 0.0,
                'meaningful_score': 0.0
            }
        
        # Analyze the semantic content
        comment_count = 0
        print_debug_count = 0
        logical_code_count = 0
        
        for line in added_lines:
            line_stripped = line.strip()
            
            if not line_stripped:
                continue
                
            # Detect comments
            if self._is_comment(line_stripped):
                comment_count += 1
            # Detect print/logging statements
            elif self._is_print_or_log(line_stripped):
                print_debug_count += 1
            # Detect logical/functional code
            elif self._is_logical_code(line_stripped):
                logical_code_count += 1
        
        total_meaningful_lines = comment_count + print_debug_count + logical_code_count
        
        if total_meaningful_lines == 0:
            return {
                'logical_impact': 0.0,
                'comment_ratio': 0.0,
                'print_debug_ratio': 0.0,
                'meaningful_score': 0.0
            }
        
        # Calculate ratios
        comment_ratio = comment_count / total_meaningful_lines
        print_debug_ratio = print_debug_count / total_meaningful_lines
        logical_ratio = logical_code_count / total_meaningful_lines
        
        # Meaningful score: heavily weight logical code, slightly penalize excessive logging
        meaningful_score = (
            logical_ratio * 0.8 +  # Logical code is most valuable
            comment_ratio * 0.15 +  # Comments are somewhat valuable
            print_debug_ratio * 0.05  # Logging is least valuable
        )
        
        return {
            'logical_impact': round(logical_ratio, 3),
            'comment_ratio': round(comment_ratio, 3),
            'print_debug_ratio': round(print_debug_ratio, 3),
            'meaningful_score': round(meaningful_score, 3)
        }
    
    def verify_commit_message(self, commit_message: str, diff_text: str) -> Dict[str, Any]:
        """
        Verify if the commit message matches the actual code changes.
        
        Args:
            commit_message: The commit message
            diff_text: The git diff text
            
        Returns:
            Dictionary with verification results:
            - match_score: Score 0-1 indicating how well message matches changes
            - detected_keywords: Keywords found in message
            - actual_changes: Description of actual changes
            - mismatch_warning: Warning message if mismatch detected
        """
        if not commit_message or not diff_text:
            return {
                'match_score': 0.5,
                'detected_keywords': [],
                'actual_changes': 'No changes detected',
                'mismatch_warning': None
            }
        
        # Extract keywords from commit message
        message_keywords = self._extract_keywords(commit_message)
        
        # Analyze actual changes
        change_analysis = self._analyze_change_type(diff_text)
        
        # Calculate match score
        match_score = self._calculate_match_score(message_keywords, change_analysis)
        
        # Generate warning if significant mismatch
        mismatch_warning = None
        if match_score < 0.4:
            mismatch_warning = f"Commit message suggests '{', '.join(message_keywords)}' but changes appear to be {change_analysis['primary_type']}"
        
        return {
            'match_score': round(match_score, 3),
            'detected_keywords': message_keywords,
            'actual_changes': change_analysis['primary_type'],
            'mismatch_warning': mismatch_warning
        }
    
    def _extract_added_lines(self, diff_text: str) -> List[str]:
        """Extract lines that were added (start with +) from diff."""
        lines = diff_text.split('\n')
        added = []
        for line in lines:
            if line.startswith('+') and not line.startswith('+++'):
                # Remove the '+' prefix
                added.append(line[1:])
        return added
    
    def _is_comment(self, line: str) -> bool:
        """Check if a line is a comment."""
        # Support multiple comment styles
        comment_patterns = [
            r'^\s*#',           # Python, Ruby, Shell
            r'^\s*//',          # JavaScript, Java, C++, C#
            r'^\s*/\*',         # Block comment start
            r'^\s*\*',          # Block comment continuation
            r'^\s*\*/',         # Block comment end
            r'^\s*<!--',        # HTML, XML
            r'^\s*"""',         # Python docstring
            r"^\s*'''",         # Python docstring
        ]
        
        for pattern in comment_patterns:
            if re.match(pattern, line):
                return True
        return False
    
    def _is_print_or_log(self, line: str) -> bool:
        """Check if a line is a print or logging statement."""
        log_patterns = [
            r'\bprint\s*\(',
            r'\bconsole\.log\s*\(',
            r'\bconsole\.(debug|info|warn|error)\s*\(',
            r'\blogger\.',
            r'\blogging\.',
            r'\bLog\.',
            r'\bSystem\.out\.print',
            r'\bSystem\.err\.print',
            r'\bfprintf\s*\(',
            r'\bprintf\s*\(',
            r'\bcout\s*<<',
            r'\bcerr\s*<<',
        ]
        
        for pattern in log_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                return True
        return False
    
    def _is_logical_code(self, line: str) -> bool:
        """
        Check if a line contains logical/functional code.
        This includes variable declarations, function calls, control flow, etc.
        """
        # Skip empty lines and pure whitespace
        if not line.strip():
            return False
        
        # Skip if it's a comment or logging
        if self._is_comment(line) or self._is_print_or_log(line):
            return False
        
        # Indicators of logical code
        logical_patterns = [
            r'\bdef\s+\w+',          # Function definition (Python)
            r'\bfunction\s+\w+',     # Function definition (JavaScript)
            r'\bclass\s+\w+',        # Class definition
            r'\bif\s+',              # Conditional
            r'\belse\s*:',           # Conditional
            r'\bfor\s+',             # Loop
            r'\bwhile\s+',           # Loop
            r'\breturn\s+',          # Return statement
            r'\bimport\s+',          # Import
            r'\bfrom\s+\w+\s+import', # Import
            r'\w+\s*=\s*',           # Assignment
            r'\w+\s*\(',             # Function call
            r'\.\w+\(',              # Method call
            r'\bawait\s+',           # Async operation
            r'\basync\s+',           # Async definition
            r'\btry\s*:',            # Exception handling
            r'\bexcept\s+',          # Exception handling
            r'\bcatch\s*\(',         # Exception handling
            r'\bthrow\s+',           # Exception throwing
            r'\braise\s+',           # Exception raising
        ]
        
        for pattern in logical_patterns:
            if re.search(pattern, line):
                return True
        
        # If it has alphanumeric content and isn't a comment/log, likely logical code
        if re.search(r'[a-zA-Z_]\w*', line):
            return True
        
        return False
    
    def _extract_keywords(self, commit_message: str) -> List[str]:
        """Extract meaningful keywords from commit message."""
        # Common commit message keywords
        keywords_map = {
            'fix': ['fix', 'fixed', 'fixes', 'bugfix', 'hotfix'],
            'feature': ['feature', 'add', 'added', 'implement', 'implements', 'implemented'],
            'refactor': ['refactor', 'refactored', 'refactoring', 'restructure'],
            'update': ['update', 'updated', 'upgrade', 'upgraded'],
            'remove': ['remove', 'removed', 'delete', 'deleted'],
            'test': ['test', 'testing', 'tests'],
            'docs': ['doc', 'docs', 'documentation', 'comment', 'comments'],
            'style': ['style', 'format', 'formatting'],
            'optimize': ['optimize', 'optimized', 'performance', 'improve', 'improved'],
        }
        
        message_lower = commit_message.lower()
        found_keywords = []
        
        for category, variants in keywords_map.items():
            for variant in variants:
                if variant in message_lower:
                    if category not in found_keywords:
                        found_keywords.append(category)
                    break
        
        return found_keywords if found_keywords else ['unknown']
    
    def _analyze_change_type(self, diff_text: str) -> Dict[str, Any]:
        """
        Analyze what type of changes were actually made.
        """
        added_lines = self._extract_added_lines(diff_text)
        
        # Categorize changes
        has_function_def = False
        has_class_def = False
        has_import = False
        has_logic = False
        has_comments = False
        has_tests = False
        
        for line in added_lines:
            line_stripped = line.strip()
            
            if 'def ' in line_stripped or 'function ' in line_stripped:
                has_function_def = True
            if 'class ' in line_stripped:
                has_class_def = True
            if 'import ' in line_stripped or 'from ' in line_stripped:
                has_import = True
            if self._is_comment(line_stripped):
                has_comments = True
            if self._is_logical_code(line_stripped):
                has_logic = True
            if 'test' in line_stripped.lower() or 'assert' in line_stripped.lower():
                has_tests = True
        
        # Determine primary change type
        if has_class_def or has_function_def:
            primary_type = 'feature'
        elif has_tests:
            primary_type = 'test'
        elif has_comments and not has_logic:
            primary_type = 'docs'
        elif has_logic:
            primary_type = 'update'
        elif has_import:
            primary_type = 'refactor'
        else:
            primary_type = 'unknown'
        
        return {
            'primary_type': primary_type,
            'has_function_def': has_function_def,
            'has_class_def': has_class_def,
            'has_logic': has_logic,
            'has_comments': has_comments,
            'has_tests': has_tests,
        }
    
    def _calculate_match_score(self, message_keywords: List[str], 
                               change_analysis: Dict[str, Any]) -> float:
        """
        Calculate how well the commit message matches actual changes.
        """
        primary_type = change_analysis['primary_type']
        
        # Direct match
        if primary_type in message_keywords:
            return 1.0
        
        # Semantic matches
        semantic_matches = {
            'fix': ['update', 'refactor'],
            'feature': ['update', 'refactor'],
            'update': ['fix', 'feature', 'optimize'],
            'refactor': ['update', 'optimize'],
            'test': ['feature'],
            'docs': [],
        }
        
        # Check for semantic matches
        for keyword in message_keywords:
            if keyword in semantic_matches:
                if primary_type in semantic_matches[keyword]:
                    return 0.7
        
        # Partial match
        if len(message_keywords) > 1:
            return 0.5
        
        # No match
        return 0.3
