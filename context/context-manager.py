#!/usr/bin/env python3
"""
Enhanced Agent OS Context Manager
Handles smart context loading, monitoring, and optimization for large-scale projects
"""

import os
import json
import time
import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import yaml

@dataclass
class ContextItem:
    """Represents a single context item with metadata"""
    path: str
    content: str
    size: int
    relevance_score: float
    last_accessed: float
    hash: str
    category: str  # 'standards', 'product', 'specs', 'code'

class ContextManager:
    """Smart context manager for Agent OS"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.agent_os_dir = self.project_root / ".agent-os"
        self.context_dir = self.agent_os_dir / "context"
        self.cache_dir = self.context_dir / "cache"
        self.analysis_dir = self.context_dir / "analysis"
        
        # Create directories if they don't exist
        self.context_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(exist_ok=True)
        self.analysis_dir.mkdir(exist_ok=True)
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize logging
        self._setup_logging()
        
        # Context storage
        self.context_items: Dict[str, ContextItem] = {}
        self.current_context_size = 0
        self.max_context_size = self.config.get('context_management', {}).get('max_context_size', 180000)
        self.warning_threshold = self.config.get('context_management', {}).get('warning_threshold', 150000)
        
        # Load cached context
        self._load_cache()
    
    def _load_config(self) -> Dict:
        """Load enhanced configuration"""
        config_path = self.agent_os_dir / "config" / "enhanced-config.yml"
        if config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def _setup_logging(self):
        """Setup logging for context manager"""
        log_dir = self.agent_os_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "context-manager.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("ContextManager")
    
    def _calculate_file_hash(self, content: str) -> str:
        """Calculate hash for content to detect changes"""
        return hashlib.md5(content.encode()).hexdigest()
    
    def _load_cache(self):
        """Load cached context items"""
        cache_file = self.cache_dir / "context_cache.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                    
                for item_data in cache_data.get('items', []):
                    context_item = ContextItem(**item_data)
                    # Verify file still exists and hasn't changed
                    if Path(context_item.path).exists():
                        with open(context_item.path, 'r') as f:
                            current_content = f.read()
                            current_hash = self._calculate_file_hash(current_content)
                            
                        if current_hash == context_item.hash:
                            self.context_items[context_item.path] = context_item
                            self.current_context_size += context_item.size
                        else:
                            self.logger.info(f"File changed, invalidating cache: {context_item.path}")
                            
            except Exception as e:
                self.logger.error(f"Error loading cache: {e}")
    
    def _save_cache(self):
        """Save context items to cache"""
        cache_file = self.cache_dir / "context_cache.json"
        cache_data = {
            'timestamp': time.time(),
            'items': [
                {
                    'path': item.path,
                    'content': item.content,
                    'size': item.size,
                    'relevance_score': item.relevance_score,
                    'last_accessed': item.last_accessed,
                    'hash': item.hash,
                    'category': item.category
                }
                for item in self.context_items.values()
            ]
        }
        
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)
    
    def _calculate_relevance_score(self, file_path: str, current_task: str = "") -> float:
        """Calculate relevance score for a file based on current task and file type"""
        path = Path(file_path)
        score = 0.5  # Base score
        
        # Category-based scoring
        if "standards" in str(path):
            score += 0.3
        elif "product" in str(path):
            score += 0.2
        elif "specs" in str(path):
            score += 0.4
        elif path.suffix in ['.py', '.js', '.ts', '.rb', '.java']:
            score += 0.1
        
        # Task-based scoring
        if current_task:
            task_lower = current_task.lower()
            file_content_lower = path.name.lower()
            
            # Check for keyword matches
            keywords = task_lower.split()
            for keyword in keywords:
                if keyword in file_content_lower:
                    score += 0.2
        
        # Recency scoring
        try:
            mtime = path.stat().st_mtime
            age_days = (time.time() - mtime) / 86400
            if age_days < 1:
                score += 0.1
            elif age_days < 7:
                score += 0.05
        except:
            pass
        
        return min(score, 1.0)
    
    def add_context_file(self, file_path: str, category: str = "unknown", current_task: str = "") -> bool:
        """Add a file to context with smart loading"""
        path = Path(file_path)
        
        if not path.exists():
            self.logger.warning(f"File not found: {file_path}")
            return False
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.logger.error(f"Error reading file {file_path}: {e}")
            return False
        
        file_size = len(content)
        file_hash = self._calculate_file_hash(content)
        relevance_score = self._calculate_relevance_score(file_path, current_task)
        
        # Check if adding this file would exceed context limit
        if self.current_context_size + file_size > self.max_context_size:
            self.logger.warning(f"Adding {file_path} would exceed context limit")
            # Try to make room by removing least relevant items
            if not self._make_room_for_file(file_size):
                return False
        
        context_item = ContextItem(
            path=str(path),
            content=content,
            size=file_size,
            relevance_score=relevance_score,
            last_accessed=time.time(),
            hash=file_hash,
            category=category
        )
        
        self.context_items[str(path)] = context_item
        self.current_context_size += file_size
        
        self.logger.info(f"Added to context: {file_path} (size: {file_size}, relevance: {relevance_score:.2f})")
        
        # Check if we're approaching the warning threshold
        if self.current_context_size > self.warning_threshold:
            self.logger.warning(f"Context size ({self.current_context_size}) approaching limit ({self.max_context_size})")
        
        return True
    
    def _make_room_for_file(self, required_size: int) -> bool:
        """Remove least relevant items to make room for new file"""
        if not self.context_items:
            return False
        
        # Sort by relevance score (ascending) and last accessed (ascending)
        sorted_items = sorted(
            self.context_items.values(),
            key=lambda x: (x.relevance_score, x.last_accessed)
        )
        
        freed_space = 0
        items_to_remove = []
        
        for item in sorted_items:
            if freed_space >= required_size:
                break
            items_to_remove.append(item.path)
            freed_space += item.size
        
        if freed_space >= required_size:
            for path in items_to_remove:
                self.remove_context_file(path)
                self.logger.info(f"Removed from context to make room: {path}")
            return True
        
        return False
    
    def remove_context_file(self, file_path: str):
        """Remove a file from context"""
        if file_path in self.context_items:
            item = self.context_items[file_path]
            self.current_context_size -= item.size
            del self.context_items[file_path]
            self.logger.info(f"Removed from context: {file_path}")
    
    def get_context_summary(self) -> Dict:
        """Get summary of current context"""
        categories = {}
        for item in self.context_items.values():
            if item.category not in categories:
                categories[item.category] = {'count': 0, 'size': 0}
            categories[item.category]['count'] += 1
            categories[item.category]['size'] += item.size
        
        return {
            'total_items': len(self.context_items),
            'total_size': self.current_context_size,
            'max_size': self.max_context_size,
            'usage_percentage': (self.current_context_size / self.max_context_size) * 100,
            'categories': categories,
            'warning_threshold': self.warning_threshold,
            'approaching_limit': self.current_context_size > self.warning_threshold
        }
    
    def optimize_context(self, current_task: str = ""):
        """Optimize context by updating relevance scores and removing low-relevance items"""
        self.logger.info("Optimizing context...")
        
        # Update relevance scores
        for item in self.context_items.values():
            item.relevance_score = self._calculate_relevance_score(item.path, current_task)
        
        # Remove items with very low relevance if we're over the warning threshold
        if self.current_context_size > self.warning_threshold:
            low_relevance_items = [
                item.path for item in self.context_items.values()
                if item.relevance_score < 0.3
            ]
            
            for path in low_relevance_items:
                self.remove_context_file(path)
                self.logger.info(f"Removed low-relevance item: {path}")
        
        self._save_cache()
        self.logger.info("Context optimization complete")
    
    def get_relevant_context(self, task: str, max_items: int = 20) -> List[ContextItem]:
        """Get most relevant context items for a specific task"""
        # Update relevance scores for current task
        for item in self.context_items.values():
            item.relevance_score = self._calculate_relevance_score(item.path, task)
            item.last_accessed = time.time()
        
        # Sort by relevance score (descending)
        sorted_items = sorted(
            self.context_items.values(),
            key=lambda x: x.relevance_score,
            reverse=True
        )
        
        return sorted_items[:max_items]
    
    def generate_context_report(self) -> str:
        """Generate a detailed context usage report"""
        summary = self.get_context_summary()
        
        report = f"""
