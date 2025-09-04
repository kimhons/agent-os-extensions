#!/usr/bin/env python3
"""
Enhanced Agent OS Git Branch Manager and Project Recovery System
Manages git branches, prevents wrong-branch commits, and provides recovery tools
"""

import os
import json
import yaml
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import re

@dataclass
class BranchInfo:
    """Information about a git branch"""
    name: str
    is_current: bool
    last_commit: str
    last_commit_date: datetime
    ahead_behind: Tuple[int, int]  # (ahead, behind) relative to main/master
    purpose: str  # 'feature', 'hotfix', 'release', 'main', 'develop'
    associated_specs: List[str] = None

@dataclass
class CommitInfo:
    """Information about a commit"""
    hash: str
    message: str
    author: str
    date: datetime
    branch: str
    files_changed: List[str]

@dataclass
class BranchStrategy:
    """Git branching strategy configuration"""
    name: str  # 'gitflow', 'github-flow', 'custom'
    main_branch: str
    develop_branch: Optional[str]
    feature_prefix: str
    hotfix_prefix: str
    release_prefix: str
    auto_cleanup: bool

class GitBranchManager:
    """Manages git branches and provides recovery tools"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.agent_os_dir = self.project_root / ".agent-os"
        self.git_dir = self.agent_os_dir / "git-management"
        
        # Create directories
        self.git_dir.mkdir(parents=True, exist_ok=True)
        (self.git_dir / "strategies").mkdir(exist_ok=True)
        (self.git_dir / "templates").mkdir(exist_ok=True)
        (self.git_dir / "recovery").mkdir(exist_ok=True)
        
        # Setup logging
        self._setup_logging()
        
        # Load configuration
        self.config = self._load_config()
        self.branch_strategy = self._load_branch_strategy()
        
        # Git repository check
        self.git_repo_path = self._find_git_repo()
        if not self.git_repo_path:
            self.logger.warning("No git repository found")
        
        # Branch tracking
        self.branches: Dict[str, BranchInfo] = {}
        self.current_branch: Optional[str] = None
        
        # Initialize
        if self.git_repo_path:
            self._refresh_branch_info()
    
    def _setup_logging(self):
        """Setup logging for git branch manager"""
        log_dir = self.agent_os_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "git-branch-manager.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("GitBranchManager")
    
    def _load_config(self) -> Dict:
        """Load git management configuration"""
        config_path = self.agent_os_dir / "config" / "enhanced-config.yml"
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config.get('git_management', {})
        return {}
    
    def _load_branch_strategy(self) -> BranchStrategy:
        """Load or create branch strategy"""
        strategy_file = self.git_dir / "strategies" / "current-strategy.json"
        
        if strategy_file.exists():
            with open(strategy_file, 'r') as f:
                data = json.load(f)
                return BranchStrategy(**data)
        
        # Create default strategy
        default_strategy = BranchStrategy(
            name="gitflow",
            main_branch="main",
            develop_branch="develop",
            feature_prefix="feature/",
            hotfix_prefix="hotfix/",
            release_prefix="release/",
            auto_cleanup=True
        )
        
        self._save_branch_strategy(default_strategy)
        return default_strategy
    
    def _save_branch_strategy(self, strategy: BranchStrategy):
        """Save branch strategy to file"""
        strategy_file = self.git_dir / "strategies" / "current-strategy.json"
        
        with open(strategy_file, 'w') as f:
            json.dump(asdict(strategy), f, indent=2)
    
    def _find_git_repo(self) -> Optional[Path]:
        """Find the git repository root"""
        current = self.project_root
        
        while current != current.parent:
            if (current / ".git").exists():
                return current
            current = current.parent
        
        return None
    
    def _run_git_command(self, command: List[str], cwd: Optional[Path] = None) -> Tuple[bool, str]:
        """Run a git command and return success status and output"""
        if not cwd:
            cwd = self.git_repo_path
        
        try:
            result = subprocess.run(
                ["git"] + command,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                return True, result.stdout.strip()
            else:
                return False, result.stderr.strip()
                
        except Exception as e:
            return False, str(e)
    
    def _refresh_branch_info(self):
        """Refresh information about all branches"""
        if not self.git_repo_path:
            return
        
        # Get current branch
        success, current_branch = self._run_git_command(["branch", "--show-current"])
        if success:
            self.current_branch = current_branch
        
        # Get all branches
        success, branch_output = self._run_git_command(["branch", "-v"])
        if not success:
            self.logger.error(f"Failed to get branch info: {branch_output}")
            return
        
        self.branches = {}
        
        for line in branch_output.split('\n'):
            if not line.strip():
                continue
            
            # Parse branch line: "* main 1234567 Last commit message"
            parts = line.strip().split()
            if len(parts) < 3:
                continue
            
            is_current = line.startswith('*')
            branch_name = parts[1] if is_current else parts[0]
            commit_hash = parts[2] if is_current else parts[1]
            
            # Get ahead/behind info
            ahead_behind = self._get_ahead_behind(branch_name)
            
            # Get last commit date
            success, date_str = self._run_git_command([
                "log", "-1", "--format=%ci", branch_name
            ])
            
            try:
                last_commit_date = datetime.fromisoformat(date_str.replace(' ', 'T', 1)) if success else datetime.now()
            except:
                last_commit_date = datetime.now()
            
            # Determine branch purpose
            purpose = self._determine_branch_purpose(branch_name)
            
            branch_info = BranchInfo(
                name=branch_name,
                is_current=is_current,
                last_commit=commit_hash,
                last_commit_date=last_commit_date,
                ahead_behind=ahead_behind,
                purpose=purpose,
                associated_specs=self._get_associated_specs(branch_name)
            )
            
            self.branches[branch_name] = branch_info
    
    def _get_ahead_behind(self, branch_name: str) -> Tuple[int, int]:
        """Get how many commits ahead/behind a branch is relative to main"""
        main_branch = self.branch_strategy.main_branch
        
        success, output = self._run_git_command([
            "rev-list", "--left-right", "--count",
            f"{main_branch}...{branch_name}"
        ])
        
        if success and output:
            parts = output.split()
            if len(parts) == 2:
                return int(parts[1]), int(parts[0])  # (ahead, behind)
        
        return (0, 0)
    
    def _determine_branch_purpose(self, branch_name: str) -> str:
        """Determine the purpose of a branch based on its name"""
        if branch_name == self.branch_strategy.main_branch:
            return "main"
        elif branch_name == self.branch_strategy.develop_branch:
            return "develop"
        elif branch_name.startswith(self.branch_strategy.feature_prefix):
            return "feature"
        elif branch_name.startswith(self.branch_strategy.hotfix_prefix):
            return "hotfix"
        elif branch_name.startswith(self.branch_strategy.release_prefix):
            return "release"
        else:
            return "custom"
    
    def _get_associated_specs(self, branch_name: str) -> List[str]:
        """Get specs associated with a branch"""
        specs = []
        
        # Look for specs that might be related to this branch
        specs_dir = self.agent_os_dir / "specs"
        if specs_dir.exists():
            for spec_dir in specs_dir.iterdir():
                if spec_dir.is_dir():
                    spec_name = spec_dir.name
                    # Simple heuristic: if branch name contains part of spec name
                    if any(part in branch_name for part in spec_name.split('-')[2:]):
                        specs.append(spec_name)
        
        return specs
    
    def validate_commit_context(self, commit_message: str = "") -> Dict[str, Any]:
        """Validate that the current context is appropriate for committing"""
        validation = {
            "valid": True,
            "warnings": [],
            "errors": [],
            "suggestions": []
        }
        
        if not self.git_repo_path:
            validation["valid"] = False
            validation["errors"].append("No git repository found")
            return validation
        
        # Check if we're on the right branch
        current_branch = self.current_branch
        if not current_branch:
            validation["valid"] = False
            validation["errors"].append("Could not determine current branch")
            return validation
        
        # Check for uncommitted changes
        success, status_output = self._run_git_command(["status", "--porcelain"])
        if not success:
            validation["warnings"].append("Could not check git status")
        elif not status_output:
            validation["warnings"].append("No changes to commit")
        
        # Validate branch purpose vs changes
        branch_info = self.branches.get(current_branch)
        if branch_info:
            if branch_info.purpose == "main" and status_output:
                validation["warnings"].append("Committing directly to main branch")
                validation["suggestions"].append("Consider creating a feature branch")
            
            elif branch_info.purpose == "feature":
                # Check if feature branch is up to date with main
                if branch_info.ahead_behind[1] > 0:
                    validation["warnings"].append(f"Feature branch is {branch_info.ahead_behind[1]} commits behind main")
                    validation["suggestions"].append("Consider rebasing or merging main into feature branch")
        
        # Validate commit message
        if commit_message:
            if len(commit_message) < 10:
                validation["warnings"].append("Commit message is very short")
            
            if not re.match(r'^[A-Z]', commit_message):
                validation["suggestions"].append("Consider starting commit message with capital letter")
        
        return validation
    
    def suggest_branch_for_task(self, task_description: str, spec_name: str = "") -> str:
        """Suggest an appropriate branch name for a task"""
        # Clean task description for branch name
        clean_task = re.sub(r'[^a-zA-Z0-9\s-]', '', task_description.lower())
        clean_task = re.sub(r'\s+', '-', clean_task.strip())
        clean_task = clean_task[:50]  # Limit length
        
        # Determine branch type
        if "fix" in task_description.lower() or "bug" in task_description.lower():
            prefix = self.branch_strategy.hotfix_prefix
        elif "release" in task_description.lower():
            prefix = self.branch_strategy.release_prefix
        else:
            prefix = self.branch_strategy.feature_prefix
        
        # Include spec name if provided
        if spec_name:
            spec_part = spec_name.split('-')[-1] if '-' in spec_name else spec_name
            branch_name = f"{prefix}{spec_part}-{clean_task}"
        else:
            branch_name = f"{prefix}{clean_task}"
        
        return branch_name
    
    def create_branch_for_task(self, task_description: str, spec_name: str = "") -> Tuple[bool, str]:
        """Create a new branch for a task"""
        branch_name = self.suggest_branch_for_task(task_description, spec_name)
        
        # Check if branch already exists
        if branch_name in self.branches:
            return False, f"Branch '{branch_name}' already exists"
        
        # Create branch from appropriate base
        base_branch = self.branch_strategy.develop_branch or self.branch_strategy.main_branch
        
        success, output = self._run_git_command(["checkout", "-b", branch_name, base_branch])
        
        if success:
            self._refresh_branch_info()
            self.logger.info(f"Created branch: {branch_name}")
            
            # Save branch context
            self._save_branch_context(branch_name, task_description, spec_name)
            
            return True, f"Created branch: {branch_name}"
        else:
            return False, f"Failed to create branch: {output}"
    
    def _save_branch_context(self, branch_name: str, task_description: str, spec_name: str):
        """Save context information for a branch"""
        context_file = self.git_dir / "recovery" / f"{branch_name}.json"
        
        context = {
            "branch_name": branch_name,
            "task_description": task_description,
            "spec_name": spec_name,
            "created_date": datetime.now().isoformat(),
            "base_branch": self.branch_strategy.develop_branch or self.branch_strategy.main_branch
        }
        
        with open(context_file, 'w') as f:
            json.dump(context, f, indent=2)
    
    def switch_to_appropriate_branch(self, task_description: str, spec_name: str = "") -> Tuple[bool, str]:
        """Switch to the most appropriate branch for a task"""
        # Look for existing branch related to the task/spec
        for branch_name, branch_info in self.branches.items():
            if spec_name and spec_name in (branch_info.associated_specs or []):
                success, output = self._run_git_command(["checkout", branch_name])
                if success:
                    self.current_branch = branch_name
                    return True, f"Switched to existing branch: {branch_name}"
                else:
                    return False, f"Failed to switch to branch: {output}"
        
        # Create new branch if no appropriate one exists
        return self.create_branch_for_task(task_description, spec_name)
    
    def recover_misplaced_commits(self, target_branch: str, commit_hashes: List[str]) -> Tuple[bool, str]:
        """Recover commits that were made on the wrong branch"""
        if not commit_hashes:
            return False, "No commit hashes provided"
        
        # Verify target branch exists
        if target_branch not in self.branches:
            return False, f"Target branch '{target_branch}' does not exist"
        
        # Switch to target branch
        success, output = self._run_git_command(["checkout", target_branch])
        if not success:
            return False, f"Failed to switch to target branch: {output}"
        
        # Cherry-pick commits
        for commit_hash in commit_hashes:
            success, output = self._run_git_command(["cherry-pick", commit_hash])
            if not success:
                self.logger.error(f"Failed to cherry-pick {commit_hash}: {output}")
                return False, f"Failed to cherry-pick {commit_hash}: {output}"
        
        self.logger.info(f"Successfully recovered {len(commit_hashes)} commits to {target_branch}")
        return True, f"Successfully recovered {len(commit_hashes)} commits to {target_branch}"
    
    def get_recent_commits(self, branch: str = "", limit: int = 10) -> List[CommitInfo]:
        """Get recent commits from a branch"""
        if not branch:
            branch = self.current_branch or self.branch_strategy.main_branch
        
        success, output = self._run_git_command([
            "log", f"-{limit}", "--format=%H|%s|%an|%ci", branch
        ])
        
        if not success:
            return []
        
        commits = []
        for line in output.split('\n'):
            if not line.strip():
                continue
            
            parts = line.split('|')
            if len(parts) >= 4:
                # Get files changed in this commit
                success, files_output = self._run_git_command([
                    "diff-tree", "--no-commit-id", "--name-only", "-r", parts[0]
                ])
                
                files_changed = files_output.split('\n') if success else []
                
                try:
                    commit_date = datetime.fromisoformat(parts[3].replace(' ', 'T', 1))
                except:
                    commit_date = datetime.now()
                
                commit = CommitInfo(
                    hash=parts[0],
                    message=parts[1],
                    author=parts[2],
                    date=commit_date,
                    branch=branch,
                    files_changed=files_changed
                )
                commits.append(commit)
        
        return commits
    
    def generate_branch_report(self) -> str:
        """Generate a comprehensive branch status report"""
        report = f"""# Git Branch Status Report

