import os
import re
import subprocess

# issues.txtを読み込む
with open('issues.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# 空行（改行2つ以上）でブロックごとに分割
blocks = re.split(r'\n\s*\n', content.strip())
new_blocks = []
modified = False

for block in blocks:
    lines = block.strip().splitlines()
    if not lines: continue
    
    title_line = lines[0]
    body = '\n'.join(lines[1:])
    
    # タイトルの末尾が「 #数字」で終わっているかチェック
    if re.search(r' #\d+$', title_line):
        new_blocks.append(block) # 既にIssue化されているのでそのまま
    else:
        # 番号がない場合は新規Issueを作成
        print(f"Creating issue: {title_line}")
        cmd = ['gh', 'issue', 'create', '--title', title_line, '--body', body]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # 出力されたURL（例: https://github.com/.../issues/10）から番号を抽出
        issue_url = result.stdout.strip()
        issue_num = issue_url.split('/')[-1]
        
        # タイトルの末尾に発行されたIssue番号を追記
        new_title_line = f"{title_line} #{issue_num}"
        new_blocks.append(f"{new_title_line}\n{body}")
        modified = True

# 新しいアイデアがあった場合のみ issues.txt を上書き
if modified:
    with open('issues.txt', 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(new_blocks) + '\n')