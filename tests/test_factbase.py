import json

import pytest

from factbase import Fact, KnowledgeNet


def test_fact_basic():
    fact = Fact("alice", "knows", "bob")
    assert fact.as_tuple() == ("alice", "knows", "bob")


def test_fact_rejects_empty():
    with pytest.raises(ValueError):
        Fact("", "knows", "bob")


def test_fact_equality_and_hash():
    assert Fact("a", "p", "b") == Fact("a", "p", "b")
    assert hash(Fact("a", "p", "b")) == hash(Fact("a", "p", "b"))
    assert Fact("a", "p", "b") != Fact("a", "p", "c")


def test_add_and_len():
    net = KnowledgeNet()
    assert net.add("a", "knows", "b") is True
    assert net.add("a", "knows", "b") is False
    assert len(net) == 1


def test_query_pattern():
    net = KnowledgeNet()
    net.add("a", "knows", "b")
    net.add("b", "knows", "c")
    net.add("a", "likes", "c")
    assert len(net.query(subject="a")) == 2
    assert len(net.query(predicate="knows")) == 2
    assert len(net.query(obj="c")) == 2
    assert len(net.query(subject="a", predicate="likes")) == 1


def test_facts_sorted():
    net = KnowledgeNet()
    net.add("b", "knows", "c")
    net.add("a", "knows", "b")
    assert [f.as_tuple() for f in net.facts()] == [("a", "knows", "b"), ("b", "knows", "c")]


# --- storage / persistence (FactBase-specific) ---


def test_merge_counts_new_facts():
    net1 = KnowledgeNet()
    net1.add("a", "knows", "b")
    net2 = KnowledgeNet()
    net2.add("a", "knows", "b")
    net2.add("c", "knows", "d")
    assert net1.merge(net2) == 1
    assert len(net1) == 2


def test_export_import_roundtrip():
    net = KnowledgeNet()
    net.add("a", "knows", "b")
    net.add("b", "knows", "c")
    payload = net.export_json()
    restored = KnowledgeNet()
    assert restored.import_json(payload) == 2
    assert restored.facts() == net.facts()


def test_import_json_reimports_are_noops():
    net = KnowledgeNet()
    net.add("a", "knows", "b")
    payload = net.export_json()
    assert net.import_json(payload) == 0


def test_import_json_rejects_malformed():
    net = KnowledgeNet()
    with pytest.raises(ValueError):
        net.import_json(json.dumps([["", "p", "o"]]))


def test_subjects_and_predicates():
    net = KnowledgeNet()
    net.add("a", "knows", "b")
    net.add("a", "likes", "c")
    net.add("d", "knows", "e")
    assert net.subjects() == ["a", "d"]
    assert net.predicates() == ["knows", "likes"]