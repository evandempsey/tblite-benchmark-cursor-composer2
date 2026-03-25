# Cursor Composer 2 on OpenThoughts-TBLite

Benchmark results for Cursor's Composer 2 model on the [OpenThoughts-TBLite](https://github.com/open-thoughts/OpenThoughts-TBLite) dataset (100 tasks), evaluated using the [Harbor](https://harborframework.com) framework.

## Results

| Metric | Value |
|--------|-------|
| Mean Reward | **0.801 (80.1%)** |
| Pass Rate | 77/95 (81.1%) |
| Perfect Scores | 72/95 |
| Errors (timeouts) | 5 |

[View the interactive results page](https://evandempsey.github.io/tblite-benchmark-cursor-composer2/) | [Detailed report](report.md)

## Reproduce

```bash
# Install dependencies
uv init && uv add harbor

# Set your Cursor API key
export CURSOR_API_KEY="<your-key>"

# Run the benchmark
uv run harbor run \
  --dataset openthoughts-tblite \
  --agent cursor-cli \
  --model cursor/composer-2 \
  --n-concurrent 4

# Generate analysis
uv run python analyze.py
```

## Caveats

- **Agent harness**: Uses `cursor-cli` agent, not the `terminus-2` agent used for published leaderboard scores. Cross-agent comparison should be interpreted with caution.
- **Single run**: 1 attempt per task with no retries or averaging.
- **Local Docker**: Run on local Docker containers, not Daytona cloud sandboxes used for official leaderboard.
- **5 timeouts**: Excluded from the mean score, which may slightly inflate the result.

## Browse Results with Harbor Viewer

The repo includes per-trial `result.json` files from both runs. To browse the full trajectories and detailed results interactively:

```bash
# Clone and install
git clone git@github.com:evandempsey/tblite-benchmark-cursor-composer2.git
cd tblite-benchmark-cursor-composer2
uv sync

# Download full job output (trajectories, verifier output, logs)
# from the GitHub release and unzip into the jobs/ directory
curl -L https://github.com/evandempsey/tblite-benchmark-cursor-composer2/releases/download/v1.0.0/jobs-full.zip -o jobs-full.zip
unzip -o jobs-full.zip

# Launch the Harbor viewer
uv run harbor view jobs
```

Then open `http://localhost:8080` in your browser.

## Project Structure

- `docs/index.html` - Interactive results website (served via GitHub Pages)
- `report.md` - Detailed markdown report with validation
- `analyze.py` - Analysis and validation script
- `generate_site_data.py` - Generates data for the results website
- `jobs/` - Per-trial result.json files from oracle and Composer 2 runs
