# PyPI Trusted Publishing Setup

This document explains how to set up PyPI trusted publishing for the jupyter-hurl-kernel package.

## What is Trusted Publishing?

Trusted Publishing is a secure way to publish packages to PyPI without using API tokens. It uses OpenID Connect (OIDC) to authenticate GitHub Actions workflows directly with PyPI.

## Setup Steps

### 1. Create PyPI Account

If you don't have one already:
1. Go to https://pypi.org
2. Register for an account
3. Verify your email address

### 2. Configure Trusted Publisher on PyPI

1. Log in to your PyPI account
2. Go to your account settings: https://pypi.org/manage/account/
3. Scroll down to "Publishing" section
4. Click "Add a new pending publisher"
5. Fill in the form:
   - **PyPI Project Name**: `jupyter-hurl-kernel`
   - **Owner**: Your GitHub username or organization (e.g., `micedre`)
   - **Repository name**: `jupyter-hurl-kernel`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi`
6. Click "Add"

### 3. (Optional) Set up TestPyPI

For testing the publishing workflow before releasing to production PyPI:

1. Go to https://test.pypi.org
2. Register for an account (separate from PyPI)
3. Follow the same steps as above, but on TestPyPI
4. Use environment name: `testpypi`

### 4. Configure GitHub Repository

1. Go to your GitHub repository settings
2. Navigate to "Environments"
3. Create a new environment named `pypi`
4. (Optional) Add protection rules:
   - Required reviewers
   - Wait timer
   - Deployment branches (e.g., only main/master)
5. Repeat for `testpypi` environment if using TestPyPI

### 5. Create a Release

Once everything is configured:

1. Update version in `pyproject.toml`
2. Commit and push changes
3. Create a new release on GitHub:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```
4. Or use GitHub's release interface to create a new release
5. The workflow will automatically trigger and publish to PyPI

## Testing the Workflow

### Manual Testing (TestPyPI)

You can manually trigger the workflow to test publishing to TestPyPI:

1. Go to "Actions" tab in your GitHub repository
2. Select "Publish to PyPI" workflow
3. Click "Run workflow"
4. Select the branch
5. Click "Run workflow"

This will build and publish to TestPyPI only (not production PyPI).

### Verify TestPyPI Publication

After publishing to TestPyPI, you can install from there to test:

```bash
pip install --index-url https://test.pypi.org/simple/ jupyter-hurl-kernel
```

## Troubleshooting

### "Workflow does not have permission to access environment"

Make sure:
- The environment name in the workflow matches exactly what's in GitHub settings
- The environment is configured in your repository settings

### "Invalid or non-existent authentication information"

Make sure:
- You've set up the trusted publisher on PyPI with the correct repository information
- The workflow name matches exactly: `publish.yml`
- The environment name matches: `pypi`

### "Package already exists"

If the version already exists on PyPI:
- Update the version number in `pyproject.toml`
- Create a new release with the new version number

## Security Best Practices

1. **Use environment protection rules**: Require manual approval for production deployments
2. **Restrict deployment branches**: Only allow deployments from main/master branch
3. **Review releases**: Always review the code before creating a release
4. **Monitor PyPI project**: Enable notifications for your PyPI project

## Resources

- [PyPI Trusted Publishers Documentation](https://docs.pypi.org/trusted-publishers/)
- [GitHub Actions OIDC Documentation](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [PyPA publish action](https://github.com/pypa/gh-action-pypi-publish)
