#!/usr/bin/env python3
"""
Enhanced Agent OS MCP (Model Context Protocol) Integration System
Discovers, manages, and orchestrates MCP tools for enhanced development workflows
"""

import os
import json
import yaml
import asyncio
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

@dataclass
class MCPTool:
    """Represents an MCP tool with its capabilities"""
    name: str
    description: str
    version: str
    capabilities: List[str]
    config_path: str
    executable_path: str
    status: str  # 'available', 'running', 'error', 'disabled'
    last_used: Optional[datetime] = None
    usage_count: int = 0
    performance_metrics: Dict[str, float] = None

@dataclass
class MCPWorkflow:
    """Represents a workflow that uses multiple MCP tools"""
    name: str
    description: str
    tools: List[str]  # Tool names
    steps: List[Dict[str, Any]]
    success_rate: float = 0.0
    avg_execution_time: float = 0.0

class MCPOrchestrator:
    """Orchestrates MCP tools for Agent OS"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.agent_os_dir = self.project_root / ".agent-os"
        self.mcp_dir = self.agent_os_dir / "mcp-integration"
        
        # Create directories
        self.mcp_dir.mkdir(parents=True, exist_ok=True)
        (self.mcp_dir / "tools").mkdir(exist_ok=True)
        (self.mcp_dir / "workflows").mkdir(exist_ok=True)
        (self.mcp_dir / "configs").mkdir(exist_ok=True)
        
        # Setup logging
        self._setup_logging()
        
        # Tool storage
        self.available_tools: Dict[str, MCPTool] = {}
        self.workflows: Dict[str, MCPWorkflow] = {}
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize
        self._load_tools()
        self._load_workflows()
    
    def _setup_logging(self):
        """Setup logging for MCP orchestrator"""
        log_dir = self.agent_os_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "mcp-orchestrator.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("MCPOrchestrator")
    
    def _load_config(self) -> Dict:
        """Load MCP configuration"""
        config_path = self.agent_os_dir / "config" / "enhanced-config.yml"
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config.get('mcp_integration', {})
        return {}
    
    def discover_mcp_tools(self) -> List[MCPTool]:
        """Discover available MCP tools in the system"""
        self.logger.info("Discovering MCP tools...")
        
        discovered_tools = []
        
        # Common MCP tool locations
        search_paths = [
            Path.home() / ".mcp" / "tools",
            Path("/usr/local/bin"),
            Path("/opt/mcp"),
            Path.cwd() / "mcp-tools",
            # Claude Desktop MCP tools location
            Path.home() / ".config" / "claude-desktop" / "mcp",
            # VS Code MCP tools
            Path.home() / ".vscode" / "extensions",
        ]
        
        # Add custom search paths from config
        custom_paths = self.config.get('tool_search_paths', [])
        search_paths.extend([Path(p) for p in custom_paths])
        
        for search_path in search_paths:
            if search_path.exists():
                discovered_tools.extend(self._scan_directory_for_tools(search_path))
        
        # Check Claude Desktop configuration
        claude_config = self._check_claude_desktop_config()
        if claude_config:
            discovered_tools.extend(claude_config)
        
        # Save discovered tools
        self._save_discovered_tools(discovered_tools)
        
        self.logger.info(f"Discovered {len(discovered_tools)} MCP tools")
        return discovered_tools
    
    def _scan_directory_for_tools(self, directory: Path) -> List[MCPTool]:
        """Scan a directory for MCP tools"""
        tools = []
        
        try:
            for item in directory.iterdir():
                if item.is_file() and item.suffix in ['.py', '.js', '.ts', '.sh']:
                    tool = self._analyze_potential_tool(item)
                    if tool:
                        tools.append(tool)
                elif item.is_dir():
                    # Check for package.json, setup.py, etc.
                    tool = self._analyze_tool_directory(item)
                    if tool:
                        tools.append(tool)
        except PermissionError:
            self.logger.warning(f"Permission denied accessing {directory}")
        except Exception as e:
            self.logger.error(f"Error scanning {directory}: {e}")
        
        return tools
    
    def _analyze_potential_tool(self, file_path: Path) -> Optional[MCPTool]:
        """Analyze a file to determine if it's an MCP tool"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for MCP-related keywords
            mcp_indicators = [
                'mcp', 'model context protocol', 'claude-mcp',
                'mcp-server', 'mcp-client', 'anthropic'
            ]
            
            content_lower = content.lower()
            if any(indicator in content_lower for indicator in mcp_indicators):
                return MCPTool(
                    name=file_path.stem,
                    description=f"MCP tool: {file_path.name}",
                    version="unknown",
                    capabilities=self._extract_capabilities_from_content(content),
                    config_path="",
                    executable_path=str(file_path),
                    status="available"
                )
        except Exception as e:
            self.logger.debug(f"Error analyzing {file_path}: {e}")
        
        return None
    
    def _analyze_tool_directory(self, dir_path: Path) -> Optional[MCPTool]:
        """Analyze a directory to determine if it contains an MCP tool"""
        # Check for common MCP tool files
        mcp_files = [
            "package.json", "setup.py", "pyproject.toml",
            "mcp-config.json", "claude-mcp.json"
        ]
        
        for mcp_file in mcp_files:
            config_file = dir_path / mcp_file
            if config_file.exists():
                return self._parse_tool_config(config_file, dir_path)
        
        return None
    
    def _parse_tool_config(self, config_file: Path, tool_dir: Path) -> Optional[MCPTool]:
        """Parse tool configuration file"""
        try:
            if config_file.name == "package.json":
                with open(config_file, 'r') as f:
                    data = json.load(f)
                
                # Check if it's an MCP tool
                keywords = data.get('keywords', [])
                description = data.get('description', '')
                
                if any('mcp' in str(k).lower() for k in keywords) or 'mcp' in description.lower():
                    return MCPTool(
                        name=data.get('name', tool_dir.name),
                        description=description,
                        version=data.get('version', 'unknown'),
                        capabilities=self._extract_capabilities_from_package_json(data),
                        config_path=str(config_file),
                        executable_path=str(tool_dir / data.get('main', 'index.js')),
                        status="available"
                    )
            
            elif config_file.name in ["setup.py", "pyproject.toml"]:
                # Python MCP tools
                return MCPTool(
                    name=tool_dir.name,
                    description=f"Python MCP tool: {tool_dir.name}",
                    version="unknown",
                    capabilities=["python-based"],
                    config_path=str(config_file),
                    executable_path=str(tool_dir),
                    status="available"
                )
        
        except Exception as e:
            self.logger.error(f"Error parsing {config_file}: {e}")
        
        return None
    
    def _check_claude_desktop_config(self) -> List[MCPTool]:
        """Check Claude Desktop configuration for MCP tools"""
        tools = []
        
        # Common Claude Desktop config locations
        config_paths = [
            Path.home() / ".config" / "claude-desktop" / "claude_desktop_config.json",
            Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json",
            Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
        ]
        
        for config_path in config_paths:
            if config_path.exists():
                try:
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                    
                    mcp_servers = config.get('mcpServers', {})
                    for server_name, server_config in mcp_servers.items():
                        tool = MCPTool(
                            name=server_name,
                            description=f"Claude Desktop MCP Server: {server_name}",
                            version="unknown",
                            capabilities=self._extract_capabilities_from_server_config(server_config),
                            config_path=str(config_path),
                            executable_path=server_config.get('command', ''),
                            status="available"
                        )
                        tools.append(tool)
                        
                except Exception as e:
                    self.logger.error(f"Error reading Claude Desktop config {config_path}: {e}")
        
        return tools
    
    def _extract_capabilities_from_content(self, content: str) -> List[str]:
        """Extract capabilities from file content"""
        capabilities = []
        
        # Common MCP capability patterns
        capability_patterns = {
            'file_operations': ['read_file', 'write_file', 'list_files'],
            'web_scraping': ['requests', 'beautifulsoup', 'selenium'],
            'database': ['sqlite', 'postgresql', 'mysql', 'mongodb'],
            'api_integration': ['rest', 'graphql', 'webhook'],
            'code_analysis': ['ast', 'parser', 'linter'],
            'git_operations': ['git', 'github', 'gitlab'],
            'terminal': ['subprocess', 'shell', 'command'],
            'image_processing': ['pillow', 'opencv', 'imageio'],
            'data_processing': ['pandas', 'numpy', 'csv']
        }
        
        content_lower = content.lower()
        for capability, patterns in capability_patterns.items():
            if any(pattern in content_lower for pattern in patterns):
                capabilities.append(capability)
        
        return capabilities
    
    def _extract_capabilities_from_package_json(self, data: Dict) -> List[str]:
        """Extract capabilities from package.json"""
        capabilities = []
        
        dependencies = {}
        dependencies.update(data.get('dependencies', {}))
        dependencies.update(data.get('devDependencies', {}))
        
        # Map dependencies to capabilities
        capability_map = {
            'fs': 'file_operations',
            'axios': 'api_integration',
            'express': 'web_server',
            'sqlite3': 'database',
            'mongodb': 'database',
            'puppeteer': 'web_scraping',
            'cheerio': 'web_scraping',
            'sharp': 'image_processing',
            'jimp': 'image_processing'
        }
        
        for dep in dependencies:
            if dep in capability_map:
                capabilities.append(capability_map[dep])
        
        return capabilities
    
    def _extract_capabilities_from_server_config(self, config: Dict) -> List[str]:
        """Extract capabilities from MCP server configuration"""
        capabilities = []
        
        # Analyze command and arguments
        command = config.get('command', '')
        args = config.get('args', [])
        
        if 'filesystem' in command or any('file' in str(arg) for arg in args):
            capabilities.append('file_operations')
        
        if 'web' in command or any('http' in str(arg) for arg in args):
            capabilities.append('web_scraping')
        
        if 'git' in command:
            capabilities.append('git_operations')
        
        if 'database' in command or 'sql' in command:
            capabilities.append('database')
        
        return capabilities
    
    def _save_discovered_tools(self, tools: List[MCPTool]):
        """Save discovered tools to file"""
        tools_file = self.mcp_dir / "tools" / "discovered-tools.json"
        
        tools_data = [asdict(tool) for tool in tools]
        
        with open(tools_file, 'w') as f:
            json.dump(tools_data, f, indent=2, default=str)
        
        self.logger.info(f"Saved {len(tools)} discovered tools to {tools_file}")
    
    def _load_tools(self):
        """Load previously discovered tools"""
        tools_file = self.mcp_dir / "tools" / "discovered-tools.json"
        
        if tools_file.exists():
            try:
                with open(tools_file, 'r') as f:
                    tools_data = json.load(f)
                
                for tool_data in tools_data:
                    # Convert datetime strings back to datetime objects
                    if tool_data.get('last_used'):
                        tool_data['last_used'] = datetime.fromisoformat(tool_data['last_used'])
                    
                    tool = MCPTool(**tool_data)
                    self.available_tools[tool.name] = tool
                    
            except Exception as e:
                self.logger.error(f"Error loading tools: {e}")
    
    def _load_workflows(self):
        """Load predefined workflows"""
        workflows_dir = self.mcp_dir / "workflows"
        
        for workflow_file in workflows_dir.glob("*.json"):
            try:
                with open(workflow_file, 'r') as f:
                    workflow_data = json.load(f)
                
                workflow = MCPWorkflow(**workflow_data)
                self.workflows[workflow.name] = workflow
                
            except Exception as e:
                self.logger.error(f"Error loading workflow {workflow_file}: {e}")
    
    def create_workflow(self, name: str, description: str, tools: List[str], steps: List[Dict[str, Any]]) -> MCPWorkflow:
        """Create a new MCP workflow"""
        workflow = MCPWorkflow(
            name=name,
            description=description,
            tools=tools,
            steps=steps
        )
        
        self.workflows[name] = workflow
        
        # Save workflow
        workflow_file = self.mcp_dir / "workflows" / f"{name}.json"
        with open(workflow_file, 'w') as f:
            json.dump(asdict(workflow), f, indent=2)
        
        self.logger.info(f"Created workflow: {name}")
        return workflow
    
    async def execute_workflow(self, workflow_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an MCP workflow"""
        if workflow_name not in self.workflows:
            raise ValueError(f"Workflow '{workflow_name}' not found")
        
        workflow = self.workflows[workflow_name]
        self.logger.info(f"Executing workflow: {workflow_name}")
        
        start_time = datetime.now()
        results = {}
        
        try:
            for i, step in enumerate(workflow.steps):
                step_name = step.get('name', f'step_{i}')
                tool_name = step.get('tool')
                action = step.get('action')
                params = step.get('params', {})
                
                self.logger.info(f"Executing step: {step_name} with tool: {tool_name}")
                
                # Execute tool action
                step_result = await self._execute_tool_action(tool_name, action, params, context)
                results[step_name] = step_result
                
                # Update context with step results
                context.update(step_result)
            
            # Update workflow metrics
            execution_time = (datetime.now() - start_time).total_seconds()
            workflow.avg_execution_time = (workflow.avg_execution_time + execution_time) / 2
            workflow.success_rate = min(workflow.success_rate + 0.1, 1.0)
            
            self.logger.info(f"Workflow '{workflow_name}' completed successfully")
            return results
            
        except Exception as e:
            self.logger.error(f"Workflow '{workflow_name}' failed: {e}")
            workflow.success_rate = max(workflow.success_rate - 0.1, 0.0)
            raise
    
    async def _execute_tool_action(self, tool_name: str, action: str, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific action with an MCP tool"""
        if tool_name not in self.available_tools:
            raise ValueError(f"Tool '{tool_name}' not available")
        
        tool = self.available_tools[tool_name]
        
        # Update tool usage
        tool.last_used = datetime.now()
        tool.usage_count += 1
        
        # Execute tool (this would need to be implemented based on actual MCP protocol)
        # For now, we'll simulate the execution
        result = {
            'tool': tool_name,
            'action': action,
            'status': 'success',
            'output': f"Simulated output from {tool_name} action {action}",
            'params': params
        }
        
        return result
    
    def get_tools_by_capability(self, capability: str) -> List[MCPTool]:
        """Get tools that have a specific capability"""
        return [tool for tool in self.available_tools.values() if capability in tool.capabilities]
    
    def recommend_tools_for_task(self, task_description: str) -> List[Tuple[MCPTool, float]]:
        """Recommend tools for a given task based on capabilities and description"""
        recommendations = []
        
        task_lower = task_description.lower()
        
        for tool in self.available_tools.values():
            score = 0.0
            
            # Score based on capabilities
            for capability in tool.capabilities:
                if capability.replace('_', ' ') in task_lower:
                    score += 0.3
            
            # Score based on tool name and description
            if tool.name.lower() in task_lower:
                score += 0.4
            
            if any(word in tool.description.lower() for word in task_lower.split()):
                score += 0.2
            
            # Score based on usage history
            if tool.usage_count > 0:
                score += 0.1
            
            if score > 0:
                recommendations.append((tool, score))
        
        # Sort by score descending
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return recommendations
    
    def generate_mcp_integration_report(self) -> str:
        """Generate a comprehensive MCP integration report"""
        report = f"""# MCP Integration Report

## Summary
- Total Tools: {len(self.available_tools)}
- Active Workflows: {len(self.workflows)}
- Tools Used: {sum(1 for tool in self.available_tools.values() if tool.usage_count > 0)}

## Available Tools
"""
        
        for tool in self.available_tools.values():
            status_emoji = "✅" if tool.status == "available" else "❌"
            report += f"{status_emoji} **{tool.name}** - {tool.description}\n"
            report += f"   Capabilities: {', '.join(tool.capabilities)}\n"
            report += f"   Usage: {tool.usage_count} times\n\n"
        
        report += "## Workflows\n"
        for workflow in self.workflows.values():
            report += f"- **{workflow.name}**: {workflow.description}\n"
            report += f"  Success Rate: {workflow.success_rate:.1%}\n"
            report += f"  Avg Execution Time: {workflow.avg_execution_time:.2f}s\n\n"
        
        return report
    
    def create_default_workflows(self):
        """Create default workflows for common development tasks"""
        
        # Code Analysis Workflow
        self.create_workflow(
            name="code_analysis",
            description="Analyze codebase structure and quality",
            tools=["file_operations", "code_analysis"],
            steps=[
                {
                    "name": "scan_files",
                    "tool": "file_operations",
                    "action": "list_files",
                    "params": {"pattern": "*.py,*.js,*.ts,*.rb"}
                },
                {
                    "name": "analyze_code",
                    "tool": "code_analysis",
                    "action": "analyze",
                    "params": {"files": "${scan_files.files}"}
                }
            ]
        )
        
        # Git Workflow
        self.create_workflow(
            name="git_status_check",
            description="Check git status and branch information",
            tools=["git_operations"],
            steps=[
                {
                    "name": "check_status",
                    "tool": "git_operations",
                    "action": "status",
                    "params": {}
                },
                {
                    "name": "check_branch",
                    "tool": "git_operations",
                    "action": "current_branch",
                    "params": {}
                }
            ]
        )
        
        # Database Schema Analysis
        self.create_workflow(
            name="database_analysis",
            description="Analyze database schema and structure",
            tools=["database", "file_operations"],
            steps=[
                {
                    "name": "find_schema_files",
                    "tool": "file_operations",
                    "action": "find",
                    "params": {"pattern": "schema.*,migrations/*"}
                },
                {
                    "name": "analyze_schema",
                    "tool": "database",
                    "action": "analyze_schema",
                    "params": {"files": "${find_schema_files.files}"}
                }
            ]
        )

def main():
    """CLI interface for MCP orchestrator"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Agent OS MCP Orchestrator")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--discover", action="store_true", help="Discover MCP tools")
    parser.add_argument("--list-tools", action="store_true", help="List available tools")
    parser.add_argument("--create-workflows", action="store_true", help="Create default workflows")
    parser.add_argument("--report", action="store_true", help="Generate integration report")
    parser.add_argument("--recommend", help="Recommend tools for task")
    
    args = parser.parse_args()
    
    orchestrator = MCPOrchestrator(args.project_root)
    
    if args.discover:
        tools = orchestrator.discover_mcp_tools()
        print(f"✅ Discovered {len(tools)} MCP tools")
    
    if args.list_tools:
        for tool_name, tool in orchestrator.available_tools.items():
            print(f"- {tool_name}: {tool.description}")
    
    if args.create_workflows:
        orchestrator.create_default_workflows()
        print("✅ Created default workflows")
    
    if args.report:
        print(orchestrator.generate_mcp_integration_report())
    
    if args.recommend:
        recommendations = orchestrator.recommend_tools_for_task(args.recommend)
        print(f"Recommended tools for '{args.recommend}':")
        for tool, score in recommendations[:5]:
            print(f"- {tool.name} (score: {score:.2f}): {tool.description}")

if __name__ == "__main__":
    main()

