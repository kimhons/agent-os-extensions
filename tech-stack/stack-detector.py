#!/usr/bin/env python3
"""
Enhanced Agent OS Tech Stack Detector
Automatically detects project tech stacks and generates appropriate standards
"""

import os
import json
import yaml
import logging
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict

@dataclass
class TechStackComponent:
    """Represents a detected technology component"""
    name: str
    version: Optional[str]
    category: str  # 'language', 'framework', 'database', 'tool', 'runtime'
    confidence: float  # 0.0 to 1.0
    evidence_files: List[str]
    package_manager: Optional[str] = None

@dataclass
class DetectedTechStack:
    """Complete detected tech stack for a project"""
    primary_language: Optional[str]
    languages: List[TechStackComponent]
    frameworks: List[TechStackComponent]
    databases: List[TechStackComponent]
    tools: List[TechStackComponent]
    runtimes: List[TechStackComponent]
    package_managers: List[str]
    build_tools: List[str]
    confidence_score: float

class TechStackDetector:
    """Detects technology stacks in projects"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.agent_os_dir = self.project_root / ".agent-os"
        self.tech_stack_dir = self.agent_os_dir / "tech-stack"
        
        # Create directories
        self.tech_stack_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self._setup_logging()
        
        # Detection patterns
        self.detection_patterns = self._load_detection_patterns()
        
    def _setup_logging(self):
        """Setup logging for tech stack detector"""
        log_dir = self.agent_os_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "tech-stack-detector.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("TechStackDetector")
    
    def _load_detection_patterns(self) -> Dict:
        """Load detection patterns for various technologies"""
        return {
            # Package managers and their associated technologies
            "package_files": {
                "package.json": {
                    "language": "javascript",
                    "package_manager": "npm",
                    "confidence": 0.9,
                    "frameworks": {
                        "react": ["react"],
                        "vue": ["vue"],
                        "angular": ["@angular/core"],
                        "express": ["express"],
                        "next": ["next"],
                        "nuxt": ["nuxt"],
                        "svelte": ["svelte"]
                    }
                },
                "requirements.txt": {
                    "language": "python",
                    "package_manager": "pip",
                    "confidence": 0.9,
                    "frameworks": {
                        "django": ["django"],
                        "flask": ["flask"],
                        "fastapi": ["fastapi"],
                        "pandas": ["pandas"],
                        "numpy": ["numpy"],
                        "tensorflow": ["tensorflow"],
                        "pytorch": ["torch"]
                    }
                },
                "Pipfile": {
                    "language": "python",
                    "package_manager": "pipenv",
                    "confidence": 0.9
                },
                "pyproject.toml": {
                    "language": "python",
                    "package_manager": "poetry",
                    "confidence": 0.9
                },
                "Gemfile": {
                    "language": "ruby",
                    "package_manager": "bundler",
                    "confidence": 0.9,
                    "frameworks": {
                        "rails": ["rails"],
                        "sinatra": ["sinatra"]
                    }
                },
                "pom.xml": {
                    "language": "java",
                    "package_manager": "maven",
                    "confidence": 0.9,
                    "frameworks": {
                        "spring": ["spring-boot", "spring-core"],
                        "hibernate": ["hibernate"]
                    }
                },
                "build.gradle": {
                    "language": "java",
                    "package_manager": "gradle",
                    "confidence": 0.9
                },
                "Cargo.toml": {
                    "language": "rust",
                    "package_manager": "cargo",
                    "confidence": 0.9
                },
                "go.mod": {
                    "language": "go",
                    "package_manager": "go modules",
                    "confidence": 0.9
                },
                "composer.json": {
                    "language": "php",
                    "package_manager": "composer",
                    "confidence": 0.9,
                    "frameworks": {
                        "laravel": ["laravel/framework"],
                        "symfony": ["symfony/symfony"]
                    }
                }
            },
            
            # Configuration files
            "config_files": {
                "tsconfig.json": {"language": "typescript", "confidence": 0.8},
                "webpack.config.js": {"tool": "webpack", "confidence": 0.7},
                "vite.config.js": {"tool": "vite", "confidence": 0.8},
                "rollup.config.js": {"tool": "rollup", "confidence": 0.7},
                "babel.config.js": {"tool": "babel", "confidence": 0.6},
                "tailwind.config.js": {"framework": "tailwindcss", "confidence": 0.7},
                "next.config.js": {"framework": "nextjs", "confidence": 0.9},
                "nuxt.config.js": {"framework": "nuxtjs", "confidence": 0.9},
                "vue.config.js": {"framework": "vue", "confidence": 0.8},
                "angular.json": {"framework": "angular", "confidence": 0.9},
                "svelte.config.js": {"framework": "svelte", "confidence": 0.9},
                "gatsby-config.js": {"framework": "gatsby", "confidence": 0.9},
                "astro.config.mjs": {"framework": "astro", "confidence": 0.9}
            },
            
            # Database files
            "database_files": {
                "schema.rb": {"database": "rails_db", "confidence": 0.8},
                "migrations/": {"database": "sql_migrations", "confidence": 0.7},
                "prisma/schema.prisma": {"database": "prisma", "confidence": 0.9},
                "knexfile.js": {"database": "knex", "confidence": 0.8},
                "sequelize-cli": {"database": "sequelize", "confidence": 0.8}
            },
            
            # Docker and containerization
            "container_files": {
                "Dockerfile": {"tool": "docker", "confidence": 0.8},
                "docker-compose.yml": {"tool": "docker-compose", "confidence": 0.8},
                "docker-compose.yaml": {"tool": "docker-compose", "confidence": 0.8},
                "kubernetes/": {"tool": "kubernetes", "confidence": 0.7}
            },
            
            # CI/CD files
            "cicd_files": {
                ".github/workflows/": {"tool": "github-actions", "confidence": 0.8},
                ".gitlab-ci.yml": {"tool": "gitlab-ci", "confidence": 0.8},
                "Jenkinsfile": {"tool": "jenkins", "confidence": 0.8},
                ".travis.yml": {"tool": "travis-ci", "confidence": 0.8}
            }
        }
    
    def detect_tech_stack(self) -> DetectedTechStack:
        """Detect the complete tech stack of the project"""
        self.logger.info(f"Detecting tech stack for project: {self.project_root}")
        
        detected_components = []
        package_managers = set()
        build_tools = set()
        
        # Scan for package files
        for filename, pattern in self.detection_patterns["package_files"].items():
            file_path = self.project_root / filename
            if file_path.exists():
                components = self._analyze_package_file(file_path, pattern)
                detected_components.extend(components)
                if pattern.get("package_manager"):
                    package_managers.add(pattern["package_manager"])
        
        # Scan for config files
        for filename, pattern in self.detection_patterns["config_files"].items():
            file_path = self.project_root / filename
            if file_path.exists():
                component = self._create_component_from_pattern(filename, pattern, [str(file_path)])
                if component:
                    detected_components.append(component)
        
        # Scan for database files
        for filename, pattern in self.detection_patterns["database_files"].items():
            if filename.endswith("/"):
                # Directory pattern
                dir_path = self.project_root / filename.rstrip("/")
                if dir_path.exists() and dir_path.is_dir():
                    component = self._create_component_from_pattern(filename, pattern, [str(dir_path)])
                    if component:
                        detected_components.append(component)
            else:
                # File pattern
                file_path = self.project_root / filename
                if file_path.exists():
                    component = self._create_component_from_pattern(filename, pattern, [str(file_path)])
                    if component:
                        detected_components.append(component)
        
        # Scan for container files
        for filename, pattern in self.detection_patterns["container_files"].items():
            file_path = self.project_root / filename
            if file_path.exists():
                component = self._create_component_from_pattern(filename, pattern, [str(file_path)])
                if component:
                    detected_components.append(component)
                    build_tools.add(pattern.get("tool", ""))
        
        # Scan for CI/CD files
        for filename, pattern in self.detection_patterns["cicd_files"].items():
            if filename.endswith("/"):
                dir_path = self.project_root / filename.rstrip("/")
                if dir_path.exists() and dir_path.is_dir():
                    component = self._create_component_from_pattern(filename, pattern, [str(dir_path)])
                    if component:
                        detected_components.append(component)
                        build_tools.add(pattern.get("tool", ""))
            else:
                file_path = self.project_root / filename
                if file_path.exists():
                    component = self._create_component_from_pattern(filename, pattern, [str(file_path)])
                    if component:
                        detected_components.append(component)
                        build_tools.add(pattern.get("tool", ""))
        
        # Categorize components
        languages = [c for c in detected_components if c.category == "language"]
        frameworks = [c for c in detected_components if c.category == "framework"]
        databases = [c for c in detected_components if c.category == "database"]
        tools = [c for c in detected_components if c.category == "tool"]
        runtimes = [c for c in detected_components if c.category == "runtime"]
        
        # Determine primary language
        primary_language = None
        if languages:
            primary_language = max(languages, key=lambda x: x.confidence).name
        
        # Calculate overall confidence
        if detected_components:
            confidence_score = sum(c.confidence for c in detected_components) / len(detected_components)
        else:
            confidence_score = 0.0
        
        tech_stack = DetectedTechStack(
            primary_language=primary_language,
            languages=languages,
            frameworks=frameworks,
            databases=databases,
            tools=tools,
            runtimes=runtimes,
            package_managers=list(package_managers),
            build_tools=list(build_tools),
            confidence_score=confidence_score
        )
        
        # Save detection results
        self._save_detection_results(tech_stack)
        
        self.logger.info(f"Tech stack detection complete. Primary language: {primary_language}")
        return tech_stack
    
    def _analyze_package_file(self, file_path: Path, pattern: Dict) -> List[TechStackComponent]:
        """Analyze a package file to detect technologies"""
        components = []
        
        try:
            if file_path.name == "package.json":
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    
                # Add language component
                if pattern.get("language"):
                    lang_component = TechStackComponent(
                        name=pattern["language"],
                        version=data.get("engines", {}).get("node"),
                        category="language",
                        confidence=pattern["confidence"],
                        evidence_files=[str(file_path)],
                        package_manager=pattern.get("package_manager")
                    )
                    components.append(lang_component)
                
                # Check for frameworks in dependencies
                all_deps = {}
                all_deps.update(data.get("dependencies", {}))
                all_deps.update(data.get("devDependencies", {}))
                
                for framework, packages in pattern.get("frameworks", {}).items():
                    for package in packages:
                        if package in all_deps:
                            framework_component = TechStackComponent(
                                name=framework,
                                version=all_deps[package],
                                category="framework",
                                confidence=0.8,
                                evidence_files=[str(file_path)],
                                package_manager=pattern.get("package_manager")
                            )
                            components.append(framework_component)
                            break
            
            elif file_path.name in ["requirements.txt", "Pipfile"]:
                # Python package files
                if pattern.get("language"):
                    lang_component = TechStackComponent(
                        name=pattern["language"],
                        version=None,
                        category="language",
                        confidence=pattern["confidence"],
                        evidence_files=[str(file_path)],
                        package_manager=pattern.get("package_manager")
                    )
                    components.append(lang_component)
                
                # Read file content to detect frameworks
                with open(file_path, 'r') as f:
                    content = f.read().lower()
                    
                for framework, packages in pattern.get("frameworks", {}).items():
                    for package in packages:
                        if package in content:
                            framework_component = TechStackComponent(
                                name=framework,
                                version=None,
                                category="framework",
                                confidence=0.7,
                                evidence_files=[str(file_path)],
                                package_manager=pattern.get("package_manager")
                            )
                            components.append(framework_component)
                            break
            
            # Add similar logic for other package file types...
            
        except Exception as e:
            self.logger.error(f"Error analyzing {file_path}: {e}")
        
        return components
    
    def _create_component_from_pattern(self, filename: str, pattern: Dict, evidence_files: List[str]) -> Optional[TechStackComponent]:
        """Create a tech stack component from a detection pattern"""
        for key in ["language", "framework", "database", "tool", "runtime"]:
            if key in pattern:
                return TechStackComponent(
                    name=pattern[key],
                    version=None,
                    category=key,
                    confidence=pattern["confidence"],
                    evidence_files=evidence_files
                )
        return None
    
    def _save_detection_results(self, tech_stack: DetectedTechStack):
        """Save detection results to file"""
        results_file = self.tech_stack_dir / "detected-stack.json"
        
        with open(results_file, 'w') as f:
            json.dump(asdict(tech_stack), f, indent=2)
        
        self.logger.info(f"Detection results saved to {results_file}")
    
    def generate_standards_from_stack(self, tech_stack: DetectedTechStack) -> Dict[str, str]:
        """Generate appropriate standards files based on detected tech stack"""
        standards = {}
        
        # Generate tech-stack.md
        tech_stack_content = self._generate_tech_stack_md(tech_stack)
        standards["tech-stack.md"] = tech_stack_content
        
        # Generate language-specific standards
        if tech_stack.primary_language:
            lang_standards = self._generate_language_standards(tech_stack.primary_language, tech_stack)
            standards.update(lang_standards)
        
        # Generate framework-specific standards
        for framework in tech_stack.frameworks:
            framework_standards = self._generate_framework_standards(framework, tech_stack)
            standards.update(framework_standards)
        
        return standards
    
    def _generate_tech_stack_md(self, tech_stack: DetectedTechStack) -> str:
        """Generate tech-stack.md content based on detected stack"""
        content = f"""# Tech Stack

