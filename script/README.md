# マスターcsvからタイムテーブルのマークダウンを作成

マスターcsvが更新された際、以下の手順でHP上のタイムテーブルを更新する。

1. マスターのスプレッドシートをcsvとしてエクスポートする。これを`timetable0.csv`としてここに置く。
    - この`timetable0.csv`には様々な情報が書かれているため、git管理しない（git管理すると全世界公開されるので） 
1. `make filter`
    - `timetable0.csv`中から必要な情報のみを抽出して`timetable.csv`を作成する。
    - この`timetable.csv`はgit管理する。
1. `make test`
    - `output_jp.md`および`output_en.md`という一時ファイル（git管理しない）が作成される。
    - このファイルは最終的にアップロードされるものと同じものなので、これを見て中身がOKかチェックする。
    - このファイルは`template_jp.md`ないし`template_en.md`に`timetable.csv`の情報を埋め込んだものである。
    - `make clean`により`output_jp.md`および`output_en.md`は削除できる。
1. `make render`
    - `output_jp.md`および`output_en.md`と同じものがhugo管理下のしかるべき位置にコピーされる。
1. 通常通り`hugo`を実行しHPを作成する。