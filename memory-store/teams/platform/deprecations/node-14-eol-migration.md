# Node.js 14 End-of-Life Migration

**Status:** Complete  
**Completed:** 2024-12-15  
**Owner:** Platform + frontend teams

## Summary

Node 14 reached EOL in April 2023. We kept it running for 18 months longer than ideal due to a dependency on a native addon (`canvas`) that didn't have pre-built binaries for Node 18 until mid-2024. That blocker is resolved; we've now moved to Node 20 LTS across the board.

## Services Updated

- `services/web-frontend` — Node 20, Webpack 5
- `services/admin-ui` — Node 20, Vite (replaced Webpack in this migration)
- `services/webhook-proxy` — Node 20, no framework changes
- `tools/cli` — Node 20; minimum Node version requirement bumped in package.json

## Things That Broke

### `crypto` module changes

Node 18+ uses OpenSSL 3, which deprecated some cipher suites. Code using `createCipher` (not `createCipheriv`) threw errors. Fixed in `services/webhook-proxy/crypto-utils.js`.

### `--openssl-legacy-provider` flag

Webpack 4 needed this flag on Node 17+. Migrating to Webpack 5 (or Vite) removed the need for it entirely. Do not carry this flag forward.

### ESM / CJS interop

Several packages updated to ESM-only between Node 14 and now. Ran into this with `node-fetch` v3 and `chalk` v5. Solutions:
- Pin `node-fetch` to `^2.7` (still maintained, CJS)
- Update `chalk` usage to v5 with dynamic `import()` or switch to `picocolors`

## Docker Base Images

All Dockerfiles updated:
```dockerfile
# Before
FROM node:14-alpine

# After
FROM node:20-alpine
```

## CI

GitHub Actions matrix updated in `.github/workflows/frontend-ci.yml`. Node 14 job removed; Node 20 and Node 22 (experimental) added.

## References

- `runbooks/frontend-deploy.md`
- [Node.js release schedule](https://github.com/nodejs/release#release-schedule)
