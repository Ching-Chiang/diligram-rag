"""Answering entry points and the output data structures.

v0.1 fixes the shapes that callers and the evaluator depend on. Retrieval and
generation are not wired yet, so ``answer`` raises ``NotImplementedError``
rather than returning an unsupported answer.

The central rule of this package: an answer without evidence is not an answer.
Use ``Answer.abstain`` when the evidence is insufficient.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

SCHEMA_VERSION = "0.1"


@dataclass(frozen=True)
class Evidence:
    """One cited span, traceable back to the parsed document.

    Attributes:
        doc_id: Document the span belongs to.
        page_no: 1-based page number.
        block_id: Block identifier from the ``doc.schema.json`` contract.
        text: The span text as used by the answer.
        quote: Optional verbatim excerpt for human verification.
    """

    doc_id: str
    page_no: int
    block_id: str
    text: str
    quote: str | None = None

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "doc_id": self.doc_id,
            "page_no": self.page_no,
            "block_id": self.block_id,
            "text": self.text,
        }
        if self.quote is not None:
            out["quote"] = self.quote
        return out


@dataclass
class Answer:
    """An answer plus the chain of evidence that supports it.

    Attributes:
        question: The original question.
        text: The answer text, or the reason for abstaining.
        evidence: Supporting spans, in the order they were used.
        abstained: True when the evidence was insufficient to answer.
    """

    question: str
    text: str
    evidence: Sequence[Evidence] = field(default_factory=tuple)
    abstained: bool = False

    def __post_init__(self) -> None:
        if not self.abstained and not self.evidence:
            raise ValueError("a non-abstained answer must cite at least one evidence span")

    @classmethod
    def abstain(cls, question: str, reason: str) -> "Answer":
        """Build an answer that explicitly reports insufficient evidence."""
        return cls(question=question, text=reason, evidence=(), abstained=True)

    def to_dict(self) -> dict[str, Any]:
        return {
            "question": self.question,
            "text": self.text,
            "abstained": self.abstained,
            "evidence": [e.to_dict() for e in self.evidence],
        }


def answer(
    question: str,
    *,
    config: Mapping[str, Any] | None = None,
) -> Answer:
    """Answer ``question`` from the indexed corpus.

    Args:
        question: Natural-language question.
        config: Optional overrides for retrieval, decomposition and generation.

    Returns:
        An ``Answer`` whose evidence spans cite ``doc.schema.json`` blocks.

    Raises:
        NotImplementedError: always, until retrieval lands in v0.2.
    """
    raise NotImplementedError(
        "retrieval and generation land in v0.2; see docs/eval.md for the "
        "baseline this must be measured against"
    )
