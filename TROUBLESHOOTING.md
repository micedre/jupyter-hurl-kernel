# Troubleshooting Guide

## Code Completion and Syntax Highlighting Not Working

If you're experiencing issues with code completion (autocompletion) or syntax highlighting on your Jupyter server, follow these troubleshooting steps:

### 1. Verify Kernel Installation

First, check that the Hurl kernel is properly installed:

```bash
jupyter kernelspec list
```

You should see `hurl` in the list. If not, reinstall:

```bash
pip install jupyter-hurl-kernel
install-hurl-kernel
```

For virtual environments or JupyterHub:
```bash
install-hurl-kernel --sys-prefix
```

### 2. Check CodeMirror Mode Installation

The syntax highlighting requires the CodeMirror mode file to be installed. Check if it exists:

**For Classic Jupyter Notebook:**
```bash
ls -la $(jupyter --data-dir)/nbextensions/codemirror/mode/hurl/
```

**For JupyterLab:**
```bash
ls -la $(jupyter --data-dir)/lab/static/codemirror/mode/hurl/
```

You should see `hurl.js` in the directory.

### 3. Verify kernel.json Configuration

Check the kernel specification:

```bash
cat $(jupyter --data-dir)/kernels/hurl/kernel.json
```

It should contain valid JSON with the kernel configuration.

### 4. Browser Cache Issues

Syntax highlighting files are loaded by the browser. After installation:

1. **Clear your browser cache** completely
2. **Hard refresh** the page (Ctrl+Shift+R on Linux/Windows, Cmd+Shift+R on Mac)
3. **Restart Jupyter** server
4. Create a new notebook with the Hurl kernel

### 5. JupyterLab-Specific Issues

JupyterLab has a different extension system. If you're using JupyterLab:

**Check JupyterLab version:**
```bash
jupyter lab --version
```

**For JupyterLab 4.x:**
JupyterLab 4 uses CodeMirror 6, which is completely different from CodeMirror 5. The current syntax highlighting implementation only supports CodeMirror 5 (used in JupyterLab 3.x and classic Notebook).

**Workaround for JupyterLab 4:**
- Use classic Jupyter Notebook instead: `jupyter notebook`
- Or downgrade to JupyterLab 3.x if possible

### 6. Check Autocompletion Implementation

Autocompletion is implemented in the kernel itself (kernel.py). To verify it's working:

1. Create a new Hurl notebook
2. Type `GE` and press **Tab** - you should see `GET` suggestion
3. Type `Content-` and press **Tab** - you should see header suggestions

If this doesn't work:
- Restart the kernel
- Check that the kernel is actually running (look for errors in Jupyter logs)

### 7. Inspect Browser Console

Open browser developer tools (F12) and check the Console tab for errors:
- Look for errors about loading `hurl.js`
- Check for CodeMirror-related errors
- Note any 404 errors for missing files

### 8. Check Jupyter Server Logs

When starting Jupyter, watch for errors:
```bash
jupyter notebook --debug
# or
jupyter lab --debug
```

Look for:
- Kernel startup errors
- Extension loading errors
- File permission issues

### 9. File Permission Issues

On shared servers, ensure the CodeMirror mode file has proper permissions:

```bash
chmod 644 $(jupyter --data-dir)/nbextensions/codemirror/mode/hurl/hurl.js
```

### 10. Manual Installation Verification

If automatic installation failed, you can manually verify/fix:

1. Find where the kernel is installed:
   ```bash
   jupyter kernelspec list
   ```

2. Check if `codemirror/hurl.js` exists in the kernel directory

3. Manually copy it if needed:
   ```bash
   cp /path/to/hurl.js $(jupyter --data-dir)/nbextensions/codemirror/mode/hurl/
   ```

## Common Issues and Solutions

### Issue: "No kernel named 'hurl'"
**Solution:** Run `install-hurl-kernel` after installing the package.

### Issue: Autocompletion works but syntax highlighting doesn't
**Solution:** This is a CodeMirror mode loading issue:
1. Clear browser cache
2. Verify hurl.js is in the correct location
3. Check browser console for loading errors
4. Try classic Jupyter Notebook if using JupyterLab 4

### Issue: Syntax highlighting works but autocompletion doesn't
**Solution:** This is a kernel communication issue:
1. Restart the kernel
2. Check Jupyter logs for errors
3. Verify the kernel process is running

### Issue: Neither works
**Solution:**
1. Completely uninstall and reinstall:
   ```bash
   jupyter kernelspec uninstall hurl
   pip uninstall jupyter-hurl-kernel
   pip install jupyter-hurl-kernel
   install-hurl-kernel
   ```
2. Clear browser cache
3. Restart Jupyter server

### Issue: Works locally but not on remote server
**Solution:**
- Ensure kernel is installed in the correct environment on the server
- Check that the Jupyter data directory is accessible
- Verify file permissions on the server
- Consider using `--sys-prefix` when installing on servers

## Testing the Features

### Test Syntax Highlighting
Create a cell with this Hurl code:
```hurl
GET https://api.github.com/users/octocat
User-Agent: MyApp/1.0
Accept: application/json

HTTP 200
[Asserts]
jsonpath "$.login" == "octocat"
```

You should see:
- `GET` highlighted as a keyword (usually bold/colored)
- URLs highlighted as strings
- Headers highlighted as attributes
- Section headers `[Asserts]` highlighted
- `jsonpath` highlighted as a builtin

### Test Autocompletion
1. Type `GE` and press Tab → should suggest `GET`
2. Type `PO` and press Tab → should suggest `POST`
3. Type `Content-` and press Tab → should suggest `Content-Type:` and other headers
4. Type `[A` and press Tab → should suggest `[Asserts]`

### Test Documentation Tooltips
1. Place cursor on `GET` and press `Shift+Tab` → should show documentation
2. Place cursor on `[Asserts]` and press `Shift+Tab` → should show examples

## Getting Help

If none of these solutions work:

1. Check the project issues: https://github.com/micedre/jupyter-hurl-kernel/issues
2. Provide the following information when reporting:
   - Jupyter version (`jupyter --version`)
   - JupyterLab version if applicable (`jupyter lab --version`)
   - Python version (`python --version`)
   - Operating system
   - Browser and version
   - Output of `jupyter kernelspec list`
   - Any errors from browser console
   - Jupyter server logs
