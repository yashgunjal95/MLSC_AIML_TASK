"""Multi-language code parser using tree-sitter and AST"""

import ast
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

@dataclass
class CodeChunk:
    """Represents a chunk of code"""
    content: str
    file_path: str
    language: str
    chunk_type: str  # function, class, module
    name: Optional[str]
    start_line: int
    end_line: int
    metadata: Dict

class CodeParser:
    """Parse code files and extract meaningful chunks"""
    
    def __init__(self):
        self.parsers = {}
    
    def parse_file(self, file_path: str, content: str, language: str) -> List[CodeChunk]:
        """Parse file and return code chunks"""
        if language == "python":
            return self._parse_python(file_path, content)
        elif language in ["javascript", "typescript"]:
            return self._parse_javascript(file_path, content)
        else:
            return self._parse_generic(file_path, content, language)
    
    def _parse_python(self, file_path: str, content: str) -> List[CodeChunk]:
        """Parse Python code using AST"""
        chunks = []
        try:
            tree = ast.parse(content)
            lines = content.split('\n')
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    start = node.lineno
                    end = node.end_lineno or start
                    chunk_content = '\n'.join(lines[start-1:end])
                    
                    chunks.append(CodeChunk(
                        content=chunk_content,
                        file_path=file_path,
                        language="python",
                        chunk_type="function",
                        name=node.name,
                        start_line=start,
                        end_line=end,
                        metadata={"args": [arg.arg for arg in node.args.args]}
                    ))
                
                elif isinstance(node, ast.ClassDef):
                    start = node.lineno
                    end = node.end_lineno or start
                    chunk_content = '\n'.join(lines[start-1:end])
                    
                    chunks.append(CodeChunk(
                        content=chunk_content,
                        file_path=file_path,
                        language="python",
                        chunk_type="class",
                        name=node.name,
                        start_line=start,
                        end_line=end,
                        metadata={"methods": [m.name for m in node.body if isinstance(m, ast.FunctionDef)]}
                    ))
            
            # Add module-level chunk if no functions/classes found
            if not chunks:
                chunks.append(CodeChunk(
                    content=content,
                    file_path=file_path,
                    language="python",
                    chunk_type="module",
                    name=Path(file_path).stem,
                    start_line=1,
                    end_line=len(lines),
                    metadata={}
                ))
                
        except Exception as e:
            logger.error(f"Error parsing Python file {file_path}: {e}")
            chunks = [self._create_fallback_chunk(file_path, content, "python")]
        
        return chunks
    
    def _parse_javascript(self, file_path: str, content: str) -> List[CodeChunk]:
        """Parse JavaScript/TypeScript code"""
        # Simple regex-based parsing for functions
        import re
        chunks = []
        lines = content.split('\n')
        
        # Find function declarations
        function_pattern = r'(function\s+(\w+)|const\s+(\w+)\s*=\s*.*?=>|(\w+)\s*:\s*function)'
        
        for match in re.finditer(function_pattern, content):
            func_name = match.group(2) or match.group(3) or match.group(4)
            start_pos = content[:match.start()].count('\n') + 1
            
            # Simple heuristic: find matching braces
            brace_count = 0
            end_pos = start_pos
            for i, line in enumerate(lines[start_pos-1:], start=start_pos):
                brace_count += line.count('{') - line.count('}')
                end_pos = i
                if brace_count == 0 and '{' in line:
                    break
            
            chunk_content = '\n'.join(lines[start_pos-1:end_pos])
            chunks.append(CodeChunk(
                content=chunk_content,
                file_path=file_path,
                language="javascript",
                chunk_type="function",
                name=func_name,
                start_line=start_pos,
                end_line=end_pos,
                metadata={}
            ))
        
        if not chunks:
            chunks = [self._create_fallback_chunk(file_path, content, "javascript")]
        
        return chunks
    
    def _parse_generic(self, file_path: str, content: str, language: str) -> List[CodeChunk]:
        """Generic parsing for unsupported languages"""
        return [self._create_fallback_chunk(file_path, content, language)]
    
    def _create_fallback_chunk(self, file_path: str, content: str, language: str) -> CodeChunk:
        """Create a single chunk for entire file"""
        lines = content.split('\n')
        return CodeChunk(
            content=content,
            file_path=file_path,
            language=language,
            chunk_type="module",
            name=Path(file_path).stem,
            start_line=1,
            end_line=len(lines),
            metadata={}
        )