## Context

Auto-detected tech stack for this project (confidence: {tech_stack.confidence_score:.1f}).

## Primary Language
- **Language**: {tech_stack.primary_language or 'Not detected'}

## Languages
"""
        
        for lang in tech_stack.languages:
            version_str = f" {lang.version}" if lang.version else ""
            content += f"- **{lang.name.title()}**{version_str} (confidence: {lang.confidence:.1f})\n"
        
        content += "\n## Frameworks\n"
        for framework in tech_stack.frameworks:
            version_str = f" {framework.version}" if framework.version else ""
            content += f"- **{framework.name.title()}**{version_str} (confidence: {framework.confidence:.1f})\n"
        
        content += "\n## Databases\n"
        for db in tech_stack.databases:
            content += f"- **{db.name.title()}** (confidence: {db.confidence:.1f})\n"
        
        content += "\n## Tools\n"
        for tool in tech_stack.tools:
            content += f"- **{tool.name.title()}** (confidence: {tool.confidence:.1f})\n"
        
        content += "\n## Package Managers\n"
        for pm in tech_stack.package_managers:
            content += f"- {pm}\n"
        
        content += "\n## Build Tools\n"
        for bt in tech_stack.build_tools:
            if bt:  # Filter out empty strings
                content += f"- {bt}\n"
        
        return content
    
    def _generate_language_standards(self, language: str, tech_stack: DetectedTechStack) -> Dict[str, str]:
        """Generate language-specific standards"""
        standards = {}
        
        if language == "javascript" or language == "typescript":
            standards["code-style/javascript-style.md"] = self._generate_js_standards(tech_stack)
        elif language == "python":
            standards["code-style/python-style.md"] = self._generate_python_standards(tech_stack)
        elif language == "ruby":
            standards["code-style/ruby-style.md"] = self._generate_ruby_standards(tech_stack)
        # Add more languages as needed
        
        return standards
    
    def _generate_js_standards(self, tech_stack: DetectedTechStack) -> str:
        """Generate JavaScript/TypeScript standards"""
        has_typescript = any(lang.name == "typescript" for lang in tech_stack.languages)
        has_react = any(fw.name == "react" for fw in tech_stack.frameworks)
        
        content = f"""# JavaScript{'/ TypeScript' if has_typescript else ''} Code Style

