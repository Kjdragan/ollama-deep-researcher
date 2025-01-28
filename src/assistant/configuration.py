import os
from dataclasses import dataclass, field, fields
from typing import Any, Optional
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

from langchain_core.runnables import RunnableConfig
from typing_extensions import Annotated

@dataclass(kw_only=True)
class Configuration:
    """The configurable fields for the research assistant."""
    max_web_research_loops: int = 3
    model: str = "deepseek-chat"  # DeepSeek chat model

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "Configuration":
        """Create a Configuration instance from a RunnableConfig."""
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )
        values: dict[str, Any] = {
            f.name: os.environ.get(f.name.upper(), configurable.get(f.name))
            for f in fields(cls)
            if f.init
        }
        return cls(**{k: v for k, v in values.items() if v})