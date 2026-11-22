# websheep — Web Sheep Mascot

画面の下を歩く、Web版デスクトップマスコットの羊バージョンです。
[cocoweb](https://github.com/Arbeit2025/cocoweb)（Cocoa Mascot）の羊版として作りました。
PCのブラウザでもスマホのブラウザでも動きます。

## できること

- 牧場の画面下を左右に散歩する（端で向きを変える、ときどき立ち止まる）
- キャラクターはSVG＋CSSアニメーションの羊（もこもこの体、耳、足アニメ、瞬き）
- タップ／クリックで吹き出しセリフ（羊用24種、連続重複なし）＋小さくジャンプ
- ドラッグで好きな場所へ移動（離すと地面に戻る）
- 「散歩を止める／はじめる」「おすわり」ボタン
- 起動時に時間帯で挨拶が変わる（朝／昼／夕方／夜）
- 呼ばれた回数を累計／今日で表示（SQLite）

## ローカル起動

```bash
pip install -r requirements.txt
python app.py
```

Flaskの開発サーバーは `flask --app app run` でも起動できます。

サーバーなしで試したい場合は、単体版 `websheep-prototype.html` をブラウザで開いてください（呼ばれた回数の保存以外は動作します）。

## 構成

- `app.py`：単一ファイル（Flask＋SQLite、`render_template_string`）
- `websheep-prototype.html`：サーバーなしで開ける単体版
- `tests/test_app.py`：表示・セリフ・SVG・カウント・healthz・エスケープ事故防止のテスト

## テスト

```bash
python -m pytest tests/
```

## 未実施・今後の候補

- Render等への公開（未実施）
- デスクトップ常駐版化やReleases等の配布形態（保留として別途検討）
- 無料プランに載せる場合、SQLiteデータは再デプロイ等で消える想定です
