"""Hurl Jupyter Kernel implementation."""

import re
import subprocess
import tempfile
from pathlib import Path

from ipykernel.kernelbase import Kernel


class HurlKernel(Kernel):
    """A Jupyter kernel for executing Hurl commands."""

    implementation = "Hurl"
    implementation_version = "0.1.0"
    language = "hurl"
    language_version = "0.1"
    language_info = {
        "name": "hurl",
        "mimetype": "text/plain",
        "file_extension": ".hurl",
    }
    banner = "Hurl kernel - Execute HTTP requests with Hurl"

    def __init__(self, **kwargs):
        """Initialize the kernel."""
        super().__init__(**kwargs)
        self._check_hurl_installation()

    def _check_hurl_installation(self):
        """Check if hurl is installed and available."""
        try:
            result = subprocess.run(
                ["hurl", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                self.hurl_version = result.stdout.strip()
            else:
                self.hurl_version = "unknown"
        except (FileNotFoundError, subprocess.TimeoutExpired):
            self.hurl_version = None

    def _parse_magic_line(self, code):
        """Parse magic line (%%include or %%verbose) from code.

        Args:
            code: The code to parse

        Returns:
            tuple: (hurl_code, mode) where mode is 'normal', 'include', or 'verbose'
        """
        lines = code.split('\n')
        mode = 'normal'
        hurl_code_lines = []

        for line in lines:
            if line.strip().startswith('%%'):
                # Parse magic line
                magic = line.strip()[2:].lower()
                if magic == 'include':
                    mode = 'include'
                elif magic == 'verbose':
                    mode = 'verbose'
            else:
                hurl_code_lines.append(line)

        return '\n'.join(hurl_code_lines), mode

    def do_execute(
        self,
        code,
        silent,
        store_history=True,
        user_expressions=None,
        allow_stdin=False,
    ):
        """Execute a Hurl command.

        Args:
            code: The Hurl code to execute
            silent: If True, don't send output to the client
            store_history: Whether to store this execution in history
            user_expressions: User expressions to evaluate
            allow_stdin: Whether to allow stdin

        Returns:
            dict: Execution result
        """
        if not code.strip():
            return {
                "status": "ok",
                "execution_count": self.execution_count,
                "payload": [],
                "user_expressions": {},
            }

        # Check if hurl is installed
        if self.hurl_version is None:
            error_message = (
                "Error: hurl is not installed or not found in PATH.\n"
                "Please install hurl from https://hurl.dev/docs/installation.html"
            )
            if not silent:
                self.send_response(
                    self.iopub_socket,
                    "stream",
                    {"name": "stderr", "text": error_message},
                )
            return {
                "status": "error",
                "execution_count": self.execution_count,
                "ename": "HurlNotFound",
                "evalue": "hurl is not installed",
                "traceback": [error_message],
            }

        # Parse magic lines and get hurl code
        hurl_code, mode = self._parse_magic_line(code)

        if not hurl_code.strip():
            return {
                "status": "ok",
                "execution_count": self.execution_count,
                "payload": [],
                "user_expressions": {},
            }

        # Create a temporary file to store the Hurl code
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".hurl", delete=False
        ) as f:
            f.write(hurl_code)
            hurl_file = f.name

        try:
            # Build hurl command based on mode
            cmd = ["hurl", "--color", hurl_file]

            if mode == 'include':
                # --include shows response headers and body
                cmd.insert(1, "--include")
            elif mode == 'verbose':
                # --verbose shows all information (request, response, headers, timing, etc.)
                cmd.insert(1, "--verbose")

            # Execute hurl command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
            )

            # Send stdout to the client
            if result.stdout and not silent:
                self.send_response(
                    self.iopub_socket,
                    "stream",
                    {"name": "stdout", "text": result.stdout},
                )

            # Send stderr to the client
            if result.stderr and not silent:
                self.send_response(
                    self.iopub_socket,
                    "stream",
                    {"name": "stderr", "text": result.stderr},
                )

            # Determine execution status
            if result.returncode == 0:
                status = "ok"
                return_dict = {
                    "status": status,
                    "execution_count": self.execution_count,
                    "payload": [],
                    "user_expressions": {},
                }
            else:
                status = "error"
                return_dict = {
                    "status": status,
                    "execution_count": self.execution_count,
                    "ename": "HurlExecutionError",
                    "evalue": f"Hurl command failed with exit code {result.returncode}",
                    "traceback": [result.stderr] if result.stderr else [],
                }

            return return_dict

        except subprocess.TimeoutExpired:
            error_message = "Error: Hurl command timed out (exceeded 30 seconds)"
            if not silent:
                self.send_response(
                    self.iopub_socket,
                    "stream",
                    {"name": "stderr", "text": error_message},
                )
            return {
                "status": "error",
                "execution_count": self.execution_count,
                "ename": "HurlTimeout",
                "evalue": "Command timed out",
                "traceback": [error_message],
            }
        except Exception as e:
            error_message = f"Error executing Hurl command: {e}"
            if not silent:
                self.send_response(
                    self.iopub_socket,
                    "stream",
                    {"name": "stderr", "text": error_message},
                )
            return {
                "status": "error",
                "execution_count": self.execution_count,
                "ename": type(e).__name__,
                "evalue": str(e),
                "traceback": [error_message],
            }
        finally:
            # Clean up temporary file
            try:
                Path(hurl_file).unlink()
            except Exception:
                pass


if __name__ == "__main__":
    from ipykernel.kernelapp import IPKernelApp

    IPKernelApp.launch_instance(kernel_class=HurlKernel)
