# npm Publishing Setup

This document explains how to set up automated publishing of the JupyterLab extension to npm.

## Prerequisites

1. **npm account**: Create one at https://www.npmjs.com/signup
2. **npm organization** (optional): For scoped packages like `@your-org/jupyterlab-hurl-extension`
3. **Access token**: Required for automated publishing

## Setup Steps

### 1. Create an npm Access Token

1. Log in to npm: https://www.npmjs.com/
2. Go to your account settings → Access Tokens
3. Click "Generate New Token" → "Classic Token"
4. Select token type: **Automation** (for CI/CD)
5. Copy the token (you won't see it again!)

### 2. Add Token to GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `NPM_TOKEN`
5. Value: Paste your npm token
6. Click **Add secret**

### 3. Verify Package Name Availability

Before publishing, check if the package name is available:

```bash
npm view jupyterlab-hurl-extension
```

If it returns an error, the name is available. If you want to use a scoped name:

```bash
npm view @your-username/jupyterlab-hurl-extension
```

**Update package.json** if you want to use a different name:
```json
{
  "name": "@your-username/jupyterlab-hurl-extension"
}
```

### 4. Test Publishing Locally (Optional)

Before setting up automation, test the publish process locally:

```bash
cd jupyterlab-hurl-extension

# Login to npm
npm login

# Build the package
jlpm install
jlpm build:prod

# Test pack (doesn't publish, just creates .tgz)
npm pack

# Dry run publish
npm publish --dry-run

# Actual publish (if everything looks good)
npm publish --access public
```

### 5. Publishing via GitHub Actions

The workflow will automatically publish when:

#### Option A: Create a GitHub Release

1. Create and push a tag:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

2. Create a release on GitHub:
   - Go to **Releases** → **Create a new release**
   - Choose the tag you created
   - Fill in release notes
   - Click **Publish release**

3. The workflow will automatically:
   - Extract version from tag (removes `v` prefix)
   - Build the extension
   - Publish to npm with provenance

#### Option B: Manual Workflow Dispatch

1. Go to **Actions** → **Publish JupyterLab Extension to npm**
2. Click **Run workflow**
3. Enter the version (e.g., `0.1.0`)
4. Click **Run workflow**

### 6. Verify Publication

After the workflow completes:

1. Check npm: https://www.npmjs.com/package/jupyterlab-hurl-extension
2. Test installation:
   ```bash
   pip install jupyterlab
   jupyter labextension install jupyterlab-hurl-extension
   ```

## Package Metadata

The package includes:

- **Name**: `jupyterlab-hurl-extension`
- **Version**: Automatically set from Git tag
- **License**: MIT
- **Repository**: Linked to GitHub repo
- **Homepage**: README with installation instructions
- **Keywords**: jupyter, jupyterlab, hurl, syntax-highlighting

## Troubleshooting

### "You do not have permission to publish"

- Verify `NPM_TOKEN` secret is set correctly
- Check token permissions (should be "Automation")
- Verify you're the owner or have publish rights

### "Package name already exists"

- Choose a different name or use scoped package (`@username/package`)
- Update `name` in package.json

### "Build failed"

- Check TypeScript compilation errors in workflow logs
- Test build locally: `jlpm build:prod`
- Verify all dependencies are in package.json

### "Version already published"

- npm doesn't allow republishing the same version
- Increment version number
- Use `npm version patch|minor|major` to bump version

## Version Management

### Automatic Versioning from Git Tags

The workflow extracts version from Git tags:
- Tag: `v0.1.0` → npm version: `0.1.0`
- Tag: `v1.2.3` → npm version: `1.2.3`

### Manual Version Bumping

```bash
cd jupyterlab-hurl-extension

# Patch version (0.1.0 → 0.1.1)
npm version patch

# Minor version (0.1.0 → 0.2.0)
npm version minor

# Major version (0.1.0 → 1.0.0)
npm version major
```

## npm Provenance

The workflow uses `--provenance` flag which:
- Links the npm package to the source code
- Shows which GitHub Actions workflow built it
- Increases trust and security
- Requires `id-token: write` permission

Read more: https://docs.npmjs.com/generating-provenance-statements

## Scoped Packages

To publish under your username or organization:

1. Update package.json:
   ```json
   {
     "name": "@your-username/jupyterlab-hurl-extension"
   }
   ```

2. Ensure `--access public` is in publish command (already included)

3. First time publishing a scoped package may require:
   ```bash
   npm login --scope=@your-username
   ```

## Maintenance

### Updating the Package

1. Make changes to the extension
2. Commit and push changes
3. Create a new tag with incremented version:
   ```bash
   git tag v0.1.1
   git push origin v0.1.1
   ```
4. Create a GitHub release
5. Workflow automatically publishes

### Unpublishing

**Warning**: Only use in emergencies within 72 hours of publishing

```bash
npm unpublish jupyterlab-hurl-extension@0.1.0
```

Better approach: Publish a new version with fixes.

## Security

- **Never commit** npm tokens to the repository
- Use GitHub Secrets for sensitive data
- Enable 2FA on your npm account
- Use Automation tokens (not your personal token)
- Regularly rotate tokens

## Links

- npm Documentation: https://docs.npmjs.com/
- GitHub Actions: https://docs.github.com/en/actions
- JupyterLab Extensions: https://jupyterlab.readthedocs.io/en/stable/extension/extension_dev.html
