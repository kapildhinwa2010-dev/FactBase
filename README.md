# FactBase

FactBase is a small Python library for storing and querying in-memory facts represented as `(subject, predicate, object)` string triples. The repository defines a usable Python module and package configuration (version `0.1.0`); it is an early-stage library, not a standalone application or command-line tool.

## Features

- Add facts while rejecting empty or non-string fields; adding an existing triple leaves the store unchanged.
- Query facts by any combination of subject, predicate, and object, or list all facts in sorted order.
- Follow a predicate through a bounded chain, derive canonical names for connected `same_as` facts, and rank related facts with the `interference()` helper.
- Merge another `KnowledgeNet`, export facts as a JSON string, import that JSON string, and list distinct subjects or predicates.

`query()` filters the in-memory fact set. Although the implementation also maintains subject and object lookup structures, they are used by the chain helper rather than by the general query method.

## Requirements and installation

Python 3.9 or later is declared in `pyproject.toml`. The package declares `numpy>=1.24` as a dependency, although the current implementation does not import NumPy.

```bash
python -m pip install .
```

To install the development/test dependencies from the repository root instead:

```bash
python -m pip install -r requirements.txt
```

There is no CLI. Use the Python module directly:

```python
from factbase import KnowledgeNet

facts = KnowledgeNet()
facts.add("alice", "knows", "bob")
facts.add("bob", "knows", "carol")

print([fact.as_tuple() for fact in facts.query(subject="alice")])
print(facts.chain("alice", "knows"))

payload = facts.export_json()  # a JSON string; this does not write a file
restored = KnowledgeNet()
restored.import_json(payload)
```

## Tests

Run the test suite from the repository root with:

```bash
python -m pytest -q
```

On commit `05c2267a1702ea5bb04d04fb74892b6b2eb28ea8`, the suite was run locally with Python 3.12.3: **11 passed**. The GitHub Actions workflow is configured to run pytest and a compile/import smoke check with Python 3.10, 3.11, and 3.12; no hosted workflow result is asserted here.

## Limitations and scope

- Facts live in memory. JSON import/export operates on strings; the library does not automatically read or write files or provide a database backend.
- General pattern queries scan the stored facts. The project does not document measured performance or provide benchmarks.
- `chain()` follows only the first matching outgoing fact at each step, in insertion order, so it does not enumerate branches. Its default maximum is four hops.
- `derive_aliases()` only derives connected components from facts whose predicate is exactly `same_as`; it does not rewrite stored facts or provide general inference/rule execution.
- The tests cover core storage, pattern queries, merge, JSON round-tripping, and listings. They do not establish behavior for every helper or production-scale usage.
- The repository contains no API service, user interface, command-line interface, versioned persistence format, or automatic conflict resolution.

## License

The repository includes an MIT License. See [LICENSE](LICENSE).
