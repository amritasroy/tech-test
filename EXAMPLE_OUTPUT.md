# Example Output

This document shows example outputs from running the Git Commit Tracker on the reference repository.

## Table Format (Default)

### Command:
```bash
python git_tracker.py /path/to/gastrointestinal-tract-diseases-efficientNet --months 0
```

### Output:
```
🔍 Analyzing repository (all commits): /path/to/gastrointestinal-tract-diseases-efficientNet

📊 Contributors (Last Month):

+-----------+-----------+-----------+-----------+---------+-----------+--------------+---------+-------------------------+
| Author    |   Commits |   Lines + |   Lines - |   Files |   Quality |   Difficulty |   Value | Work Style              |
+===========+===========+===========+===========+=========+===========+==============+=========+=========================+
| Your Name |         5 |      5875 |      1153 |      36 |      59.9 |         64   |    38.4 | Complex problem solver  |
+-----------+-----------+-----------+-----------+---------+-----------+--------------+---------+-------------------------+
| A S Roy   |        13 |        28 |        26 |      13 |      92.5 |         20.4 |    25.1 | Maintenance contributor |
+-----------+-----------+-----------+-----------+---------+-----------+--------------+---------+-------------------------+

================================================================================
📋 OVERALL SUMMARY (Last Month)
================================================================================
  Total Contributors: 2
  Total Commits: 18
  Total Lines Added: 5903
  Total Lines Deleted: 1179
  Net Change: 4724 lines
  Total Files Modified: 49

  Average Quality Score: 76.22/100
  Average Difficulty Score: 42.21/100
  Average Value Score: 31.72/100
================================================================================
```

## Detailed Format

### Command:
```bash
python git_tracker.py /path/to/gastrointestinal-tract-diseases-efficientNet --months 0 --format detailed
```

### Output:
```
🔍 Analyzing repository (all commits): /path/to/gastrointestinal-tract-diseases-efficientNet

👥 Contributors (Last Month) - Detailed View:

================================================================================
1. Your Name
================================================================================
  📈 Activity Metrics:
     • Commits: 5
     • Lines Added: 5875
     • Lines Deleted: 1153
     • Files Modified: 36
     • Net Contribution: 4722 lines

  🎯 Performance Scores:
     • Quality Score: 59.92/100
     • Difficulty Score: 64.00/100
     • Value Score: 38.38/100

  💼 Work Style: Complex problem solver

================================================================================
2. A S Roy
================================================================================
  📈 Activity Metrics:
     • Commits: 13
     • Lines Added: 28
     • Lines Deleted: 26
     • Files Modified: 13
     • Net Contribution: 2 lines

  🎯 Performance Scores:
     • Quality Score: 92.52/100
     • Difficulty Score: 20.42/100
     • Value Score: 25.05/100

  💼 Work Style: Maintenance contributor

================================================================================
📋 OVERALL SUMMARY (Last Month)
================================================================================
  Total Contributors: 2
  Total Commits: 18
  Total Lines Added: 5903
  Total Lines Deleted: 1179
  Net Change: 4724 lines
  Total Files Modified: 49

  Average Quality Score: 76.22/100
  Average Difficulty Score: 42.21/100
  Average Value Score: 31.72/100
================================================================================
```

## Analysis Interpretation

### Contributor 1: "Your Name"
- **Work Style**: Complex problem solver
- **Strength**: High difficulty score (64/100) indicates tackling complex changes
- **Analysis**: Made significant code contributions (4722 net lines), modified many files (36), indicating foundational work
- **Quality**: Moderate (59.92/100) suggests focus on functionality over refinement
- **Value**: Good (38.38/100) relative to the complexity undertaken

### Contributor 2: "A S Roy"
- **Work Style**: Maintenance contributor
- **Strength**: Excellent quality score (92.52/100) indicates high attention to detail
- **Analysis**: Many small commits (13) with minimal line changes (2 net lines), typical of documentation updates and maintenance
- **Quality**: Outstanding (92.52/100) with balanced additions/deletions
- **Value**: Good (25.05/100) for maintenance work

## Different Sorting Options

### Sort by Quality
```bash
python git_tracker.py /path/to/repo --sort-by quality
```
Shows contributors with the highest quality scores first (best code practices)

### Sort by Difficulty
```bash
python git_tracker.py /path/to/repo --sort-by difficulty
```
Shows contributors tackling the most complex tasks first

### Sort by Commits
```bash
python git_tracker.py /path/to/repo --sort-by commits
```
Shows most active contributors first

### Sort by Value (Default)
```bash
python git_tracker.py /path/to/repo --sort-by value
```
Shows contributors with the highest overall impact first
