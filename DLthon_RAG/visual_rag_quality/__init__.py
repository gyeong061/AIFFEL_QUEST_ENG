"""Quality, comparison, and reproducibility tools for visual RAG."""

from .gate import GateReport, QualityGate
from .pipeline import QualityAwarePipeline
from .schemas import ComicRequest, PipelineConfig

__all__ = [
    "ComicRequest",
    "GateReport",
    "PipelineConfig",
    "QualityAwarePipeline",
    "QualityGate",
]

__version__ = "0.1.0"

