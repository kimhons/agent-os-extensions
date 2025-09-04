# Git Branch Manager

The Git Branch Manager is a critical enhancement that provides advanced Git integration for Agent OS. It addresses the common challenges of managing Git branches when working with AI agents, such as preventing commits to the wrong branch and providing tools for project recovery.

## Key Features

- **Branch-Aware Context:** The manager provides different context to the AI based on the current Git branch, ensuring that the agent is always working with the correct information.
- **Branch Strategy Enforcement:** You can define and enforce a specific Git branching strategy, such as GitFlow or GitHub Flow, to ensure consistency across your team.
- **Pre-Commit Validation:** The manager can automatically validate the context before a commit is made, preventing common errors such as committing to the wrong branch.
- **Branch Recovery Tools:** If a commit is accidentally made to the wrong branch, the manager provides tools to easily move the commit to the correct branch.
- **Automated Branch Management:** The system can automatically create and switch to the appropriate branch for a given task, streamlining your development workflow.

## How It Works

The Git Branch Manager works by integrating with your project's Git repository to monitor the current branch and provide context-aware information to the AI. It uses a combination of Git hooks and CLI tools to enforce your branching strategy and prevent common errors.

When you start a new task, the manager can automatically create a new feature branch for you based on your defined branching strategy. As you work, the manager provides the AI with context that is specific to that branch, such as the associated spec and task description.

Before you commit your changes, the manager can run a pre-commit validation check to ensure that you are on the correct branch and that your commit message follows the correct format. If any issues are detected, the manager will warn you and provide suggestions for how to fix them.

## Usage

The Git Branch Manager is enabled by default in the enhanced version of Agent OS. You can configure its behavior in the `config/enhanced-config.yml` file.

To use the Git Branch Manager, you can run the `branch-manager.py` script:

```bash
# Get a report on the current branch status
python3 .agent-os/git-management/branch-manager.py --report

# Create a new branch for a task
python3 .agent-os/git-management/branch-manager.py --create-branch "your task description"

# Setup pre-commit hooks for validation
python3 .agent-os/git-management/branch-manager.py --setup-hooks
```

## Benefits

- **Prevents Common Git Errors:** The pre-commit validation and branch-aware context features help prevent common errors such as committing to the wrong branch or losing context when switching branches.
- **Improves Code Consistency:** The branch strategy enforcement feature ensures that all team members follow the same branching conventions, improving code consistency and making it easier to manage your project.
- **Streamlines Your Workflow:** The automated branch management features streamline your development workflow by automatically creating and switching to the appropriate branch for each task.
- **Provides Project Recovery Options:** The branch recovery tools provide a safety net in case of errors, allowing you to easily recover misplaced commits and get your project back on track.


