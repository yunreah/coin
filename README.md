# 使い方
1. Anaconda等を使ってpythonをインストール
2. 自分のLINEのアクセストークンを取得
3. coinAlertToLine.pyの17行目にアクセストークンを入力
4. アラートの設定を行って実行　　　
 常時PCを起動する必要あり

# 設定項目
* cycle: 価格を確認&通知を行う周期　デフォルト2分
* waittime: 一度通知した通貨に対して，再度通知を行うまでの待ち時間(連続通知を防ぐ役割)　デフォルト1時間
* lowalert: 指定した価格を下回った時に通知
* hihalert: 指定した価格を上回った時に通知
