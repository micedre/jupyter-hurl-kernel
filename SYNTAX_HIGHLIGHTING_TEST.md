# Syntax Highlighting Testing Guide

## Quick Verification Steps

Run these checks on your Jupyter server to diagnose syntax highlighting issues:

### 1. Run the Diagnostic Script

```bash
python verify_installation.py
```

This will check:
- Kernel installation
- CodeMirror mode file locations
- File permissions
- Configuration issues

### 2. Check Browser Developer Console

1. Open your Jupyter notebook
2. Press **F12** to open Developer Tools
3. Go to the **Console** tab
4. Look for errors containing:
   - `hurl.js`
   - `CodeMirror`
   - `mode`
   - `404` (file not found)

**Common errors:**
- `Failed to load resource: hurl.js` → CodeMirror mode not properly installed
- `CodeMirror.defineMode is not a function` → CodeMirror not loaded
- `Cannot read property 'hurl'` → Mode registration failed

### 3. Check Network Tab

1. In Developer Tools, go to **Network** tab
2. Reload the page (Ctrl+R)
3. Filter for "hurl"
4. Look for:
   - `hurl.js` loading successfully (Status 200)
   - If Status 404: File not in correct location
   - If no hurl.js request: Mode not being requested by Jupyter

### 4. Manual File Verification

On your server, check if these files exist:

```bash
# Find Jupyter data directory
jupyter --data-dir

# Check for Notebook mode file
ls -la $(jupyter --data-dir)/nbextensions/codemirror/mode/hurl/hurl.js

# Check for kernel spec
cat $(jupyter --data-dir)/kernels/hurl/kernel.json
```

### 5. Check JupyterLab vs Classic Notebook

**Important:** JupyterLab 4.x uses CodeMirror 6, which is incompatible with this mode (designed for CodeMirror 5).

Check your version:
```bash
jupyter lab --version
```

- **JupyterLab 3.x**: Should work ✓
- **JupyterLab 4.x**: Won't work ✗ (use classic Notebook instead)
- **Classic Jupyter Notebook**: Should work ✓

To use classic Notebook:
```bash
jupyter notebook
```

## Test Code for Syntax Highlighting

Create a new Hurl notebook and paste this code. Each element should be highlighted differently:

```hurl
# This is a comment - should be grey/green

%%verbose
# Magic line above should be highlighted

GET https://api.github.com/users/octocat
User-Agent: Mozilla/5.0
Accept: application/json
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "key": "value",
  "number": 123,
  "bool": true
}

HTTP 200
[Asserts]
status == 200
jsonpath "$.login" == "octocat"
header "Content-Type" contains "application/json"
duration < 1000

[Captures]
user_id: jsonpath "$.id"

POST https://httpbin.org/post
Content-Type: application/x-www-form-urlencoded

[FormParams]
username: john
password: secret123
```

## Expected Highlighting Colors

Based on the token types returned by the CodeMirror mode:

| Element | Token Type | Typical Color |
|---------|-----------|---------------|
| `GET`, `POST`, `HTTP` | `keyword` | Blue/Purple |
| URLs | `string-2` | Green/Teal |
| `[Asserts]`, `[Captures]` | `header` | Bold/Orange |
| Headers (`Content-Type:`) | `attribute` | Brown/Orange |
| `status`, `jsonpath`, `header` | `builtin` | Cyan/Teal |
| `==`, `!=`, `<` | `operator` | Red/Orange |
| `200`, `123`, `1000` | `number` | Green |
| `"value"`, `"text"` | `string` | Green/Red |
| `true`, `false`, `null` | `atom` | Blue |
| `$.login`, `$.id` | `variable-2` | Purple |
| `# comments` | `comment` | Grey/Green |
| `%%verbose` | `meta` | Purple/Magenta |
| `{{token}}` | `variable` | Orange |

**Note:** Exact colors depend on your Jupyter theme.

## What "Working" Looks Like

If syntax highlighting is working correctly:

