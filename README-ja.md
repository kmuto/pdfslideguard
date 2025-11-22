# 🛡️ PDF Slide Guard

[English](README.md)

## 概要

**PDF Slide Guard**は、特定のオンラインスライド共有サイトや旧式のPDFビューアで発生する表示不具合やレンダリングエラーを回避するために設計されたコマンドラインツールです。

元のPDFの**テキスト情報を失うことなく**、すべてのページを**高解像度の画像**として再構築し、その上に**検索可能な透明なテキストレイヤー**を重ね合わせます。

これにより、表示の**互換性**を確保しつつ、テキストの**検索性・コピー機能**を維持します。

-----

## 特徴

- **互換性の最大化:** 複雑なベクトルデータ（フォント、図形など）を単一の画像に変換することで、PDFパーサーのエラーを根本的に回避します。
- **検索性の維持:** 元のテキストデータを透明なレイヤーとして埋め込むため、生成されたPDFはテキスト検索可能です。
- **高解像度出力:** ズーム倍率とJPEG品質を調整できるため、画質とファイルサイズのバランスを自由に設定できます。
- **柔軟なページサイズ:** スライドサイトでの再スケーリングによる劣化を防ぐため、出力サイズを**元のサイズに戻す（`-k`）**か、**拡大サイズを保持する（デフォルト）**かを選択できます。
- **日本語対応:** 透明テキストの埋め込みにおいて、日本語フォントをサポートします。

## Dockerを使う場合
Docker Hubおよびghcr.ioにイメージを用意しています。

```
docker pull kenshimuto/pdfslideguard:latest
または
docker pull ghcr.io/kmuto/pdfslideguard:latest
```

## Dockerを使わずインストールする場合

### 1. 依存ライブラリのインストール
このツールは、PyMuPDF、pypdf、ReportLabに依存しています。`requirements.txt`を使用してインストールします。

```bash
pip3 install -r requirements.txt
```

### 2. 日本語フォントの準備
透明テキストの埋め込みには、システムまたは指定パスに日本語TrueType/OpenTypeフォントが必要です。デフォルトではIPAex Gothic（ipaexg.ttf）を探します。

```bash
/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf
```

別のフォントを使用する場合は、後述の`-f`オプションでパスを指定してください。

### 3. パッケージのインストール
[リリース](https://github.com/kmuto/pdfslideguard/releases)ページから最新のpdfslideguardのパッケージをダウンロードし、`pip3`コマンドでインストールしてください。

```bash
pip3 install pdfslideguard-X.X.X.tar.gz
```

## 使用方法

### 基本構文

```bash
pdfslideguard [OPTIONS] INPUT_PDF OUTPUT_PDF
```

### オプション

| オプション | 引数  | デフォルト | 説明  |
| ---------- | ----- | ---------- | ----- |
| `-z`, `--zoom_factor` | `float` | `3.0` | 高解像度画像化のためのズーム倍率。高いほど高画質になります。 |
| `-j`, `--jpeg_quality` | `int` | `85` | JPEG画像の品質（1-100）。低いほどファイルサイズは小さくなります。 |
| `-f`, `--font_path` | `str` | デフォルトパス | 日本語フォントファイル（.ttf, .otf）へのパス。 |
| `-q`, `--quiet` | (フラグ) | `False` | INFOメッセージを抑制し、WARNING/ERRORのみを表示します。 |
| `-k`, `--keep_size` | (フラグ) | `False` | フラグがある場合、最終的なPDFサイズを**元のサイズに戻します**。フラグがない場合（デフォルト）は、**拡大サイズを保持します**。 |

Dockerイメージを利用する場合、コンテナ内でファイル処理を行うために、以下のように入出力フォルダをマウントして使います。

```bash
docker run --rm \
    -v ".:/work" \
    kenshimuto/pdfslideguard [OPTIONS] \
    /work/INPUT_PDF /work/OUTPUT_PDF
```

### 実行例
#### 1. デフォルト設定で実行（拡大サイズを維持）

```bash
pdfslideguard presentation_input.pdf final_output.pdf
# 結果: 拡大サイズを維持した、JPEG品質85のPDFが出力される。
```

#### 2. ファイルサイズを削減し、元のサイズに戻す場合

```bash
pdfslideguard presentation_input.pdf final_output.pdf -z 1.8 -j 70 -k
# 結果: ズーム倍率1.8、JPEG品質70で圧縮され、ページサイズは元の寸法に戻る。
```

#### 3. 別のフォントパスを指定する場合

```bash
pdfslideguard input.pdf output.pdf -f /home/user/my_fonts/NotoSansJP-Regular.otf
```

## ライセンス
MIT License を適用しています。

```
Copyright 2025 Kenshi Muto

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
