"""Configuration management for the research assistant.

This module provides configuration classes and utilities for managing
research assistant settings and runtime parameters."""

import os
from dataclasses import dataclass
from typing import Any, Optional

from dotenv import load_dotenv
from langchain_core.runnables import RunnableConfig

# Load environment variables at module import
load_dotenv()

@dataclass(kw_only=True)
class Configuration:
    """Configuration parameters for the research assistant.
    
    Attributes:
        max_web_research_loops: Maximum number of research iterations.
        model: Name of the DeepSeek chat model to use.
    """
    max_web_research_loops: int = 3
    model: str = "deepseek-chat"

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "Configuration":
        """Create a Configuration instance from a RunnableConfig.
        
        Args:
            config: Optional RunnableConfig instance with configuration parameters.
            
        Returns:
            Configuration: New instance with parameters from config.
        """
        if not config:
            return cls()
            
        config_dict = config.get("configurable", {})
        return cls(**{
            k: v for k, v in config_dict.items()
            if k in [f.name for f in cls.__dataclass_fields__.values()]
        })