# Context Usage Report

## Summary
- Total Items: {summary['total_items']}
- Total Size: {summary['total_size']:,} characters
- Max Size: {summary['max_size']:,} characters
- Usage: {summary['usage_percentage']:.1f}%
- Status: {'⚠️ Approaching Limit' if summary['approaching_limit'] else '✅ Normal'}

## Categories
"""
        
        for category, data in summary['categories'].items():
            report += f"- {category.title()}: {data['count']} items, {data['size']:,} characters\n"
        
        report += "\n## Top 10 Most Relevant Items\n"
        
        sorted_items = sorted(
            self.context_items.values(),
            key=lambda x: x.relevance_score,
            reverse=True
        )
        
        for i, item in enumerate(sorted_items[:10], 1):
            report += f"{i}. {item.path} (relevance: {item.relevance_score:.2f}, size: {item.size:,})\n"
        
        return report

def main():
    """CLI interface for context manager"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Agent OS Context Manager")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--add-file", help="Add file to context")
    parser.add_argument("--remove-file", help="Remove file from context")
    parser.add_argument("--optimize", action="store_true", help="Optimize context")
    parser.add_argument("--report", action="store_true", help="Generate context report")
    parser.add_argument("--task", default="", help="Current task for relevance scoring")
    
    args = parser.parse_args()
    
    manager = ContextManager(args.project_root)
    
    if args.add_file:
        success = manager.add_context_file(args.add_file, current_task=args.task)
        print(f"{'✅' if success else '❌'} Add file: {args.add_file}")
    
    if args.remove_file:
        manager.remove_context_file(args.remove_file)
        print(f"✅ Removed file: {args.remove_file}")
    
    if args.optimize:
        manager.optimize_context(args.task)
        print("✅ Context optimized")
    
    if args.report:
        print(manager.generate_context_report())
    
    # Always show summary
    summary = manager.get_context_summary()
    print(f"\nContext: {summary['total_items']} items, {summary['usage_percentage']:.1f}% usage")

if __name__ == "__main__":
    main()

