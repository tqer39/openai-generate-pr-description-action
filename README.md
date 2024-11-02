./docs/README.ja.md を英語で書き直す

# Generate Pull Request Title and Description

This workflow uses an article generation model by OpenAI to generate the title and body of a pull request.

## Usage

```yaml
name: OpenAI PR Description Generator

on:
  pull_request:
    types:
      - opened
      - synchronize

jobs:
  pull-request:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    permissions:
      pull-requests: write
      contents: read
    if: contains(github.event.pull_request.user.login, 'renovate') == false
    steps:
      - uses: actions/checkout@v4
      - uses: tqer39/generate-pr-description-action@v0.0.1-alpha
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          open-api-key: ${{ secrets.OPENAI_API_KEY }}
```

## Inputs

### `github-token`

**Required** GitHub token. Specify `${{ secrets.GITHUB_TOKEN }}`.

### `open-api-key`

**Required** OpenAI API key. Specify `${{ secrets.OPENAI_API_KEY }}`.
