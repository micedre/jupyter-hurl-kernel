#!/usr/bin/env python3
"""Diagnostic script to verify Hurl kernel installation for syntax highlighting."""

import json
import sys
from pathlib import Path

from jupyter_core.paths import jupyter_data_dir


def check_file(path, description):
    """Check if a file exists and is readable."""
    if path.exists():
        print(f"✓ {description}: {path}")
        return True
    else:
        print(f"✗ {description}: NOT FOUND at {path}")
        return False


def main():
    """Run installation verification checks."""
    print("=" * 70)
    print("Jupyter Hurl Kernel - Installation Verification")
    print("=" * 70)
    print()

    # Get Jupyter data directory
    data_dir = Path(jupyter_data_dir())
    print(f"Jupyter data directory: {data_dir}")
    print()

    issues = []

    # Check kernel spec
    print("1. Checking Kernel Specification...")
    print("-" * 70)
    kernel_dir = data_dir / "kernels" / "hurl"
    kernel_json = kernel_dir / "kernel.json"

    if check_file(kernel_json, "kernel.json"):
        try:
            with open(kernel_json) as f:
                spec = json.load(f)
                print(f"   Display name: {spec.get('display_name')}")
                print(f"   Language: {spec.get('language')}")
                print(f"   CodeMirror mode: {spec.get('language_info', {}).get('codemirror_mode', 'NOT SET')}")

                # This is the critical part for syntax highlighting
                if spec.get('language_info', {}).get('codemirror_mode') != 'hurl':
                    issues.append("kernel.json doesn't specify 'codemirror_mode': 'hurl'")
        except Exception as e:
            issues.append(f"Error reading kernel.json: {e}")
    else:
        issues.append("kernel.json not found - kernel not installed")
    print()

    # Check CodeMirror mode in kernel directory
    print("2. Checking CodeMirror Mode in Kernel Directory...")
    print("-" * 70)
    kernel_cm_dir = kernel_dir / "codemirror"
    kernel_cm_file = kernel_cm_dir / "hurl.js"
    check_file(kernel_cm_file, "CodeMirror mode in kernel dir")
    print()

    # Check CodeMirror mode for Notebook
    print("3. Checking CodeMirror Mode for Jupyter Notebook...")
    print("-" * 70)
    nb_cm_dir = data_dir / "nbextensions" / "codemirror" / "mode" / "hurl"
    nb_cm_file = nb_cm_dir / "hurl.js"
    if check_file(nb_cm_file, "CodeMirror mode for Notebook"):
        # Check file size
        size = nb_cm_file.stat().st_size
        print(f"   File size: {size} bytes")
        if size < 100:
            issues.append("CodeMirror mode file seems too small")
    else:
        issues.append("CodeMirror mode not installed for Jupyter Notebook")
    print()

    # Check CodeMirror mode for JupyterLab
    print("4. Checking CodeMirror Mode for JupyterLab...")
    print("-" * 70)
    lab_cm_dir = data_dir / "lab" / "static" / "codemirror" / "mode" / "hurl"
    lab_cm_file = lab_cm_dir / "hurl.js"
    if check_file(lab_cm_file, "CodeMirror mode for JupyterLab"):
        size = lab_cm_file.stat().st_size
        print(f"   File size: {size} bytes")
    else:
        print("   Note: This is optional, mainly for older JupyterLab versions")
    print()

    # Check Python package
    print("5. Checking Python Package...")
    print("-" * 70)
    try:
        import jupyter_hurl_kernel
        print(f"✓ jupyter_hurl_kernel module found")
        print(f"   Location: {jupyter_hurl_kernel.__file__}")

        # Check if kernel class exists
        from jupyter_hurl_kernel.kernel import HurlKernel
        print(f"✓ HurlKernel class found")
        print(f"   Language info: {HurlKernel.language_info}")

    except ImportError as e:
        issues.append(f"Python package not properly installed: {e}")
        print(f"✗ Error importing: {e}")
    print()

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    if issues:
        print("\n⚠️  ISSUES FOUND:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        print("\nRecommended actions:")
        print("  1. Run: install-hurl-kernel --sys-prefix")
        print("  2. Restart Jupyter server")
        print("  3. Clear browser cache (Ctrl+Shift+R)")
        print("  4. Check browser console for JavaScript errors")
        return 1
    else:
        print("\n✓ All checks passed!")
        print("\nIf syntax highlighting still doesn't work:")
        print("  1. Clear browser cache (Ctrl+Shift+R)")
        print("  2. Restart Jupyter server")
        print("  3. Try classic Jupyter Notebook if using JupyterLab 4+")
        print("  4. Check browser developer console (F12) for errors")
        return 0


if __name__ == "__main__":
    sys.exit(main())
