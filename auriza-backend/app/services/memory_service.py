"""
Memory Service - Handles long-term and short-term user memory
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)


class MemoryService:
    """
    Manages AURIZA's memory system:
    - Short-term memory (current session)
    - Long-term memory (persistent user profile)
    - Pattern learning
    """
    
    def __init__(self):
        self.short_term_memory: Dict[str, List[Dict[str, Any]]] = {}
        self.long_term_memory: Dict[str, Dict[str, Any]] = {}
        self.patterns: Dict[str, Dict[str, Any]] = {}
        
    async def store_memory(
        self,
        user_id: str,
        content: str,
        memory_type: str = "short_term",
        tags: Optional[List[str]] = None,
        importance: int = 1
    ) -> None:
        """
        Store a memory for a user
        
        Args:
            user_id: User identifier
            content: Memory content
            memory_type: "short_term" or "long_term"
            tags: List of tags for organization
            importance: Importance level (1-10)
        """
        
        memory_entry = {
            "content": content,
            "tags": tags or [],
            "importance": importance,
            "timestamp": datetime.now().isoformat()
        }
        
        if memory_type == "short_term":
            if user_id not in self.short_term_memory:
                self.short_term_memory[user_id] = []
            self.short_term_memory[user_id].append(memory_entry)
            
            # Keep only last 100 short-term memories
            if len(self.short_term_memory[user_id]) > 100:
                self.short_term_memory[user_id] = self.short_term_memory[user_id][-100:]
        
        elif memory_type == "long_term":
            if user_id not in self.long_term_memory:
                self.long_term_memory[user_id] = {}
            
            # Store with key based on tags or generic
            key = "_".join(tags) if tags else f"memory_{datetime.now().timestamp()}"
            self.long_term_memory[user_id][key] = memory_entry
    
    async def retrieve_memory(
        self,
        user_id: str,
        memory_type: str = "short_term",
        tags: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Retrieve memories for a user
        
        Args:
            user_id: User identifier
            memory_type: Type of memory to retrieve
            tags: Filter by tags
            limit: Maximum number of memories
        
        Returns:
            List of memories
        """
        
        memories = []
        
        if memory_type == "short_term" and user_id in self.short_term_memory:
            memories = self.short_term_memory[user_id]
        elif memory_type == "long_term" and user_id in self.long_term_memory:
            memories = list(self.long_term_memory[user_id].values())
        
        # Filter by tags if provided
        if tags:
            memories = [
                m for m in memories
                if any(tag in m.get("tags", []) for tag in tags)
            ]
        
        # Sort by importance and timestamp, return most recent
        memories = sorted(
            memories,
            key=lambda x: (-x.get("importance", 0), x.get("timestamp", "")),
            reverse=True
        )
        
        return memories[:limit]
    
    async def learn_pattern(
        self,
        user_id: str,
        pattern_name: str,
        pattern_data: Dict[str, Any],
        confidence: float = 0.5
    ) -> None:
        """
        Learn a user pattern (behavior, preferences, etc.)
        
        Example: 
        - \"morning_routine\": open_spotify, set_volume_high
        - \"work_hours\": disable_notifications
        """
        
        if user_id not in self.patterns:
            self.patterns[user_id] = {}
        
        self.patterns[user_id][pattern_name] = {
            "data": pattern_data,
            "confidence": confidence,
            "last_used": datetime.now().isoformat(),
            "usage_count": self.patterns[user_id].get(pattern_name, {}).get("usage_count", 0) + 1
        }
        
        logger.info(f"Learned pattern '{pattern_name}' for user {user_id}")
    
    async def get_patterns(self, user_id: str) -> Dict[str, Any]:
        """Get all learned patterns for a user"""
        return self.patterns.get(user_id, {})
    
    async def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get complete user profile/context"""
        
        return {
            "user_id": user_id,
            "short_term_memory_count": len(self.short_term_memory.get(user_id, [])),
            "long_term_memory_count": len(self.long_term_memory.get(user_id, {})),
            "learned_patterns": list(self.patterns.get(user_id, {}).keys()),
            "patterns_confidence": {
                name: data.get("confidence", 0)
                for name, data in self.patterns.get(user_id, {}).items()
            }
        }
    
    async def clear_old_memories(
        self,
        user_id: str,
        memory_type: str = "short_term",
        days_old: int = 30
    ) -> int:
        """Clear memories older than specified days"""
        
        cutoff_date = datetime.now() - timedelta(days=days_old)
        removed_count = 0
        
        if memory_type == "short_term" and user_id in self.short_term_memory:
            initial_count = len(self.short_term_memory[user_id])
            self.short_term_memory[user_id] = [
                m for m in self.short_term_memory[user_id]
                if datetime.fromisoformat(m.get("timestamp", "")) > cutoff_date
            ]
            removed_count = initial_count - len(self.short_term_memory[user_id])
        
        logger.info(f"Cleared {removed_count} old memories for user {user_id}")
        return removed_count
