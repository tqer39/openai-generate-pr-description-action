from openai import OpenAI
import os
import subprocess

# OpenAI API キーを設定
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key is not set.")

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.getenv("OPENAI_API_KEY")
)


# プロンプトの準備
def create_prompt(commit_logs):
    return f"""
    ## 指示内容

    - 以下のコミットログとファイルの差分を読んで、理解し易いプルリクエストのタイトルと詳細な説明を日本語で作成してください。
    - Markdown 形式で記述してください。
        - ただし出力内容の1行目は例外です。`# `, `## ` などは不要です。
        - ファイル名はバッククオートで囲んでください。
        - https://github.com/orgs/community/discussions/16925 を参考にしてください。
            - 内容に応じて NOTE, TIPS, IMPORTANT, WARNING, CAUTION を使用してください。

                例:
                ```
                > [!WARNING]
                >
                > - 💣 breaking change が含まれています。注意してください。
                ```

    - プルリクエストのタイトル
        - タイトルの冒頭には総合的に適した emoji をつけてください。
        - 1行目に出力してください。2行目以降がプルリクエストの説明です。
    - プルリクエストの説明
        - コミットログとファイルを読んで、変更点の概要と技術的な詳細や注意点を記述してください。
            - なければ項目ごと出力しないでください。
            - 嘘を書かないでください。
        - 変更点の概要
            - 概要を簡潔に説明する。
        -  技術的な詳細や注意点
            - 各項目の先頭に適切な emoji をつけてください。

    ## コミットログとファイルの差分

    {commit_logs}

    ## 出力形式

    プルリクエストのタイトル

    ## 📓 変更点の概要

    - 概要を簡潔に説明する。

    ## ⚒ 技術的な詳細や注意点

    - 詳細な説明A
    - 詳細な説明B
    """


# OpenAI API でのリクエスト
def generate_pr_description(commit_logs):
    prompt = create_prompt(commit_logs)

    response = client.chat.completions.create(
        model="gpt-4o",  # GPT-3.5の場合は "gpt-3.5-turbo" に変更
        messages=[
            {"role": "system", "content": "あなたは優秀なソフトウェアエンジニアです。"},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1000,
        temperature=0.1,
    )

    return response.choices[0].message.content.strip()


# Git コミットログとファイルの差分の取得
def get_commit_logs_and_diffs():
    # リモートの変更を取得
    subprocess.run(["git", "fetch", "origin"], check=True)

    result = subprocess.run(
        ["git", "log", "--pretty=format:%H %s", "origin/main..HEAD", "-n", "70"],
        capture_output=True,
        text=True,
    )  # コミットログの数を制限
    commit_logs = result.stdout.strip().split("\n")

    if not commit_logs or commit_logs == [""]:
        return ""

    logs_and_diffs = []
    for commit in commit_logs:
        commit_hash = commit.split()[0]
        if commit_hash:
            diff_result = subprocess.run(
                ["git", "diff", commit_hash + "^!", "--"],
                capture_output=True,
                text=True,
            )
            logs_and_diffs.append(f"Commit: {commit}\nDiff:\n{diff_result.stdout}")

    return "\n\n".join(logs_and_diffs)


# メインロジック
if __name__ == "__main__":
    commit_logs_and_diffs = get_commit_logs_and_diffs()

    if commit_logs_and_diffs:
        pr_description = generate_pr_description(commit_logs_and_diffs)
        print(pr_description)
    else:
        print("No new commits detected.")
