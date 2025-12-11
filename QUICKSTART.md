# Quick Start Guide

## Installation

1. Clone the repository:
```bash
git clone https://github.com/amritasroy/tech-test.git
cd tech-test
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Basic Usage

### Analyze Current Repository
```bash
python git_tracker.py
```

### Analyze Any Repository
```bash
python git_tracker.py /path/to/repository
```

### Common Use Cases

#### 1. Quick Team Performance Overview
```bash
# See who contributed last month and their overall value
python git_tracker.py /path/to/repo
```

#### 2. Detailed Individual Analysis
```bash
# Get detailed metrics for each contributor
python git_tracker.py /path/to/repo --format detailed
```

#### 3. Historical Analysis
```bash
# Analyze all commits in the repository
python git_tracker.py /path/to/repo --months 0

# Analyze last 3 months
python git_tracker.py /path/to/repo --months 3
```

#### 4. Find Top Quality Contributors
```bash
python git_tracker.py /path/to/repo --sort-by quality
```

#### 5. Identify Complex Problem Solvers
```bash
python git_tracker.py /path/to/repo --sort-by difficulty
```

## Understanding the Output

### Metrics Explained

- **Commits**: Total number of commits by the contributor
- **Lines +**: Total lines of code added
- **Lines -**: Total lines of code deleted
- **Files**: Total number of files modified
- **Quality Score (0-100)**: Based on code churn ratio and commit message quality
  - 80+: Excellent, very balanced changes
  - 60-80: Good, solid contributions
  - 40-60: Average, room for improvement
  - <40: Needs attention, high churn
- **Difficulty Score (0-100)**: Based on complexity of changes
  - 80+: Very complex work (large scale refactoring, architecture changes)
  - 60-80: Complex work (multi-file changes, significant features)
  - 40-60: Moderate complexity (standard features)
  - <40: Simple changes (small fixes, documentation)
- **Value Score (0-100)**: Overall impact vs effort
  - 80+: Exceptional value
  - 60-80: High value
  - 40-60: Good value
  - 20-40: Moderate value
  - <20: Low value (may need mentoring or clearer tasks)

### Work Style Categories

- **High-impact contributor**: Delivers high quality and value consistently
- **Complex problem solver**: Tackles difficult technical challenges
- **Consistent high-quality contributor**: Regular, well-crafted commits
- **Quality-focused contributor**: Fewer commits but excellent quality
- **Maintenance contributor**: Keeps code clean and up-to-date
- **Balanced contributor**: Well-rounded contributions across metrics

## Tips for Managers

1. **Use monthly reports** to track team progress:
   ```bash
   python git_tracker.py /path/to/repo --months 1 > monthly_report.txt
   ```

2. **Identify training needs** by looking for low quality or difficulty scores

3. **Recognize top performers** using the value score and work style

4. **Compare across time periods**:
   ```bash
   # This month
   python git_tracker.py /path/to/repo --months 1
   
   # Last quarter
   python git_tracker.py /path/to/repo --months 3
   ```

5. **Use detailed view for 1-on-1s**:
   ```bash
   python git_tracker.py /path/to/repo --format detailed --sort-by value
   ```

## Tips for Developers

1. **Improve your quality score**:
   - Write meaningful commit messages
   - Balance additions and deletions (refactor, don't just add)
   - Keep commits focused

2. **Increase your value score**:
   - Focus on meaningful contributions
   - Avoid unnecessary churn
   - Take on challenging but impactful work

3. **Track your progress**:
   ```bash
   # See your contributions
   python git_tracker.py /path/to/repo --format detailed
   ```

## Troubleshooting

### "Invalid git repository" error
- Make sure you're pointing to a valid git repository
- Check that the `.git` directory exists

### "No commits found" message
- Try using `--months 0` to analyze all commits
- Check if there are actually commits in the specified time period

### Large repositories taking too long
- The tool analyzes all commits in the time period
- Use shorter time periods for large repos
- Consider analyzing specific branches

## Examples

### Example 1: Team Sprint Review
```bash
python git_tracker.py /project/repo --months 1 --sort-by value
```

### Example 2: Onboarding New Developer
```bash
python git_tracker.py /project/repo --format detailed --months 3
```

### Example 3: Code Review Preparation
```bash
python git_tracker.py /project/repo --sort-by quality
```

### Example 4: Project Post-Mortem
```bash
python git_tracker.py /project/repo --months 0 --format detailed
```
