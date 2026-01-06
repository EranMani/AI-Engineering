"""
Example: Relative Imports

Relative imports use dots (.) to indicate position within a package.
They work when the file is INSIDE the package.

Syntax:
  .module_name     = current package
  ..module_name    = parent package
  .subpackage.module = subpackage in current package

Example (if this file were inside src/):
  from .data_loader import DataLoader
  from .model_trainer import ModelTrainer
"""

print("Relative imports use dots (.) to reference modules within a package.")
print("\nExample syntax:")
print("  from .data_loader import DataLoader  # sibling module")
print("  from .. import DataLoader            # parent package")
print("\nNote: Relative imports only work inside packages, not in scripts.")

