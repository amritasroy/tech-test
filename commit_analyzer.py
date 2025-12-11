#!/usr/bin/env python3
"""
Git Repository Commit Tracker and Value Analyzer

This module analyzes git commits to measure contributor value based on:
- Amount: Number of commits, lines changed, files modified
- Quality: Code consistency, meaningful changes
- Difficulty: Complexity of changes, scope
- Value: Actual impact vs churn ratio
"""

import os
import re
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Tuple

from git import Repo
from dateutil.relativedelta import relativedelta


class CommitAnalyzer:
    """Analyzes git commits and calculates contributor metrics."""
    
    def __init__(self, repo_path: str):
        """
        Initialize the analyzer with a git repository.
        
        Args:
            repo_path: Path to the git repository
        """
        self.repo_path = repo_path
        try:
            self.repo = Repo(repo_path)
        except Exception as e:
            raise ValueError(f"Invalid git repository: {repo_path}. Error: {str(e)}")
        
        if self.repo.bare:
            raise ValueError(f"Repository at {repo_path} is bare")
    
    def get_commits_last_month(self, months: int = 1) -> List:
        """
        Get all commits from the specified number of months.
        
        Args:
            months: Number of months to look back (0 for all commits)
        """
        commits = []
        
        if months == 0:
            # Get all commits
            for commit in self.repo.iter_commits():
                commits.append(commit)
        else:
            # Get commits from the last N months
            cutoff_date = datetime.now() - relativedelta(months=months)
            for commit in self.repo.iter_commits():
                commit_date = datetime.fromtimestamp(commit.committed_date)
                if commit_date >= cutoff_date:
                    commits.append(commit)
                else:
                    # Commits are in reverse chronological order
                    break
        
        return commits
    
    def analyze_commit(self, commit) -> Dict:
        """
        Analyze a single commit for various metrics.
        
        Returns:
            Dictionary with lines_added, lines_deleted, files_modified, complexity_score
        """
        stats = {
            'lines_added': 0,
            'lines_deleted': 0,
            'files_modified': 0,
            'complexity_score': 0
        }
        
        try:
            # Get commit diff stats
            if commit.parents:
                diffs = commit.parents[0].diff(commit, create_patch=True)
            else:
                # First commit has no parent
                diffs = commit.diff(None, create_patch=True)
            
            stats['files_modified'] = len(diffs)
            
            for diff in diffs:
                # Count lines added and deleted
                if diff.diff:
                    diff_text = diff.diff.decode('utf-8', errors='ignore')
                    lines = diff_text.split('\n')
                    for line in lines:
                        if line.startswith('+') and not line.startswith('+++'):
                            stats['lines_added'] += 1
                        elif line.startswith('-') and not line.startswith('---'):
                            stats['lines_deleted'] += 1
                
                # Calculate complexity based on file types and change patterns
                if diff.a_path:
                    path = diff.a_path
                    # Higher complexity for core files
                    if any(ext in path for ext in ['.py', '.java', '.cpp', '.c', '.js', '.ts']):
                        stats['complexity_score'] += 2
                    elif any(ext in path for ext in ['.json', '.xml', '.yaml', '.yml']):
                        stats['complexity_score'] += 1
                    
                    # Higher complexity for smaller focused changes (likely bug fixes)
                    if 1 <= stats['files_modified'] <= 3:
                        stats['complexity_score'] += 1
        
        except Exception as e:
            # Some commits might have issues with diff calculation
            pass
        
        return stats
    
    def calculate_quality_score(self, author_stats: Dict) -> float:
        """
        Calculate quality score based on commit patterns.
        
        Higher quality indicators:
        - Balanced additions/deletions (refactoring)
        - Consistent commit sizes
        - Meaningful commit messages
        """
        total_commits = author_stats['commit_count']
        if total_commits == 0:
            return 0.0
        
        lines_added = author_stats['lines_added']
        lines_deleted = author_stats['lines_deleted']
        
        # Quality based on code churn ratio (lower is better)
        # Avoid division by zero
        if lines_added + lines_deleted == 0:
            churn_ratio = 1.0
        else:
            # Balanced changes get higher score
            total_changes = lines_added + lines_deleted
            net_changes = abs(lines_added - lines_deleted)
            churn_ratio = 1 - (net_changes / total_changes) if total_changes > 0 else 0.5
        
        # Commit message quality (based on length and keywords)
        avg_message_quality = author_stats.get('avg_message_quality', 0.5)
        
        # Combine factors (scale 0-100)
        quality_score = (churn_ratio * 40) + (avg_message_quality * 60)
        
        return round(quality_score, 2)
    
    def calculate_difficulty_score(self, author_stats: Dict) -> float:
        """
        Calculate difficulty score based on complexity of changes.
        
        Higher difficulty indicators:
        - More files modified
        - Higher complexity score
        - Larger scope of changes
        """
        total_commits = author_stats['commit_count']
        if total_commits == 0:
            return 0.0
        
        # Average files per commit (normalized)
        avg_files = author_stats['files_modified'] / total_commits
        files_score = min(avg_files * 10, 40)  # Cap at 40
        
        # Complexity score (normalized)
        complexity_score = min(author_stats['complexity_score'] / total_commits * 10, 40)  # Cap at 40
        
        # Lines changed per commit (normalized)
        total_lines = author_stats['lines_added'] + author_stats['lines_deleted']
        avg_lines = total_lines / total_commits if total_commits > 0 else 0
        lines_score = min(avg_lines / 10, 20)  # Cap at 20
        
        difficulty = files_score + complexity_score + lines_score
        
        return round(difficulty, 2)
    
    def calculate_value_score(self, author_stats: Dict) -> float:
        """
        Calculate value score: actual impact vs effort.
        
        Higher value indicators:
        - Net positive contribution (more additions than deletions)
        - Consistent meaningful commits
        - Good quality-to-effort ratio
        """
        total_commits = author_stats['commit_count']
        if total_commits == 0:
            return 0.0
        
        lines_added = author_stats['lines_added']
        lines_deleted = author_stats['lines_deleted']
        quality = author_stats.get('quality_score', 0)
        difficulty = author_stats.get('difficulty_score', 0)
        
        # Net contribution (positive impact)
        net_lines = lines_added - lines_deleted
        contribution_score = min(max(net_lines / 100, 0), 30)  # Cap at 30
        
        # Commit frequency (consistency)
        frequency_score = min(total_commits * 2, 30)  # Cap at 30
        
        # Quality-adjusted impact
        quality_factor = quality / 100 if quality > 0 else 0.5
        
        # Value = contribution + frequency, adjusted by quality
        value = (contribution_score + frequency_score) * (0.5 + quality_factor * 0.5)
        
        # Bonus for tackling difficult work
        if difficulty > 50:
            value *= 1.2
        
        return round(min(value, 100), 2)
    
    def analyze_commit_message_quality(self, message: str) -> float:
        """
        Analyze commit message quality.
        
        Returns score between 0 and 1.
        """
        if not message:
            return 0.0
        
        score = 0.5  # Base score
        
        # Length check (reasonable commit messages)
        if 20 <= len(message) <= 200:
            score += 0.2
        elif len(message) > 10:
            score += 0.1
        
        # Contains keywords indicating meaningful work
        meaningful_keywords = [
            'fix', 'add', 'update', 'implement', 'refactor',
            'improve', 'optimize', 'feature', 'bug', 'issue'
        ]
        if any(keyword in message.lower() for keyword in meaningful_keywords):
            score += 0.2
        
        # Not just merge commit
        if not message.lower().startswith('merge'):
            score += 0.1
        
        return min(score, 1.0)
    
    def get_work_style(self, author_stats: Dict) -> str:
        """
        Determine work style based on metrics.
        """
        quality = author_stats.get('quality_score', 0)
        difficulty = author_stats.get('difficulty_score', 0)
        value = author_stats.get('value_score', 0)
        commit_count = author_stats['commit_count']
        
        # Analyze patterns
        if quality > 70 and value > 60:
            return "High-impact contributor"
        elif difficulty > 60 and quality > 50:
            return "Complex problem solver"
        elif commit_count > 20 and quality > 60:
            return "Consistent high-quality contributor"
        elif commit_count > 15 and value < 40:
            return "High activity, focus on value"
        elif quality > 60 and commit_count < 10:
            return "Quality-focused contributor"
        elif difficulty < 30 and commit_count > 10:
            return "Maintenance contributor"
        else:
            return "Balanced contributor"
    
    def analyze_repository(self, months: int = 1) -> Dict[str, Dict]:
        """
        Analyze the entire repository for the specified time period.
        
        Args:
            months: Number of months to analyze (0 for all commits)
        
        Returns:
            Dictionary mapping author names to their statistics
        """
        commits = self.get_commits_last_month(months=months)
        
        if not commits:
            return {}
        
        # Aggregate statistics per author
        author_stats = defaultdict(lambda: {
            'commit_count': 0,
            'lines_added': 0,
            'lines_deleted': 0,
            'files_modified': 0,
            'complexity_score': 0,
            'message_qualities': []
        })
        
        for commit in commits:
            author = commit.author.name
            author_stats[author]['commit_count'] += 1
            
            # Analyze commit
            stats = self.analyze_commit(commit)
            author_stats[author]['lines_added'] += stats['lines_added']
            author_stats[author]['lines_deleted'] += stats['lines_deleted']
            author_stats[author]['files_modified'] += stats['files_modified']
            author_stats[author]['complexity_score'] += stats['complexity_score']
            
            # Analyze message quality
            msg_quality = self.analyze_commit_message_quality(commit.message)
            author_stats[author]['message_qualities'].append(msg_quality)
        
        # Calculate derived metrics for each author
        results = {}
        for author, stats in author_stats.items():
            # Calculate average message quality
            if stats['message_qualities']:
                stats['avg_message_quality'] = sum(stats['message_qualities']) / len(stats['message_qualities'])
            else:
                stats['avg_message_quality'] = 0.5
            
            # Calculate scores
            stats['quality_score'] = self.calculate_quality_score(stats)
            stats['difficulty_score'] = self.calculate_difficulty_score(stats)
            stats['value_score'] = self.calculate_value_score(stats)
            stats['work_style'] = self.get_work_style(stats)
            
            # Remove temporary data
            del stats['message_qualities']
            
            results[author] = stats
        
        return results
