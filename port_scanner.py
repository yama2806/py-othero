import socket
import sys

# --- ここから設定 ---

# スキャン対象のIPアドレス（今回は自分自身を指す '127.0.0.1' を指定）
target_ip = '127.0.0.1'

# スキャンするポートの範囲
start_port = 1
end_port = 1024

# --- 設定はここまで ---


print(f"スキャン対象: {target_ip}")
print(f"スキャン範囲: {start_port} - {end_port}")
print("-" * 30)

try:
    # 指定されたポート範囲を1つずつチェック
    for port in range(start_port, end_port + 1):
        # 1. ソケットを作成
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # 2. タイムアウトを1秒に設定
        sock.settimeout(1)
        
        # 3. 接続を試みる 
        result = sock.connect_ex((target_ip, port))
        
        # 4. 接続に成功した場合（結果コードが0の場合）
        if result == 0:
            print(f"ポート {port} は開いています")
        
        # 5. ソケットを閉じる
        sock.close()

except KeyboardInterrupt:
    print("\nスキャンを中断しました。")
    sys.exit()

except socket.gaierror:
    print("\nホスト名が解決できませんでした。IPアドレスが正しいか確認してください。")
    sys.exit()

except socket.error:
    print("\nサーバーに接続できませんでした。")
    sys.exit()

print("-" * 30)
print("スキャンが完了しました。")