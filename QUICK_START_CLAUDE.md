# Quick Start Guide for Claude Desktop Users

Get Agent OS Extensions running in Claude Desktop in under 5 minutes with automatic MCP tools integration.

## ⚡ 5-Minute Setup

### 1. Open Claude Desktop and Navigate to Your Project

```bash
# Go to your project directory (or create one)
cd /path/to/your/project
```

### 2. Install Agent OS Extensions

```bash
# Clone and install in one command
git clone https://github.com/kimhons/agent-os-extensions.git && cd agent-os-extensions && ./install-extensions.sh
```

### 3. Verify Installation

```bash
# Check your MCP tools are integrated
python3 .agent-os/mcp-integration/enhanced-mcp-orchestrator.py --list-tools
```

**That's it!** Your Claude Desktop MCP tools are now integrated with enhanced Agent OS.

## 🚀 Immediate Usage

### Use Enhanced Agent OS Commands

```bash
# These commands now use your MCP tools automatically:
/analyze-product    # + Auto tech stack detection
/create-spec       # + Enhanced context management  
/create-tasks      # + Smart context loading
/execute-tasks     # + Automatic MCP tool integration
```

### Example: Complete a Failed App

```bash
# 1. Navigate to your incomplete project
cd ~/projects/my-failed-app

# 2. Install extensions
git clone https://github.com/kimhons/agent-os-extensions.git && cd agent-os-extensions && ./install-extensions.sh

# 3. Analyze and continue development
/analyze-product
/create-spec
/create-tasks
/execute-tasks

# Your filesystem, git, and other MCP tools work automatically!
```

## 🎯 What You Get Instantly

✅ **All your Claude Desktop MCP tools** automatically integrated  
✅ **Large codebase support** (300k+ LOC) without context overflow  
✅ **Automatic tool selection** based on task requirements  
✅ **Multi-tool workflows** orchestrated seamlessly  
✅ **Enhanced Agent OS commands** with your existing tools  

## 📊 Quick Verification Commands

```bash
# See all integrated tools
python3 .agent-os/mcp-integration/enhanced-mcp-orchestrator.py --list-tools

# View integration report  
python3 .agent-os/mcp-integration/enhanced-mcp-orchestrator.py --report

# Check codebase analysis
python3 .agent-os/codebase-analysis/codebase-analyzer.py --report
```

## 🔧 Common Claude Desktop MCP Tools Automatically Integrated

- **filesystem** → File operations in `/execute-tasks`
- **brave-search** → Web research in `/analyze-product`  
- **mcp-server-git** → Git operations across all commands
- **postgres/sqlite** → Database operations when needed
- **And all your other MCP tools!**

## 🎉 Ready to Build!

Your Claude Desktop now has enhanced Agent OS with automatic MCP integration. Continue using Agent OS as normal, but now with superpowers for large-scale development!

For detailed instructions, see [CLAUDE_DESKTOP_INSTALLATION.md](CLAUDE_DESKTOP_INSTALLATION.md)

