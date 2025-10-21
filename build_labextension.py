#!/usr/bin/env python
"""Build script for JupyterLab extension.

This script is run automatically by uv during package build.
It compiles the TypeScript extension and prepares it for bundling.
"""

import subprocess
import sys
from pathlib import Path


def build_extension():
    """Build the JupyterLab extension."""
    print("=" * 70)
    print("Building JupyterLab extension...")
    print("=" * 70)

    # Get the labextension source directory
    labext_src = Path(__file__).parent / "src" / "jupyter_hurl_kernel" / "labextension_src"
    labext_dest = Path(__file__).parent / "src" / "jupyter_hurl_kernel" / "labextension"

    # Check if source exists
    if not labext_src.exists():
        print(f"Warning: Extension source not found at {labext_src}")
        print("Skipping extension build.")
        return

    # Check if already built
    package_json = labext_dest / "package.json"
    if package_json.exists():
        print(f"Extension already built at {labext_dest}")
        print("Skipping build.")
        return

    print(f"Source: {labext_src}")
    print(f"Destination: {labext_dest}")

    # Change to extension source directory
    original_dir = Path.cwd()

    try:
        import os
        os.chdir(labext_src)

        # Install npm dependencies
        print("\n📦 Installing npm dependencies...")
        result = subprocess.run(
            ["npm", "install"],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode != 0:
            print("Error installing npm dependencies:")
            print(result.stderr)
            # Don't fail the build, just warn
            print("⚠️  Extension build failed, but continuing package build...")
            return

        print("✓ Dependencies installed")

        # Build the extension
        print("\n🔨 Building extension...")
        result = subprocess.run(
            ["npm", "run", "build:prod"],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode != 0:
            print("Error building extension:")
            print(result.stderr)
            print("⚠️  Extension build failed, but continuing package build...")
            return

        print("✓ Extension built successfully")

        # Verify output
        if labext_dest.exists():
            files = list(labext_dest.glob("**/*"))
            print(f"\n✓ Built extension contains {len(files)} files")
        else:
            print(f"\n⚠️  Warning: Expected output directory not found: {labext_dest}")

    except FileNotFoundError as e:
        print(f"⚠️  npm not found: {e}")
        print("⚠️  Skipping extension build. Install Node.js to build the extension.")
    except Exception as e:
        print(f"⚠️  Error during extension build: {e}")
        print("⚠️  Continuing package build without extension...")
    finally:
        os.chdir(original_dir)

    print("=" * 70)
    print("Extension build complete")
    print("=" * 70)


if __name__ == "__main__":
    build_extension()
