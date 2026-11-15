# TemporalMemory - Fact memory with multi-hop event chains derived at query time
# Part of the Kapildhinwa2010-dev Toolkit.

"""KnowledgeNet - facts, alias derivation and chain reasoning.

Lineage: reserv.dean-part-2 (HELIX). Facts are stored as (subject, predicate,
object) triples; aliases are derived transitively from equality facts; chain
reasoning walks predicates to answer multi-hop queries.
"""

from __future__ import annotations

from collections import defaultdict

import numpy as np

__all__ = ["Fact", "KnowledgeNet"]


class Fact:
    """A single (subject, predicate, object) triple."""

    __slots__ = ("subject", "predicate", "object")

    def __init__(self, subject: str, predicate: str, obj: str) -> None:
        for value in (subject, predicate, obj):
            if not isinstance(value, str) or not value:
                raise ValueError("subject, predicate and object must be non-empty strings")
        self.subject = subject
        self.predicate = predicate
        self.object = obj

    def as_tuple(self):
        return (self.subject, self.predicate, self.object)

    def __eq__(self, other) -> bool:
        return isinstance(other, Fact) and self.as_tuple() == other.as_tuple()

    def __hash__(self) -> int:
        return hash(self.as_tuple())

    def __repr__(self) -> str:
        return "Fact({!r}, {!r}, {!r})".format(*self.as_tuple())


class KnowledgeNet:
    """Zero-overhead fact base with alias and chain reasoning."""

    def __init__(self) -> None:
        self._facts: set = set()
        self._by_subject: dict = defaultdict(list)
        self._by_object: dict = defaultdict(list)

    def add(self, subject: str, predicate: str, obj: str) -> bool:
        """Add a fact; returns False if it already exists."""
        fact = Fact(subject, predicate, obj)
        if fact in self._facts:
            return False
        self._facts.add(fact)
        self._by_subject[fact.subject].append(fact)
        self._by_object[fact.object].append(fact)
        return True

    def facts(self):
        return sorted(self._facts, key=lambda f: f.as_tuple())

    def __len__(self) -> int:
        return len(self._facts)

    def query(self, subject=None, predicate=None, obj=None):
        """Return facts matching the given pattern (None = wildcard)."""
        results = self._facts
        if subject is not None:
            results = [f for f in results if f.subject == subject]
        if predicate is not None:
            results = [f for f in results if f.predicate == predicate]
        if obj is not None:
            results = [f for f in results if f.object == obj]
        return sorted(results, key=lambda f: f.as_tuple())

    def derive_aliases(self) -> dict:
        """Transitive closure of ``same_as`` equality facts."""
        adjacency: dict = defaultdict(set)
        for fact in self._facts:
            if fact.predicate == "same_as":
                adjacency[fact.subject].add(fact.object)
                adjacency[fact.object].add(fact.subject)
        aliases: dict = {}
        for node in list(adjacency):
            if node in aliases:
                continue
            component = set()
            stack = [node]
            while stack:
                current = stack.pop()
                if current in component:
                    continue
                component.add(current)
                stack.extend(adjacency[current] - component)
            canonical = min(component)
            for member in component:
                aliases[member] = canonical
        return aliases

    def chain(self, start: str, predicate: str, max_hops: int = 4) -> list:
        """Multi-hop walk following ``predicate`` from ``start``."""
        if max_hops < 1:
            raise ValueError("max_hops must be >= 1")
        hops = []
        current = start
        seen = {start}
        for _ in range(max_hops):
            nxt = [f.object for f in self._by_subject.get(current, []) if f.predicate == predicate]
            if not nxt:
                break
            hops.append(nxt[0])
            if nxt[0] in seen:
                break
            seen.add(nxt[0])
            current = nxt[0]
        return hops

    def interference(self, query: str, top_k: int = 3) -> list:
        """Rank facts related to ``query`` by co-occurrence interference."""
        if top_k < 1:
            raise ValueError("top_k must be >= 1")
        scores: dict = {}
        for fact in self._facts:
            if query in (fact.subject, fact.object):
                related = self.query(subject=fact.object) + self.query(obj=fact.subject)
                scores[fact] = len(related)
        ranked = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0].as_tuple()))
        return [fact for fact, _ in ranked[:top_k]]