## Language Standards
- Use {'TypeScript' if has_typescript else 'JavaScript'} for all new code
- Use ES6+ features and modern syntax
- Prefer const/let over var
- Use arrow functions for callbacks

## Formatting
- Use 2 spaces for indentation
- Use semicolons
- Use single quotes for strings
- Max line length: 100 characters

"""
        
        if has_react:
            content += """## React Standards
- Use functional components with hooks
- Use TypeScript for prop types
- Follow React naming conventions
- Use JSX for component rendering

"""
        
        return content
    
    def _generate_python_standards(self, tech_stack: DetectedTechStack) -> str:
        """Generate Python standards"""
        has_django = any(fw.name == "django" for fw in tech_stack.frameworks)
        has_flask = any(fw.name == "flask" for fw in tech_stack.frameworks)
        
        content = """# Python Code Style

## Language Standards
- Follow PEP 8 style guide
- Use Python 3.8+ features
- Use type hints for function signatures
- Use f-strings for string formatting

## Formatting
- Use 4 spaces for indentation
- Max line length: 88 characters (Black formatter)
- Use double quotes for strings
- Use trailing commas in multi-line structures

"""
        
        if has_django:
            content += """## Django Standards
- Follow Django naming conventions
- Use Django's built-in features over custom solutions
- Organize apps by functionality
- Use Django's migration system

