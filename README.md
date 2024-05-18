# 自作CPU用アセンブラ+α
## 命令リファレンス
```nand <dst> <src1> <src2>```\
```src1```レジスタと```src2```レジスタの値をNAND演算して、その結果を```dst```レジスタに格納します。

```shift <dst> <src> <cnt>```\
```src```レジスタの値を```cnt```レジスタの値分だけ左シフトして、その結果を```dst```レジスタに格納します。

```save <address>```\
```address```で指定されたメモリアドレスにrレジスタの値を格納します。

```load <address>```\
```address```で指定されたメモリアドレスの値をrレジスタに格納します。

```#```\
コメントアウトです。必ず```#```の直後に半角スペースを用いて、かつ、コメント中に半角スペースを含めないでください。

## レジスタリファレンス
```t``` : トゥルーレジスタ。読み取り専用で常に0000 0001を出力します。 

```r``` : リザルトレジスタ。強制ではありませんが、演算結果の出力先に用います。また、saveとloadで参照されます。

```a``` : 汎用レジスタ。

```b``` : 汎用レジスタ。

## アセンブラ
アセンブラはpython3で動作します。\
実行する際は\
```$ assembler.py <InputFile>.tcp <OutputFile>.bin```\
でアセンブリ言語ファイルと出力先のbinファイルを指定して実行してください。

## エミュレータ
エミュレータはpython3で動作します。\
実行する際は\
```$ emulator <CodeFile>.bin```\
でbinファイルを指定して実行してください。\
Enterキーを押すことで処理が進みます。