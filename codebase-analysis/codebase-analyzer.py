#!/usr/bin/env python3
"""
Enhanced Agent OS Codebase Analyzer
Analyzes large codebases, detects patterns, prevents duplication, and provides insights
"""

import os
import json
import ast
import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import re

@dataclass
class CodeFile:
    """Represents a code file with metadata"""
    path: str
    language: str
    size: int
    lines_of_code: int
    complexity_score: float
    dependencies: List[str]
    exports: List[str]
    functions: List[str]
    classes: List[str]
    hash: str

@dataclass
class CodeDuplication:
    """Represents detected code duplication"""
    similarity_score: float
    file1: str
    file2: str
    duplicate_lines: List[Tuple[int, int]]  # (line1, line2) pairs
    duplicate_content: str

@dataclass
class DependencyRelation:
    """Represents a dependency relationship between files/modules"""
    source: str
    target: str
    relation_type: str  # 'import', 'require', 'include', 'inherit'
    strength: float  # 0.0 to 1.0

@dataclass
class CodebaseMetrics:
    """Overall codebase metrics"""
    total_files: int
    total_lines: int
    languages: Dict[str, int]
    complexity_distribution: Dict[str, int]
    dependency_depth: int
    duplication_percentage: float
    test_coverage_estimate: float

class CodebaseAnalyzer:
    """Analyzes codebases for structure, quality, and patterns"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.agent_os_dir = self.project_root / ".agent-os"
        self.analysis_dir = self.agent_os_dir / "codebase-analysis"
        
        # Create directories
        self.analysis_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self._setup_logging()
        
        # Analysis data
        self.code_files: Dict[str, CodeFile] = {}
        self.duplications: List[CodeDuplication] = []
        self.dependencies: List[DependencyRelation] = []
        self.metrics: Optional[CodebaseMetrics] = None
        
        # Configuration
        self.config = self._load_config()
        
        # Language patterns
        self.language_patterns = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'javascript',
            '.tsx': 'typescript',
            '.rb': 'ruby',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp',
            '.php': 'php',
            '.go': 'go',
            '.rs': 'rust',
            '.swift': 'swift',
            '.kt': 'kotlin'
        }
        
        # Exclude patterns
        self.exclude_patterns = [
            'node_modules', '.git', 'dist', 'build', '__pycache__',
            '.venv', 'venv', '.env', 'vendor', 'target', '.next',
            'coverage', '.nyc_output', 'logs', '*.log'
        ]
    
    def _setup_logging(self):
        """Setup logging for codebase analyzer"""
        log_dir = self.agent_os_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "codebase-analyzer.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("CodebaseAnalyzer")
    
    def _load_config(self) -> Dict:
        """Load codebase analysis configuration"""
        config_path = self.agent_os_dir / "config" / "enhanced-config.yml"
        if config_path.exists():
            import yaml
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config.get('codebase_analysis', {})
        return {}
    
    def _should_exclude_path(self, path: Path) -> bool:
        """Check if a path should be excluded from analysis"""
        path_str = str(path)
        
        for pattern in self.exclude_patterns:
            if pattern in path_str:
                return True
        
        # Check custom exclude patterns from config
        custom_patterns = self.config.get('exclude_patterns', [])
        for pattern in custom_patterns:
            if pattern in path_str:
                return True
        
        return False
    
    def analyze_codebase(self) -> CodebaseMetrics:
        """Perform comprehensive codebase analysis"""
        self.logger.info(f"Starting codebase analysis for {self.project_root}")
        
        # Scan all code files
        self._scan_code_files()
        
        # Analyze dependencies
        self._analyze_dependencies()
        
        # Detect duplications
        self._detect_duplications()
        
        # Calculate metrics
        self.metrics = self._calculate_metrics()
        
        # Save results
        self._save_analysis_results()
        
        self.logger.info("Codebase analysis complete")
        return self.metrics
    
    def _scan_code_files(self):
        """Scan and analyze all code files in the project"""
        self.logger.info("Scanning code files...")
        
        max_files = self.config.get('max_analysis_files', 10000)
        file_count = 0
        
        for file_path in self.project_root.rglob('*'):
            if file_count >= max_files:
                self.logger.warning(f"Reached maximum file limit ({max_files})")
                break
            
            if not file_path.is_file():
                continue
            
            if self._should_exclude_path(file_path):
                continue
            
            if file_path.suffix not in self.language_patterns:
                continue
            
            try:
                code_file = self._analyze_code_file(file_path)
                if code_file:
                    self.code_files[str(file_path)] = code_file
                    file_count += 1
                    
                    if file_count % 100 == 0:
                        self.logger.info(f"Analyzed {file_count} files...")
                        
            except Exception as e:
                self.logger.error(f"Error analyzing {file_path}: {e}")
        
        self.logger.info(f"Scanned {len(self.code_files)} code files")
    
    def _analyze_code_file(self, file_path: Path) -> Optional[CodeFile]:
        """Analyze a single code file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            self.logger.debug(f"Could not read {file_path}: {e}")
            return None
        
        language = self.language_patterns.get(file_path.suffix, 'unknown')
        
        # Basic metrics
        lines = content.split('\n')
        lines_of_code = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
        
        # Language-specific analysis
        dependencies = []
        exports = []
        functions = []
        classes = []
        complexity_score = 0.0
        
        if language == 'python':
            dependencies, exports, functions, classes, complexity_score = self._analyze_python_file(content)
        elif language in ['javascript', 'typescript']:
            dependencies, exports, functions, classes, complexity_score = self._analyze_js_file(content)
        elif language == 'java':
            dependencies, exports, functions, classes, complexity_score = self._analyze_java_file(content)
        # Add more language-specific analyzers as needed
        
        file_hash = hashlib.md5(content.encode()).hexdigest()
        
        return CodeFile(
            path=str(file_path.relative_to(self.project_root)),
            language=language,
            size=len(content),
            lines_of_code=lines_of_code,
            complexity_score=complexity_score,
            dependencies=dependencies,
            exports=exports,
            functions=functions,
            classes=classes,
            hash=file_hash
        )
    
    def _analyze_python_file(self, content: str) -> Tuple[List[str], List[str], List[str], List[str], float]:
        """Analyze Python file for dependencies, exports, functions, classes, and complexity"""
        dependencies = []
        exports = []
        functions = []
        classes = []
        complexity_score = 0.0
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        dependencies.append(alias.name)
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        dependencies.append(node.module)
                
                elif isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                    # Simple complexity: count nested structures
                    complexity_score += 1 + len([n for n in ast.walk(node) if isinstance(n, (ast.If, ast.For, ast.While, ast.Try))])
                
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                    complexity_score += 2  # Classes add to complexity
            
            # Exports are typically functions and classes at module level
            exports = functions + classes
            
        except SyntaxError:
            # File has syntax errors, skip detailed analysis
            pass
        
        return dependencies, exports, functions, classes, complexity_score
    
    def _analyze_js_file(self, content: str) -> Tuple[List[str], List[str], List[str], List[str], float]:
        """Analyze JavaScript/TypeScript file (simplified analysis)"""
        dependencies = []
        exports = []
        functions = []
        classes = []
        complexity_score = 0.0
        
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Import statements
            if line.startswith('import ') or line.startswith('const ') and 'require(' in line:
                # Extract module name (simplified)
                if 'from ' in line:
                    module = line.split('from ')[-1].strip().strip('\'"')
                    dependencies.append(module)
                elif 'require(' in line:
                    match = re.search(r'require\([\'"]([^\'"]+)[\'"]', line)
                    if match:
                        dependencies.append(match.group(1))
            
            # Export statements
            elif line.startswith('export '):
                if 'function ' in line:
                    match = re.search(r'function\s+(\w+)', line)
                    if match:
                        exports.append(match.group(1))
                elif 'class ' in line:
                    match = re.search(r'class\s+(\w+)', line)
                    if match:
                        exports.append(match.group(1))
            
            # Function declarations
            elif 'function ' in line:
                match = re.search(r'function\s+(\w+)', line)
                if match:
                    functions.append(match.group(1))
                complexity_score += 1
            
            # Class declarations
            elif line.startswith('class '):
                match = re.search(r'class\s+(\w+)', line)
                if match:
                    classes.append(match.group(1))
                complexity_score += 2
            
            # Complexity indicators
            elif any(keyword in line for keyword in ['if ', 'for ', 'while ', 'switch ', 'try ']):
                complexity_score += 0.5
        
        return dependencies, exports, functions, classes, complexity_score
    
    def _analyze_java_file(self, content: str) -> Tuple[List[str], List[str], List[str], List[str], float]:
        """Analyze Java file (simplified analysis)"""
        dependencies = []
        exports = []
        functions = []
        classes = []
        complexity_score = 0.0
        
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Import statements
            if line.startswith('import '):
                import_name = line.replace('import ', '').replace(';', '').strip()
                dependencies.append(import_name)
            
            # Class declarations
            elif 'class ' in line and not line.startswith('//'):
                match = re.search(r'class\s+(\w+)', line)
                if match:
                    class_name = match.group(1)
                    classes.append(class_name)
                    exports.append(class_name)
                complexity_score += 2
            
            # Method declarations
            elif re.search(r'(public|private|protected).*\w+\s*\(', line):
                match = re.search(r'\s+(\w+)\s*\(', line)
                if match:
                    functions.append(match.group(1))
                complexity_score += 1
            
            # Complexity indicators
            elif any(keyword in line for keyword in ['if ', 'for ', 'while ', 'switch ', 'try ']):
                complexity_score += 0.5
        
        return dependencies, exports, functions, classes, complexity_score
    
    def _analyze_dependencies(self):
        """Analyze dependencies between files"""
        self.logger.info("Analyzing dependencies...")
        
        # Create a mapping of exports to files
        exports_map = defaultdict(list)
        for file_path, code_file in self.code_files.items():
            for export in code_file.exports:
                exports_map[export].append(file_path)
        
        # Find dependency relationships
        for file_path, code_file in self.code_files.items():
            for dependency in code_file.dependencies:
                # Look for internal dependencies
                if dependency in exports_map:
                    for target_file in exports_map[dependency]:
                        if target_file != file_path:
                            relation = DependencyRelation(
                                source=file_path,
                                target=target_file,
                                relation_type='import',
                                strength=1.0
                            )
                            self.dependencies.append(relation)
                
                # Check for relative imports
                elif dependency.startswith('.'):
                    # Handle relative imports (simplified)
                    base_path = Path(file_path).parent
                    target_path = (base_path / dependency).with_suffix('.py')  # Assume Python for now
                    
                    if str(target_path) in self.code_files:
                        relation = DependencyRelation(
                            source=file_path,
                            target=str(target_path),
                            relation_type='import',
                            strength=0.8
                        )
                        self.dependencies.append(relation)
    
    def _detect_duplications(self):
        """Detect code duplications across files"""
        self.logger.info("Detecting code duplications...")
        
        # Simple hash-based duplication detection
        file_hashes = {}
        for file_path, code_file in self.code_files.items():
            if code_file.hash in file_hashes:
                # Exact duplicate
                duplication = CodeDuplication(
                    similarity_score=1.0,
                    file1=file_hashes[code_file.hash],
                    file2=file_path,
                    duplicate_lines=[],
                    duplicate_content="Exact file duplicate"
                )
                self.duplications.append(duplication)
            else:
                file_hashes[code_file.hash] = file_path
        
        # Function-level duplication detection
        function_signatures = defaultdict(list)
        for file_path, code_file in self.code_files.items():
            for function in code_file.functions:
                function_signatures[function].append(file_path)
        
        for function_name, files in function_signatures.items():
            if len(files) > 1:
                # Potential function duplication
                for i in range(len(files)):
                    for j in range(i + 1, len(files)):
                        duplication = CodeDuplication(
                            similarity_score=0.7,  # Estimated
                            file1=files[i],
                            file2=files[j],
                            duplicate_lines=[],
                            duplicate_content=f"Function '{function_name}' appears in multiple files"
                        )
                        self.duplications.append(duplication)
    
    def _calculate_metrics(self) -> CodebaseMetrics:
        """Calculate overall codebase metrics"""
        if not self.code_files:
            return CodebaseMetrics(0, 0, {}, {}, 0, 0.0, 0.0)
        
        total_files = len(self.code_files)
        total_lines = sum(cf.lines_of_code for cf in self.code_files.values())
        
        # Language distribution
        languages = Counter(cf.language for cf in self.code_files.values())
        
        # Complexity distribution
        complexity_ranges = {'low': 0, 'medium': 0, 'high': 0, 'very_high': 0}
        for code_file in self.code_files.values():
            if code_file.complexity_score < 10:
                complexity_ranges['low'] += 1
            elif code_file.complexity_score < 25:
                complexity_ranges['medium'] += 1
            elif code_file.complexity_score < 50:
                complexity_ranges['high'] += 1
            else:
                complexity_ranges['very_high'] += 1
        
        # Dependency depth (simplified)
        dependency_depth = len(set(dep.target for dep in self.dependencies))
        
        # Duplication percentage
        duplicated_files = len(set(d.file1 for d in self.duplications) | set(d.file2 for d in self.duplications))
        duplication_percentage = (duplicated_files / total_files) * 100 if total_files > 0 else 0
        
        # Test coverage estimate (based on test file presence)
        test_files = len([cf for cf in self.code_files.values() if 'test' in cf.path.lower()])
        test_coverage_estimate = min((test_files / total_files) * 100, 100) if total_files > 0 else 0
        
        return CodebaseMetrics(
            total_files=total_files,
            total_lines=total_lines,
            languages=dict(languages),
            complexity_distribution=complexity_ranges,
            dependency_depth=dependency_depth,
            duplication_percentage=duplication_percentage,
            test_coverage_estimate=test_coverage_estimate
        )
    
    def _save_analysis_results(self):
        """Save analysis results to files"""
        # Save code files analysis
        files_data = {path: asdict(code_file) for path, code_file in self.code_files.items()}
        with open(self.analysis_dir / "code-files.json", 'w') as f:
            json.dump(files_data, f, indent=2)
        
        # Save dependencies
        deps_data = [asdict(dep) for dep in self.dependencies]
        with open(self.analysis_dir / "dependencies.json", 'w') as f:
            json.dump(deps_data, f, indent=2)
        
        # Save duplications
        dups_data = [asdict(dup) for dup in self.duplications]
        with open(self.analysis_dir / "duplications.json", 'w') as f:
            json.dump(dups_data, f, indent=2)
        
        # Save metrics
        if self.metrics:
            with open(self.analysis_dir / "metrics.json", 'w') as f:
                json.dump(asdict(self.metrics), f, indent=2)
        
        self.logger.info(f"Analysis results saved to {self.analysis_dir}")
    
    def get_files_by_complexity(self, min_complexity: float = 25.0) -> List[CodeFile]:
        """Get files with complexity above threshold"""
        return [cf for cf in self.code_files.values() if cf.complexity_score >= min_complexity]
    
    def get_dependency_graph(self) -> Dict[str, List[str]]:
        """Get dependency graph as adjacency list"""
        graph = defaultdict(list)
        for dep in self.dependencies:
            graph[dep.source].append(dep.target)
        return dict(graph)
    
    def find_circular_dependencies(self) -> List[List[str]]:
        """Find circular dependencies in the codebase"""
        graph = self.get_dependency_graph()
        cycles = []
        
        def dfs(node, path, visited):
            if node in path:
                # Found a cycle
                cycle_start = path.index(node)
                cycle = path[cycle_start:] + [node]
                cycles.append(cycle)
                return
            
            if node in visited:
                return
            
            visited.add(node)
            path.append(node)
            
            for neighbor in graph.get(node, []):
                dfs(neighbor, path, visited)
            
            path.pop()
        
        visited = set()
        for node in graph:
            if node not in visited:
                dfs(node, [], visited)
        
        return cycles
    
    def generate_analysis_report(self) -> str:
        """Generate a comprehensive analysis report"""
        if not self.metrics:
            return "No analysis data available. Run analyze_codebase() first."
        
        report = f"""# Codebase Analysis Report

## Overview
- **Total Files**: {self.metrics.total_files:,}
- **Total Lines of Code**: {self.metrics.total_lines:,}
- **Dependency Depth**: {self.metrics.dependency_depth}
- **Code Duplication**: {self.metrics.duplication_percentage:.1f}%
- **Estimated Test Coverage**: {self.metrics.test_coverage_estimate:.1f}%

## Language Distribution
"""
        
        for language, count in self.metrics.languages.items():
            percentage = (count / self.metrics.total_files) * 100
            report += f"- **{language.title()}**: {count} files ({percentage:.1f}%)\n"
        
        report += "\n## Complexity Distribution\n"
        for level, count in self.metrics.complexity_distribution.items():
            percentage = (count / self.metrics.total_files) * 100
            report += f"- **{level.replace('_', ' ').title()}**: {count} files ({percentage:.1f}%)\n"
        
        # High complexity files
        high_complexity_files = self.get_files_by_complexity(25.0)
        if high_complexity_files:
            report += f"\n## High Complexity Files ({len(high_complexity_files)} files)\n"
            for cf in sorted(high_complexity_files, key=lambda x: x.complexity_score, reverse=True)[:10]:
                report += f"- **{cf.path}**: {cf.complexity_score:.1f} complexity, {cf.lines_of_code} LOC\n"
        
        # Duplications
        if self.duplications:
            report += f"\n## Code Duplications ({len(self.duplications)} detected)\n"
            for dup in self.duplications[:10]:
                report += f"- **{dup.file1}** ↔ **{dup.file2}** (similarity: {dup.similarity_score:.1%})\n"
        
        # Circular dependencies
        cycles = self.find_circular_dependencies()
        if cycles:
            report += f"\n## Circular Dependencies ({len(cycles)} detected)\n"
            for cycle in cycles[:5]:
                report += f"- {' → '.join(cycle)}\n"
        
        return report
    
    def suggest_refactoring_opportunities(self) -> List[Dict[str, Any]]:
        """Suggest refactoring opportunities based on analysis"""
        suggestions = []
        
        # High complexity files
        high_complexity = self.get_files_by_complexity(30.0)
        for cf in high_complexity:
            suggestions.append({
                'type': 'complexity_reduction',
                'file': cf.path,
                'description': f'File has high complexity ({cf.complexity_score:.1f}). Consider breaking into smaller functions/classes.',
                'priority': 'high' if cf.complexity_score > 50 else 'medium'
            })
        
        # Duplicated code
        for dup in self.duplications:
            if dup.similarity_score > 0.8:
                suggestions.append({
                    'type': 'code_duplication',
                    'files': [dup.file1, dup.file2],
                    'description': f'High similarity detected. Consider extracting common functionality.',
                    'priority': 'medium'
                })
        
        # Circular dependencies
        cycles = self.find_circular_dependencies()
        for cycle in cycles:
            suggestions.append({
                'type': 'circular_dependency',
                'files': cycle,
                'description': 'Circular dependency detected. Consider restructuring dependencies.',
                'priority': 'high'
            })
        
        # Large files
        large_files = [cf for cf in self.code_files.values() if cf.lines_of_code > 500]
        for cf in large_files:
            suggestions.append({
                'type': 'file_size',
                'file': cf.path,
                'description': f'Large file ({cf.lines_of_code} LOC). Consider splitting into smaller modules.',
                'priority': 'low' if cf.lines_of_code < 1000 else 'medium'
            })
        
        return suggestions

