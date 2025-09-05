# Agent OS Extensions - Claude Desktop Installation Guide

Complete step-by-step instructions for installing Agent OS Extensions in Claude Desktop (Claude Code) to enhance your large-scale development workflow with automatic MCP tools integration.

## 📋 Prerequisites

Before starting, ensure you have:
- ✅ **Claude Desktop** installed and working
- ✅ **Python 3.8+** installed on your system
- ✅ **Git** installed (for Git-related features)
- ✅ **Your existing MCP tools** configured in Claude Desktop
- ✅ **A project directory** where you want to use enhanced Agent OS

## 🚀 Step-by-Step Installation

### Step 1: Navigate to Your Project Directory

In Claude Desktop, open a new conversation and navigate to your project:

```bash
# Navigate to your project directory
cd /path/to/your/project

# Or create a new project directory
mkdir my-enhanced-project
cd my-enhanced-project
```

**Example for different scenarios:**
```bash
# For an existing failed app you want to complete
cd ~/projects/my-failed-app

# For a new large-scale project
mkdir ~/projects/enterprise-app
cd ~/projects/enterprise-app

# For a microservices project
cd ~/projects/microservices-platform
```

### Step 2: Clone Agent OS Extensions

```bash
# Clone the Agent OS Extensions repository
git clone https://github.com/kimhons/agent-os-extensions.git

# Navigate into the extensions directory
cd agent-os-extensions
```

### Step 3: Run the Automatic Installation

```bash
# Make the installation script executable
chmod +x install-extensions.sh

# Run the installation (this will automatically discover your MCP tools)
./install-extensions.sh
```

**What happens during installation:**
- ✅ Preserves any existing Agent OS setup
- ✅ Auto-detects your project's tech stack
- ✅ **Automatically discovers all your Claude Desktop MCP tools**
- ✅ Configures tools for Agent OS integration
- ✅ Creates workflows combining multiple tools
- ✅ Analyzes your existing codebase (if any)
- ✅ Sets up Git hooks for branch management

### Step 4: Verify Installation

After installation completes, verify everything is working:

```bash
# Check discovered MCP tools
python3 .agent-os/mcp-integration/enhanced-mcp-orchestrator.py --list-tools

# View integration report
python3 .agent-os/mcp-integration/enhanced-mcp-orchestrator.py --report

# Check codebase analysis (if you have existing code)
python3 .agent-os/codebase-analysis/codebase-analyzer.py --report
```

**Expected output example:**
```
🛠️  Discovered MCP Tools (15 total):
   • filesystem (claude-desktop) - configured
   • brave-search (claude-desktop) - configured
   • mcp-server-git (claude-desktop) - configured
   • postgres (claude-desktop) - configured
   • sqlite (claude-desktop) - configured
   ...

📊 MCP Tools Integration Report:
   Total Tools: 15
   By Source: {'claude-desktop': 15}
   By Status: {'configured': 13, 'available': 2}
```

## 🎯 Using Enhanced Agent OS in Claude Desktop

### Basic Usage (Same as Original Agent OS)

Your existing Agent OS workflow remains unchanged:

```bash
# Analyze your product (now with auto tech stack detection)
/analyze-product

# Create specifications (now with enhanced context management)
/create-spec

# Create tasks (now with smart context loading)
/create-tasks

# Execute tasks (now with automatic MCP tool integration)
/execute-tasks
```

### Enhanced Features in Action

#### 1. Large Codebase Support

For projects with 300k+ lines of code:

```bash
# The context manager automatically prevents overflow
/create-tasks

# Smart context loading ensures relevant information only
# No more "context too large" errors
```

#### 2. Automatic MCP Tool Integration

When you use `/execute-tasks`, your MCP tools are automatically used:

```bash
# Example: Task requires file operations
/execute-tasks

# System automatically:
# 1. Selects your filesystem MCP tool
# 2. Uses it for file operations
# 3. Integrates results seamlessly
# 4. No manual tool selection needed
```

#### 3. Multi-Tool Workflows

For complex tasks requiring multiple tools:

```bash
# Example: "Analyze database and update documentation"
/execute-tasks

# System automatically orchestrates:
# 1. postgres MCP tool → Extract schema
# 2. filesystem MCP tool → Read existing docs
# 3. git MCP tool → Create branch
# 4. filesystem MCP tool → Write new docs
# 5. git MCP tool → Commit changes
```

## 🔧 Configuration for Claude Desktop

### Viewing Your Claude Desktop MCP Tools

Check what tools were discovered from your Claude Desktop config:

```bash
# Show tools discovered from Claude Desktop specifically
python3 .agent-os/mcp-integration/enhanced-mcp-orchestrator.py --list-tools | grep "claude-desktop"
```

### Claude Desktop Config Location

The system automatically reads your MCP tools from:

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
~/AppData/Roaming/Claude/claude_desktop_config.json
```

**Linux:**
```
~/.config/claude-desktop/claude_desktop_config.json
```

### Customizing Integration

Edit the enhanced configuration:

```bash
# Open configuration file
nano .agent-os/config/enhanced-config.yml
```

**Key settings for Claude Desktop users:**
```yaml
mcp_integration:
  enabled: true
  auto_discovery: true
  auto_configure: true
  create_workflows: true
  
context_management:
  enabled: true
  max_context_size: 180000    # Adjust based on your Claude model
  warning_threshold: 150000
  
tech_stack_detection:
  enabled: true
  auto_detect: true
