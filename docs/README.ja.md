# Generate Pull Request

このワークフローでは OpenAI による文章生成モデルを使って、プルリクエストのタイトルと本文を生成します。

## 使い方

```yaml
name: OpenAI PR Description Generator

on:
  pull_request:
    types:
      - opened
      - synchronize

permissions:
  pull-requests: write
  contents: read

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

**必須** GitHub トークン。`${{ secrets.GITHUB_TOKEN }}` を指定します。

### `open-api-key`

**必須** OpenAI API キー。`${{ secrets.OPENAI_API_KEY }}` を指定します。
