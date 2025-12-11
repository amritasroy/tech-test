#!/usr/bin/env python3
"""
Git Commit Tracker CLI

Command-line interface for analyzing git repository commits and contributor value.
"""

import click
import os
from tabulate import tabulate
from commit_analyzer import CommitAnalyzer


@click.command()
@click.argument('repo_path', type=click.Path(exists=True), default='.')
@click.option('--format', '-f', type=click.Choice(['table', 'detailed']), default='table',
              help='Output format (table or detailed)')
@click.option('--sort-by', '-s', type=click.Choice(['value', 'quality', 'difficulty', 'commits']), 
              default='value', help='Sort results by metric')
@click.option('--months', '-m', type=int, default=1,
              help='Number of months to analyze (default: 1, use 0 for all commits)')
def analyze(repo_path, format, sort_by, months):
    """
    Analyze git repository commits and show contributor metrics.
    
    REPO_PATH: Path to the git repository (default: current directory)
    
    Example:
        git-tracker /path/to/repo
        git-tracker . --format detailed --sort-by quality
        git-tracker /path/to/repo --months 3
        git-tracker /path/to/repo --months 0  # Analyze all commits
    """
    if months == 0:
        time_period_text = "(All Commits)"
        click.echo(f"\n🔍 Analyzing repository (all commits): {os.path.abspath(repo_path)}\n")
    else:
        time_period_text = f"(Last {months} Month{'s' if months > 1 else ''})"
        click.echo(f"\n🔍 Analyzing repository (last {months} month{'s' if months > 1 else ''}): {os.path.abspath(repo_path)}\n")
    
    try:
        analyzer = CommitAnalyzer(repo_path)
        results = analyzer.analyze_repository(months=months)
        
        if not results:
            if months == 0:
                click.echo("ℹ️  No commits found in the repository.")
            else:
                click.echo(f"ℹ️  No commits found in the last {months} month{'s' if months > 1 else ''}.")
            return
        
        # Sort results
        sort_keys = {
            'value': 'value_score',
            'quality': 'quality_score',
            'difficulty': 'difficulty_score',
            'commits': 'commit_count'
        }
        sorted_results = sorted(
            results.items(), 
            key=lambda x: x[1][sort_keys[sort_by]], 
            reverse=True
        )
        
        if format == 'table':
            display_table(sorted_results, time_period_text)
        else:
            display_detailed(sorted_results, time_period_text)
        
        # Display summary
        display_summary(results, time_period_text)
        
    except ValueError as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Unexpected error: {str(e)}", err=True)
        raise click.Abort()


def display_table(results, time_period_text):
    """Display results in a compact table format."""
    headers = [
        'Author', 
        'Commits', 
        'Lines +', 
        'Lines -', 
        'Files', 
        'Quality', 
        'Difficulty', 
        'Value',
        'Work Style'
    ]
    
    rows = []
    for author, stats in results:
        rows.append([
            author,
            stats['commit_count'],
            stats['lines_added'],
            stats['lines_deleted'],
            stats['files_modified'],
            f"{stats['quality_score']:.1f}",
            f"{stats['difficulty_score']:.1f}",
            f"{stats['value_score']:.1f}",
            stats['work_style']
        ])
    
    click.echo(f"📊 Contributors {time_period_text}:\n")
    click.echo(tabulate(rows, headers=headers, tablefmt='grid'))


def display_detailed(results, time_period_text):
    """Display results in detailed format."""
    click.echo(f"👥 Contributors {time_period_text} - Detailed View:\n")
    
    for i, (author, stats) in enumerate(results, 1):
        click.echo(f"{'='*80}")
        click.echo(f"{i}. {author}")
        click.echo(f"{'='*80}")
        click.echo(f"  📈 Activity Metrics:")
        click.echo(f"     • Commits: {stats['commit_count']}")
        click.echo(f"     • Lines Added: {stats['lines_added']}")
        click.echo(f"     • Lines Deleted: {stats['lines_deleted']}")
        click.echo(f"     • Files Modified: {stats['files_modified']}")
        click.echo(f"     • Net Contribution: {stats['lines_added'] - stats['lines_deleted']} lines")
        click.echo()
        click.echo(f"  🎯 Performance Scores:")
        click.echo(f"     • Quality Score: {stats['quality_score']:.2f}/100")
        click.echo(f"     • Difficulty Score: {stats['difficulty_score']:.2f}/100")
        click.echo(f"     • Value Score: {stats['value_score']:.2f}/100")
        click.echo()
        click.echo(f"  💼 Work Style: {stats['work_style']}")
        click.echo()


def display_summary(results, time_period_text):
    """Display overall repository summary."""
    total_commits = sum(stats['commit_count'] for stats in results.values())
    total_lines_added = sum(stats['lines_added'] for stats in results.values())
    total_lines_deleted = sum(stats['lines_deleted'] for stats in results.values())
    total_files = sum(stats['files_modified'] for stats in results.values())
    
    avg_quality = sum(stats['quality_score'] for stats in results.values()) / len(results)
    avg_difficulty = sum(stats['difficulty_score'] for stats in results.values()) / len(results)
    avg_value = sum(stats['value_score'] for stats in results.values()) / len(results)
    
    click.echo(f"\n{'='*80}")
    click.echo(f"📋 OVERALL SUMMARY {time_period_text}")
    click.echo(f"{'='*80}")
    click.echo(f"  Total Contributors: {len(results)}")
    click.echo(f"  Total Commits: {total_commits}")
    click.echo(f"  Total Lines Added: {total_lines_added}")
    click.echo(f"  Total Lines Deleted: {total_lines_deleted}")
    click.echo(f"  Net Change: {total_lines_added - total_lines_deleted} lines")
    click.echo(f"  Total Files Modified: {total_files}")
    click.echo()
    click.echo(f"  Average Quality Score: {avg_quality:.2f}/100")
    click.echo(f"  Average Difficulty Score: {avg_difficulty:.2f}/100")
    click.echo(f"  Average Value Score: {avg_value:.2f}/100")
    click.echo(f"{'='*80}\n")


if __name__ == '__main__':
    analyze()