## Current Branch: {self.current_branch or 'Unknown'}

## Branch Strategy: {self.branch_strategy.name}
- Main Branch: {self.branch_strategy.main_branch}
- Develop Branch: {self.branch_strategy.develop_branch or 'None'}
- Feature Prefix: {self.branch_strategy.feature_prefix}
- Hotfix Prefix: {self.branch_strategy.hotfix_prefix}

## All Branches
"""
        
        for branch_name, branch_info in self.branches.items():
            current_marker = "👉 " if branch_info.is_current else "   "
            ahead, behind = branch_info.ahead_behind
            
            report += f"{current_marker}**{branch_name}** ({branch_info.purpose})\n"
            report += f"   Last Commit: {branch_info.last_commit[:8]} - {branch_info.last_commit_date.strftime('%Y-%m-%d %H:%M')}\n"
            
            if ahead > 0 or behind > 0:
                report += f"   Status: {ahead} ahead, {behind} behind main\n"
            
            if branch_info.associated_specs:
                report += f"   Associated Specs: {', '.join(branch_info.associated_specs)}\n"
            
            report += "\n"
        
        # Add recent commits
        recent_commits = self.get_recent_commits(limit=5)
        if recent_commits:
            report += "## Recent Commits\n"
            for commit in recent_commits:
                report += f"- {commit.hash[:8]} - {commit.message} ({commit.author})\n"
        
        return report
    
    def setup_pre_commit_hooks(self) -> bool:
        """Setup pre-commit hooks for validation"""
        if not self.git_repo_path:
            return False
        
        hooks_dir = self.git_repo_path / ".git" / "hooks"
        pre_commit_hook = hooks_dir / "pre-commit"
        
        hook_script = f"""#!/bin/bash
