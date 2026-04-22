# S3 Path-Style Access Removal

**Status:** Blocking items remain — see tracker  
**Owner:** Platform Infra  
**AWS Enforcement Date:** Already enforced for new buckets; legacy buckets get enforcement by end of 2025

## Problem

Path-style S3 access (`https://s3.amazonaws.com/<bucket>/<key>`) was deprecated by AWS years ago in favor of virtual-hosted style (`https://<bucket>.s3.amazonaws.com/<key>`). AWS has started enforcing this for new buckets and will extend enforcement to older buckets.

We have services constructing S3 URLs manually instead of using the SDK. Those will break.

## Finding Offending Code

```bash
# Find hardcoded path-style URL construction
grep -rn 's3\.amazonaws\.com/' services/ --include="*.py" --include="*.go" | grep -v '.amazonaws.com/'