#!/usr/bin/env python3
"""
Enhanced Agent OS MCP Orchestrator with Automatic Discovery and Integration
Automatically discovers, configures, and integrates all existing MCP tools during installation
"""

import os
import json
import yaml
import logging
import subprocess
import platform
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class MCPTool:
    """Represents an MCP tool with its capabilities"""
    name: str
    description: str
    version: str
    source: str  # 'claude-desktop', 'vscode', 'system', 'npm', 'pip'
    capabilities: List[str]
    config_path: str
    executable_path: str
    command: List[str]  # Command to run the tool
    status: str  # 'available', 'configured', 'error', 'disabled'
    auto_discovered: bool = True
    integration_config: Dict[str, Any] = None

@dataclass
class MCPWorkflow:
    """Represents a workflow combining multiple MCP tools"""
    name: str
    description: str
    tools: List[str]
    steps: List[Dict[str, Any]]
    auto_generated: bool = True

class EnhancedMCPOrchestrator:
    """Enhanced MCP Orchestrator with automatic discovery and integration"""
    
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
        self.discovered_tools: Dict[str, MCPTool] = {}
        self.workflows: Dict[str, MCPWorkflow] = {}
        
        # Load configuration
        self.config = self._load_config()
        
        # Common MCP tool patterns
        self.mcp_patterns = [
            'mcp', 'model-context-protocol', 'claude-mcp', 'mcp-server',
            'anthropic-mcp', 'context-protocol', 'mcp-client'
        ]
    
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
        self.logger = logging.getLogger("EnhancedMCPOrchestrator")
    
    def _load_config(self) -> Dict:
        """Load MCP configuration"""
        config_path = self.agent_os_dir / "config" / "enhanced-config.yml"
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config.get('mcp_integration', {})
        return {
            'enabled': True,
            'auto_discovery': True,
            'auto_configure': True,
            'create_workflows': True
        }
    
    def auto_discover_and_integrate(self) -> Dict[str, Any]:
        """Automatically discover and integrate all MCP tools"""
        self.logger.info("🔍 Starting automatic MCP tool discovery and integration...")
        
        if not self.config.get('auto_discovery', True):
            self.logger.info("Auto-discovery disabled in configuration")
            return {}
        
        # Comprehensive discovery
        all_tools = {}
        
        # 1. Claude Desktop MCP tools
        self.logger.info("📱 Discovering Claude Desktop MCP tools...")
        claude_tools = self._discover_claude_desktop_tools()
        all_tools.update(claude_tools)
        self.logger.info(f"   Found {len(claude_tools)} Claude Desktop tools")
        
        # 2. VS Code MCP extensions
        self.logger.info("🔧 Discovering VS Code MCP extensions...")
        vscode_tools = self._discover_vscode_mcp_tools()
        all_tools.update(vscode_tools)
        self.logger.info(f"   Found {len(vscode_tools)} VS Code MCP tools")
        
        # 3. System-wide MCP tools
        self.logger.info("💻 Discovering system-wide MCP tools...")
        system_tools = self._discover_system_mcp_tools()
        all_tools.update(system_tools)
        self.logger.info(f"   Found {len(system_tools)} system MCP tools")
        
        # 4. Package manager installed tools
        self.logger.info("📦 Discovering package manager MCP tools...")
        package_tools = self._discover_package_manager_tools()
        all_tools.update(package_tools)
        self.logger.info(f"   Found {len(package_tools)} package manager tools")
        
        # 5. Common directories
        self.logger.info("📁 Scanning common MCP directories...")
        directory_tools = self._discover_directory_tools()
        all_tools.update(directory_tools)
        self.logger.info(f"   Found {len(directory_tools)} directory-based tools")
        
        # Auto-configure discovered tools
        if self.config.get('auto_configure', True):
            self.logger.info("⚙️ Auto-configuring discovered tools...")
            configured_tools = self._auto_configure_tools(all_tools)
        else:
            configured_tools = all_tools
        
        # Save discovered tools
        self._save_discovered_tools(configured_tools)
        
        # Create default workflows
        if self.config.get('create_workflows', True):
            self.logger.info("🔄 Creating default workflows...")
            self._create_default_workflows(configured_tools)
        
        # Generate integration report
        report = self._generate_integration_report(configured_tools)
        
        self.logger.info(f"✅ Successfully discovered and integrated {len(configured_tools)} MCP tools")
        return {
            'tools': configured_tools,
            'report': report,
            'total_discovered': len(configured_tools)
        }
    
    def _discover_claude_desktop_tools(self) -> Dict[str, MCPTool]:
        """Discover MCP tools from Claude Desktop configuration"""
        tools = {}
        
        # Common Claude Desktop config locations
        config_paths = [
            Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json",  # macOS
            Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json",  # Windows
            Path.home() / ".config" / "claude-desktop" / "claude_desktop_config.json",  # Linux
            Path.home() / ".claude" / "claude_desktop_config.json",  # Alternative Linux
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
                            source="claude-desktop",
                            capabilities=self._extract_capabilities_from_config(server_config),
                            config_path=str(config_path),
                            executable_path=server_config.get('command', ''),
                            command=self._build_command_from_config(server_config),
                            status="available",
                            integration_config=server_config
                        )
                        tools[f"claude-{server_name}"] = tool
                        
                except Exception as e:
                    self.logger.error(f"Error reading Claude Desktop config {config_path}: {e}")
        
        return tools
    
    def _discover_vscode_mcp_tools(self) -> Dict[str, MCPTool]:
        """Discover MCP tools from VS Code extensions"""
        tools = {}
        
        # VS Code extensions directory
        vscode_extensions_dirs = [
            Path.home() / ".vscode" / "extensions",
            Path.home() / ".vscode-insiders" / "extensions",
            Path.home() / "AppData" / "Local" / "Programs" / "Microsoft VS Code" / "resources" / "app" / "extensions",  # Windows
        ]
        
        for extensions_dir in vscode_extensions_dirs:
            if extensions_dir.exists():
                for extension_dir in extensions_dir.iterdir():
                    if extension_dir.is_dir():
                        # Check for MCP-related extensions
                        package_json = extension_dir / "package.json"
                        if package_json.exists():
                            try:
                                with open(package_json, 'r') as f:
                                    package_data = json.load(f)
                                
                                # Check if extension is MCP-related
                                name = package_data.get('name', '')
                                description = package_data.get('description', '')
                                keywords = package_data.get('keywords', [])
                                
                                if any(pattern in name.lower() or 
                                      pattern in description.lower() or
                                      any(pattern in keyword.lower() for keyword in keywords)
                                      for pattern in self.mcp_patterns):
                                    
                                    tool = MCPTool(
                                        name=name,
                                        description=description,
                                        version=package_data.get('version', 'unknown'),
                                        source="vscode",
                                        capabilities=self._extract_capabilities_from_package(package_data),
                                        config_path=str(package_json),
                                        executable_path=str(extension_dir),
                                        command=self._build_vscode_command(extension_dir, package_data),
                                        status="available",
                                        integration_config=package_data
                                    )
                                    tools[f"vscode-{name}"] = tool
                                    
                            except Exception as e:
                                self.logger.debug(f"Error reading VS Code extension {extension_dir}: {e}")
        
        return tools
    
    def _discover_system_mcp_tools(self) -> Dict[str, MCPTool]:
        """Discover system-wide MCP tools"""
        tools = {}
        
        # Common system paths
        system_paths = [
            Path("/usr/local/bin"),
            Path("/usr/bin"),
            Path("/opt"),
            Path.home() / ".local" / "bin",
            Path.home() / "bin",
        ]
        
        # Add PATH directories
        path_env = os.environ.get('PATH', '')
        for path_str in path_env.split(os.pathsep):
            if path_str:
                system_paths.append(Path(path_str))
        
        for system_path in system_paths:
            if system_path.exists() and system_path.is_dir():
                try:
                    for item in system_path.iterdir():
                        if item.is_file() and os.access(item, os.X_OK):
                            # Check if executable is MCP-related
                            if any(pattern in item.name.lower() for pattern in self.mcp_patterns):
                                tool = MCPTool(
                                    name=item.name,
                                    description=f"System MCP tool: {item.name}",
                                    version=self._get_tool_version(item),
                                    source="system",
                                    capabilities=self._detect_tool_capabilities(item),
                                    config_path="",
                                    executable_path=str(item),
                                    command=[str(item)],
                                    status="available"
                                )
                                tools[f"system-{item.name}"] = tool
                                
                except PermissionError:
                    self.logger.debug(f"Permission denied accessing {system_path}")
                except Exception as e:
                    self.logger.debug(f"Error scanning {system_path}: {e}")
        
        return tools
    
    def _discover_package_manager_tools(self) -> Dict[str, MCPTool]:
        """Discover MCP tools installed via package managers"""
        tools = {}
        
        # NPM packages
        npm_tools = self._discover_npm_mcp_tools()
        tools.update(npm_tools)
        
        # Python packages
        pip_tools = self._discover_pip_mcp_tools()
        tools.update(pip_tools)
        
        return tools
    
    def _discover_npm_mcp_tools(self) -> Dict[str, MCPTool]:
        """Discover MCP tools installed via NPM"""
        tools = {}
        
        try:
            # Check global npm packages
            result = subprocess.run(['npm', 'list', '-g', '--json'], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                npm_data = json.loads(result.stdout)
                dependencies = npm_data.get('dependencies', {})
                
                for package_name, package_info in dependencies.items():
                    if any(pattern in package_name.lower() for pattern in self.mcp_patterns):
                        tool = MCPTool(
                            name=package_name,
                            description=f"NPM MCP package: {package_name}",
                            version=package_info.get('version', 'unknown'),
                            source="npm",
                            capabilities=self._detect_npm_capabilities(package_name),
                            config_path="",
                            executable_path=package_name,
                            command=['npx', package_name],
                            status="available"
                        )
                        tools[f"npm-{package_name}"] = tool
                        
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, json.JSONDecodeError) as e:
            self.logger.debug(f"Error discovering NPM MCP tools: {e}")
        except FileNotFoundError:
            self.logger.debug("NPM not found, skipping NPM MCP tool discovery")
        
        return tools
    
    def _discover_pip_mcp_tools(self) -> Dict[str, MCPTool]:
        """Discover MCP tools installed via pip"""
        tools = {}
        
        try:
            # Check installed Python packages
            result = subprocess.run(['pip', 'list', '--format=json'], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                packages = json.loads(result.stdout)
                
                for package in packages:
                    package_name = package['name']
                    if any(pattern in package_name.lower() for pattern in self.mcp_patterns):
                        tool = MCPTool(
                            name=package_name,
                            description=f"Python MCP package: {package_name}",
                            version=package['version'],
                            source="pip",
                            capabilities=self._detect_pip_capabilities(package_name),
                            config_path="",
                            executable_path=package_name,
                            command=['python', '-m', package_name],
                            status="available"
                        )
                        tools[f"pip-{package_name}"] = tool
                        
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, json.JSONDecodeError) as e:
            self.logger.debug(f"Error discovering pip MCP tools: {e}")
        except FileNotFoundError:
            self.logger.debug("pip not found, skipping pip MCP tool discovery")
        
        return tools
    
    def _discover_directory_tools(self) -> Dict[str, MCPTool]:
        """Discover MCP tools in common directories"""
        tools = {}
        
        # Common MCP tool directories
        search_dirs = [
            Path.home() / ".mcp",
            Path.home() / "mcp-tools",
            Path.home() / ".local" / "share" / "mcp",
            Path("/opt/mcp"),
            self.project_root / "mcp-tools",
            self.project_root / ".mcp",
        ]
        
        for search_dir in search_dirs:
            if search_dir.exists() and search_dir.is_dir():
                for item in search_dir.rglob('*'):
                    if item.is_file():
                        # Check for MCP tool indicators
                        if (item.suffix in ['.py', '.js', '.ts', '.sh'] and
                            any(pattern in item.name.lower() for pattern in self.mcp_patterns)):
                            
                            tool = MCPTool(
                                name=item.stem,
                                description=f"Directory MCP tool: {item.name}",
                                version="unknown",
                                source="directory",
                                capabilities=self._analyze_file_capabilities(item),
                                config_path="",
                                executable_path=str(item),
                                command=self._build_file_command(item),
                                status="available"
                            )
                            tools[f"dir-{item.stem}"] = tool
        
        return tools
    
    def _auto_configure_tools(self, tools: Dict[str, MCPTool]) -> Dict[str, MCPTool]:
        """Automatically configure discovered tools for Agent OS integration"""
        configured_tools = {}
        
        for tool_id, tool in tools.items():
            try:
                # Test tool availability
                if self._test_tool_availability(tool):
                    tool.status = "configured"
                    
                    # Generate Agent OS integration config
                    integration_config = self._generate_integration_config(tool)
                    tool.integration_config = integration_config
                    
                    configured_tools[tool_id] = tool
                    self.logger.debug(f"Configured tool: {tool.name}")
                else:
                    tool.status = "error"
                    self.logger.warning(f"Tool not available: {tool.name}")
                    
            except Exception as e:
                self.logger.error(f"Error configuring tool {tool.name}: {e}")
                tool.status = "error"
        
        return configured_tools
    
    def _test_tool_availability(self, tool: MCPTool) -> bool:
        """Test if a tool is available and working"""
        try:
            if tool.command:
                # Try to run the tool with a help or version flag
                test_commands = [
                    tool.command + ['--help'],
                    tool.command + ['--version'],
                    tool.command + ['-h'],
                    tool.command + ['-v']
                ]
                
                for test_cmd in test_commands:
                    try:
                        result = subprocess.run(test_cmd, capture_output=True, 
                                              text=True, timeout=10)
                        if result.returncode == 0:
                            return True
                    except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
                        continue
                        
            # If executable path exists, consider it available
            if tool.executable_path and Path(tool.executable_path).exists():
                return True
                
        except Exception as e:
            self.logger.debug(f"Error testing tool {tool.name}: {e}")
        
        return False
    
    def _generate_integration_config(self, tool: MCPTool) -> Dict[str, Any]:
        """Generate Agent OS integration configuration for a tool"""
        return {
            'agent_os_command': f"mcp-{tool.name.lower().replace(' ', '-')}",
            'description': tool.description,
            'capabilities': tool.capabilities,
            'usage_examples': self._generate_usage_examples(tool),
            'integration_type': 'mcp_tool',
            'auto_configured': True
        }
    
    def _create_default_workflows(self, tools: Dict[str, MCPTool]) -> None:
        """Create default workflows combining multiple tools"""
        workflows = {}
        
        # Categorize tools by capabilities
        tool_categories = self._categorize_tools_by_capabilities(tools)
        
        # Create common workflows
        if 'file_operations' in tool_categories and 'code_analysis' in tool_categories:
            workflows['code_review'] = MCPWorkflow(
                name="code_review",
                description="Comprehensive code review using file operations and analysis tools",
                tools=tool_categories['file_operations'] + tool_categories['code_analysis'],
                steps=[
                    {"action": "read_files", "tools": tool_categories['file_operations']},
                    {"action": "analyze_code", "tools": tool_categories['code_analysis']},
                    {"action": "generate_report", "tools": tool_categories['file_operations']}
                ]
            )
        
        if 'git_operations' in tool_categories:
            workflows['git_workflow'] = MCPWorkflow(
                name="git_workflow",
                description="Enhanced git workflow with MCP tools",
                tools=tool_categories['git_operations'],
                steps=[
                    {"action": "check_status", "tools": tool_categories['git_operations']},
                    {"action": "create_branch", "tools": tool_categories['git_operations']},
                    {"action": "commit_changes", "tools": tool_categories['git_operations']}
                ]
            )
        
        # Save workflows
        for workflow_name, workflow in workflows.items():
            self._save_workflow(workflow_name, workflow)
        
        self.workflows.update(workflows)
    
    def _save_discovered_tools(self, tools: Dict[str, MCPTool]) -> None:
        """Save discovered tools to file"""
        tools_file = self.mcp_dir / "tools" / "discovered-tools.json"
        
        # Convert tools to serializable format
        tools_data = {}
        for tool_id, tool in tools.items():
            tools_data[tool_id] = asdict(tool)
        
        with open(tools_file, 'w') as f:
            json.dump(tools_data, f, indent=2, default=str)
        
        self.logger.info(f"Saved {len(tools)} discovered tools to {tools_file}")
    
    def _save_workflow(self, name: str, workflow: MCPWorkflow) -> None:
        """Save a workflow to file"""
        workflow_file = self.mcp_dir / "workflows" / f"{name}.json"
        
        with open(workflow_file, 'w') as f:
            json.dump(asdict(workflow), f, indent=2)
    
    def _generate_integration_report(self, tools: Dict[str, MCPTool]) -> Dict[str, Any]:
        """Generate integration report"""
        report = {
            'total_tools': len(tools),
            'by_source': {},
            'by_status': {},
            'capabilities_summary': {},
            'integration_timestamp': datetime.now().isoformat()
        }
        
        # Count by source
        for tool in tools.values():
            source = tool.source
            report['by_source'][source] = report['by_source'].get(source, 0) + 1
        
        # Count by status
        for tool in tools.values():
            status = tool.status
            report['by_status'][status] = report['by_status'].get(status, 0) + 1
        
        # Capabilities summary
        all_capabilities = []
        for tool in tools.values():
            all_capabilities.extend(tool.capabilities)
        
        from collections import Counter
        capability_counts = Counter(all_capabilities)
        report['capabilities_summary'] = dict(capability_counts.most_common(10))
        
        return report
    
    # Helper methods for capability detection and configuration
    def _extract_capabilities_from_config(self, config: Dict) -> List[str]:
        """Extract capabilities from tool configuration"""
        capabilities = []
        
        # Analyze command and arguments
        command = config.get('command', '')
        args = config.get('args', [])
        
        if 'file' in command.lower() or any('file' in arg.lower() for arg in args):
            capabilities.append('file_operations')
        if 'git' in command.lower() or any('git' in arg.lower() for arg in args):
            capabilities.append('git_operations')
        if 'database' in command.lower() or any('db' in arg.lower() for arg in args):
            capabilities.append('database_operations')
        if 'web' in command.lower() or any('http' in arg.lower() for arg in args):
            capabilities.append('web_operations')
        
        return capabilities or ['general']
    
    def _build_command_from_config(self, config: Dict) -> List[str]:
        """Build command list from configuration"""
        command = config.get('command', '')
        args = config.get('args', [])
        
        if isinstance(command, str):
            cmd_list = [command]
        else:
            cmd_list = command
        
        if args:
            cmd_list.extend(args)
        
        return cmd_list
    
    def _extract_capabilities_from_package(self, package_data: Dict) -> List[str]:
        """Extract capabilities from package.json data"""
        capabilities = []
        
        keywords = package_data.get('keywords', [])
        description = package_data.get('description', '').lower()
        
        capability_keywords = {
            'file_operations': ['file', 'filesystem', 'fs'],
            'git_operations': ['git', 'version-control', 'vcs'],
            'database_operations': ['database', 'db', 'sql'],
            'web_operations': ['web', 'http', 'api', 'rest'],
            'code_analysis': ['lint', 'analyze', 'ast', 'parse'],
            'testing': ['test', 'spec', 'jest', 'mocha']
        }
        
        for capability, keywords_list in capability_keywords.items():
            if (any(keyword in keywords for keyword in keywords_list) or
                any(keyword in description for keyword in keywords_list)):
                capabilities.append(capability)
        
        return capabilities or ['general']
    
    def _build_vscode_command(self, extension_dir: Path, package_data: Dict) -> List[str]:
        """Build command for VS Code extension"""
        # Most VS Code MCP extensions provide a server script
        main_file = package_data.get('main', 'index.js')
        main_path = extension_dir / main_file
        
        if main_path.exists():
            return ['node', str(main_path)]
        
        return ['code', '--install-extension', str(extension_dir)]
    
    def _get_tool_version(self, executable: Path) -> str:
        """Get version of a tool"""
        try:
            result = subprocess.run([str(executable), '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return result.stdout.strip().split('\n')[0]
        except:
            pass
        return 'unknown'
    
    def _detect_tool_capabilities(self, executable: Path) -> List[str]:
        """Detect capabilities of a tool by analyzing its help output"""
        capabilities = []
        
        try:
            result = subprocess.run([str(executable), '--help'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                help_text = result.stdout.lower()
                
                if 'file' in help_text:
                    capabilities.append('file_operations')
                if 'git' in help_text:
                    capabilities.append('git_operations')
                if 'database' in help_text or 'db' in help_text:
                    capabilities.append('database_operations')
                if 'web' in help_text or 'http' in help_text:
                    capabilities.append('web_operations')
                    
        except:
            pass
        
        return capabilities or ['general']
    
    def _detect_npm_capabilities(self, package_name: str) -> List[str]:
        """Detect capabilities of NPM package"""
        # Simple heuristic based on package name
        capabilities = []
        name_lower = package_name.lower()
        
        if 'file' in name_lower or 'fs' in name_lower:
            capabilities.append('file_operations')
        if 'git' in name_lower:
            capabilities.append('git_operations')
        if 'db' in name_lower or 'database' in name_lower:
            capabilities.append('database_operations')
        if 'web' in name_lower or 'http' in name_lower:
            capabilities.append('web_operations')
        
        return capabilities or ['general']
    
    def _detect_pip_capabilities(self, package_name: str) -> List[str]:
        """Detect capabilities of pip package"""
        # Simple heuristic based on package name
        capabilities = []
        name_lower = package_name.lower()
        
        if 'file' in name_lower or 'os' in name_lower:
            capabilities.append('file_operations')
        if 'git' in name_lower:
            capabilities.append('git_operations')
        if 'sql' in name_lower or 'database' in name_lower:
            capabilities.append('database_operations')
        if 'web' in name_lower or 'http' in name_lower or 'requests' in name_lower:
            capabilities.append('web_operations')
        
        return capabilities or ['general']
    
    def _analyze_file_capabilities(self, file_path: Path) -> List[str]:
        """Analyze file to detect capabilities"""
        capabilities = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().lower()
            
            if 'file' in content or 'filesystem' in content:
                capabilities.append('file_operations')
            if 'git' in content:
                capabilities.append('git_operations')
            if 'database' in content or 'sql' in content:
                capabilities.append('database_operations')
            if 'http' in content or 'web' in content:
                capabilities.append('web_operations')
                
        except:
            pass
        
        return capabilities or ['general']
    
    def _build_file_command(self, file_path: Path) -> List[str]:
        """Build command to execute a file"""
        if file_path.suffix == '.py':
            return ['python3', str(file_path)]
        elif file_path.suffix in ['.js', '.ts']:
            return ['node', str(file_path)]
        elif file_path.suffix == '.sh':
            return ['bash', str(file_path)]
        else:
            return [str(file_path)]
    
    def _generate_usage_examples(self, tool: MCPTool) -> List[str]:
        """Generate usage examples for a tool"""
        examples = []
        
        for capability in tool.capabilities:
            if capability == 'file_operations':
                examples.append(f"Use {tool.name} to read, write, or manipulate files")
            elif capability == 'git_operations':
                examples.append(f"Use {tool.name} for git operations like commit, push, branch")
            elif capability == 'database_operations':
                examples.append(f"Use {tool.name} for database queries and operations")
            elif capability == 'web_operations':
                examples.append(f"Use {tool.name} for web requests and API calls")
            else:
                examples.append(f"Use {tool.name} for {capability}")
        
        return examples
    
    def _categorize_tools_by_capabilities(self, tools: Dict[str, MCPTool]) -> Dict[str, List[str]]:
        """Categorize tools by their capabilities"""
        categories = {}
        
        for tool_id, tool in tools.items():
            for capability in tool.capabilities:
                if capability not in categories:
                    categories[capability] = []
                categories[capability].append(tool_id)
        
        return categories

def main():
    """CLI interface for enhanced MCP orchestrator"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Agent OS MCP Orchestrator")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--auto-discover", action="store_true", help="Auto-discover and integrate MCP tools")
    parser.add_argument("--list-tools", action="store_true", help="List discovered tools")
    parser.add_argument("--report", action="store_true", help="Generate integration report")
    
    args = parser.parse_args()
    
    orchestrator = EnhancedMCPOrchestrator(args.project_root)
    
    if args.auto_discover:
        result = orchestrator.auto_discover_and_integrate()
        print(f"✅ Discovered and integrated {result['total_discovered']} MCP tools")
        
        if result['report']:
            print("\n📊 Integration Report:")
            print(f"   By Source: {result['report']['by_source']}")
            print(f"   By Status: {result['report']['by_status']}")
    
    if args.list_tools:
        tools_file = orchestrator.mcp_dir / "tools" / "discovered-tools.json"
        if tools_file.exists():
            with open(tools_file, 'r') as f:
                tools = json.load(f)
            
            print(f"\n🛠️  Discovered MCP Tools ({len(tools)} total):")
            for tool_id, tool_data in tools.items():
                print(f"   • {tool_data['name']} ({tool_data['source']}) - {tool_data['status']}")
        else:
            print("No tools discovered yet. Run --auto-discover first.")
    
    if args.report:
        tools_file = orchestrator.mcp_dir / "tools" / "discovered-tools.json"
        if tools_file.exists():
            with open(tools_file, 'r') as f:
                tools_data = json.load(f)
            
            # Generate summary report
            by_source = {}
            by_status = {}
            
            for tool_data in tools_data.values():
                source = tool_data['source']
                status = tool_data['status']
                
                by_source[source] = by_source.get(source, 0) + 1
                by_status[status] = by_status.get(status, 0) + 1
            
            print(f"\n📊 MCP Tools Integration Report:")
            print(f"   Total Tools: {len(tools_data)}")
            print(f"   By Source: {by_source}")
            print(f"   By Status: {by_status}")
        else:
            print("No integration report available. Run --auto-discover first.")

if __name__ == "__main__":
    main()

