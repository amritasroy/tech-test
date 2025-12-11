# Example: Detecting Low-Value and Misleading Commits

This document demonstrates how the LLM-based code impact analysis catches problematic commits that would otherwise appear valuable based on line counts alone.

## Scenario 1: Debug Statements Disguised as Features

### Commit Message
```
feat: implement user authentication system
```

### Actual Changes
```python
+print("Starting authentication")
+console.log("User login attempt")
+logger.info("Checking credentials")
+print("Authentication complete")
+# TODO: Implement actual authentication
```

### Analysis Results
```
Lines Added: 5
Logical Impact: 0% (functional code)
Print/Debug Ratio: 80%
Commit Message Match: 30%
Warning: Commit message suggests 'feature' but changes appear to be docs
Meaningful Score: 5%
```

**Interpretation**: Despite adding 5 lines, this commit has almost zero value. It's mostly debug statements with no actual functional code.

---

## Scenario 2: Comments Pretending to be Implementation

### Commit Message
```
fix: resolve database connection issues
```

### Actual Changes
```python
+# Fix database connection
+# Need to add retry logic
+# Handle connection timeouts
+# Update connection string
```

### Analysis Results
```
Lines Added: 4
Logical Impact: 0% (functional code)
Comment Ratio: 100%
Commit Message Match: 30%
Warning: Commit message suggests 'fix' but changes appear to be docs
Meaningful Score: 15%
```

**Interpretation**: The commit claims to fix an issue but only adds comments. No actual code was changed.

---

## Scenario 3: Genuine High-Impact Commit

### Commit Message
```
feat: add user validation with email verification
```

### Actual Changes
```python
+def validate_user(user):
+    """Validate user input and email format."""
+    if not user or not user.email:
+        raise ValueError("User email required")
+    
+    if not validate_email_format(user.email):
+        raise ValueError("Invalid email format")
+    
+    return True
+
+def validate_email_format(email):
+    """Check if email matches valid pattern."""
+    import re
+    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
+    return re.match(pattern, email) is not None
```

### Analysis Results
```
Lines Added: 16
Logical Impact: 87% (functional code)
Comment Ratio: 13%
Print/Debug Ratio: 0%
Commit Message Match: 100%
Meaningful Score: 75%
```

**Interpretation**: This is a genuine high-value commit. Most lines are functional code, message matches changes, and meaningful score is high.

---

## Scenario 4: Mixed Quality Commit

### Commit Message
```
refactor: improve data processing logic
```

### Actual Changes
```python
+# Refactor data processing
+def process_data(data):
+    # Validate input
+    print(f"Processing {len(data)} items")
+    
+    # Transform data
+    result = [item.strip().lower() for item in data]
+    
+    print(f"Processed {len(result)} items")
+    return result
```

### Analysis Results
```
Lines Added: 11
Logical Impact: 45% (functional code)
Comment Ratio: 27%
Print/Debug Ratio: 18%
Commit Message Match: 70%
Meaningful Score: 42%
```

**Interpretation**: Mixed quality. Has some functional code but also unnecessary logging. Message reasonably matches changes.

---

## Scenario 5: Mismatch - Fix vs Feature

### Commit Message
```
fix: correct login validation bug
```

### Actual Changes
```python
+class NewUserDashboard:
+    """New dashboard for user analytics."""
+    def __init__(self):
+        self.metrics = []
+    
+    def add_metric(self, metric):
+        self.metrics.append(metric)
+    
+    def render(self):
+        return {"metrics": self.metrics}
```

### Analysis Results
```
Lines Added: 10
Logical Impact: 88% (functional code)
Comment Ratio: 12%
Print/Debug Ratio: 0%
Commit Message Match: 30%
Warning: Commit message suggests 'fix' but changes appear to be feature
Meaningful Score: 75%
```

**Interpretation**: High-quality code but the commit message is misleading. Claims to fix a bug but actually adds a new feature class.

---

## Real Repository Example

Running on the tech-test repository:

```bash
$ python git_tracker.py --months 0 --format detailed
```

```
👥 Contributors (All Commits) - Detailed View:

================================================================================
1. copilot-swe-agent[bot]
================================================================================
  📈 Activity Metrics:
     • Commits: 4
     • Lines Added: 990
     • Lines Deleted: 51
     • Files Modified: 11
     • Net Contribution: 939 lines

  🎯 Performance Scores:
     • Quality Score: 59.40/100
     • Difficulty Score: 80.00/100
     • Value Score: 16.57/100

  🤖 LLM-Based Code Analysis:
     • Logical Impact: 54.00% (functional code)
     • Meaningful Score: 45.60% (overall quality)
     • Comment Ratio: 15.00%
     • Print/Debug Ratio: 8.00%
     • Commit Message Match: 75.00%

  💼 Work Style: Complex problem solver
```

**Interpretation**: 
- 54% logical impact shows about half the code is functional (rest is comments/docs/debug)
- 75% message match indicates good alignment between commits and changes
- 45.6% meaningful score reflects a mix of functional code and supporting documentation

---

## Key Takeaways

1. **Line counts alone are misleading** - A commit with 100 lines could be 100% comments
2. **Commit messages can be deceptive** - Message says "fix" but adds a new feature
3. **Debug statements inflate metrics** - Lots of print/logging doesn't equal value
4. **LLM analysis catches these issues** - Semantic analysis reveals true impact

## Usage

To analyze any repository:

```bash
# Table view with LLM metrics
python git_tracker.py /path/to/repo --months 0

# Detailed view with warnings
python git_tracker.py /path/to/repo --months 0 --format detailed
```

Look for:
- **Low Logical%** (<30%) - Mostly non-functional changes
- **Low Msg Match%** (<40%) - Commit message doesn't match changes
- **Mismatch warnings** - Specific alerts about discrepancies
