# FactBase

[![CI](https://github.com/kapildhinwa2010-dev/FactBase/actions/workflows/ci.yml/badge.svg)](https://github.com/kapildhinwa2010-dev/FactBase/actions/workflows/ci.yml)
[![CodeQL](https://github.com/kapildhinwa2010-dev/FactBase/actions/workflows/codeql.yml/badge.svg)](https://github.com/kapildhinwa2010-dev/FactBase/actions/workflows/codeql.yml)


Durable fact storage: (subject, predicate, object) triples with JSON persistence and indexed queries.

**Part of the [Kapildhinwa2010-dev Toolkit](https://github.com/kapildhinwa2010-dev/Kapildhinwa2010-dev).**

## What it does

FactBase is the STORAGE layer of the fact-tool family. It holds
triples with indexed direct and reverse queries, merges other stores,
and exports/imports facts as JSON. Rules live in RuleEngine; alias
derivation in AliasDeriver; path analysis in ChainReasoner.

## Install

```bash
pip install -r requirements.txt
```

## Quick start

```python
from factbase import KnowledgeNet

a = KnowledgeNet()
a.add("alice", "knows", "bob")
b = KnowledgeNet()
b.import_json(a.export_json())
print(b.subjects())   # ["alice"]
```

## API

- add / query / facts / chain / interference - shared triple store
- merge(other) - add every fact from another store
- export_json() / import_json(payload) - persistence round-trip
- subjects() / predicates() - distinct index listings

## Honest results and limitations

- import_json validates entries and raises ValueError on malformed
  triples; it does not repair or skip them.
- Storage is in-memory only - export_json() is the only durability
  mechanism; nothing is written to disk automatically.
- No versioning, timestamps, or conflict resolution on merge.

## License

MIT - see [LICENSE](LICENSE).
