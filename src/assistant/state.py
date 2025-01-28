"""State management for the research assistant.

This module defines the state classes used to track research progress
and manage data flow between graph nodes."""

import operator
from dataclasses import dataclass, field
from typing_extensions import TypedDict, Annotated

@dataclass(kw_only=True)
class SummaryState:
    """State for tracking research progress.
    
    Attributes:
        research_topic: Topic to research
        search_query: Current search query
        web_research_results: List of raw research results
        sources_gathered: List of formatted sources
        research_loop_count: Number of research iterations completed
        running_summary: Current summary of findings
        max_research_loops: Maximum number of research iterations
    """
    research_topic: str = field(default=None)  # Report topic     
    search_query: str = field(default=None)  # Search query
    web_research_results: Annotated[list, operator.add] = field(default_factory=list) 
    sources_gathered: Annotated[list, operator.add] = field(default_factory=list) 
    research_loop_count: int = field(default=0)  # Research loop count
    running_summary: str = field(default=None)  # Final report
    max_research_loops: int = field(default=3)  # Maximum research iterations

@dataclass(kw_only=True)
class SummaryStateInput(TypedDict):
    """Input state for initializing research.
    
    Attributes:
        research_topic: Topic to research
        max_research_loops: Optional maximum number of research iterations
    """
    research_topic: str = field(default=None)  # Report topic
    max_research_loops: int = field(default=3)  # Maximum research iterations

@dataclass(kw_only=True)
class SummaryStateOutput(TypedDict):
    """Output state containing research results.
    
    Attributes:
        running_summary: Final research summary
    """
    running_summary: str = field(default=None)  # Final report