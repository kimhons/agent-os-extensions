# Automatic MCP Tools Integration Guide

This guide explains how Agent OS Extensions automatically discovers and integrates your existing 25+ MCP tools during installation, making the process completely seamless.

## 🚀 Automatic Integration Process

When you run `./install-extensions.sh`, the system automatically:

1. **Discovers all your MCP tools** from multiple sources
2. **Tests their availability** and functionality
3. **Configures them for Agent OS integration**
4. **Creates workflows** that combine multiple tools
5. **Generates usage documentation** for each tool

## 🔍 Discovery Sources

The enhanced MCP orchestrator automatically scans these locations for your tools:

### 1. Claude Desktop MCP Tools
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `~/AppData/Roaming/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/claude-desktop/claude_desktop_config.json`

### 2. VS Code MCP Extensions
- `~/.vscode/extensions/`
- `~/.vscode-insiders/extensions/`
- Scans for extensions with MCP-related keywords

### 3. System-Wide MCP Tools
- `/usr/local/bin`, `/usr/bin`, `/opt`
- `~/.local/bin`, `~/bin`
- All directories in your `PATH` environment variable

### 4. Package Manager Tools
- **NPM**: Global packages with MCP patterns
- **pip**: Python packages with MCP patterns
- Automatically detects tools installed via package managers

### 5. Common MCP Directories
- `~/.mcp`, `~/mcp-tools`
- `~/.local/share/mcp`, `/opt/mcp`
- Project-specific: `./mcp-tools`, `./.mcp`

## 🛠️ What Gets Automatically Configured

For each discovered tool, the system automatically:

### Tool Information
- **Name and description**
- **Version detection**
- **Source identification** (Claude Desktop, VS Code, system, etc.)
- **Capability analysis** (file operations, git, database, web, etc.)
- **Command structure** for execution

### Integration Configuration
- **Agent OS command mapping** (e.g., `mcp-file-operations`)
- **Usage examples** based on capabilities
- **Integration type** and configuration
- **Availability testing** and status

### Workflow Creation
- **Capability-based grouping** of tools
- **Default workflows** for common tasks
- **Multi-tool orchestration** patterns

## 📊 Integration Report

After installation, you get a comprehensive report showing:

```bash
python3 .agent-os/mcp-integration/enhanced-mcp-orchestrator.py --report
```

**Sample Output:**
```
📊 MCP Tools Integration Report:
   Total Tools: 28
   By Source: {'claude-desktop': 15, 'vscode': 8, 'npm': 3, 'system': 2}
   By Status: {'configured': 25, 'available': 2, 'error': 1}
```

## 🔧 Viewing Your Integrated Tools

List all discovered and integrated tools:

```bash
python3 .agent-os/mcp-integration/enhanced-mcp-orchestrator.py --list-tools
```

**Sample Output:**
```
🛠️  Discovered MCP Tools (28 total):
   • file-operations (claude-desktop) - configured
   • git-manager (claude-desktop) - configured
   • database-query (vscode) - configured
   • web-scraper (npm) - configured
   • code-analyzer (system) - configured
   ...
```

## 🔄 Automatic Workflows

The system creates default workflows combining your tools:

### Code Review Workflow
Combines file operations + code analysis tools:
```json
{
  "name": "code_review",
  "description": "Comprehensive code review using multiple MCP tools",
  "tools": ["file-operations", "code-analyzer", "git-manager"],
  "steps": [
    {"action": "read_files", "tools": ["file-operations"]},
    {"action": "analyze_code", "tools": ["code-analyzer"]},
    {"action": "generate_report", "tools": ["file-operations"]}
  ]
}
```

### Git Workflow
Combines all git-related tools:
```json
{
  "name": "git_workflow",
  "description": "Enhanced git workflow with MCP tools",
  "tools": ["git-manager", "branch-helper"],
  "steps": [
    {"action": "check_status", "tools": ["git-manager"]},
    {"action": "create_branch", "tools": ["branch-helper"]},
    {"action": "commit_changes", "tools": ["git-manager"]}
  ]
}
```

## 🎯 Using Integrated Tools in Agent OS

Your MCP tools are now seamlessly integrated with Agent OS commands:

