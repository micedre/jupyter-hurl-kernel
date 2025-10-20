# JupyterLab 4 Installation Guide

This guide explains how to install syntax highlighting support for Hurl in JupyterLab 4.x.

## Why a Separate Extension?

JupyterLab 4 uses **CodeMirror 6**, which is completely different from CodeMirror 5 used in JupyterLab 3 and classic Jupyter Notebook. The extensions are incompatible, so we need to install a separate JupyterLab extension.

## Prerequisites

1. **Python** >= 3.8
2. **JupyterLab** >= 4.0.0
3. **Hurl kernel** (will be installed in Step 1)

**Note**: Node.js is **NOT required** if you install from npm (recommended method). It's only needed if you're building from source for development.

## Installation Steps

### Step 1: Install the Hurl Kernel

If you haven't already:

```bash
pip install jupyter-hurl-kernel
install-hurl-kernel --sys-prefix
```

### Step 2: Install the JupyterLab Extension

#### Option A: Install from npm (Recommended)

```bash
# Install the extension from npm
jupyter labextension install jupyterlab-hurl-extension
```

This is the simplest method and doesn't require Node.js or building from source.

#### Option B: Install from Source (For Development)

If you want to modify the extension or are developing it:

```bash
cd /path/to/jupyter-hurl-kernel/jupyterlab-hurl-extension

# Install Node.js dependencies
npm install

# Build the extension
npm run build

# Install the extension to JupyterLab
jupyter labextension develop . --overwrite
```

### Step 3: Verify Installation

```bash
jupyter labextension list
```

You should see:
```
jupyterlab-hurl-extension v0.1.0 enabled OK (python, jupyterlab-hurl-extension)
```

### Step 4: Restart JupyterLab

Completely stop and restart your JupyterLab server:

```bash
# Stop the server (Ctrl+C)
# Then start it again
jupyter lab
```

### Step 5: Test Syntax Highlighting

1. Create a new notebook
2. Select **Hurl** as the kernel
3. Type some Hurl code:

```hurl
GET https://api.github.com/users/octocat
Accept: application/json

HTTP 200
[Asserts]
status == 200
jsonpath "$.login" == "octocat"
```

4. You should see syntax highlighting!

## Troubleshooting

### "npm: command not found"

Install Node.js if not already installed:
```bash
conda install -c conda-forge 'nodejs>=18'
```

### "Node.js version too old"

Check your Node.js version:
```bash
node --version
```

If it's less than 18, upgrade:
```bash
conda install -c conda-forge 'nodejs>=18'
```

### Extension not appearing in list

Try rebuilding JupyterLab:
```bash
jupyter lab build
jupyter labextension list
```

### Syntax highlighting not working

1. **Check the browser console** (F12) for errors

2. **Verify the extension is loaded:**
   Open browser console and run:
   ```javascript
   console.log(window.jupyterapp.serviceManager.terminals);
   ```

3. **Clear JupyterLab cache:**
   ```bash
   jupyter lab clean
   jupyter lab build
   ```

4. **Verify kernel.json:**
   ```bash
   cat $(jupyter --data-dir)/kernels/hurl/kernel.json
   ```

   Make sure it contains:
   ```json
   "language_info": {
     "name": "hurl",
     "mimetype": "text/x-hurl",
     "codemirror_mode": "hurl"
   }
   ```

5. **Reinstall everything:**
   ```bash
   # Uninstall
   jupyter labextension uninstall jupyterlab-hurl-extension

   # Rebuild extension
   cd jupyterlab-hurl-extension
   npm run clean:all
   npm install
   npm run build

   # Reinstall
   jupyter labextension develop . --overwrite

   # Restart JupyterLab
   ```

### Build errors

If you get TypeScript or build errors:

```bash
# Clean everything
cd jupyterlab-hurl-extension
rm -rf node_modules lib
npm install
npm run build
```

### Permission errors

If you get permission errors during installation, you might need to:

1. Use a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install jupyterlab jupyter-hurl-kernel
   ```

2. Or install with `--sys-prefix`:
   ```bash
   install-hurl-kernel --sys-prefix
   ```

## Development Mode

If you want to modify the extension:

```bash
cd jupyterlab-hurl-extension

# Watch for changes
npm run watch
```

In another terminal:
```bash
jupyter lab --watch
```

Now changes to the TypeScript source will automatically rebuild, and you just need to refresh your browser.

## Uninstallation

```bash
# Uninstall the JupyterLab extension
jupyter labextension uninstall jupyterlab-hurl-extension

# Uninstall the kernel
jupyter kernelspec uninstall hurl

# Uninstall the Python package
pip uninstall jupyter-hurl-kernel
```

## Alternative: Use Classic Jupyter Notebook

If you encounter issues with JupyterLab 4, you can use classic Jupyter Notebook which uses CodeMirror 5 and works with the built-in syntax highlighting:

```bash
pip install notebook
jupyter notebook
```

The built-in CodeMirror 5 mode will work automatically without needing the JupyterLab extension.

## Getting Help

If you're still having issues:

1. Run the debug script:
   ```bash
   bash debug_syntax_highlighting.sh
   ```

2. Check for errors in:
   - Browser console (F12)
   - JupyterLab build output
   - Terminal running JupyterLab

3. Report issues at: https://github.com/micedre/jupyter-hurl-kernel/issues

Include:
- Output of `jupyter --version`
- Output of `jupyter labextension list`
- Output of `node --version`
- Browser console errors
- JupyterLab terminal output
