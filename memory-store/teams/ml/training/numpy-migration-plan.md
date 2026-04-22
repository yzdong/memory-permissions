# NumPy Migration Plan (1.x → 2.x)

**Status**: In progress — blocked on `faiss-cpu` compatibility  
**Tracking issue**: ML-204  
**Owner**: @chen-ml + infra support from Platform

---

## Why We're Pinned at `numpy<2.0`

The training image (CUDA 11.7, pytorch 1.13) relies on compiled extensions that were built against numpy 1.x's C API. Specifically:

- `faiss-cpu==1.7.4` — the `.so` files in this wheel use deprecated numpy C-level APIs removed in 2.0
- An internal Cython extension in `src/data/cpp_readers/` that was compiled in 2022 and hasn't been rebuilt
- Indirect: `numba==0.57.1` also breaks on numpy 2.x

## Migration Steps

### Phase 1 — Audit (complete)

- [x] Identify all packages with numpy C-API dependencies
- [x] Check for upstream numpy 2.x compatible releases
- [x] File upstream issues where needed

### Phase 2 — Fix internal extension (in progress)

- [ ] Rebuild `src/data/cpp_readers/` with numpy 2.x-compatible calls
- [ ] Update `setup.py` to use `numpy.get_include()` correctly
- [ ] Add CI test matrix for `numpy==1.26` and `numpy==2.1`

### Phase 3 — Update faiss

- `faiss-cpu` 1.8.x claims numpy 2.x support; waiting on a stable release and internal validation
- Alternative: switch to `faiss-gpu` wheel built in-house (Platform team offered to help)

### Phase 4 — Bump base image

- Update `docker/Dockerfile.train` to use PyTorch 2.x base
- Re-run full training benchmark to confirm no regressions

## Do Not Bump numpy in the meantime

The `dep-audit` CI check in `.github/workflows/dep-audit.yml` enforces `numpy<2.0`. If you see a PR that removes this pin, flag it in review. Breaking the training image costs the team hours of debugging.

## Timeline Estimate

Phase 2 is expected to complete by end of Q1. Phase 3 depends on `faiss` upstream. No hard deadline — correctness and stability over speed.
