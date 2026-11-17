import pytest

from diligram_rag import Answer, Evidence


def make_evidence() -> Evidence:
    return Evidence(
        doc_id="sample-idcard-0001",
        page_no=1,
        block_id="p1-b2",
        text="姓名 张三",
        quote="姓名 张三",
    )


def test_answer_serialises_evidence():
    ans = Answer(question="张三的姓名是？", text="张三", evidence=[make_evidence()])
    payload = ans.to_dict()

    assert payload["abstained"] is False
    assert payload["evidence"][0]["block_id"] == "p1-b2"
    assert payload["evidence"][0]["page_no"] == 1
    assert payload["evidence"][0]["quote"] == "姓名 张三"


def test_answer_without_evidence_is_rejected():
    with pytest.raises(ValueError):
        Answer(question="某问题", text="某答案", evidence=[])


def test_abstain_carries_no_evidence():
    ans = Answer.abstain("无法回答的问题", "证据不足")

    assert ans.abstained is True
    assert ans.to_dict()["evidence"] == []
    assert ans.text == "证据不足"


def test_evidence_without_quote_omits_field():
    ev = Evidence(doc_id="d", page_no=2, block_id="p2-b1", text="片段")
    assert "quote" not in ev.to_dict()
