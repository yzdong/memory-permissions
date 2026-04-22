# gRPC-Gateway v1 Removal

**Status:** Removal targeted Q3 2025  
**Owner:** Platform / API Gateway  
**Slack:** #platform-grpc

## Background

We use `grpc-gateway` to expose gRPC services as RESTful HTTP/JSON APIs. We're still running the v1 (`github.com/grpc-ecosystem/grpc-gateway`) in three services alongside the v2 (`github.com/grpc-ecosystem/grpc-gateway/v2`). v1 is unmaintained and the protobuf serialization behavior has subtle differences that have caused two incidents where v1 and v2 services returned inconsistent field names for the same resource.

## What's Different in v2

- Uses `google.golang.org/protobuf` (not `github.com/golang/protobuf`)
- JSON field names follow proto3 JSON mapping by default (camelCase)
- Error responses use the `google.rpc.Status` format properly
- `HttpBody` handling is cleaner

## Migration Steps

1. Update import paths from `github.com/grpc-ecosystem/grpc-gateway/runtime` to `github.com/grpc-ecosystem/grpc-gateway/v2/runtime`
2. Update proto generation annotations if using `google.api.http` options — they're the same syntax but regenerate your pb files with the v2 plugin
3. Check JSON serialization behavior: v2 uses `protojson` which omits zero-value fields by default. If clients expect zero-value fields, set `EmitUnpopulated: true` in the marshaler options
4. Update `go.mod` and remove the v1 dependency

```go
// v2 mux setup
mux := runtime.NewServeMux(
    runtime.WithMarshalerOption(runtime.MIMEWildcard, &runtime.JSONPb{
        MarshalOptions: protojson.MarshalOptions{
            EmitUnpopulated: true,
        },
    }),
)
```

## Services Still on v1

| Service | Assigned To | ETA |
|---|---|---|
| routing-service | @dchang | 2025-06-01 |
| catalog-api | @mpayne | 2025-07-01 |
| search-service | @tford | 2025-07-01 |

## Related

- `runbooks/grpc-debugging.md`
- `../api-gateway/proto-conventions.md`