# Agent OS Enhanced Pre-commit Hook

# Run branch validation
python3 "{self.git_dir / 'branch-manager.py'}" --validate-commit

if [ $? -ne 0 ]; then
    echo "❌ Pre-commit validation failed"
    exit 1
fi

echo "✅ Pre-commit validation passed"
exit 0
"""
        
        try:
            with open(pre_commit_hook, 'w') as f:
                f.write(hook_script)
            
            # Make executable
            os.chmod(pre_commit_hook, 0o755)
            
            self.logger.info("Pre-commit hooks installed")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to install pre-commit hooks: {e}")
            return False

def main():
    """CLI interface for git branch manager"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Agent OS Git Branch Manager")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--create-branch", help="Create branch for task description")
    parser.add_argument("--spec-name", help="Associated spec name")
    parser.add_argument("--switch-branch", help="Switch to appropriate branch for task")
    parser.add_argument("--validate-commit", action="store_true", help="Validate current commit context")
    parser.add_argument("--report", action="store_true", help="Generate branch status report")
    parser.add_argument("--setup-hooks", action="store_true", help="Setup pre-commit hooks")
    parser.add_argument("--recover-commits", nargs="+", help="Recover commits to current branch")
    
    args = parser.parse_args()
    
    manager = GitBranchManager(args.project_root)
    
    if args.create_branch:
        success, message = manager.create_branch_for_task(args.create_branch, args.spec_name or "")
        print(f"{'✅' if success else '❌'} {message}")
    
    if args.switch_branch:
        success, message = manager.switch_to_appropriate_branch(args.switch_branch, args.spec_name or "")
        print(f"{'✅' if success else '❌'} {message}")
    
    if args.validate_commit:
        validation = manager.validate_commit_context()
        if validation["valid"]:
            print("✅ Commit context is valid")
        else:
            print("❌ Commit context validation failed")
            for error in validation["errors"]:
                print(f"   Error: {error}")
        
        for warning in validation["warnings"]:
            print(f"   ⚠️ Warning: {warning}")
        
        for suggestion in validation["suggestions"]:
            print(f"   💡 Suggestion: {suggestion}")
    
    if args.report:
        print(manager.generate_branch_report())
    
    if args.setup_hooks:
        success = manager.setup_pre_commit_hooks()
        print(f"{'✅' if success else '❌'} Pre-commit hooks setup")
    
    if args.recover_commits:
        current_branch = manager.current_branch
        if current_branch:
            success, message = manager.recover_misplaced_commits(current_branch, args.recover_commits)
            print(f"{'✅' if success else '❌'} {message}")
        else:
            print("❌ No current branch detected")

if __name__ == "__main__":
    main()

