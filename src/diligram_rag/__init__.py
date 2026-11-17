"""diligram-rag: multi-hop retrieval and answering over parsed documents.

Input documents follow the ``doc.schema.json`` contract owned by
``diligram-ocr-vlm``; this package is a consumer of that contract and never
re-implements parsing.
"""

from __future__ import annotations

from .pipeline import Answer, Evidence, answer

__all__ = ["Answer", "Evidence", "answer"]
__version__ = "0.1.0"
