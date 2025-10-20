# Jupyter Hurl Kernel

A Jupyter kernel for executing [Hurl](https://hurl.dev) commands directly in Jupyter notebooks.

## What is Hurl?

Hurl is a command line tool that runs HTTP requests defined in a simple plain text format. It's designed for testing HTTP endpoints, APIs, and web services. Learn more at [hurl.dev](https://hurl.dev).

## Features

- Execute Hurl commands directly in Jupyter notebook cells
- Get HTTP responses displayed in the notebook
- Supports all Hurl syntax and features
- Easy to install and use

## Prerequisites

1. **Python 3.13+** - This project requires Python 3.13 or higher
2. **Hurl** - Install Hurl from [hurl.dev/docs/installation.html](https://hurl.dev/docs/installation.html)

### Installing Hurl

**On macOS:**
```bash
brew install hurl
```

**On Linux:**
```bash
# Debian/Ubuntu
curl -LO https://github.com/Orange-OpenSource/hurl/releases/latest/download/hurl_amd64.deb
sudo dpkg -i hurl_amd64.deb

# Or build from source
cargo install hurl
```

**On Windows:**
```bash
# Using Scoop
scoop install hurl

# Or using Chocolatey
choco install hurl
```

Verify the installation:
```bash
hurl --version
```

## Installation

### From PyPI (Recommended)

```bash
pip install jupyter-hurl-kernel
install-hurl-kernel
```

For installation in a virtual environment:
```bash
pip install jupyter-hurl-kernel
install-hurl-kernel --sys-prefix
```

### From Source

1. Clone or download this repository:
```bash
git clone https://github.com/micedre/jupyter-hurl-kernel.git
cd jupyter-hurl-kernel
```

2. Install the package using uv:
```bash
uv pip install -e .
```

3. Install the Jupyter kernel:
```bash
install-hurl-kernel
```

For installation in a virtual environment:
```bash
install-hurl-kernel --sys-prefix
```

4. Verify the kernel is installed:
```bash
jupyter kernelspec list
```

You should see `hurl` in the list of available kernels.

## Usage

1. Start Jupyter Notebook or JupyterLab:
```bash
jupyter notebook
# or
jupyter lab
```

2. Create a new notebook and select "Hurl" as the kernel

3. Write Hurl commands in notebook cells:

**Example 1: Simple GET request**
```hurl
GET https://www.insee.fr
```

**Example 2: GET with headers**
```hurl
GET https://api.github.com/users/octocat
User-Agent: MyApp/1.0
Accept: application/json
```

**Example 3: POST request**
```hurl
POST https://httpbin.org/post
Content-Type: application/json
{
  "name": "John Doe",
  "age": 30
}
```

**Example 4: Testing with assertions**
```hurl
GET https://httpbin.org/json
HTTP 200
[Asserts]
jsonpath "$.slideshow.title" == "Sample Slide Show"
```

4. Run the cell (Shift+Enter) to execute the Hurl command

The kernel will display:
- HTTP response output
- Any errors or validation failures

## How It Works

The kernel works by:
1. Taking the Hurl code from the notebook cell
2. Writing it to a temporary `.hurl` file
3. Executing `hurl --color <file>`
4. Capturing and displaying the output in the notebook
5. Cleaning up the temporary file

## Troubleshooting

### "hurl is not installed" error

Make sure Hurl is installed and available in your PATH:
```bash
which hurl
hurl --version
```

### Kernel not appearing in Jupyter

Try reinstalling the kernel:
```bash
install-hurl-kernel --user
jupyter kernelspec list
```

### Command timeout

By default, commands timeout after 30 seconds. For long-running requests, this can be adjusted in the kernel code.

## Development

To modify the kernel:

1. Clone the repository:
   ```bash
   git clone https://github.com/micedre/jupyter-hurl-kernel.git
   cd jupyter-hurl-kernel
   ```

2. Install in development mode:
   ```bash
   uv pip install -e .
   install-hurl-kernel --sys-prefix
   ```

3. Make your changes to the kernel code in `src/jupyter_hurl_kernel/`

4. Restart your Jupyter notebook kernel to test changes

## Uninstallation

To remove the kernel:
```bash
jupyter kernelspec uninstall hurl
```

To uninstall the package:
```bash
uv pip uninstall jupyter-hurl-kernel
```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Resources

- [Hurl Documentation](https://hurl.dev/docs/manual.html)
- [Hurl Tutorial](https://hurl.dev/docs/tutorial/your-first-hurl-file.html)
- [Jupyter Kernel Documentation](https://jupyter-client.readthedocs.io/en/stable/kernels.html)
