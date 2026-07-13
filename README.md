# EuroPython 2026 — Beyond Optional in Real-World Projects

Slidev presentation: *Beyond Optional in Real-World Projects: Missing, `None`, and Unset*

## Setup

```bash
make install   # pnpm install
make dev       # pnpm exec slidev --open --force
make build     # static build to dist/
make export    # PDF export
```

## Code examples

The Python examples used in the deck are extracted into `src/` and tested with
`unittest`.

```bash
uv run python -m unittest discover -s tests
uv run ty check src tests
```

The default tox environment checks Python 3.14 plus `typing_extensions`.

```bash
uv run tox -e py314
```

Python 3.15 beta can also be checked when a beta interpreter is available. Set
`PYTHON315B1` to the beta executable. On macOS framework installs, set
`DYLD_FRAMEWORK_PATH` only if that interpreter needs it.

```bash
PYTHON315B1=python3.15 \
uv run tox -e py315b1
```
