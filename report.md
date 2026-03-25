# Cursor Composer 2 — OpenThoughts-TBLite Benchmark Report

## Executive Summary

- **Model**: Cursor Composer 2 (`cursor/composer-2`)
- **Dataset**: OpenThoughts-TBLite (100 tasks)
- **Framework**: Harbor v0.1.45
- **Mean Reward**: 0.801
- **Pass Rate**: 77/95 (81.1%)
- **Perfect Scores**: 72/95
- **Errors**: 5 (AgentTimeoutError)

## Methodology

- **Evaluation harness**: Harbor, the official Terminal-Bench evaluation framework
- **Execution environment**: Local Docker containers on Linux (6.17.0-19-generic)
- **Concurrency**: 4 concurrent trials
- **Agent invocation**: `harbor run --dataset openthoughts-tblite --agent cursor-cli --model cursor/composer-2`
- **Agent implementation**: Harbor's built-in `CursorCli` installed agent, which runs `cursor-agent --yolo --print --model=composer-2`
- **Attempts**: 1 attempt per task (no retries)
- **Oracle baseline**: Separate run with `--agent oracle` for comparison

## Results

### Score Distribution

| Metric | Value |
|--------|-------|
| Total tasks | 100 |
| Scored trials | 95 |
| Errors (timeouts) | 5 |
| Mean reward | 0.8009 |
| Median reward | 1.0000 |
| Std deviation | 0.3915 |
| Perfect scores (1.0) | 72 |
| Partial credit (0 < r < 1) | 5 |
| Zero scores (0.0) | 18 |
| Pass rate (reward > 0) | 81.1% |

### Partial Credit Breakdown

| Task | Reward |
|------|--------|
| bash-log-processor-fix | 0.8270 |
| pgn-chess-repair-puzzles | 0.7600 |
| security-breach-incident-response | 0.7833 |
| security-incident-log-analysis | 0.8820 |
| tsl-test-case-generation | 0.8298 |

### Timing

| Metric | Agent Execution |
|--------|----------------|
| Min | 37.2s |
| P50 | 223.5s |
| P90 | 541.0s |
| P95 | 873.7s |
| Max | 2175.9s |
| Mean | 291.7s |

## Validation

### Completeness

All 100 of 100 tasks were executed. 95 produced scores, 5 timed out.

### Reward Consistency

All reward values in `result.json` match the corresponding `reward.txt` files.

### Oracle Comparison

- Oracle mean reward: 0.622 (many tasks have no oracle solution)
- Composer 2 mean reward: 0.801
- Tasks Composer 2 solved that oracle could not: **33**
- Tasks oracle solved but Composer 2 failed: **15** (regressions)

**Regressions** (Oracle=1.0, Composer 2=0.0):

