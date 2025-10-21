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

        # Build the TypeScript library
        print("\n🔨 Building TypeScript library...")
        result = subprocess.run(
            ["npm", "run", "build:lib:prod"],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode != 0:
            print("Error building TypeScript:")
            print(result.stderr)
            print("⚠️  Extension build failed, but continuing package build...")
            return

        print("✓ TypeScript compiled successfully")

        # Manually create the labextension structure
        print("\n📦 Creating labextension package...")
        import shutil
        import json

        # Create labextension directory
        labext_dest.mkdir(parents=True, exist_ok=True)

        # Copy compiled lib directory
        lib_src = labext_src / "lib"
        lib_dest = labext_dest / "lib"
        if lib_src.exists():
            if lib_dest.exists():
                shutil.rmtree(lib_dest)
            shutil.copytree(lib_src, lib_dest)
            print(f"  ✓ Copied lib/ to {lib_dest}")

        # Copy style directory if exists
        style_src = labext_src / "style"
        style_dest = labext_dest / "style"
        if style_src.exists():
            if style_dest.exists():
                shutil.rmtree(style_dest)
            shutil.copytree(style_src, style_dest)
            print(f"  ✓ Copied style/ to {style_dest}")

        # Copy schema directory if exists
        schema_src = labext_src / "schema"
        schema_dest = labext_dest / "schema"
        if schema_src.exists():
            if schema_dest.exists():
                shutil.rmtree(schema_dest)
            shutil.copytree(schema_src, schema_dest)
            print(f"  ✓ Copied schema/ to {schema_dest}")

        # Copy package.json
        pkg_json_src = labext_src / "package.json"
        pkg_json_dest = labext_dest / "package.json"
        if pkg_json_src.exists():
            shutil.copy2(pkg_json_src, pkg_json_dest)
            print(f"  ✓ Copied package.json")

        # Create install.json if it doesn't exist
        install_json_src = labext_src / "install.json"
        if install_json_src.exists():
            install_json_dest = labext_dest / "install.json"
            shutil.copy2(install_json_src, install_json_dest)
            print(f"  ✓ Copied install.json")

        print("✓ Extension packaged successfully")

        # Clean up node_modules to avoid including in package
        print("\n🧹 Cleaning up build artifacts...")
        node_modules = labext_src / "node_modules"
        if node_modules.exists():
            shutil.rmtree(node_modules)
            print("  ✓ Removed node_modules")

        lib_dir = labext_src / "lib"
        if lib_dir.exists():
            shutil.rmtree(lib_dir)
            print("  ✓ Removed lib/")

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