"""
        elif has_flask:
            content += """## Flask Standards
- Use Flask blueprints for organization
- Use Flask-SQLAlchemy for database operations
- Follow Flask application factory pattern
- Use environment variables for configuration

"""
        
        return content
    
    def _generate_ruby_standards(self, tech_stack: DetectedTechStack) -> str:
        """Generate Ruby standards"""
        has_rails = any(fw.name == "rails" for fw in tech_stack.frameworks)
        
        content = """# Ruby Code Style

## Language Standards
- Follow Ruby community style guide
- Use Ruby 3.0+ features
- Prefer symbols over strings for keys
- Use snake_case for variables and methods

## Formatting
- Use 2 spaces for indentation
- Max line length: 120 characters
- Use single quotes for strings
- Use trailing commas in multi-line structures

"""
        
        if has_rails:
            content += """## Rails Standards
- Follow Rails conventions and patterns
- Use Rails generators appropriately
- Organize code using Rails directory structure
- Use Rails migrations for database changes

"""
        
        return content
    
    def _generate_framework_standards(self, framework: TechStackComponent, tech_stack: DetectedTechStack) -> Dict[str, str]:
        """Generate framework-specific standards"""
        standards = {}
        
        # This could be expanded to generate specific standards for each framework
        # For now, we'll include framework-specific guidelines in the main standards
        
        return standards

def main():
    """CLI interface for tech stack detector"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Agent OS Tech Stack Detector")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--detect", action="store_true", help="Detect tech stack")
    parser.add_argument("--generate-standards", action="store_true", help="Generate standards from detected stack")
    parser.add_argument("--output-dir", help="Output directory for generated standards")
    
    args = parser.parse_args()
    
    detector = TechStackDetector(args.project_root)
    
    if args.detect:
        tech_stack = detector.detect_tech_stack()
        print(f"✅ Tech stack detected. Primary language: {tech_stack.primary_language}")
        print(f"   Confidence: {tech_stack.confidence_score:.1f}")
        print(f"   Languages: {[lang.name for lang in tech_stack.languages]}")
        print(f"   Frameworks: {[fw.name for fw in tech_stack.frameworks]}")
    
    if args.generate_standards:
        # Load existing detection results
        results_file = Path(args.project_root) / ".agent-os" / "tech-stack" / "detected-stack.json"
        if results_file.exists():
            with open(results_file, 'r') as f:
                data = json.load(f)
                # Convert back to DetectedTechStack object
                tech_stack = DetectedTechStack(**data)
                
            standards = detector.generate_standards_from_stack(tech_stack)
            
            output_dir = Path(args.output_dir) if args.output_dir else Path(args.project_root) / ".agent-os" / "standards"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            for filename, content in standards.items():
                output_file = output_dir / filename
                output_file.parent.mkdir(parents=True, exist_ok=True)
                with open(output_file, 'w') as f:
                    f.write(content)
                print(f"✅ Generated: {output_file}")
        else:
            print("❌ No detection results found. Run --detect first.")

if __name__ == "__main__":
    main()