- `application-debug`: 
- `bandit-delayed-feedback`: 
- `bloom-filter-cache-penetration-prevention`: 
- `breast-cancer-mlflow`: 
- `build-merkle-tree-cli-sha512`: 
- `build-system-task-ordering`: 
- `california-housing-api`: 
- `iot-device-registration-server`: FAIL: Expected 2 devices in the list (the two good ones), but found 0.
- `neural-architecture-search-final`: 
- `python-api-rate-limit`: 
- `rsa-jwt-token-api-redis-blacklist`: 
- `sales-data-csv-analysis`: ✓ `analysis_results.json` is valid JSON. | ✗ EDA: Region 'Region A' std_dev_sales mismatch (Expected
- `systemd-log-monitoring`: 
- `token-auth-websocket`: 
- `vimscript-vim-quine`: 

### Error Analysis

5 tasks failed with exceptions:

| Task | Exception | Message |
|------|-----------|---------|
| distributed-test-execution-scheduler | AgentTimeoutError | Agent execution timed out after 1200.0 seconds |
| neural-architecture-search-final | AgentTimeoutError | Agent execution timed out after 800.0 seconds |
| reverse-engineer-stack-vm | AgentTimeoutError | Agent execution timed out after 800.0 seconds |
| scan-linux-persistence-artifacts | AgentTimeoutError | Agent execution timed out after 900.0 seconds |
| todos-api | AgentTimeoutError | Agent execution timed out after 500.0 seconds |

### Failure Analysis (reward = 0.0)

18 tasks scored zero:

| Task | Feedback |
|------|----------|
| application-debug |  |
| bandit-delayed-feedback |  |
| bloom-filter-cache-penetration-prevention |  |
| breast-cancer-mlflow |  |
| build-merkle-tree-cli-sha512 |  |
| build-system-task-ordering |  |
| california-housing-api |  |
| etl_checkpoint_resume_bug |  |
| git-repo-forensics | Git internals knowledge needed | Wrong total commit count | Wrong branch commit count | Missed dangling commits | Wrong  |
| iot-device-registration-server | FAIL: Expected 2 devices in the list (the two good ones), but found 0. |
| protein-sequence |  |
| python-api-rate-limit |  |
| rsa-jwt-token-api-redis-blacklist |  |
| sales-data-csv-analysis | ✓ `analysis_results.json` is valid JSON. | ✗ EDA: Region 'Region A' std_dev_sales mismatch (Expected: 9.56, Got: 9.01).  |
| smiles-data-lab |  |
| systemd-log-monitoring |  |
| token-auth-websocket |  |
| vimscript-vim-quine |  |

## Comparison to Published Results

Cursor reported Composer 2 scores **61.7** on the full Terminal-Bench 2.0 benchmark (500+ tasks).
Our TBLite score of **80.1%** is higher in absolute terms, which is expected:

- TBLite is a curated 100-task subset with difficulty calibration biased toward tractable tasks
- The full TB2 includes harder, longer-horizon tasks that drag down scores
- TBLite correlates with full TB2 at r=0.911 (rank-order preservation, not absolute score equivalence)

The result is **plausible and consistent** with a model scoring 61.7 on full TB2.

## Limitations

1. **Single run**: Only 1 attempt per task — no averaging across multiple runs to reduce variance
2. **Local Docker execution**: Networking, resource constraints, and timeout behavior may differ from the Daytona cloud sandboxes used for official leaderboard scores
3. **Oracle baseline issues**: 26 tasks have no oracle solution, and some oracle solutions themselves are buggy (oracle mean = 0.622)
4. **5 timeout errors**: These tasks were not scored and are excluded from the mean, which slightly inflates the reported score
5. **No cost tracking**: The Cursor CLI agent does not report token usage or cost data

## Task-by-Task Results

| Task | Oracle | Composer 2 | Notes |
|------|--------|------------|-------|
| acl-permissions-inheritance | 1.00 | 1.00 |  |
| amuse-install | 0.00 | 1.00 | Agent solved (no oracle) |
| anomaly-detection-ranking | 1.00 | 1.00 |  |
| api-endpoint-permission-canonicalizer | 1.00 | 1.00 |  |
| application-debug | 1.00 | 0.00 | REGRESSION |
| auth_token_race_condition | 1.00 | 1.00 |  |
| bandit-delayed-feedback | 1.00 | 0.00 | REGRESSION |
| bash-log-processor-fix | 0.61 | 0.83 |  |
| basic-message-queue | 0.00 | 1.00 | Agent solved (no oracle) |
| battery-charging-optimization | 0.00 | 1.00 | Agent solved (no oracle) |
| bloom-filter-cache-penetration-prevention | 1.00 | 0.00 | REGRESSION |
| book-portfolio-analysis | 0.00 | 1.00 | Agent solved (no oracle) |
| bracket-sequence-restoration | 0.00 | 1.00 | Agent solved (no oracle) |
| breast-cancer-mlflow | 1.00 | 0.00 | REGRESSION |
| broken-python | 1.00 | 1.00 |  |
| build-merkle-tree-cli-sha512 | 1.00 | 0.00 | REGRESSION |
| build-system-task-ordering | 1.00 | 0.00 | REGRESSION |
| california-housing-api | 1.00 | 0.00 | REGRESSION |
| chained-forensic-extraction_20260101_011957 | 1.00 | 1.00 |  |
| competitive-programming-solver | 0.00 | 1.00 | Agent solved (no oracle) |
| container-registry-optimization | 1.00 | 1.00 |  |
| convolutional-layers | 1.00 | 1.00 |  |
| corrupted-filesystem-recovery | 0.00 | 1.00 | Agent solved (no oracle) |
| cosign-keyless-signing | 1.00 | 1.00 |  |
| cpp-daemon-sighup-segfault | 1.00 | 1.00 |  |
| cryptographic-protocol-verifier | 1.00 | 1.00 |  |
| csv-json-jsonl-merger | 1.00 | 1.00 |  |
| db-migration-local-storage | 1.00 | 1.00 |  |
| distributed-test-execution-scheduler | 1.00 | ERROR | AgentTimeoutError |
| ekf-localization | 1.00 | 1.00 |  |
| etl_checkpoint_resume_bug | 0.00 | 0.00 |  |
| fix-js-network-controller | 1.00 | 1.00 |  |
| fix_async_worker_queue | 1.00 | 1.00 |  |
| floor-plan-geometry | 0.00 | 1.00 | Agent solved (no oracle) |
| game-of-stones | 0.00 | 1.00 | Agent solved (no oracle) |
| git-repo-forensics | 0.00 | 0.00 |  |
| grid-pathfinding | 0.00 | 1.00 | Agent solved (no oracle) |
| grpc-plant-position-server | 0.00 | 1.00 | Agent solved (no oracle) |
| html-index-analysis | 0.00 | 1.00 | Agent solved (no oracle) |
| hydra-debug-slurm-mode | 1.00 | 1.00 |  |
| image-tile-identification | 0.00 | 1.00 | Agent solved (no oracle) |
| industrial-kiln-controller | 1.00 | 1.00 |  |
| iot-device-registration-server | 1.00 | 0.00 | REGRESSION |
| iris-dataset-classification | 0.00 | 1.00 | Agent solved (no oracle) |
| jq-data-processing | 1.00 | 1.00 |  |
| jsonl-aggregator | 1.00 | 1.00 |  |
| legal-summary-extraction | 0.00 | 1.00 | Agent solved (no oracle) |
| log-summary | 1.00 | 1.00 |  |
| malicious-package-forensics | 1.00 | 1.00 |  |
| maven-slf4j-conflict | 1.00 | 1.00 |  |
| mech-system | 1.00 | 1.00 |  |
| mlflow-register | 1.00 | 1.00 |  |
| monorepo-changelog-cli | 1.00 | 1.00 |  |
| mtls-cert-rotation | 1.00 | 1.00 |  |
| multi-labeller | 1.00 | 1.00 |  |
| multi-server-configuration | 0.00 | 1.00 | Agent solved (no oracle) |
| network-log-normalization | 0.00 | 1.00 | Agent solved (no oracle) |
| neural-architecture-search-final | 1.00 | ERROR | AgentTimeoutError |
| neutron-submission | 1.00 | 1.00 |  |
| okhttp-trailers-crash | 0.00 | 1.00 | Agent solved (no oracle) |
| pandas-etl | 1.00 | 1.00 |  |
| pandas-numpy-data-analysis | 0.00 | 1.00 | Agent solved (no oracle) |
| parking-lot-pathfinding | 0.00 | 1.00 | Agent solved (no oracle) |
| pdf-table-parsing | 0.00 | 1.00 | Agent solved (no oracle) |
| permutation-construction-100k | 0.00 | 1.00 | Agent solved (no oracle) |
| pgn-chess-repair-puzzles | 1.00 | 0.76 |  |
| playing-card-recognition | 0.00 | 1.00 | Agent solved (no oracle) |
| prediction-model-evaluation | 0.00 | 1.00 | Agent solved (no oracle) |
| protein-sequence | 0.00 | 0.00 |  |
| publisher-market-analysis | 0.00 | 1.00 | Agent solved (no oracle) |
| publisher-market-analysis-v2 | 0.00 | 1.00 | Agent solved (no oracle) |
| python-api-rate-limit | 1.00 | 0.00 | REGRESSION |
| raft-log-repair-concurrent-access | 1.00 | 1.00 |  |
| react-typescript-debugg | 1.00 | 1.00 |  |
| reproducibility-and-envsetup | 1.00 | 1.00 |  |
| reverse-engineer-stack-vm | 1.00 | ERROR | AgentTimeoutError |
| rsa-jwt-token-api-redis-blacklist | 1.00 | 0.00 | REGRESSION |
| sakila-sqlite-queries | 0.00 | 1.00 | Agent solved (no oracle) |
| sales-data-csv-analysis | 1.00 | 0.00 | REGRESSION |
| scan-linux-persistence-artifacts | 1.00 | ERROR | AgentTimeoutError |
| schedule-vacation | 1.00 | 1.00 |  |
| security-breach-incident-response | 0.75 | 0.78 |  |
| security-incident-log-analysis | 0.92 | 0.88 |  |
| server-log-analysis | 0.00 | 1.00 | Agent solved (no oracle) |
| service-deployment-wave-planner | 1.00 | 1.00 |  |
| sign-vector-game | 1.00 | 1.00 |  |
| simple-database-query-tool | 0.00 | 1.00 | Agent solved (no oracle) |
| smiles-data-lab | 0.00 | 0.00 |  |
| sql-injection-forensics | 0.00 | 1.00 | Agent solved (no oracle) |
| submission_a63937a5_20251224_152124 | 1.00 | 1.00 |  |
| supply-chain-fulfillment | 1.00 | 1.00 |  |
| symlink-chain-traversal | 0.00 | 1.00 | Agent solved (no oracle) |
| sympy-bug-fix | 0.00 | 1.00 | Agent solved (no oracle) |
| systemd-log-monitoring | 1.00 | 0.00 | REGRESSION |
| task-xxe-exploit | 1.00 | 1.00 |  |
| todos-api | 1.00 | ERROR | AgentTimeoutError |
| token-auth-websocket | 1.00 | 0.00 | REGRESSION |
| tsl-test-case-generation | 0.88 | 0.83 |  |
| vimscript-vim-quine | 1.00 | 0.00 | REGRESSION |
| word-derangement-mapping | 0.00 | 1.00 | Agent solved (no oracle) |
