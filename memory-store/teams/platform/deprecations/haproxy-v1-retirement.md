# HAProxy 1.x Retirement

**Status:** Retired 2025-01-31  
**Owner:** Platform / Networking  
**Replacement:** HAProxy 2.8 LTS + Envoy sidecar for east-west traffic

## Context

We've had two HAProxy 1.8 instances fronting our internal service mesh since 2019. They worked fine but:

- 1.8 is EOL; last security patch was 2022
- No HTTP/2 support for backend connections
- Config reload was disruptive on high-throughput ACLs
- No native gRPC support — we were hacking around this

## What Changed

### North-South Traffic (External → Cluster)
Upgraded to HAProxy 2.8 LTS. Config format is backward compatible for most directives, but a few deprecated options needed cleanup:

- `reqrep` / `rspdel` directives are gone — replace with `http-request replace-header` / `http-response del-header`
- `balance roundrobin` is still valid; `leastconn` behavior slightly changed under surge conditions
- SSL config: `ssl-default-bind-options no-sslv3 no-tlsv10 no-tlsv11` is now the default, but be explicit anyway

### East-West Traffic (Service → Service)
Moved to Envoy sidecar injection. This is managed by the platform team — services don't need to change anything except ensuring they bind on the loopback port declared in `services/registry.yaml`.

## Migration Validation

After cutover we watched:
- P99 latency (expected slight improvement due to HTTP/2 multiplexing)
- Connection error rate in Datadog (`haproxy.frontend.denied_requests`)
- SSL handshake failures in the HAProxy stats page

P99 improved by about 8ms on the API gateway path. No material increase in errors.

## Old Config Archive

Old HAProxy 1.8 configs are archived at `archive/haproxy-1.8/haproxy.cfg`. Do not restore without reading the compatibility notes above.

## Related

- `runbooks/haproxy-reload.md`
- `../infrastructure/service-mesh-topology.md`
- `../infrastructure/envoy-sidecar-config.md`