### Enhanced `/execute-tasks`
When you use `/execute-tasks`, the system automatically:
- **Selects appropriate MCP tools** based on the task
- **Orchestrates multiple tools** for complex operations
- **Provides tool-specific context** to the AI
- **Handles tool execution** and result integration

### Example Integration
```
Task: "Analyze the database schema and generate documentation"

Automatic tool selection:
1. database-query tool → Extract schema information
2. file-operations tool → Read existing documentation
3. markdown-generator tool → Create new documentation
4. git-manager tool → Commit the changes
```

## ⚙️ Configuration Options

Customize the integration in `.agent-os/config/enhanced-config.yml`:

```yaml
mcp_integration:
  enabled: true
  auto_discovery: true          # Automatically discover tools
  auto_configure: true          # Automatically configure discovered tools
  create_workflows: true        # Create default workflows
  tool_search_paths:           # Additional search paths
    - "/custom/mcp/tools"
    - "~/my-mcp-tools"
  discovery_timeout: 30        # Timeout for tool discovery (seconds)
  test_tools: true            # Test tool availability during discovery
```

## 🔍 Manual Re-Discovery

If you install new MCP tools after the initial setup, re-run discovery:

```bash
python3 .agent-os/mcp-integration/enhanced-mcp-orchestrator.py --auto-discover
```

This will:
- Discover any new tools
- Update existing tool configurations
- Create new workflows if applicable
- Update the integration report

## 🛠️ Tool Categories and Capabilities

The system automatically categorizes tools by capabilities:

### File Operations
- File reading/writing tools
- Filesystem navigation tools
- File manipulation utilities

### Git Operations
- Git command tools
- Branch management tools
- Repository analysis tools

### Database Operations
- Database query tools
- Schema analysis tools
- Data manipulation tools

### Web Operations
- HTTP request tools
- Web scraping tools
- API interaction tools

### Code Analysis
- Linting tools
- AST parsing tools
- Code quality tools

### Testing
- Test execution tools
- Coverage analysis tools
- Test generation tools

## 🚨 Troubleshooting

### Tool Not Discovered
If a tool isn't discovered automatically:

1. **Check the tool location** - Ensure it's in a standard location
2. **Verify tool naming** - Tool should contain MCP-related keywords
3. **Add custom search path** - Add the tool's directory to `enhanced-config.yml`
4. **Manual discovery** - Run discovery with verbose logging

### Tool Not Working
If a discovered tool shows as "error" status:

1. **Check tool availability** - Ensure the tool is properly installed
2. **Verify permissions** - Ensure the tool is executable
3. **Check dependencies** - Ensure all tool dependencies are installed
4. **Review logs** - Check `.agent-os/logs/mcp-orchestrator.log`

### Re-run Discovery
```bash
# Re-discover with verbose output
python3 .agent-os/mcp-integration/enhanced-mcp-orchestrator.py --auto-discover --verbose
```

## 📈 Benefits of Automatic Integration

### For You
- **Zero manual configuration** - Everything works out of the box
- **Immediate tool availability** - All tools ready to use after installation
- **Intelligent orchestration** - Tools work together automatically
- **Consistent interface** - All tools accessible through Agent OS

### For Your Workflow
- **Enhanced Agent OS commands** - `/execute-tasks` now uses all your tools
- **Automatic tool selection** - Best tool chosen for each task
- **Multi-tool workflows** - Complex tasks use multiple tools seamlessly
- **Context-aware execution** - Tools receive relevant project context

### For Large-Scale Development
- **Scalable tool management** - Handles 25+ tools effortlessly
- **Performance optimization** - Tools cached and optimized for speed
- **Error handling** - Graceful fallbacks when tools fail
- **Comprehensive logging** - Full audit trail of tool usage

## 🎉 Success Indicators

After installation, you should see:

✅ **All your MCP tools discovered** - Check with `--list-tools`  
✅ **Tools properly configured** - Status shows "configured"  
✅ **Workflows created** - Default workflows available  
✅ **Agent OS commands enhanced** - `/execute-tasks` uses your tools  
✅ **Integration report generated** - Comprehensive tool summary  

Your 25+ MCP tools are now seamlessly integrated with Agent OS, providing powerful capabilities for large-scale development without any manual configuration!

