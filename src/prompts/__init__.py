"""
Prompts Module

Contains MCP prompt definitions for AI interaction templates.
Prompts provide templates that can be used to guide AI conversations.
"""

from .user_prompts import register_prompts

__all__ = [
    "register_prompts",
]

# Prompt names for reference
AVAILABLE_PROMPTS = [
    "user_management_assistant",
    "data_analysis_prompt",
    "interactive_user_prompt",
]