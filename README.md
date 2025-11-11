# Z80emulator

**Z80emulator** は、Pythonで書かれた Z80 CPU エミュレータと BASIC-to-Z80 コンパイラのパッケージです。  
BASIC 風の簡易命令を Z80 マシン語に変換し、Python 上で Z80 プログラムをエミュレーション可能です。

## 特徴

- 完全な Z80 命令セットのサポート（基本命令 + CB + ED + DD/FD プレフィックス）
- Visual Basic 風の簡易命令を Z80 マシン語に変換
- CPU、メモリ、フラグをモジュールとして分離
- ラベル・条件ジャンプ対応
- PyPI 配布済みで簡単インストール

## インストール

```bash
pip install Z80emulator
```

---

## ドキュメント

<https://flandollscarlet495.github.io/Z80emulator/index.html>

## ソースコード

<https://github.com/FlandollScarlet495/Z80emulator>

## 使用例

```python
from Z80emulator import Z80emulator as Z80emu

# CPU インスタンス作成
cpu = Z80emu["CPU"]()

# メモリ初期化
mem = Z80emu["Memory"]()
cpu.memory = mem

# アセンブラで Z80 命令を生成
assembler = Z80emu["Assembler"]()
bytecode = assembler.assemble([
    "LD A,10",
    "LD B,20",
    "ADD A,B",
    "HALT"
])

# メモリにロード
for addr, b in enumerate(bytecode):
    mem.write(addr, b)

# CPU 実行
while not cpu.halted:
    cpu.step()
print("Aレジスタの値:", cpu.reg['A'])

# BASIC 風プログラムをコンパイル
basic = Z80emu["BasicCompiler"]()
basic_code = [
    "LET A = 10",
    "LET B = 20",
    "PRINT A",
    "END"
]
bytecode2 = basic.compile(basic_code)
```

## LISENCE

MIT License

---

```sql
MIT License

Copyright (c) 2025 雪島 雪乃

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