```

## 📊 Monitoring and Debugging

### Check Logs

If you encounter issues:

```bash
# View MCP orchestrator logs
tail -f .agent-os/logs/mcp-orchestrator.log

# View context manager logs
tail -f .agent-os/logs/context-manager.log

# View all logs
ls -la .agent-os/logs/
```

### Re-run Discovery

If you add new MCP tools to Claude Desktop:

```bash
# Re-discover and integrate new tools
python3 .agent-os/mcp-integration/enhanced-mcp-orchestrator.py --auto-discover
```

### Test Individual Tools

Test if a specific MCP tool is working:

```bash
# Test filesystem tool (example)
echo '{"method": "tools/list"}' | npx @modelcontextprotocol/server-filesystem /path/to/directory

# Check tool status in Agent OS
python3 .agent-os/mcp-integration/enhanced-mcp-orchestrator.py --report
```

## 🎯 Practical Examples for Claude Desktop

### Example 1: Completing a Failed Large Application

```bash
# 1. Navigate to your failed project
cd ~/projects/my-failed-app

# 2. Install extensions
git clone https://github.com/kimhons/agent-os-extensions.git
cd agent-os-extensions
./install-extensions.sh

# 3. Analyze what you have
python3 .agent-os/codebase-analysis/codebase-analyzer.py --analyze --suggestions

# 4. Use enhanced Agent OS
/analyze-product
/create-spec
/create-tasks
/execute-tasks

# Your MCP tools (filesystem, git, etc.) are automatically used
```

### Example 2: Starting a New Large Project

```bash
# 1. Create project directory
mkdir ~/projects/enterprise-app
cd ~/projects/enterprise-app

# 2. Install extensions
git clone https://github.com/kimhons/agent-os-extensions.git
cd agent-os-extensions
./install-extensions.sh

# 3. Begin development with enhanced capabilities
/analyze-product
# (System auto-detects you're starting fresh)

/create-spec
# (Uses appropriate standards for detected tech stack)

/create-tasks
# (Smart context management prevents overflow)

/execute-tasks
# (Automatically uses your MCP tools)
```

### Example 3: Multi-Technology Project

```bash
# For projects with multiple tech stacks (frontend/backend/mobile)
cd ~/projects/full-stack-app

# Install extensions
git clone https://github.com/kimhons/agent-os-extensions.git
cd agent-os-extensions
./install-extensions.sh

# System automatically detects:
# - React frontend
# - Node.js backend  
# - PostgreSQL database
# - And generates appropriate standards for each

# Your MCP tools work across all technologies
```

## 🔄 Workflow Integration

### Enhanced Agent OS Commands in Claude Desktop

| Original Command | Enhanced Capabilities |
|------------------|----------------------|
| `/analyze-product` | + Auto tech stack detection<br>+ MCP tool integration for research |
| `/create-spec` | + Tech stack-aware standards<br>+ Context optimization |
| `/create-tasks` | + Smart context loading<br>+ Duplication prevention |
| `/execute-tasks` | + Automatic MCP tool selection<br>+ Multi-tool orchestration |

### MCP Tool Workflows

Your Claude Desktop MCP tools now work together automatically:

**File Operations + Git Workflow:**
```
Task: "Refactor authentication module"
→ filesystem tool: Read current auth files
→ git tool: Create feature branch
→ filesystem tool: Write refactored code
→ git tool: Commit changes
```

**Database + Documentation Workflow:**
```
Task: "Document database schema"
→ postgres tool: Extract schema information
→ filesystem tool: Read existing documentation
→ filesystem tool: Generate new documentation
→ git tool: Commit documentation updates
```

## 🚨 Troubleshooting

### Common Issues in Claude Desktop

**Issue: "No MCP tools discovered"**
```bash
# Check Claude Desktop config exists
ls -la ~/Library/Application\ Support/Claude/claude_desktop_config.json  # macOS
ls -la ~/.config/claude-desktop/claude_desktop_config.json              # Linux

# Manually re-run discovery
python3 .agent-os/mcp-integration/enhanced-mcp-orchestrator.py --auto-discover
```

**Issue: "Context too large" errors**
```bash
# Adjust context limits
nano .agent-os/config/enhanced-config.yml

# Set smaller context size:
context_management:
  max_context_size: 120000  # Reduce if needed
```

**Issue: "Tool not working"**
```bash
# Test individual MCP tool
# (Use the same command you have in claude_desktop_config.json)

# Check tool status
python3 .agent-os/mcp-integration/enhanced-mcp-orchestrator.py --report
```

## ✅ Success Checklist

After installation, you should have:

- [ ] **Agent OS Extensions installed** in your project
- [ ] **All Claude Desktop MCP tools discovered** and configured
- [ ] **Enhanced Agent OS commands** working with your tools
- [ ] **Context management** preventing overflow in large codebases
- [ ] **Tech stack detection** working for your project
- [ ] **Git branch management** set up (if using Git)
- [ ] **Codebase analysis** completed (if existing code)

## 🎉 You're Ready!

Your Claude Desktop now has enhanced Agent OS capabilities:

- ✅ **Handle large codebases** (300k+ LOC) without context issues
- ✅ **Automatic MCP tool integration** with all your existing tools
- ✅ **Intelligent workflows** combining multiple tools
- ✅ **Enhanced context management** for better AI responses
- ✅ **Tech stack awareness** for appropriate standards
- ✅ **Git branch safety** preventing wrong commits

Continue using Agent OS as before, but now with superpowers for large-scale development! 🚀

