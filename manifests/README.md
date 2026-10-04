# Manifests

This folder contains the current GitHub-package manifests for the runnable E50 VCM repository package.

## Current Files To Use

| File | Purpose |
|---|---|
| `REPOSITORY_PACKAGE_MANIFEST_CURRENT.md` | Current file inventory, sizes, and SHA-256 hashes for the repository package. The manifest intentionally omits its own self-hash. |
| `DEPLOYABILITY_REPAIR_MANIFEST_20261004.md` | Records the package-only repair that made the GitHub deployment package runnable from a fresh download. |

## Superseded Files

Older 2026-10-02 manifest stubs were removed from this folder. They described earlier package states, accepted-baseline compilation steps, or stale pre-repair inventories. The current repository reader should use only the files listed above.

## Current Runtime Location

The authoritative current runtime package is:

```text
4b - DEPLOYMENT/vcm_pi_package
```

Current launch instructions are in:

```text
4a - DEPLOYMENT_QUICKSTART.md
4b - DEPLOYMENT/vcm_pi_package/README_PI_DEPLOYMENT.md
```

## Boundary

These manifests do not modify E37, E50, E40, runtime code, model weights, response WAVs, datasets, benchmark results, or the independent E53 experiment.
