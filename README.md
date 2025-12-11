# Git Repository Commit Tracker

A Python-based CLI tool that analyzes git repository commits and measures contributor value based on multiple metrics including amount of work, quality, difficulty, and actual impact.

## Features

- 📊 **Comprehensive Metrics**: Analyzes commits from the last month
- 👥 **Contributor Analysis**: Tracks individual contributor performance
- 🎯 **Value Measurement**: Evaluates quality vs. quantity of contributions
- 💼 **Work Style Classification**: Identifies contributor patterns
- 📈 **Multiple Views**: Table and detailed output formats

## Metrics Explained

### Amount
- Number of commits
- Lines added and deleted
- Files modified
- Commit frequency

### Quality Score (0-100)
- Code churn ratio (balanced additions/deletions indicate refactoring)
- Commit message quality
- Consistency of changes

### Difficulty Score (0-100)
- Number of files modified per commit
- Complexity of changes (based on file types)
- Scope of modifications

### Value Score (0-100)
- Net positive contribution
- Actual impact vs. effort
- Quality-adjusted effectiveness
- Consistency of meaningful commits

### Work Style Categories
- **High-impact contributor**: High quality and value
- **Complex problem solver**: Tackles difficult tasks with good quality
- **Consistent high-quality contributor**: Regular, quality commits
- **Quality-focused contributor**: Few but excellent commits
- **Maintenance contributor**: Regular upkeep work
- **Balanced contributor**: Well-rounded contributions

## Installation

1. Clone this repository:
```bash
git clone https://github.com/amritasroy/tech-test.git
cd tech-test
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Analyze the current directory:
```bash
python git_tracker.py
```

Analyze a specific repository:
```bash
python git_tracker.py /path/to/repo
```

### Advanced Options

Show detailed view:
```bash
python git_tracker.py --format detailed
```

Analyze all commits (not just last month):
```bash
python git_tracker.py --months 0
```

Analyze last 3 months:
```bash
python git_tracker.py --months 3
```

Sort by different metrics:
```bash
python git_tracker.py --sort-by quality
python git_tracker.py --sort-by difficulty
python git_tracker.py --sort-by commits
python git_tracker.py --sort-by value
```

Combine options:
```bash
python git_tracker.py /path/to/repo --format detailed --sort-by quality --months 0
```

### Command-Line Options

- `REPO_PATH`: Path to git repository (default: current directory)
- `--format, -f`: Output format - `table` (default) or `detailed`
- `--sort-by, -s`: Sort by - `value` (default), `quality`, `difficulty`, or `commits`
- `--months, -m`: Number of months to analyze (default: 1, use 0 for all commits)

## Example Output

### Table Format
```
📊 Contributors (Last Month):

+----------------+---------+----------+----------+-------+---------+------------+-------+---------------------------+
| Author         | Commits | Lines +  | Lines -  | Files | Quality | Difficulty | Value | Work Style                |
+----------------+---------+----------+----------+-------+---------+------------+-------+---------------------------+
| John Doe       | 25      | 1500     | 800      | 45    | 72.5    | 65.3       | 78.2  | High-impact contributor   |
| Jane Smith     | 15      | 2000     | 500      | 30    | 68.0    | 58.7       | 71.5  | Complex problem solver    |
+----------------+---------+----------+----------+-------+---------+------------+-------+---------------------------+

📋 OVERALL SUMMARY (Last Month)
Total Contributors: 2
Total Commits: 40
Average Quality Score: 70.25/100
Average Value Score: 74.85/100
```

### Detailed Format
```
👥 Contributors (Last Month) - Detailed View:

1. John Doe
  📈 Activity Metrics:
     • Commits: 25
     • Lines Added: 1500
     • Lines Deleted: 800
     • Files Modified: 45
     • Net Contribution: 700 lines
  
  🎯 Performance Scores:
     • Quality Score: 72.50/100
     • Difficulty Score: 65.30/100
     • Value Score: 78.20/100
  
  💼 Work Style: High-impact contributor
```

## Testing

Test the tool with the reference repository:

```bash
# Clone the reference repository
git clone https://github.com/amritasroy/gastrointestinal-tract-diseases-efficientNet.git

# Analyze it (use --months 0 to analyze all commits since the repo is older)
python git_tracker.py ./gastrointestinal-tract-diseases-efficientNet --months 0

# View detailed analysis
python git_tracker.py ./gastrointestinal-tract-diseases-efficientNet --months 0 --format detailed
```

## Requirements

- Python 3.7+
- GitPython
- Click
- Tabulate
- python-dateutil

## How It Works

1. **Commit Extraction**: Retrieves all commits from the last month using GitPython
2. **Diff Analysis**: Analyzes each commit's diff to count lines changed, files modified
3. **Metric Calculation**: Computes quality, difficulty, and value scores using heuristics
4. **Work Style Classification**: Categorizes contributors based on their patterns
5. **Presentation**: Displays results in user-friendly formats

## License

MIT License

## Author

Created for tech-test repository