# MCP Orchestrator

The MCP (Model Context Protocol) Orchestrator is a powerful enhancement that allows Agent OS to seamlessly integrate with your existing development tools, including your 25+ MCP tools. It provides a system for discovering, managing, and orchestrating these tools to create powerful, automated development workflows.

## Key Features

- **Automatic Tool Discovery:** The orchestrator can automatically discover the MCP tools you have installed on your system, including those from Claude Desktop and VS Code.
- **Tool Management:** The system provides a centralized place to manage your tools, including their configurations and capabilities.
- **Workflow Orchestration:** You can create and execute complex workflows that combine multiple MCP tools to automate common development tasks.
- **Tool Recommendation:** The system can recommend the best tool for a given task based on its capabilities and your project's context.
- **Performance Monitoring:** The orchestrator can monitor the performance of your tools and workflows, providing insights for optimization.

## How It Works

The MCP Orchestrator works by scanning your system for MCP tools and creating a catalog of their capabilities. It then uses this catalog to provide you with a range of services, including tool recommendations, workflow orchestration, and performance monitoring.

When you start a new task, the orchestrator can recommend the best tool for the job based on the task description and your project's context. You can then use the orchestrator to execute the tool and get the results.

You can also create custom workflows that combine multiple tools to automate more complex tasks. For example, you could create a workflow that uses a file operation tool to read a file, a code analysis tool to analyze the code, and a Git tool to commit the changes.

## Usage

The MCP Orchestrator is enabled by default in the enhanced version of Agent OS. You can configure its behavior in the `config/enhanced-config.yml` file.

To use the MCP Orchestrator, you can run the `mcp-orchestrator.py` script:

```bash
# Discover the MCP tools on your system
python3 .agent-os/mcp-integration/mcp-orchestrator.py --discover

# Get a list of available tools
python3 .agent-os/mcp-integration/mcp-orchestrator.py --list-tools

# Get a recommendation for a task
python3 .agent-os/mcp-integration/mcp-orchestrator.py --recommend "your task description"
```

## Benefits

- **Seamless Tool Integration:** The orchestrator provides a seamless way to integrate your existing tools with Agent OS, creating a powerful, unified development environment.
- **Increased Automation:** The workflow orchestration feature allows you to automate complex development tasks, saving you time and effort.
- **Improved Efficiency:** The tool recommendation and performance monitoring features help you use your tools more efficiently, improving your overall development productivity.
- **Greater Flexibility:** The orchestrator is designed to be flexible and extensible, allowing you to easily add new tools and workflows as your needs change.


