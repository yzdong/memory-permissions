# Input Preprocessing Contracts

This documents what preprocessing ML inference expects vs what Platform's API service sends. Mismatches here are a recurring source of subtle bugs.

## Why This Document Exists

In August, we had a 4-hour latency degradation because Platform updated their tokenizer to use a newer vocabulary file while our model still expected the old one. Scores didn't break (no hard errors) but quality tanked. We caught it through offline evaluation, not monitoring.

## Contract: ranker_v8

**Input:**
```json
{
  "inputs": [
    {"name": "input_ids",      "datatype": "INT64", "shape": [batch, 512]},
    {"name": "attention_mask", "datatype": "INT64", "shape": [batch, 512]}
  ]
}
```

**Tokenizer:** HuggingFace `bert-base-uncased`, vocab v4.31.0
**Max sequence length:** 512 (pad with 0, truncate right)
**CLS/SEP tokens:** Must be present — Platform is responsible for adding them

**Output:**
```json
{"outputs": [{"name": "logits", "datatype": "FP32", "shape": [batch, 1]}]}
```

## Contract: embedder_v3

**Input:**
```json
{
  "inputs": [
    {"name": "input_ids",      "datatype": "INT64", "shape": [batch, 256]},
    {"name": "attention_mask", "datatype": "INT64", "shape": [batch, 256]}
  ]
}
```

**Tokenizer:** Same as ranker_v8 (important — they must stay in sync)
**Max sequence length:** 256 for embedder (catalog items are shorter)
**Output:** `[batch, 768]` float32 embedding vector

## Versioning

Tokenizer version is embedded in the Triton model metadata as a custom property:

```bash
curl triton-svc:8000/v2/models/ranker_v8 | jq '.parameters.tokenizer_version'
# "hf-bert-base-uncased-4.31.0"
```

Platform's preprocessing service reads this and validates on startup. If there's a mismatch, Platform should fail fast rather than silently serve wrong results.

## Validation Test

```bash
# Run the contract validation against staging
python tools/validate_contract.py \
  --triton-url http://triton-staging-svc:8000 \
  --model ranker_v8 \
  --test-payloads tests/fixtures/ranker_contract_payloads.jsonl
```

This runs as part of CI on any change to `triton/model_repository/`.

## Change Process

Any change to tokenizer version, max sequence length, or input/output schema:
1. File an issue tagged `infra-contract-change`
2. Get sign-off from Platform (@platform-ml-liaison)
3. Coordinate staged rollout (both sides must update in same deploy window)

Related: `triton-serving-setup.md`, `../platform-handoff/api-contract.md`
