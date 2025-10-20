#!/bin/bash
# Debug script for syntax highlighting issues

echo "=========================================="
echo "Syntax Highlighting Debug Information"
echo "=========================================="
echo ""

echo "1. Jupyter Version:"
echo "-------------------"
jupyter --version
echo ""

echo "2. Kernel Specification:"
echo "------------------------"
jupyter kernelspec list | grep hurl
KERNEL_DIR=$(jupyter --data-dir)/kernels/hurl
echo "Kernel directory: $KERNEL_DIR"
echo ""

echo "3. kernel.json contents:"
echo "------------------------"
if [ -f "$KERNEL_DIR/kernel.json" ]; then
    cat "$KERNEL_DIR/kernel.json"
else
    echo "ERROR: kernel.json not found at $KERNEL_DIR/kernel.json"
fi
echo ""

echo "4. CodeMirror mode file locations:"
echo "-----------------------------------"
DATA_DIR=$(jupyter --data-dir)
echo "Jupyter data dir: $DATA_DIR"
echo ""

echo "Checking Notebook location:"
NB_MODE="$DATA_DIR/nbextensions/codemirror/mode/hurl/hurl.js"
if [ -f "$NB_MODE" ]; then
    echo "✓ Found: $NB_MODE"
    echo "  Size: $(wc -c < "$NB_MODE") bytes"
else
    echo "✗ NOT FOUND: $NB_MODE"
fi
echo ""

echo "Checking Lab location:"
LAB_MODE="$DATA_DIR/lab/static/codemirror/mode/hurl/hurl.js"
if [ -f "$LAB_MODE" ]; then
    echo "✓ Found: $LAB_MODE"
    echo "  Size: $(wc -c < "$LAB_MODE") bytes"
else
    echo "✗ NOT FOUND: $LAB_MODE"
fi
echo ""

echo "Checking kernel directory:"
KERNEL_MODE="$KERNEL_DIR/codemirror/hurl.js"
if [ -f "$KERNEL_MODE" ]; then
    echo "✓ Found: $KERNEL_MODE"
    echo "  Size: $(wc -c < "$KERNEL_MODE") bytes"
else
    echo "✗ NOT FOUND: $KERNEL_MODE"
fi
echo ""

echo "5. Are you using JupyterLab or Notebook?"
echo "-----------------------------------------"
if command -v jupyter-lab &> /dev/null; then
    echo "JupyterLab version: $(jupyter-lab --version)"
fi
if command -v jupyter-notebook &> /dev/null; then
    echo "Jupyter Notebook version: $(jupyter-notebook --version)"
fi
echo ""

echo "6. CodeMirror mode content check:"
echo "----------------------------------"
if [ -f "$NB_MODE" ]; then
    echo "First few lines of hurl.js:"
    head -20 "$NB_MODE"
    echo ""
    echo "Checking for 'defineMode':"
    if grep -q "defineMode" "$NB_MODE"; then
        echo "✓ defineMode found in hurl.js"
    else
        echo "✗ defineMode NOT found - file may be corrupted"
    fi
fi
echo ""

echo "=========================================="
echo "Please share this output for diagnosis"
echo "=========================================="
