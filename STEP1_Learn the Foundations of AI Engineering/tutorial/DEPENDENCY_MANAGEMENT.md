# Managing Dependencies and Virtual Environments

A comprehensive guide to dependency management and virtual environments using modern tools like `uv` and `pip`.

## Table of Contents

1. [Isolation: The "Why"](#isolation-the-why)
2. [The pyproject.toml Standard](#the-pyprojecttoml-standard)
3. [Dependency Resolution: The "How"](#dependency-resolution-the-how)
4. [Lock Files: Reproducibility](#lock-files-reproducibility)
5. [uv vs pip: Modern Tools](#uv-vs-pip-modern-tools)
6. [Best Practices](#best-practices)

---

## Isolation: The "Why"

### What is a Virtual Environment?

A **virtual environment** is an isolated Python environment that contains:
- Its own Python interpreter
- Its own set of installed packages
- Its own package installation directory

Think of it as a separate "workspace" for each project, completely isolated from your system Python and other projects.

### Why Do We Need Virtual Environments?

#### Problem 1: Version Conflicts

**Without virtual environments:**
```bash
# Project A needs pandas 1.5.0
pip install pandas==1.5.0

# Project B needs pandas 2.0.0
pip install pandas==2.0.0  # This overwrites 1.5.0!

# Now Project A breaks! 💥
```

**With virtual environments:**
```bash
# Project A has its own environment
project_a/.venv/bin/pip install pandas==1.5.0  # ✅ Works

# Project B has its own environment
project_b/.venv/bin/pip install pandas==2.0.0  # ✅ Also works

# No conflicts! 🎉
```

#### Problem 2: Dependency Hell

**The Scenario:**
- Your system Python has `numpy==1.20.0`
- Project A needs `pandas` (which requires `numpy>=1.21.0`)
- Project B needs `scipy` (which requires `numpy==1.20.0`)
- Installing both breaks one of them!

**The Solution:**
Each project gets its own virtual environment with compatible versions of all dependencies.

#### Problem 3: System Python Pollution

**Without isolation:**
- All packages install to system Python
- System Python becomes cluttered
- Hard to track what's needed for what
- Can break system tools that depend on specific versions

**With isolation:**
- Each project is self-contained
- Easy to delete and recreate
- No impact on system Python
- Clear separation of concerns

### What Happens Without Virtual Environments?

```python
# Your system Python might have:
# - pandas 2.0.0 (for a data science project)
# - Django 4.2 (for a web project)
# - tensorflow 2.15 (for an ML project)
# - numpy 1.24 (required by all of the above, but different versions!)

# When you run:
python my_script.py

# Python might:
# 1. Import the wrong version of a package
# 2. Fail to find a package (wrong environment)
# 3. Import a package with incompatible dependencies
# 4. Work on your machine but fail on others
```

**The Result:** "It works on my machine" syndrome, deployment failures, and debugging nightmares.

---

## The pyproject.toml Standard

### What is pyproject.toml?

`pyproject.toml` is the **modern standard** for Python project configuration. It's a single file that defines:
- Project metadata (name, version, description)
- Dependencies
- Build system requirements
- Tool configurations (linting, formatting, etc.)

### Why pyproject.toml?

**Old Way (requirements.txt):**
```txt
# requirements.txt
pandas>=2.3.3
numpy>=1.24.0
scikit-learn>=1.3.0
```

**Problems:**
- No project metadata
- No version constraints
- No build system info
- Separate files for dev dependencies
- Hard to manage

**New Way (pyproject.toml):**
```toml
[project]
name = "ai-engineering"
version = "0.1.0"
description = "Add your description here"
requires-python = ">=3.13"
dependencies = [
    "ipykernel>=7.1.0",
    "pandas>=2.3.3",
]
```

**Benefits:**
- ✅ All project info in one place
- ✅ Standardized format (PEP 621)
- ✅ Works with modern tools (uv, pip, poetry)
- ✅ Supports optional dependencies
- ✅ Better for packaging and distribution

### Understanding pyproject.toml Structure

#### Basic Project Definition

```toml
[project]
name = "my-ai-project"
version = "0.1.0"
description = "My awesome AI project"
readme = "README.md"
requires-python = ">=3.10"
```

#### Dependencies

```toml
[project]
dependencies = [
    "pandas>=2.3.3",           # Minimum version
    "numpy>=1.24.0,<2.0.0",    # Version range
    "requests==2.31.0",        # Exact version
    "scikit-learn",            # Latest version
]
```

#### Optional Dependencies

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "mypy>=1.0.0",
]
jupyter = [
    "ipykernel>=7.1.0",
    "jupyterlab>=4.0.0",
]
ml = [
    "tensorflow>=2.15.0",
    "torch>=2.0.0",
]
```

**Usage:**
```bash
# Install with optional dependencies
uv sync --extra dev
uv sync --extra jupyter
uv sync --extra ml
```

#### How uv Uses pyproject.toml

When you run `uv sync` or `uv pip install`:

1. **Reads pyproject.toml** to find dependencies
2. **Resolves dependencies** (finds compatible versions)
3. **Creates/updates uv.lock** (locks exact versions)
4. **Installs packages** into virtual environment
5. **Manages virtual environment** automatically

**Example workflow:**
```bash
# uv automatically:
# 1. Creates .venv if it doesn't exist
# 2. Reads pyproject.toml
# 3. Resolves all dependencies
# 4. Updates uv.lock
# 5. Installs everything

uv sync
```

---

## Dependency Resolution: The "How"

### What Happens When You Ask for "numpy"?

When you write `dependencies = ["numpy"]` in pyproject.toml, what actually happens?

#### Step 1: Dependency Declaration

```toml
[project]
dependencies = ["numpy"]
```

This says: "I need numpy, any version is fine."

#### Step 2: Dependency Resolution

The tool (uv or pip) must:

1. **Find numpy** on PyPI (Python Package Index)
2. **Check version constraints** from other packages
3. **Resolve conflicts** between requirements
4. **Find transitive dependencies** (dependencies of dependencies)

**Example Resolution Tree:**
```
Your Project
  └── numpy (you requested)
      └── No dependencies (numpy is standalone)
```

**More Complex Example:**
```
Your Project
  └── pandas (you requested)
      ├── numpy>=1.24.0 (pandas needs numpy)
      ├── python-dateutil>=2.8.2 (pandas needs this)
      │   └── six>=1.5 (python-dateutil needs this)
      └── pytz>=2020.1 (pandas needs this)
```

#### Step 3: Version Conflict Resolution

**The Challenge:**
```
Project needs:
  - pandas>=2.0.0 (requires numpy>=1.24.0)
  - scipy==1.10.0 (requires numpy==1.23.0)
  
Conflict! numpy 1.24.0 vs 1.23.0
```

**How uv Resolves This:**

1. **Satisfiability Solving**: Uses a SAT solver to find compatible versions
2. **Backtracking**: Tries different version combinations
3. **Error Reporting**: If impossible, shows why

**Resolution Strategies:**

```toml
# Strategy 1: Use version ranges (flexible)
dependencies = [
    "pandas>=2.0.0",
    "scipy>=1.10.0",  # More flexible
]

# Strategy 2: Pin compatible versions (exact)
dependencies = [
    "pandas==2.0.0",
    "numpy==1.24.0",  # Works with both
    "scipy==1.10.0",
]
```

#### Step 4: Installation

Once resolved, packages are:
1. Downloaded from PyPI
2. Verified (checksums, signatures)
3. Installed into virtual environment
4. Recorded in lock file

### Real-World Example: Installing pandas

```bash
$ uv add pandas
```

**What happens behind the scenes:**

```
1. uv reads pyproject.toml
   └── Finds: dependencies = ["pandas"]

2. uv queries PyPI
   └── Finds: pandas 2.2.0 (latest)

3. uv resolves dependencies
   └── pandas 2.2.0 requires:
       - numpy>=1.23.2,<2.0.0
       - python-dateutil>=2.8.2
       - pytz>=2020.1
       - tzdata>=2022.7

4. uv resolves transitive dependencies
   └── python-dateutil requires:
       - six>=1.5

5. uv creates dependency graph
   └── All compatible versions found

6. uv downloads packages
   └── Downloads wheels/sdists

7. uv installs packages
   └── Installs to .venv/

8. uv updates uv.lock
   └── Records exact versions
```

### Dependency Resolution Algorithms

#### pip's Approach (Older)
- **Algorithm**: Simple backtracking
- **Speed**: Slower for complex dependencies
- **Reliability**: Can fail on complex cases
- **Lock files**: Not built-in (needs pip-tools)

#### uv's Approach (Modern)
- **Algorithm**: Advanced SAT solver (similar to Poetry)
- **Speed**: 10-100x faster than pip
- **Reliability**: Better conflict resolution
- **Lock files**: Built-in (uv.lock)

---

## Lock Files: Reproducibility

### What is a Lock File?

A **lock file** (like `uv.lock`) records the **exact versions** of all packages and their dependencies that were installed.

### Why is uv.lock Critical?

#### The Reproducibility Problem

**Without lock files:**

```bash
# Developer A (January 2024)
pip install pandas  # Installs pandas 2.1.0

# Developer B (March 2024)
pip install pandas  # Installs pandas 2.2.0 (newer!)

# Different versions = Different behavior! 🐛
```

**With lock files:**

```bash
# Developer A
uv sync  # Installs exact versions from uv.lock

# Developer B
uv sync  # Installs SAME exact versions from uv.lock

# Identical environments = Reproducible results! ✅
```

### What's in uv.lock?

```toml
# uv.lock (simplified example)

[[package]]
name = "pandas"
version = "2.2.0"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "numpy", specifier = ">=1.23.2,<2.0.0" },
    { name = "python-dateutil", specifier = ">=2.8.2" },
]

[[package]]
name = "numpy"
version = "1.26.0"  # Exact version resolved
source = { registry = "https://pypi.org/simple" }
# ... hash, URL, etc. for reproducibility
```

**Key Information:**
- ✅ Exact package versions
- ✅ Dependency relationships
- ✅ Package hashes (security)
- ✅ Source URLs
- ✅ Platform-specific packages

### Lock File Workflow

#### Development Workflow

```bash
# 1. Add a new dependency
uv add numpy

# 2. uv automatically:
#    - Updates pyproject.toml
#    - Resolves dependencies
#    - Updates uv.lock
#    - Installs packages

# 3. Commit both files
git add pyproject.toml uv.lock
git commit -m "Add numpy dependency"
```

#### Production Deployment

```bash
# On production server:
# 1. Clone repository (includes uv.lock)
git clone <repo>

# 2. Install exact versions from lock file
uv sync

# 3. Guaranteed: Same versions as development! ✅
```

### Lock File Best Practices

#### ✅ DO:

1. **Commit uv.lock to version control**
   ```bash
   git add uv.lock
   git commit -m "Update dependencies"
   ```

2. **Regenerate lock file when updating dependencies**
   ```bash
   uv lock --upgrade
   ```

3. **Use lock file in CI/CD**
   ```yaml
   # .github/workflows/test.yml
   - run: uv sync  # Uses uv.lock
   ```

#### ❌ DON'T:

1. **Don't manually edit uv.lock**
   - It's auto-generated
   - Manual edits break reproducibility

2. **Don't ignore uv.lock in .gitignore**
   - Team needs it for reproducibility
   - Production needs it for deployments

3. **Don't commit lock files for libraries**
   - Only for applications
   - Libraries should be flexible

### Lock Files in Production AI Systems

**Why it matters for AI:**

```python
# Model trained with:
# - numpy 1.24.0
# - pandas 2.0.0
# - scikit-learn 1.3.0

# Production server with different versions:
# - numpy 1.26.0  # Different behavior!
# - pandas 2.2.0  # API changes!
# - scikit-learn 1.4.0  # Model might not load!

# Result: Model fails in production! 💥
```

**With lock files:**
```bash
# Training environment
uv sync  # Installs exact versions

# Production environment
uv sync  # Installs SAME exact versions

# Result: Model works identically! ✅
```

---

## uv vs pip: Modern Tools

### What is uv?

**uv** is a modern, fast Python package installer and resolver written in Rust. It's designed to be a drop-in replacement for pip, pip-tools, and virtualenv.

### uv vs pip Comparison

| Feature | pip | uv |
|---------|-----|-----|
| **Speed** | Baseline | 10-100x faster |
| **Lock files** | Requires pip-tools | Built-in (uv.lock) |
| **Virtual envs** | Requires venv/virtualenv | Built-in management |
| **Dependency resolution** | Basic | Advanced SAT solver |
| **Project management** | Manual | pyproject.toml support |
| **Written in** | Python | Rust |

### uv Commands

#### Basic Package Management

```bash
# Install packages (adds to pyproject.toml)
uv add pandas numpy

# Install with version constraints
uv add "pandas>=2.0.0"

# Install dev dependencies
uv add --dev pytest black

# Remove packages
uv remove pandas

# Sync environment (install from pyproject.toml + uv.lock)
uv sync

# Update all packages
uv sync --upgrade
```

#### Virtual Environment Management

```bash
# uv automatically manages .venv
# No need to create manually!

# Activate (if needed)
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Or use uv run (no activation needed!)
uv run python script.py
uv run pytest
```

#### Lock File Management

```bash
# Generate/update lock file
uv lock

# Update lock file with latest versions
uv lock --upgrade

# Check for outdated packages
uv lock --check
```

### pip Commands (For Comparison)

```bash
# Install packages
pip install pandas numpy

# Install from requirements.txt
pip install -r requirements.txt

# Create virtual environment (manual)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Freeze current environment
pip freeze > requirements.txt
```

### When to Use Which?

#### Use uv when:
- ✅ Starting a new project
- ✅ Want fast installation
- ✅ Need built-in lock files
- ✅ Working with pyproject.toml
- ✅ Want modern tooling

#### Use pip when:
- ✅ Working with legacy projects
- ✅ Team already uses pip
- ✅ Simple one-off installations
- ✅ System package management

### Migration from pip to uv

**Step 1: Install uv**
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Step 2: Convert requirements.txt to pyproject.toml**
```bash
# Create pyproject.toml
uv init

# Or manually create pyproject.toml from requirements.txt
```

**Step 3: Generate lock file**
```bash
uv lock
```

**Step 4: Install**
```bash
uv sync
```

---

## Best Practices

### 1. Always Use Virtual Environments

```bash
# ✅ Good: uv automatically creates .venv
uv sync

# ❌ Bad: Installing to system Python
pip install pandas  # Don't do this!
```

### 2. Commit Lock Files

```bash
# ✅ Good: Commit uv.lock
git add uv.lock
git commit -m "Update dependencies"

# ❌ Bad: Ignoring lock file
echo "uv.lock" >> .gitignore  # Don't do this!
```

### 3. Use Version Constraints

```toml
# ✅ Good: Flexible but safe
dependencies = [
    "pandas>=2.0.0,<3.0.0",  # Allows 2.x but not 3.x
    "numpy>=1.24.0",
]

# ⚠️ Acceptable: Exact version (for critical deps)
dependencies = [
    "tensorflow==2.15.0",  # Pin if needed
]

# ❌ Bad: No constraints (too flexible)
dependencies = [
    "pandas",  # Could break with major updates
]
```

### 4. Separate Dev Dependencies

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "mypy>=1.0.0",
]
```

```bash
# Install with dev dependencies
uv sync --extra dev

# Production (no dev deps)
uv sync
```

### 5. Regular Updates

```bash
# Check for updates
uv lock --check

# Update dependencies
uv sync --upgrade

# Test after updates
uv run pytest
```

### 6. Document Dependencies

```toml
[project]
name = "my-project"
description = "Clear description of what this project does"
dependencies = [
    "pandas>=2.0.0",  # For data processing
    "numpy>=1.24.0",  # Required by pandas
]
```

### 7. Use uv run for Scripts

```bash
# ✅ Good: No activation needed
uv run python train_model.py
uv run pytest

# ⚠️ Acceptable: Traditional activation
source .venv/bin/activate
python train_model.py
```

### 8. Keep pyproject.toml Clean

```toml
# ✅ Good: Organized
[project]
dependencies = [
    "pandas>=2.0.0",
    "numpy>=1.24.0",
]

[project.optional-dependencies]
dev = ["pytest"]
ml = ["tensorflow"]

# ❌ Bad: Everything mixed
[project]
dependencies = [
    "pandas", "numpy", "pytest", "tensorflow"  # Unclear!
]
```

---

## Summary

### Key Takeaways

1. **Virtual environments provide isolation** - Each project gets its own dependencies
2. **pyproject.toml is the modern standard** - Single file for project configuration
3. **Dependency resolution is complex** - Tools handle version conflicts automatically
4. **Lock files ensure reproducibility** - Critical for production AI systems
5. **uv is a modern, fast alternative** - Built-in lock files and virtual env management

### Quick Reference

```bash
# Initialize project
uv init

# Add dependency
uv add pandas

# Install all dependencies
uv sync

# Run script
uv run python script.py

# Update dependencies
uv sync --upgrade

# Generate lock file
uv lock
```

### Next Steps

1. **Practice**: Create a new project with `uv init`
2. **Experiment**: Add dependencies and watch `uv.lock` update
3. **Compare**: Try the same project with `pip` to see the difference
4. **Deploy**: Use lock files in a production environment

---

**Remember**: Good dependency management is the foundation of reproducible, maintainable AI systems! 🚀

