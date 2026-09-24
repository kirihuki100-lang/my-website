# Jリート・ハブ 公開手順（GitHub → Cloudflare Pages）

1. このフォルダの中身（index.html・reit/・sitemap.xml・robots.txt など）を、GitHubリポジトリ（kirihuki100-lang/my-website）の中身と入れ替えてコミットしてください。デプロイ対象ファイルは `index.html` という名前でリポジトリ直下に置く必要があります。
2. Cloudflare Pages が自動でビルド・公開します（既存の連携設定のまま）。
3. 公開URL（`xxxx.pages.dev` または独自ドメイン）が確定したら教えてください。sitemap.xml・robots.txt・各ページの canonical / og:url にある `https://YOUR-NAME.github.io/jreit-hub/` の部分を実際のURLに一括置換して再ビルドします（今はプレースホルダーのままです）。
4. URL確定後、Google Search Console にサイトを登録し、sitemap.xml（`公開URL/sitemap.xml`）を送信すると検索に載りやすくなります。

## 実装済みのSEO対策
- 各ページに <title>・meta description・canonical・robots(index,follow)
- OGP（og:title/og:description/og:type/og:url）・Twitter Card
- JSON-LD 構造化データ（WebSite / WebPage）
- sitemap.xml・robots.txt・.nojekyll
- JS無効環境向けの noscript フォールバック（トップページに銘柄リンク一覧）
- 銘柄ごとの静的HTML（reit/*.html）に主要指標・財務推移・分配金・保有物件トップ15を平文で掲載（クローラーが内容を読める）
