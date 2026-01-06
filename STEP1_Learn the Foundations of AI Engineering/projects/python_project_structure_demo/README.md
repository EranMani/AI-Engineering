# Python Project Structure Demo

A simple demonstration of proper Python project structure covering modules, packages, and imports.

## 📁 Project Structure

```
python_project_structure_demo/
│
├── src/                          # Main source code package
│   ├── __init__.py              # Makes 'src' a package + exposes imports
│   ├── data_loader.py           # Example module
│   └── model_trainer.py         # Example module
│
├── tests/                       # Test package
│   ├── __init__.py
│   └── test_data_loader.py      # Example test
│
├── examples/                    # Example scripts
│   ├── example_absolute_imports.py
│   ├── example_relative_imports.py
│   └── example_using_package.py
│
└── README.md
```

## 🎯 Key Concepts

### 1. Modules
Any `.py` file is a module. Modules break down code into logical chunks.

**Example:**
- `data_loader.py` - handles data operations
- `model_trainer.py` - handles model training

### 2. Packages
A directory with modules and `__init__.py` becomes a package.

**Key Points:**
- `__init__.py` makes a folder a package
- `__init__.py` can expose common imports
- Packages can contain subpackages

### 3. The Role of `__init__.py`

The `__init__.py` file:
1. Makes a directory a package
2. Controls what gets imported
3. Runs initialization code when package is imported

**Example from `src/__init__.py`:**
```python
from .data_loader import DataLoader
from .model_trainer import ModelTrainer

# Now users can do:
# from src import DataLoader
# Instead of:
# from src.data_loader import DataLoader
```

### 4. Imports: Absolute vs Relative

#### Absolute Imports
Start from the package name. Explicit and clear.

```python
from src.data_loader import DataLoader
from src.model_trainer import ModelTrainer
from src import DataLoader  # Using __init__.py exports
```

**When to use:**
- ✅ Production code
- ✅ Scripts outside the package
- ✅ When you want explicit imports

#### Relative Imports
Use dots (`.`) to indicate position within a package.

```python
# Inside src/data_loader.py, importing from sibling:
from .model_trainer import ModelTrainer

# Inside a subpackage, importing from parent:
from ..data_loader import DataLoader
```

**When to use:**
- ✅ Inside a package, importing from the same package
- ❌ NOT for scripts run directly (as `__main__`)

**Syntax:**
- `.module_name` = current package
- `..module_name` = parent package
- `.subpackage.module` = subpackage in current package

## 🚀 How to Use

### Run the Examples

```bash
cd python_project_structure_demo
python examples/example_absolute_imports.py
python examples/example_using_package.py
```

### Key Files to Examine

1. **`src/__init__.py`**: Package-level exports
2. **`src/data_loader.py`**: Example module
3. **`src/model_trainer.py`**: Module with imports
4. **`examples/example_absolute_imports.py`**: Absolute imports demo

## ⚠️ Common Pitfalls

### `ModuleNotFoundError`
**Solution:**
1. Ensure package is in Python path
2. `__init__.py` files exist in all package directories
3. Use correct import paths

### Relative imports don't work
**Solution:**
- Relative imports only work inside packages
- Use absolute imports for scripts outside packages

## 📝 Best Practices

1. ✅ Always include `__init__.py` in package directories
2. ✅ Use absolute imports for production code
3. ✅ Keep `__init__.py` files clean
4. ✅ Separate tests into their own package
5. ✅ Use descriptive module names
6. ✅ Keep modules focused on single responsibility

---

**Remember**: Good structure makes your code modular and easy to deploy! 🚀