1. **HTTP methods** (`GET`, `POST`) should be **bold and colored** (not plain text)
2. **URLs** should be a **different color** from regular text
3. **Section headers** `[Asserts]` should be **bold/distinct**
4. **Comments** (`#`) should be **greyed out or green**
5. **Strings in quotes** should be colored differently
6. **Numbers** should have their own color
7. All elements should NOT be the same color

If everything appears in **the same color** (all black or all white), syntax highlighting is **not working**.

## Common Issues and Solutions

### Issue 1: All text is the same color

**Cause:** CodeMirror mode not loaded

**Solutions:**
1. Check browser console for errors
2. Verify hurl.js exists in the right location
3. Clear browser cache (Ctrl+Shift+R)
4. Reinstall: `install-hurl-kernel --sys-prefix`
5. Restart Jupyter server

### Issue 2: Some highlighting works, some doesn't

**Cause:** Pattern matching issues in CodeMirror mode

**Solutions:**
1. Ensure you have the latest version of hurl.js
2. Check for JavaScript errors in browser console
3. Report specific patterns that don't highlight

### Issue 3: Highlighting works in new cells but not existing ones

**Cause:** Cell type not properly set

**Solutions:**
1. Create a new cell and test there
2. Restart kernel
3. Clear cell output and re-run

### Issue 4: Works locally but not on server

**Causes:**
- Different Jupyter version
- File permissions
- Different installation method
- Browser cache

**Solutions:**
1. Check Jupyter versions match: `jupyter --version`
2. Verify file permissions: `chmod 644 $(jupyter --data-dir)/nbextensions/codemirror/mode/hurl/hurl.js`
3. Use `--sys-prefix` when installing on servers
4. Clear browser cache on the client machine

### Issue 5: Works in Classic Notebook but not JupyterLab

**Cause:** JupyterLab 4 uses CodeMirror 6 (incompatible)

**Solution:**
- Use Classic Jupyter Notebook: `jupyter notebook`
- Or downgrade to JupyterLab 3.x (not recommended)

## Debugging Steps

### Step 1: Verify Mode Registration

Open browser console and run:
```javascript
// Check if CodeMirror is loaded
console.log(typeof CodeMirror);  // Should be "object" or "function"

// Check if hurl mode is registered
console.log(CodeMirror.modes);  // Should include "hurl"

// Try to get the mode
console.log(CodeMirror.getMode({}, "hurl"));
```

### Step 2: Check MIME Type

In browser console:
```javascript
// Check MIME type registration
console.log(CodeMirror.mimeModes["text/x-hurl"]);  // Should be "hurl"
```

### Step 3: Force Mode Reload

In a notebook cell, try setting the mode manually:
```python
from IPython.display import Javascript
Javascript("""
require(['codemirror/lib/codemirror'], function(CodeMirror) {
    console.log('CodeMirror modes:', Object.keys(CodeMirror.modes));
    console.log('Hurl mode:', CodeMirror.modes.hurl);
});
""")
```

## Reinstallation from Scratch

If nothing works, try complete reinstallation:

```bash
# 1. Uninstall everything
jupyter kernelspec uninstall hurl
pip uninstall jupyter-hurl-kernel

# 2. Clean cache
rm -rf ~/.cache/jupyter
rm -rf $(jupyter --data-dir)/nbextensions/codemirror/mode/hurl
rm -rf $(jupyter --data-dir)/kernels/hurl

# 3. Reinstall
pip install jupyter-hurl-kernel
install-hurl-kernel --sys-prefix

# 4. Verify
jupyter kernelspec list
python verify_installation.py

# 5. Restart Jupyter
# Stop current server (Ctrl+C)
jupyter notebook  # or jupyter lab

# 6. Clear browser cache (Ctrl+Shift+R in the browser)
```

## Getting Help

If syntax highlighting still doesn't work after trying all these steps, collect this information:

1. Output of `python verify_installation.py`
2. Jupyter version: `jupyter --version`
3. JupyterLab version (if applicable): `jupyter lab --version`
4. Browser and version
5. Screenshot showing the issue
6. Browser console errors (F12 → Console tab)
7. Network requests for hurl.js (F12 → Network tab)

Report the issue with this information to:
https://github.com/micedre/jupyter-hurl-kernel/issues
