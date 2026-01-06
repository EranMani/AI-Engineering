# What Happens in This Demo Project

This document explains what each part of the Python project structure demo does and how it all works together.

## Overview

This demo project shows you how to structure a Python project properly using **modules**, **packages**, and **imports**. It demonstrates the fundamental concepts you need to move from experimental scripts to production-ready code.

## Project Structure

```
python_project_structure_demo/
├── src/                          # The main package
│   ├── __init__.py              # Makes src a package + simplifies imports
│   ├── data_loader.py           # Module 1: Data loading functionality
│   └── model_trainer.py         # Module 2: Model training functionality
│
├── tests/                       # Test package
│   ├── __init__.py              # Makes tests a package
│   └── test_data_loader.py      # Tests for DataLoader
│
├── examples/                    # Example scripts
│   ├── example_absolute_imports.py
│   ├── example_relative_imports.py
│   └── example_using_package.py
│
└── README.md                    # Quick reference guide
```

## What Each File Does

### 1. `src/__init__.py` - Package Initialization

**What it does:**
- Makes the `src` folder a Python **package** (not just a regular folder)
- Exposes commonly used classes at the package level for easier imports

**The code:**
```python
from .data_loader import DataLoader
from .model_trainer import ModelTrainer

__all__ = ["DataLoader", "ModelTrainer"]
```

**What this means:**
- Without `__init__.py`, Python wouldn't recognize `src` as a package
- The imports allow users to write: `from src import DataLoader` instead of `from src.data_loader import DataLoader`
- `__all__` defines what gets imported when someone does `from src import *`

**Key concept:** The `__init__.py` file is what turns a folder into a package. It can be empty, or it can contain code to simplify how others use your package.

---

### 2. `src/data_loader.py` - Module Example

**What it does:**
- Demonstrates a simple **module** (a `.py` file with related functionality)
- Contains a `DataLoader` class that handles data operations

**The code structure:**
```python
import pandas as pd
from pathlib import Path
from typing import Optional

class DataLoader:
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path("data")
    
    def load_csv(self, filename: str) -> pd.DataFrame:
        filepath = self.data_dir / filename
        return pd.read_csv(filepath)
    
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.dropna()
```

**What this demonstrates:**
- A module is just a `.py` file with code
- Modules can contain classes, functions, or variables
- This module is focused on one responsibility: data loading

**Key concept:** Modules break down large scripts into logical, reusable pieces.

---

### 3. `src/model_trainer.py` - Module with Imports

**What it does:**
- Shows how one module can **import from another module** in the same package
- Demonstrates **relative imports** (using `.` notation)

**The code:**
```python
from typing import Optional
import pandas as pd
from .data_loader import DataLoader  # ← Relative import!

class ModelTrainer:
    def __init__(self, data_loader: Optional[DataLoader] = None):
        self.data_loader = data_loader or DataLoader()
    
    def train(self, data: pd.DataFrame) -> dict:
        return {"accuracy": 0.95, "loss": 0.05, "epochs": 10}
```

**What this demonstrates:**
- **Relative import:** `from .data_loader import DataLoader`
  - The `.` means "from the current package"
  - This works because `model_trainer.py` is inside the `src` package
- One module can use classes/functions from another module
- This creates **modularity** - each module has a specific job

**Key concept:** Relative imports (`.module_name`) work when you're inside a package and importing from the same package.

---

### 4. `examples/example_absolute_imports.py` - Absolute Imports Demo

**What it does:**
- Shows how to use **absolute imports** from outside the package
- Demonstrates two ways to import: direct module import vs package-level import

**The code:**
```python
import sys
from pathlib import Path

# Add project root to Python path (so Python can find the src package)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Method 1: Direct module import
from src.data_loader import DataLoader
from src.model_trainer import ModelTrainer

# Method 2: Package-level import (uses __init__.py)
from src import DataLoader, ModelTrainer

# Use the imports
loader = DataLoader()
trainer = ModelTrainer(loader)
```

**What this demonstrates:**
- **Absolute imports:** Start from the package name (`src.data_loader`)
- **Python path setup:** Adding the project root to `sys.path` so Python can find the package
- **Two import styles:**
  - `from src.data_loader import DataLoader` - direct module import
  - `from src import DataLoader` - package-level import (simpler, uses `__init__.py`)

**Key concept:** Absolute imports are explicit and work from anywhere, as long as the package is in Python's path.

---

### 5. `examples/example_relative_imports.py` - Relative Imports Explanation

**What it does:**
- Explains **relative imports** conceptually (since this file is outside the package)
- Shows the syntax and when to use relative imports

**The code:**
```python
print("Relative imports use dots (.) to reference modules within a package.")
print("\nExample syntax:")
print("  from .data_loader import DataLoader  # sibling module")
print("  from .. import DataLoader            # parent package")
```

**What this demonstrates:**
- **Relative import syntax:**
  - `.module_name` = current package
  - `..module_name` = parent package
  - `.subpackage.module` = subpackage in current package
- **When to use:** Inside a package, importing from the same package
- **When NOT to use:** In scripts run directly (as `__main__`)

