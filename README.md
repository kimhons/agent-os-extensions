# Agent OS Extensions for Large-Scale Development

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Agent OS Compatible](https://img.shields.io/badge/Agent%20OS-Compatible-green.svg)](https://buildermethods.com/agent-os)

Powerful extensions for [Agent OS](https://buildermethods.com/agent-os) that enable AI agents to handle large-scale applications (300k+ LOC), prevent context loss, manage diverse tech stacks, and integrate with your existing development tools.

## 🎯 Problem Solved

If you've experienced:
- ❌ **Large applications that AI agents couldn't complete** due to context limitations
- ❌ **Code duplication** because agents lost track of existing functionality  
- ❌ **Wrong branch commits** due to lost context about Git workflow
- ❌ **Inconsistent behavior** across projects with different tech stacks
- ❌ **Fragmented tooling** with 25+ MCP tools that don't work together

**Agent OS Extensions** solves these problems while preserving all your existing Agent OS functionality.

## ✨ What This Adds to Agent OS

### 🧠 Smart Context Manager
- **Prevents context overflow** in large codebases (300k+ LOC)
- **Intelligent relevance scoring** ensures AI gets the right information
- **Real-time monitoring** with configurable size limits and warnings
- **Task-specific optimization** loads only what's needed for current work

### 🔧 Tech Stack Detector  
- **Automatic detection** of programming languages, frameworks, and tools
- **Dynamic standards generation** appropriate for each tech stack
- **Multi-stack support** for microservices and complex architectures
- **Validation** ensures standards match actual project setup

### 🌿 Git Branch Manager
- **Pre-commit validation** prevents commits to wrong branches
- **Branch-aware context** provides different information per branch
- **Automated branch creation** with proper naming conventions
- **Commit recovery tools** for moving misplaced commits

### 📊 Codebase Analyzer
- **Deep code understanding** maps structure and dependencies
- **Duplication detection** prevents recreating existing functionality
- **Complexity metrics** identifies refactoring opportunities
- **Architecture insights** for better design decisions

### 🛠️ MCP Orchestrator
- **Automatic tool discovery** finds your existing MCP tools during installation
- **Seamless integration** configures all tools for Agent OS automatically
- **Intelligent workflows** combines multiple tools for powerful automation
- **Zero configuration** - your 25+ MCP tools work immediately after installation

## 🚀 Quick Start

### Prerequisites
- [Agent OS](https://buildermethods.com/agent-os) (recommended but not required)
- Python 3.8+
- Git (for Git-related features)
- Your existing MCP tools

### Installation

1. **Clone this repository to your project:**
   ```bash
   git clone https://github.com/[username]/agent-os-extensions.git
   cd agent-os-extensions
   ```

2. **Run the installation script:**
   ```bash
   ./install-extensions.sh
   ```

3. **Verify installation:**
   ```bash
   python3 .agent-os/codebase-analysis/codebase-analyzer.py --report
   python3 .agent-os/git-management/branch-manager.py --report
   python3 .agent-os/context/context-manager.py --report
   ```

The installation script:
- ✅ Preserves your existing Agent OS setup
- ✅ Adds extensions alongside current functionality  
- ✅ Auto-detects your project's tech stack
- ✅ **Automatically discovers and integrates all your MCP tools**
- ✅ Analyzes your codebase structure
- ✅ Sets up Git hooks for branch management
- ✅ **Creates workflows combining your MCP tools**

## 📖 How It Enhances Agent OS

### Enhanced Existing Commands

Your familiar Agent OS commands now have superpowers:

#### `/create-spec` → Enhanced with Tech Stack Detection
- **Before:** Manual tech stack configuration
- **After:** Automatic detection and appropriate standards generation

#### `/create-tasks` → Enhanced with Smart Context  
- **Before:** Static context loading that could overflow
- **After:** Intelligent context management with relevance scoring

#### `/execute-tasks` → Enhanced with Tool Integration
- **Before:** Basic task execution
- **After:** MCP tool orchestration, branch management, duplication prevention

### New Capabilities

Access advanced features through CLI tools:

```bash
# Analyze your codebase for insights
python3 .agent-os/codebase-analysis/codebase-analyzer.py --analyze --report

# Manage Git branches intelligently  
python3 .agent-os/git-management/branch-manager.py --create-branch "implement user auth"

# Optimize context for specific tasks
python3 .agent-os/context/context-manager.py --optimize --task "fix payment bug"

# Orchestrate your MCP tools
python3 .agent-os/mcp-integration/mcp-orchestrator.py --list-tools --recommend "code review"
```

## 🏗️ Architecture

```
Your Project
├── .agent-os/                    (Enhanced Agent OS)
│   ├── commands/                 (Original - unchanged)
│   ├── instructions/             (Original - unchanged)
│   ├── standards/                (Original + auto-generated)
│   ├── context/                  (NEW: Smart Context Manager)
│   ├── tech-stack/               (NEW: Tech Stack Detector)
│   ├── git-management/           (NEW: Git Branch Manager)
│   ├── codebase-analysis/        (NEW: Codebase Analyzer)
│   ├── mcp-integration/          (NEW: MCP Orchestrator)
│   └── config/                   (NEW: Enhanced Configuration)
└── your-project-files...
```

## 🎮 Usage Examples

### Completing a Large, Failed Application

```bash
# 1. Install extensions in your project
./install-extensions.sh

# 2. Analyze what you have
python3 .agent-os/codebase-analysis/codebase-analyzer.py --analyze --suggestions

# 3. Create proper branch for completion work
python3 .agent-os/git-management/branch-manager.py --create-branch "complete user authentication"

# 4. Optimize context for the specific task
python3 .agent-os/context/context-manager.py --optimize --task "complete user authentication system"

# 5. Use enhanced Agent OS commands
# /create-spec (now with full codebase understanding)
# /create-tasks (now with smart context management)  
# /execute-tasks (now with duplication prevention)
```

### Working with Multiple Tech Stacks

```bash
# Auto-detect different stacks in microservices
python3 .agent-os/tech-stack/stack-detector.py --detect --project-root ./frontend
python3 .agent-os/tech-stack/stack-detector.py --detect --project-root ./backend  
python3 .agent-os/tech-stack/stack-detector.py --detect --project-root ./mobile

# Each gets appropriate standards automatically
```

### Automatic MCP Tools Integration

Your 25+ MCP tools are automatically discovered and integrated:

```bash
# View all your integrated tools (automatic after installation)
python3 .agent-os/mcp-integration/enhanced-mcp-orchestrator.py --list-tools

# See integration report
python3 .agent-os/mcp-integration/enhanced-mcp-orchestrator.py --report

# Your tools are now available in Agent OS commands automatically
# /execute-tasks will use appropriate tools based on the task
```

## ⚙️ Configuration

Customize behavior in `.agent-os/config/enhanced-config.yml`:

```yaml
context_management:
  enabled: true
  max_context_size: 180000      # Adjust for your model
  warning_threshold: 150000
  cache_enabled: true

tech_stack_detection:
  enabled: true
  auto_detect: true
  custom_patterns: []

git_management:
  enabled: true
  branch_strategy: "gitflow"    # or "github-flow", "custom"
  auto_cleanup: true

codebase_analysis:
  enabled: true
  max_analysis_files: 10000
  complexity_threshold: 25.0

mcp_integration:
  enabled: true
  auto_discovery: true
  workflow_timeout: 300
```

## 🔧 Extension Details

### Smart Context Manager
- **File:** `.agent-os/context/context-manager.py`
- **Purpose:** Prevents context overflow and optimizes relevance
- **Key Features:** Size monitoring, relevance scoring, task-specific optimization
- **Usage:** Automatic enhancement of Agent OS commands + CLI tool

### Tech Stack Detector  
- **File:** `.agent-os/tech-stack/stack-detector.py`
- **Purpose:** Auto-detects project technologies and generates standards
- **Supports:** 15+ languages, major frameworks, databases, build tools
- **Usage:** Automatic detection during installation + manual CLI

### Git Branch Manager
- **File:** `.agent-os/git-management/branch-manager.py`  
- **Purpose:** Advanced Git workflow management
- **Features:** Pre-commit hooks, branch validation, commit recovery
- **Usage:** Automatic Git integration + CLI for manual operations

### Codebase Analyzer
- **File:** `.agent-os/codebase-analysis/codebase-analyzer.py`
- **Purpose:** Deep understanding of large codebases
- **Capabilities:** Dependency mapping, duplication detection, complexity analysis
- **Usage:** CLI tool for analysis and reporting

### MCP Orchestrator
- **File:** `.agent-os/mcp-integration/mcp-orchestrator.py`
- **Purpose:** Discovers and orchestrates MCP tools
- **Features:** Auto-discovery, workflow creation, performance monitoring
- **Usage:** CLI tool for tool management and workflow execution

## 🐛 Troubleshooting

### Common Issues

**Context Overflow:**
```bash
python3 .agent-os/context/context-manager.py --optimize --task "your current task"
```

**Wrong Branch Commits:**
```bash
python3 .agent-os/git-management/branch-manager.py --validate-commit
python3 .agent-os/git-management/branch-manager.py --recover-commits <hash>
```

**MCP Tools Not Found:**
```bash
python3 .agent-os/mcp-integration/mcp-orchestrator.py --discover --verbose
```

**Tech Stack Not Detected:**
```bash
python3 .agent-os/tech-stack/stack-detector.py --detect --verbose
```

### Getting Help

1. Check logs in `.agent-os/logs/`
2. Run diagnostic commands with `--verbose` flag
3. Review configuration in `.agent-os/config/enhanced-config.yml`
4. Open an issue with detailed error information

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality  
4. Update documentation
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built as extensions to [Agent OS](https://buildermethods.com/agent-os) by Brian Casel
- Designed for integration with Claude Desktop, Cursor, and other AI coding tools
- Compatible with the Model Context Protocol (MCP) ecosystem

## 📞 Support

- **Documentation:** See individual component READMEs in each directory
- **Issues:** Use GitHub Issues for bug reports and feature requests
- **Discussions:** Use GitHub Discussions for questions and community support

---

**Transform your AI coding workflow from struggling with large codebases to confidently completing complex applications.** 🚀

