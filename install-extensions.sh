#!/bin/bash

# Agent OS Extensions Installation Script
# This script adds extensions to your existing Agent OS installation

set -e

echo "🚀 Installing Agent OS Extensions..."
echo "This will enhance your existing Agent OS with advanced capabilities."
echo ""

# Check if we're in a project directory
if [ ! -f "package.json" ] && [ ! -f "requirements.txt" ] && [ ! -f "Gemfile" ] && [ ! -f "pom.xml" ] && [ ! -f "go.mod" ] && [ ! -f "Cargo.toml" ]; then
    echo "⚠️  Warning: No project files detected. Make sure you're in your project root directory."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 1
    fi
fi

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed. Please install pip and try again."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install pyyaml pathlib dataclasses typing-extensions

# Create .agent-os directory if it doesn't exist
if [ ! -d ".agent-os" ]; then
    echo "📁 Creating .agent-os directory..."
    mkdir -p .agent-os/{logs,specs,product}
    echo "ℹ️  No existing Agent OS installation found. Extensions will be installed as standalone tools."
    echo "   Consider installing the base Agent OS from https://buildermethods.com/agent-os"
else
    echo "✅ Found existing .agent-os directory. Extensions will be added alongside existing Agent OS."
fi

# Create extension directories
echo "📁 Creating extension directories..."
mkdir -p .agent-os/{context,tech-stack,git-management,codebase-analysis,mcp-integration}
mkdir -p .agent-os/logs
mkdir -p .agent-os/config

# Copy extension files
echo "📋 Installing extension modules..."

# Context Manager
cp -r context/* .agent-os/context/
chmod +x .agent-os/context/context-manager.py
echo "  ✅ Smart Context Manager installed"

# Tech Stack Detector
cp -r tech-stack/* .agent-os/tech-stack/
chmod +x .agent-os/tech-stack/stack-detector.py
echo "  ✅ Tech Stack Detector installed"

# Git Branch Manager
cp -r git-management/* .agent-os/git-management/
chmod +x .agent-os/git-management/branch-manager.py
echo "  ✅ Git Branch Manager installed"

# Codebase Analyzer
cp -r codebase-analysis/* .agent-os/codebase-analysis/
chmod +x .agent-os/codebase-analysis/codebase-analyzer.py
echo "  ✅ Codebase Analyzer installed"

# MCP Orchestrator
cp -r mcp-integration/* .agent-os/mcp-integration/
chmod +x .agent-os/mcp-integration/mcp-orchestrator.py
echo "  ✅ MCP Orchestrator installed"

# Enhanced Configuration
if [ ! -f ".agent-os/config/enhanced-config.yml" ]; then
    cp config/enhanced-config.yml .agent-os/config/
    echo "  ✅ Enhanced configuration installed"
else
    echo "  ⚠️  Enhanced configuration already exists, skipping to preserve settings"
fi

# Run initial setup
echo ""
echo "🔍 Running initial extension setup..."

# Detect tech stack
echo "  - Detecting tech stack..."
if python3 .agent-os/tech-stack/stack-detector.py --detect --generate-standards --output-dir .agent-os/standards 2>/dev/null; then
    echo "    ✅ Tech stack detected and standards generated"
else
    echo "    ⚠️  Tech stack detection completed with warnings (check logs)"
fi

# Discover MCP tools
echo "  - Discovering MCP tools..."
if python3 .agent-os/mcp-integration/mcp-orchestrator.py --discover --create-workflows 2>/dev/null; then
    echo "    ✅ MCP tools discovered"
else
    echo "    ⚠️  MCP tool discovery completed with warnings (check logs)"
fi

# Analyze codebase (if there are source files)
echo "  - Analyzing codebase..."
if find . -maxdepth 3 -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.rb" -o -name "*.java" | head -1 | grep -q .; then
    if python3 .agent-os/codebase-analysis/codebase-analyzer.py --analyze 2>/dev/null; then
        echo "    ✅ Codebase analysis completed"
    else
        echo "    ⚠️  Codebase analysis completed with warnings (check logs)"
    fi
else
    echo "    ℹ️  No source files found, skipping codebase analysis"
fi

# Setup Git hooks if in a Git repository
if [ -d ".git" ]; then
    echo "  - Setting up Git hooks..."
    if python3 .agent-os/git-management/branch-manager.py --setup-hooks 2>/dev/null; then
        echo "    ✅ Git hooks installed"
    else
        echo "    ⚠️  Git hooks setup completed with warnings (check logs)"
    fi
else
    echo "    ℹ️  Not a Git repository, skipping Git setup"
fi

# Initialize context manager
echo "  - Initializing context manager..."
if python3 .agent-os/context/context-manager.py --optimize 2>/dev/null; then
    echo "    ✅ Context manager initialized"
else
    echo "    ⚠️  Context manager initialization completed with warnings (check logs)"
fi

echo ""
echo "✅ Agent OS Extensions installation complete!"
echo ""
echo "📊 Installation Summary:"
echo "======================="

# Show tech stack detection results
if [ -f ".agent-os/tech-stack/detected-stack.json" ]; then
    echo "🔧 Tech Stack: Detected and configured"
else
    echo "🔧 Tech Stack: Manual configuration may be needed"
fi

# Show MCP tools discovery results
if [ -f ".agent-os/mcp-integration/tools/discovered-tools.json" ]; then
    TOOL_COUNT=$(python3 -c "import json; data=json.load(open('.agent-os/mcp-integration/tools/discovered-tools.json')); print(len(data))" 2>/dev/null || echo "0")
    echo "🛠️  MCP Tools: $TOOL_COUNT tools discovered"
else
    echo "🛠️  MCP Tools: Discovery pending or no tools found"
fi

# Show codebase analysis results
if [ -f ".agent-os/codebase-analysis/metrics.json" ]; then
    TOTAL_FILES=$(python3 -c "import json; data=json.load(open('.agent-os/codebase-analysis/metrics.json')); print(data['total_files'])" 2>/dev/null || echo "0")
    TOTAL_LINES=$(python3 -c "import json; data=json.load(open('.agent-os/codebase-analysis/metrics.json')); print(data['total_lines'])" 2>/dev/null || echo "0")
    echo "📁 Codebase: $TOTAL_FILES files, $TOTAL_LINES lines analyzed"
else
    echo "📁 Codebase: Analysis pending"
fi

# Show Git status
if [ -d ".git" ]; then
    echo "🌿 Git: Enhanced branch management active"
else
    echo "🌿 Git: Not a Git repository"
fi

echo ""
echo "🎯 Next Steps:"
echo "=============="
echo "1. Your existing Agent OS commands now have enhanced capabilities:"
echo "   - /create-spec (now with tech stack detection)"
echo "   - /create-tasks (now with smart context management)"
echo "   - /execute-tasks (now with MCP integration and branch management)"
echo ""
echo "2. Use new extension tools directly:"
echo "   - python3 .agent-os/codebase-analysis/codebase-analyzer.py --report"
echo "   - python3 .agent-os/git-management/branch-manager.py --report"
echo "   - python3 .agent-os/context/context-manager.py --report"
echo "   - python3 .agent-os/mcp-integration/mcp-orchestrator.py --list-tools"
echo ""
echo "3. Configure extensions in .agent-os/config/enhanced-config.yml"
echo ""
echo "4. Check logs in .agent-os/logs/ if you encounter any issues"
echo ""
echo "🚀 Your Agent OS is now enhanced for large-scale development!"
echo "   Continue using your existing Agent OS workflow with new superpowers."

