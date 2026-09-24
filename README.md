# Jリート・ハブ 公開手順（GitHub Pages）

1. github.com で無料アカウントを作り、New repository で `jreit-hub`（Public）を作成
2. 「uploading an existing file」から、この site フォルダの中身をすべてドラッグして Commit
3. Settings → Pages → Branch を `main` / `/(root)` にして Save
4. 数分後に https://ユーザー名.github.io/jreit-hub/ で公開されます
5. ユーザー名を含むURLが決まったら、sitemap.xml・robots.txt・各ページの canonical にある `YOUR-NAME` を実際のURLに置換してください（Claudeに頼めば再生成します）
6. Google Search Console でURLを登録し、sitemap.xml を送信すると検索に載りやすくなります
