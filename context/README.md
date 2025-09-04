# Smart Context Manager

The Smart Context Manager is a core enhancement to Agent OS that addresses the critical challenge of managing context when working with large language models (LLMs) on complex codebases. It provides a sophisticated system for loading, monitoring, and optimizing the context provided to the AI, ensuring that the agent has the right information at the right time without exceeding its context window.

## Key Features

- **Smart Context Loading:** Instead of loading all context files at once, the manager intelligently selects the most relevant files based on the current task, file type, and recent activity.
- **Context Size Monitoring:** The manager continuously tracks the size of the current context and warns you when it approaches the LLM's limit, preventing context overflow and errors.
- **Incremental Context Building:** Context is built progressively as needed, rather than all at once, which is more efficient for large projects.
- **Context Caching:** Frequently used context items are cached for faster access, improving performance.
- **Relevance Scoring:** Each context item is assigned a relevance score based on its relationship to the current task, allowing the system to prioritize the most important information.
- **Automated Context Optimization:** The manager can automatically remove low-relevance items from the context to make room for more important information.

## How It Works

The Smart Context Manager works by creating a database of all potential context items in your project, including source code files, documentation, and Agent OS standards. When you start a new task, the manager analyzes the task description and selects a subset of the most relevant context items to provide to the AI.

As you work, the manager monitors the context and dynamically adjusts it based on your actions. For example, if you open a new file, the manager will add it to the context. If the context becomes too large, the manager will remove the least relevant items to make room.

## Usage

The Smart Context Manager is enabled by default in the enhanced version of Agent OS. You can configure its behavior in the `config/enhanced-config.yml` file.

To interact with the context manager directly, you can use the `context-manager.py` script:

```bash
# Get a report on the current context
python3 .agent-os/context/context-manager.py --report

# Add a file to the context for a specific task
python3 .agent-os/context/context-manager.py --add-file path/to/your/file.py --task "your task description"

# Optimize the context for a specific task
python3 .agent-os/context/context-manager.py --optimize --task "your task description"
```

## Benefits

- **Prevents Context Loss:** By intelligently managing the context, the manager ensures that the AI always has the information it needs to complete the task, reducing the likelihood of errors and code duplication.
- **Improves Performance:** The context caching and incremental loading features significantly improve the performance of the system, especially on large projects.
- **Increases Accuracy:** By providing the AI with a more focused and relevant context, the manager helps the agent generate more accurate and consistent code.
- **Reduces Manual Effort:** The automated context management features reduce the need for you to manually manage the context provided to the AI, saving you time and effort.