**Key concept:** Relative imports only work inside packages, not in standalone scripts.

---

### 6. `examples/example_using_package.py` - Real-World Usage

**What it does:**
- Shows the typical way you'd use this package in a real project
- Demonstrates clean, simple imports

**The code:**
```python
import sys
from pathlib import Path

# Setup Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import using package-level imports (cleanest)
from src import DataLoader, ModelTrainer

# Use the package
loader = DataLoader()
trainer = ModelTrainer(loader)
```

**What this demonstrates:**
- **Production pattern:** How you'd actually use the package
- **Clean imports:** Using `__init__.py` exports makes imports simpler
- **Path setup:** Always needed when running scripts outside the package

**Key concept:** This is the pattern you'd use in real applications.

---

### 7. `tests/test_data_loader.py` - Testing Structure

**What it does:**
- Shows how to structure **tests** in a separate package
- Demonstrates importing from the main package for testing

**The code:**
```python
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data_loader import DataLoader

def test_data_loader_initialization():
    loader = DataLoader()
    assert loader is not None
    assert loader.data_dir == Path("data")

def test_data_loader_custom_dir():
    custom_dir = Path("custom_data")
    loader = DataLoader(data_dir=custom_dir)
    assert loader.data_dir == custom_dir
```

**What this demonstrates:**
- **Test structure:** Tests live in a separate `tests/` package
- **Import pattern:** Same absolute import pattern as examples
- **Test organization:** Each test function tests one thing

**Key concept:** Tests are separate from source code but use the same import patterns.

---

## How It All Works Together

### The Import Flow

1. **Inside the package** (`src/model_trainer.py`):
   ```python
   from .data_loader import DataLoader  # Relative import
   ```
   - Uses relative import because it's inside the `src` package
   - The `.` means "current package"

2. **Outside the package** (`examples/example_absolute_imports.py`):
   ```python
   from src.data_loader import DataLoader  # Absolute import
   ```
   - Uses absolute import because it's outside the package
   - Must add project root to `sys.path` first

3. **Using package-level exports** (`examples/example_using_package.py`):
   ```python
   from src import DataLoader  # Uses __init__.py exports
   ```
   - Simplest import style
   - Works because `src/__init__.py` exports `DataLoader`

### The Package Structure Flow

```
User's Script
    ↓
Adds project root to sys.path
    ↓
Imports from src package
    ↓
Python finds src/__init__.py (makes it a package)
    ↓
__init__.py imports from .data_loader and .model_trainer
    ↓
Those modules can import from each other using relative imports
    ↓
Everything works! ✓
```

## Key Concepts Demonstrated

### 1. **Modules** (`.py` files)
- `data_loader.py` and `model_trainer.py` are modules
- Each module has a specific responsibility
- Modules can import from each other

### 2. **Packages** (folders with `__init__.py`)
- `src/` is a package because it has `__init__.py`
- `tests/` is also a package
- Packages organize related modules together

### 3. **Absolute Imports**
- Start from package name: `from src.data_loader import DataLoader`
- Work from anywhere (if package is in Python path)
- Preferred for production code

### 4. **Relative Imports**
- Use dots: `from .data_loader import DataLoader`
- Only work inside packages
- Useful for imports within the same package

### 5. **`__init__.py` Magic**
- Makes folders into packages
- Can simplify imports by exposing common items
- Runs when package is first imported

## Running the Examples

### Example 1: Absolute Imports
```bash
cd python_project_structure_demo
python examples/example_absolute_imports.py
```

**What happens:**
1. Script adds project root to Python path
2. Imports `DataLoader` and `ModelTrainer` using absolute imports
3. Creates instances and prints confirmation

### Example 2: Using the Package
```bash
python examples/example_using_package.py
```

**What happens:**
1. Script sets up Python path
2. Uses clean package-level imports (`from src import ...`)
3. Creates and uses the classes

### Running Tests
```bash
# If you have pytest installed
pytest tests/

# Or run directly
python -m pytest tests/test_data_loader.py
```

**What happens:**
1. Tests import from the `src` package
2. Test functions verify the `DataLoader` class works correctly
3. Assertions check expected behavior

## Common Questions

### Why do I need `__init__.py`?
Without it, Python treats `src` as a regular folder, not a package. You won't be able to import from it.

### Why add to `sys.path`?
Python needs to know where to find your package. Adding the project root to `sys.path` tells Python where to look.

### When should I use relative vs absolute imports?
- **Relative imports:** Inside a package, importing from the same package
- **Absolute imports:** Everywhere else (scripts, tests, production code)

### Can I skip `__init__.py`?
In Python 3.3+, you can sometimes skip it for "namespace packages", but it's still best practice to include it for clarity and to control exports.

## Summary

This demo project shows you:
- ✅ How to structure code into modules and packages
- ✅ How `__init__.py` makes packages work
- ✅ How to use absolute and relative imports
- ✅ How to organize tests separately
- ✅ How to use your package from outside scripts

The key takeaway: **Good structure makes your code modular, reusable, and easy to understand.** This is the foundation for building production-ready Python applications.

