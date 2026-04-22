# Internal RPC: REST-over-HTTP/1.1 → gRPC Migration

**Status:** Opt-in for new services; mandatory for services in `services/core/` by 2025-10-01  
**Owner:** Platform  
**Tracking:** `PLAT-2901` (epic)

## Motivation

Service-to-service calls currently go over REST/JSON on HTTP/1.1. This is fine for low-frequency calls but becomes a bottleneck for the high-fanout paths (e.g., the order processing pipeline makes 12 downstream calls per request). Switching to gRPC gives us:

- HTTP/2 multiplexing — fewer TCP connections, lower latency
- Protobuf encoding — ~60% smaller payloads on most of our message shapes
- Generated client stubs — less hand-rolled HTTP client code to maintain
- Streaming support for cases where we're currently polling

## What We're NOT Doing

We are not exposing gRPC externally. The public API stays REST/JSON. This is purely internal service mesh traffic.

## Getting Started

Proto files live in `proto/` at the repo root. Each service that wants to expose a gRPC interface adds a `.proto` file there and registers in `proto/registry.yaml`.

Code generation:

```bash
# From repo root
make proto-gen SERVICE=my-service
```

This outputs generated stubs to `services/my-service/generated/`.

## Service Mesh Configuration

gRPC traffic routes through Envoy. Config is in `infra/envoy/grpc-routes.yaml`. Platform manages the base config; services add their own route entries via a PR.

## Compatibility During Transition

Services should expose both REST and gRPC during the transition window so callers can migrate at their own pace. The REST endpoints for migrated services will be deprecated per the standard 90-day policy (see `deprecated-endpoints-2025.md`).

## Services Migrated So Far

- `services/core/user-service` — done, gRPC-only internally
- `services/core/inventory` — gRPC live, REST still running
- `services/billing-worker` — planned Q3 2025

## References

- `proto/README.md`
- `infra/envoy/README.md`
- `runbooks/grpc-debugging.md`
