import pytest

from temporalmemory import Fact, KnowledgeNet


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


def test_derive_aliases_transitive():
    net = KnowledgeNet()
    net.add("x", "same_as", "y")
    net.add("y", "same_as", "z")
    aliases = net.derive_aliases()
    assert aliases["x"] == aliases["y"] == aliases["z"]


def test_derive_aliases_ignores_other_predicates():
    net = KnowledgeNet()
    net.add("x", "knows", "y")
    assert net.derive_aliases() == {}


def test_chain_walk():
    net = KnowledgeNet()
    net.add("a", "next", "b")
    net.add("b", "next", "c")
    net.add("c", "next", "d")
    assert net.chain("a", "next") == ["b", "c", "d"]


def test_chain_respects_max_hops():
    net = KnowledgeNet()
    net.add("a", "next", "b")
    net.add("b", "next", "c")
    assert net.chain("a", "next", max_hops=1) == ["b"]


def test_chain_handles_cycles():
    net = KnowledgeNet()
    net.add("a", "next", "b")
    net.add("b", "next", "a")
    assert net.chain("a", "next") == ["b"]


def test_interference_ranks_related():
    net = KnowledgeNet()
    net.add("hub", "knows", "a")
    net.add("hub", "knows", "b")
    net.add("lonely", "knows", "c")
    top = net.interference("hub")
    assert top and top[0].subject == "hub"


def test_chain_rejects_bad_hops():
    net = KnowledgeNet()
    with pytest.raises(ValueError):
        net.chain("a", "next", max_hops=0)