def main():
    """CLI interface for codebase analyzer"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Agent OS Codebase Analyzer")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--analyze", action="store_true", help="Perform full codebase analysis")
    parser.add_argument("--report", action="store_true", help="Generate analysis report")
    parser.add_argument("--suggestions", action="store_true", help="Get refactoring suggestions")
    parser.add_argument("--complexity-threshold", type=float, default=25.0, help="Complexity threshold for reporting")
    
    args = parser.parse_args()
    
    analyzer = CodebaseAnalyzer(args.project_root)
    
    if args.analyze:
        metrics = analyzer.analyze_codebase()
        print(f"✅ Analysis complete: {metrics.total_files} files, {metrics.total_lines:,} LOC")
    
    if args.report:
        print(analyzer.generate_analysis_report())
    
    if args.suggestions:
        suggestions = analyzer.suggest_refactoring_opportunities()
        print(f"\n## Refactoring Suggestions ({len(suggestions)} found)\n")
        
        for suggestion in suggestions:
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(suggestion['priority'], "⚪")
            print(f"{priority_emoji} **{suggestion['type'].replace('_', ' ').title()}**")
            print(f"   {suggestion['description']}")
            
            if 'file' in suggestion:
                print(f"   File: {suggestion['file']}")
            elif 'files' in suggestion:
                print(f"   Files: {', '.join(suggestion['files'])}")
            print()

if __name__ == "__main__":
    main()

