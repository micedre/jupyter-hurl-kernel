#!/bin/bash
# Installation script for JupyterLab 4 Hurl extension

set -e

echo "=========================================="
echo "JupyterLab 4 Hurl Extension Installer"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "Error: Please run this script from the jupyter-hurl-kernel root directory"
    exit 1
fi

# Check Node.js version
echo "1. Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed"
    echo "Please install Node.js >= 18:"
    echo "  conda install -c conda-forge 'nodejs>=18'"
    echo "  or visit: https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "Error: Node.js version is too old ($NODE_VERSION)"
    echo "Please upgrade to Node.js >= 18:"
    echo "  conda install -c conda-forge 'nodejs>=18'"
    exit 1
fi

echo "✓ Node.js version: $(node --version)"
echo ""

# Check JupyterLab
echo "2. Checking JupyterLab..."
if ! command -v jupyter &> /dev/null; then
    echo "Error: JupyterLab is not installed"
    echo "Please install JupyterLab:"
    echo "  pip install jupyterlab"
    exit 1
fi

LAB_VERSION=$(jupyter lab --version 2>/dev/null || echo "not installed")
echo "✓ JupyterLab version: $LAB_VERSION"
echo ""

# Install Python package
echo "3. Installing Hurl kernel..."
pip install -e .
install-hurl-kernel --sys-prefix
echo "✓ Hurl kernel installed"
echo ""

# Install JupyterLab extension
echo "4. Installing JupyterLab extension..."

# Check if we should install from npm or local source
if [ -d "jupyterlab-hurl-extension" ]; then
    echo "  Installing from local source (development mode)..."
    cd jupyterlab-hurl-extension

    echo "  Installing Node.js dependencies..."
    npm install

    echo "  Building extension..."
    npm run build

    echo "  Installing extension to JupyterLab..."
    jupyter labextension develop . --overwrite

    cd ..
else
    echo "  Installing from npm..."
    jupyter labextension install jupyterlab-hurl-extension
fi

echo "✓ JupyterLab extension installed"
echo ""

# Verify installation
echo "5. Verifying installation..."
echo ""
echo "Installed JupyterLab extensions:"
jupyter labextension list | grep -A5 "jupyterlab-hurl-extension" || echo "Warning: Extension not found in list"
echo ""

echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Restart your JupyterLab server if it's running"
echo "2. Clear your browser cache (Ctrl+Shift+R)"
echo "3. Create a new notebook and select 'Hurl' as the kernel"
echo "4. Test syntax highlighting with Hurl code"
echo ""
echo "Troubleshooting:"
echo "- See JUPYTERLAB4_INSTALLATION.md for detailed instructions"
echo "- Run: bash debug_syntax_highlighting.sh"
echo ""
