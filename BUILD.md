# Build System Documentation

## Overview

The `jupyter-hurl-kernel` package uses `uv` as the build backend with a custom build script to compile the JupyterLab extension before packaging.

## Build Process

### What Happens During Build

1. **Pre-build Hook**: `build_labextension.py` is executed
   - Compiles TypeScript extension from `src/jupyter_hurl_kernel/labextension_src/`
   - Outputs to `src/jupyter_hurl_kernel/labextension/`
   - Uses npm to install dependencies and build

2. **Package Build**: `uv` builds the Python package
   - Includes compiled extension in package data
   - Installs extension to `share/jupyter/labextensions/`
   - Installs kernel spec to `share/jupyter/kernels/`
   - Installs CodeMirror 5 mode for classic Notebook

### Requirements

**For Users (pip install)**:
- Python >= 3.13
- No Node.js required (extension is pre-built)

**For Developers (building from source)**:
- Python >= 3.13
- Node.js >= 18
- npm (comes with Node.js)
- uv

## Building from Source

### Quick Start

```bash
# Clone repository
git clone https://github.com/micedre/jupyter-hurl-kernel.git
cd jupyter-hurl-kernel

# Build with uv
uv build

# Result: dist/jupyter_hurl_kernel-X.Y.Z.tar.gz and .whl
```

### Development Installation

```bash
# Install in editable mode
pip install -e .

# Install kernel
install-hurl-kernel --sys-prefix
```

**Note**: Editable installs require manually building the extension first:

```bash
cd src/jupyter_hurl_kernel/labextension_src
npm install
npm run build
```

### Extension Development

For active extension development with auto-rebuild:

```bash
# Terminal 1: Watch TypeScript changes
cd src/jupyter_hurl_kernel/labextension_src
npm install
npm run watch

# Terminal 2: Run JupyterLab with auto-reload
jupyter lab --watch
```

## Build Configuration

### pyproject.toml

```toml
[build-system]
requires = ["uv_build>=0.9.4,<0.10.0"]
build-backend = "uv_build"

[tool.uv.build-backend]
before-build = ["python build_labextension.py"]
```

### build_labextension.py

Custom build script that:
- Checks if extension is already built
- Runs `npm install` to get dependencies
- Runs `npm run build:prod` to compile TypeScript
- Handles errors gracefully (won't fail package build if npm is missing)

### Package Data

The following files are included in the distribution:

```python
[tool.setuptools.package-data]
jupyter_hurl_kernel = [
    "labextension/**/*",           # Compiled extension
    "labextension_src/install.json", # Extension metadata
    "resources/**/*",              # Kernel spec and CM5 mode
]
```

### Installation Paths

Files are installed to:
- `site-packages/jupyter_hurl_kernel/` - Python package
- `share/jupyter/labextensions/jupyterlab-hurl-extension/` - JupyterLab extension
- `share/jupyter/kernels/hurl/` - Kernel specification (via install-hurl-kernel)
- `share/jupyter/nbextensions/codemirror/mode/hurl/` - Classic Notebook mode (via install-hurl-kernel)

## Troubleshooting

### Extension not building

**Symptom**: Build succeeds but extension isn't included

**Solution**:
```bash
# Manually build extension first
cd src/jupyter_hurl_kernel/labextension_src
npm install
npm run build

# Then build package
uv build
```

### npm not found

**Symptom**: Warning during build about npm not found

**Effect**: Package builds successfully but without JupyterLab 4 extension
- Classic Notebook and JupyterLab 3 still work (CodeMirror 5 mode)
- JupyterLab 4 syntax highlighting won't work

**Solution**: Install Node.js and rebuild:
```bash
# Install Node.js (version 18+)
# Then rebuild
uv build
```

### Build fails completely

**Check**:
1. Is uv installed? `uv --version`
2. Is Python 3.13+? `python --version`
3. Are dependencies available? `uv sync`

### Extension changes not reflected

**For development**:
```bash
# Rebuild extension
cd src/jupyter_hurl_kernel/labextension_src
npm run build

# Restart JupyterLab
# Clear browser cache (Ctrl+Shift+R)
```

## CI/CD

### GitHub Actions

The publish workflow:

```yaml
- name: Set up Node.js  # Required for extension build
  uses: actions/setup-node@v4
  with:
    node-version: '20'

- name: Install uv
  uses: astral-sh/setup-uv@v4

- name: Build package
  run: uv build  # Automatically runs build_labextension.py
```

### Version Management

Version is managed in:
- `pyproject.toml` - Package version
- `src/jupyter_hurl_kernel/__init__.py` - `__version__` variable

Both are updated automatically by GitHub Actions on release.

## Testing Build

```bash
# Build
uv build

# Install locally
pip install dist/jupyter_hurl_kernel-*.whl

# Test
install-hurl-kernel --sys-prefix
jupyter lab

# Verify extension is loaded
jupyter labextension list
# Should show: jupyterlab-hurl-extension
```

## Clean Build

```bash
# Remove build artifacts
rm -rf dist/ build/ *.egg-info
rm -rf src/jupyter_hurl_kernel/labextension/

# Clean extension
cd src/jupyter_hurl_kernel/labextension_src
npm run clean:all
rm -rf node_modules

# Fresh build
cd ../../..
uv build
```

## References

- [uv Documentation](https://github.com/astral-sh/uv)
- [JupyterLab Extension Guide](https://jupyterlab.readthedocs.io/en/stable/extension/extension_dev.html)
- [Python Packaging](https://packaging.python.org/)
