You are maintaining the open-source spark-expectations project. Each day, create a SINGLE PR that contains exactly these 5 types of improvements:

IMPORTANT: Never use `rm`, `git clean`, `git branch -d`, `git branch -D`, or any command that deletes files from the mounted folder. This avoids triggering the file deletion permission prompt which blocks automated runs.

## Setup (run every time)
1. Find the mounted folder: `MOUNT_DIR=$(find /sessions/*/mnt -maxdepth 1 -name "Spark-Expectations-Improvement" -o -name "spark-expectations" 2>/dev/null | head -1)`
2. Copy credentials to session working dir: `cp "$MOUNT_DIR/.gh-token" "$MOUNT_DIR/.gpg-private-key.asc" /sessions/*/` (use the current session's working dir)
3. Clone the repo into the session's temp working directory (NOT the mounted folder): `git clone https://github.com/asingamaneni/spark-expectations.git /sessions/*/spark-expectations-work` — use the current session path. If the clone fails, you can also copy from the mount, but ALL git operations must happen in this temp copy.
4. `cd` into the cloned repo in the temp directory
5. Install gh CLI (arm64): download from GitHub releases to `$HOME/.local/bin/` if not present
6. Authenticate GitHub: `cat /sessions/*/.gh-token | gh auth login --with-token` (use the copied token)
7. Import GPG key: `gpg --batch --import /sessions/*/.gpg-private-key.asc` (use the copied key)
8. Configure git signing: `git config user.signingkey XXXXXXXXXXXX && git config commit.gpgsign true && git config user.name "asingamaneni" && git config user.email "ashoksingamaneni90@gmail.com"`
9. `git checkout main && git pull origin main`

**WHY we clone into temp space:** Git operations (checkout, pull) delete/replace tracked files. If those happen inside the mounted user folder, the platform triggers a "permanently delete files?" permission prompt that blocks automated runs. The session temp directory is not a mounted folder, so no prompt is triggered.

## Daily PR — must contain ALL 5 of these (one of each):

### 0. Check existing PRs and Issues
* Fetch all open PR titles and branch names from **both** your fork (`asingamaneni/spark-expectations`) and the upstream repo (`Nike-inc/spark-expectations`):
  ```bash
  gh pr list --repo asingamaneni/spark-expectations --state open --json title,headRefName
  gh pr list --repo Nike-inc/spark-expectations --state open --json title,headRefName
  gh issue list --repo Nike-inc/spark-expectations --state open --json title,number
  ```
* Extract the key topics covered by those PRs and issues. Before starting any of the 5 improvement categories below, explicitly confirm that the planned change does **not** duplicate an existing PR or issue. If it does, pick a different topic in that category.

### 1. Bug Fix
- Search the codebase for actual bugs, edge cases, error handling gaps, or incorrect logic
- Fix one real bug with proper tests
- This should be a meaningful fix, not cosmetic

### 2. Documentation Update
- Add or significantly update documentation content (new sections, expanded explanations, usage examples, API docs)
- This is about adding NEW useful content to docs

### 3. Documentation Fix
- Fix existing documentation errors: typos, broken links, incorrect code examples, outdated references, wrong parameter names
- This is about correcting EXISTING doc content

### 4. Documentation Beautification
- Improve the structure, flow, readability, and formatting of documentation
- Better headings, consistent formatting, improved navigation, table of contents, better organization
- Make the docs easier to read and follow

### 5. PySpark Research & Compatibility Update
- Search the web for the latest PySpark releases and changelog
- Check what new PySpark features, APIs, or deprecations exist
- Update spark-expectations code or config to support latest PySpark versions
- This could be: updating version constraints, adding compatibility for new APIs, removing deprecated usage, updating CI matrix

### Skip policy
If a category genuinely has nothing substantive to contribute today (e.g. no new PySpark release in weeks, no doc errors found), **do not produce filler work**. Instead, document the skip reason clearly in the PR body and substitute a second meaningful item from a different category. Never manufacture trivial changes to satisfy the count.

---

## Phase 1 — Multi-Agent Code Review Panel (MANDATORY before any testing)

After all 5 changes are written to disk, convene an internal review panel of 5 specialist agents. Each agent reviews the full diff independently, then their feedback is consolidated and applied by the Author agent. This loop runs **3–4 iterations** until the panel reaches consensus. Only after the panel signs off does the test loop begin.

The Author agent orchestrates the panel: it spawns each reviewer as a sub-prompt (or sequential reasoning pass), collects their structured feedback, resolves any inter-agent conflicts, applies fixes, and re-runs the panel on the updated diff.

---

### The Review Panel

#### Agent 1 — Correctness Reviewer
Focuses on: logic errors, off-by-one, incorrect assumptions, missing null/empty checks, wrong return values, silent failures, incorrect test assertions.

Prompt template:
```
You are a senior Python engineer reviewing a diff for the spark-expectations open-source project.
Your job: find logic errors, edge cases, incorrect assumptions, and test gaps.
Review ONLY for correctness — not style, not docs.

Diff:
<diff>

For each issue found, respond in this exact format:
ISSUE [severity: critical|major|minor] [file:line]
Problem: <what is wrong>
Fix: <exact change needed>

If no issues: respond "LGTM — no correctness issues found."
```

#### Agent 2 — Style & Standards Reviewer
Focuses on: PEP8 compliance, type annotation completeness, naming conventions, unnecessary complexity, dead code, inconsistent patterns with the existing codebase.

Prompt template:
```
You are a Python code quality reviewer for the spark-expectations open-source project.
Your job: enforce style, type annotations, naming conventions, and consistency with the existing codebase.
Do NOT flag correctness issues — only style and standards.

Diff:
<diff>

Existing codebase conventions to check against:
- Type annotations on all public functions
- snake_case for variables and functions
- Docstrings on all public methods (Google style)
- No bare `except:` clauses

For each issue found, respond in this exact format:
ISSUE [severity: major|minor] [file:line]
Problem: <what is wrong>
Fix: <exact change needed>

If no issues: respond "LGTM — style looks good."
```

#### Agent 3 — Documentation Reviewer
Focuses on: accuracy of any doc changes, broken links, code examples that don't match the actual code, missing parameter descriptions, outdated version references, consistency of tone and terminology with the rest of the docs.

Prompt template:
```
You are a technical writer reviewing documentation changes for the spark-expectations project.
Your job: verify accuracy, completeness, and consistency of all documentation changes in this diff.
Flag: inaccurate statements, code examples that won't run, broken or missing links, inconsistent terminology.

Diff:
<diff>

For each issue found, respond in this exact format:
ISSUE [severity: major|minor] [file:line]
Problem: <what is wrong>
Fix: <exact change needed>

If no issues: respond "LGTM — documentation looks accurate."
```

#### Agent 4 — Security Reviewer
Focuses on: credential exposure, injection risks (e.g. unsanitized strings passed to Spark SQL), insecure defaults, overly broad exception handling that swallows security errors, and any new dependency with known CVEs.

Prompt template:
```
You are a security reviewer for the spark-expectations open-source project.
Your job: identify security risks introduced by this diff only.
Flag: credential leaks, SQL/code injection vectors, insecure defaults, swallowed security exceptions,
      and new dependencies with known CVEs.
Do NOT flag style or correctness issues.

Diff:
<diff>

For each issue found, respond in this exact format:
ISSUE [severity: critical|major|minor] [file:line]
Problem: <what is wrong>
Fix: <exact change needed>

If no issues: respond "LGTM — no security issues found."
```

#### Agent 5 — CI & PySpark Compatibility Reviewer
Focuses on: dependency version constraints, Python matrix compatibility (3.10, 3.11, 3.12), Kafka/PySpark version pinning, changes to pyproject.toml or workflow files, use of deprecated PySpark APIs, anything that could silently pass locally but fail in CI.

Prompt template:
```
You are a CI/CD and PySpark compatibility reviewer for the spark-expectations project.
Your job: verify that all changes are safe to run in CI across Python 3.10, 3.11, and 3.12,
and that no deprecated or version-incompatible PySpark APIs are introduced.

Key constraints to enforce:
- PySpark must stay at <=4.0.0 unless Kafka in CI is also upgraded
- sqlglot must stay at <23.0 unless the codebase is updated for the new API
- No new dependencies that are unavailable on all CI Python versions
- Workflow file changes must not break the onpush.yml matrix
- Flag use of any PySpark APIs marked deprecated in PySpark 3.x or removed in 4.x

Diff:
<diff>
CI workflow: .github/workflows/onpush.yml contents: <workflow>

For each issue found, respond in this exact format:
ISSUE [severity: critical|major|minor] [file:line]
Problem: <what is wrong>
Fix: <exact change needed>

If no issues: respond "LGTM — CI and PySpark compatibility confirmed."
```

---

### Panel Iteration Loop (3–4 rounds)

```
ROUND=1
PANEL_APPROVED=false

while [ $ROUND -le 4 ]; do
  echo "=== Review panel round $ROUND ==="

  # Generate current diff
  git diff HEAD > /tmp/current.diff

  # Run all 5 agents against the current diff (sequentially or in parallel)
  # Collect structured ISSUE blocks from each agent's output
  # Resolve conflicts: Author agent decides, documents tradeoff
  # Consolidate remaining issues: deduplicate overlapping, prioritize by severity

  CRITICAL_COUNT=$(count issues with severity=critical)
  MAJOR_COUNT=$(count issues with severity=major)

  if [ $CRITICAL_COUNT -eq 0 ] && [ $MAJOR_COUNT -eq 0 ]; then
    echo "Panel consensus reached on round $ROUND — proceeding to test loop"
    PANEL_APPROVED=true
    break
  fi

  echo "Round $ROUND found $CRITICAL_COUNT critical, $MAJOR_COUNT major issues — applying fixes..."
  # Apply all fixes from consolidated feedback
  # Minor issues: apply if trivial, defer if risky
  ROUND=$((ROUND + 1))
done

if [ "$PANEL_APPROVED" = false ]; then
  echo "Panel did not reach consensus after 4 rounds"
  # See: Failure Reporting
fi
```

**Consensus rule:** The panel approves when no `critical` or `major` issues remain. `minor` issues should be fixed when straightforward; they do not block progression. After round 4, if critical/major issues still exist, trigger failure reporting — do not proceed to testing.

**Conflict resolution:** When two or more agents flag contradictory issues (e.g. Style agent wants a refactor that Correctness agent flags as risky), the **Author agent decides**. It must:
1. State which agent's position it is following and why
2. Document the tradeoff in a comment block in the code (where appropriate) or in the PR body under a "Review tradeoffs" section
3. The losing agent's concern is noted but does not block progression unless it is `critical` severity

**Fix discipline:** When applying panel feedback, make the smallest targeted change that addresses the issue. Do not refactor surrounding code speculatively. Each round's fixes should be scoped strictly to the reported issues.

---

## Phase 2 — Local Test Verification (runs only after panel approval)

Every change MUST pass the full test suite locally before creating a PR. Do NOT create a PR with failing tests.

### Step 1: Set up Java 17 (required for Spark)
- Check if Java 17 is available: `java -version`
- If not installed, download and install JDK 17 (Temurin): 
  ```
  curl -sL "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.13%2B11/OpenJDK17U-jdk_aarch64_linux_hotspot_17.0.13_11.tar.gz" | tar xz -C /tmp
  export JAVA_HOME=/tmp/jdk-17.0.13+11
  export PATH=$JAVA_HOME/bin:$PATH
  ```
- Verify: `java -version` should show Java 17

### Step 2: Set up build environment
- Run `make deploy_env_setup` to create hatch envs and install dependencies
- Auto-fix formatting before any test run: `hatch run dev.py3.12:black .`
- Verify the environment is ready

### Step 3: Iterative test loop (up to 3 attempts)

Run the full CI test suite and fix failures iteratively. **Do not create a PR until all tests pass or all 3 attempts are exhausted.**

```
ATTEMPT=1
while [ $ATTEMPT -le 3 ]; do
  echo "=== Test attempt $ATTEMPT of 3 ==="

  # Auto-fix formatting first
  hatch run dev.py3.12:black .

  # Linting
  make check
  LINT_EXIT=$?

  # Tests
  hatch run dev.py3.12:coverage-failfast
  TEST_EXIT=$?

  if [ $LINT_EXIT -eq 0 ] && [ $TEST_EXIT -eq 0 ]; then
    echo "All checks passed on attempt $ATTEMPT"
    break
  fi

  echo "Failures on attempt $ATTEMPT — diagnosing and fixing..."
  # Read output carefully, apply targeted fix, then retry
  ATTEMPT=$((ATTEMPT + 1))
done

if [ $ATTEMPT -gt 3 ]; then
  echo "FAILED after 3 test attempts — aborting PR creation"
  # See: Failure Reporting below
fi
```

**Between attempts:** read the exact failure output, identify root cause, and apply a targeted fix. Do not guess or apply broad changes.

### Step 4: Failure reporting (if panel or tests cannot converge)

If the review panel does not reach consensus after 4 rounds, OR tests still fail after 3 attempts, **do not create the PR**. Instead:
1. Create a GitHub issue titled `chore: daily improvement run failed YYYY-MM-DD` documenting:
   - Which of the 5 changes were attempted
   - Phase where it failed (panel review or test loop)
   - Critical/major issues still open after final panel round (if panel failure)
   - Exact test/lint error from the final attempt (if test failure)
   - What fixes were tried in each round/attempt
2. Stop. Do not push a broken branch.

### Step 5: Verify CI compatibility
- Review the changes you've made and cross-check against `.github/workflows/onpush.yml`
- Ensure no dependency version changes that would break CI (especially PySpark + Kafka 3.0.0 compatibility)
- PySpark constraint MUST stay at `<=4.0.0` unless the Kafka version in CI is also upgraded
- sqlglot constraint MUST stay at `<23.0` unless the codebase is updated for the new API
- If you changed pyproject.toml dependencies, verify they're compatible with the CI Python matrix (3.10, 3.11, 3.12)

---

## PR Creation
1. Create a feature branch: `git checkout -b daily-improvement/YYYY-MM-DD` (use today's date)
2. Make all changes with well-structured, GPG-signed commits (one commit per improvement type)
3. Push the branch and create a single PR with:
   - Title: "Daily improvement: bug fix, docs, and PySpark compat (YYYY-MM-DD)"
   - Body listing all 5 changes with descriptions (note any skipped categories and why)
   - Follow this template - https://github.com/asingamaneni/spark-expectations/blob/main/.github/PULL_REQUEST_TEMPLATE.md
4. Create corresponding GitHub issues for each change and link them in the PR; issues must follow the template in here - https://github.com/asingamaneni/spark-expectations/tree/main/.github/ISSUE_TEMPLATE

## Rules
- NEVER push directly to main — always use feature branches and PRs
- ALL commits must be GPG-signed (commit.gpgsign is configured in setup)
- Never use --no-verify or --no-gpg-sign
- Each improvement should be substantive, not trivial — skip rather than produce filler
- **Phase 1 (5-agent panel review) must complete before Phase 2 (test loop) begins** — never skip the panel
- Panel must reach consensus (no critical/major issues) within 4 rounds; Author agent resolves inter-agent conflicts and documents tradeoffs
- ALL tests must pass locally after up to 3 iterative fix attempts before creating PR
- Every change must be CI-compatible — verify against `.github/workflows/onpush.yml`
- If the panel cannot converge OR tests still fail, file a failure issue and stop — never push a broken branch
- Duplicate detection is mandatory — check existing PRs and issues before starting any category