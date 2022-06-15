#================================================================
#================================================================
# API-DIO(LNX)
# デジタル入力カウンタサンプル
#                                                CONTEC Co., Ltd.
#                                                Ver1.00
#================================================================
#================================================================
import ctypes
import sys
import cdio


#================================================================
# コマンド定義
#================================================================
COMMAND_DIO_INIT = 1                # DioInit
COMMAND_DIO_SETCOUNTEDGE = 2        # DioSetCountEdge
COMMAND_DIO_SETCOUNTMATCHVALUE = 3  # DioSetCountMatchValue
COMMAND_DIO_STARTCOUNT = 4          # DioStartCount
COMMAND_DIO_READCOUNT = 5           # DioReadCount
COMMAND_DIO_GETCOUTNSTATUS = 6      # DioGetCountStatus
COMMAND_DIO_COUNTPRESET = 7         # DioCountPreset
COMMAND_DIO_STOPCOUNT = 8           # DioStopCount
COMMAND_DIO_EXIT = 9                # DioExit
COMMAND_EXIT = 10                   # Exit
MAX_CHANNEL = 8                     # 最大カウンタチャネル数


#================================================================
# 文字列を数値に変換できるかどうか確認する関数
#================================================================
def isnum(str, base):
    try:
        if 16 == base:
            int(str, 16)
        else:
            int(str)
    except:
        return False
    return True


#================================================================
# main関数
#================================================================
def main():
    err_str = ctypes.create_string_buffer(256)          # 入力文字列格納用バッファ
    command = ctypes.c_int()                            # コマンド番号格納用変数
    lret = ctypes.c_long()                              # 関数戻り値格納用変数
    id = ctypes.c_short()                               # ID格納用変数
    channel_num = ctypes.c_short()                      # カウンタチャネル格納用変数
    channel_no_type = ctypes.c_short * MAX_CHANNEL      # 配列タイプを作成
    channel_no = channel_no_type()                      # カウンタチャネル番号格納用配列
    count_edge_type = ctypes.c_short * MAX_CHANNEL      # 配列タイプを作成
    count_edge = count_edge_type()                      # カウント方向格納用配列
    compare_count_type = ctypes.c_uint * MAX_CHANNEL    # 配列タイプを作成
    compare_count = compare_count_type()                # 比較値格納用配列
    compare_reg_no_type = ctypes.c_short * MAX_CHANNEL  # 配列タイプを作成
    compare_reg_no = compare_reg_no_type()              # 比較値格納用配列
    preset_count_type = ctypes.c_uint * MAX_CHANNEL     # 配列タイプを作成
    preset_count = preset_count_type()                  # プリセット格納用配列
    count_type = ctypes.c_uint * MAX_CHANNEL            # 比較値格納用配列
    count = count_type()                                # カウント値格納用配列
    count_status_type = ctypes.c_uint * MAX_CHANNEL     # 比較値格納用配列
    count_status = count_status_type()                  # ステータス格納用配列
    i = ctypes.c_int()                                  # ループカウント用変数

    #----------------------------------------
    # カウンタチャネル番号を初期化
    #----------------------------------------
    for i in range(0, MAX_CHANNEL):
        channel_no[i] = i
    #----------------------------------------
    # 入力待ちループ
    #----------------------------------------
    while True:
        #----------------------------------------
        # コマンドの表示
        #----------------------------------------
        print('1.DioInit')
        print('2.DioSetCountEdge')
        print('3.DioSetCountMatchValue')
        print('4.DioStartCount')
        print('5.DioReadCount')
        print('6.DioGetCountStatus')
        print('7.DioCountPreset')
        print('8.DioStopCount')
        print('9.DioExit')
        print('10.Exit')
        #----------------------------------------
        # 入力待ち
        #----------------------------------------
        while True:
            buf = input('input command: ')
            if False == isnum(buf, 10):
                continue
            command = ctypes.c_int(int(buf))
            break
        #----------------------------------------
        # コマンド毎の関連情報入力
        #----------------------------------------
        #----------------------------------------
        # DioInit
        #----------------------------------------
        if command.value == COMMAND_DIO_INIT:
            #----------------------------------------
            # 選択した関数名の表示
            #----------------------------------------
            print('----------------------------------------')
            print('DioInit')
            print('----------------------------------------')
            #----------------------------------------
            # デバイス名の入力
            #----------------------------------------
            buf = input('Please input a device name: ')
        #----------------------------------------
        # DioSetCountEdge
        #----------------------------------------
        elif command.value == COMMAND_DIO_SETCOUNTEDGE:
            #----------------------------------------
            # 選択した関数名の表示
            #----------------------------------------
            print('----------------------------------------')
            print('DioSetCountEdge')
            print('----------------------------------------')
            #----------------------------------------
            # カウント方向の入力
            #----------------------------------------
            while True:
                buf = input('Please input count edge: ')
                if False == isnum(buf, 10):
                    continue
                else:
                    break
        #----------------------------------------
        # DioSetCountMatchValue
        #----------------------------------------
        elif command.value == COMMAND_DIO_SETCOUNTMATCHVALUE:
            #----------------------------------------
            # 選択した関数名の表示
            #----------------------------------------
            print('----------------------------------------')
            print('DioSetCountMatchValue')
            print('----------------------------------------')
            #----------------------------------------
            # 比較値の入力
            #----------------------------------------
            while True:
                buf = input('Please input match value: ')
                if False == isnum(buf, 10):
                    continue
                else:
                    break
        #----------------------------------------
        # DioStartCount
        #----------------------------------------
        elif command.value == COMMAND_DIO_STARTCOUNT:
            #----------------------------------------
            # 選択した関数名の表示
            #----------------------------------------
            print('----------------------------------------')
            print('DioStartCount')
            print('----------------------------------------')
        #----------------------------------------
        # DioReadCount
        #----------------------------------------
        elif command.value == COMMAND_DIO_READCOUNT:
            #----------------------------------------
            # 選択した関数名の表示
            #----------------------------------------
            print('----------------------------------------')
            print('DioReadCount')
            print('----------------------------------------')
        #----------------------------------------
        # DioGetCountStatus
        #----------------------------------------
        elif command.value == COMMAND_DIO_GETCOUTNSTATUS:
            #----------------------------------------
            # 選択した関数名の表示
            #----------------------------------------
            print('----------------------------------------')
            print('DioGetCountStatus')
            print('----------------------------------------')
        #----------------------------------------
        # DioCountPreset
        #----------------------------------------
        elif command.value == COMMAND_DIO_COUNTPRESET:
            #----------------------------------------
            # 選択した関数名の表示
            #----------------------------------------
            print('----------------------------------------')
            print('DioCountPreset')
            print('----------------------------------------')
            #----------------------------------------
            # プリセット値の入力
            #----------------------------------------
            while True:
                buf = input('Please input preset: ')
                if False == isnum(buf, 10):
                    continue
                else:
                    break
        #----------------------------------------
        # DioStopCount
        #----------------------------------------
        elif command.value == COMMAND_DIO_STOPCOUNT:
            #----------------------------------------
            # 選択した関数名の表示
            #----------------------------------------
            print('----------------------------------------')
            print('DioStopCount')
            print('----------------------------------------')
        #----------------------------------------
        # DioExit
        #----------------------------------------
        elif command.value == COMMAND_DIO_EXIT:
            #----------------------------------------
            # 選択した関数名の表示
            #----------------------------------------
            print('----------------------------------------')
            print('DioExit')
            print('----------------------------------------')
        #----------------------------------------
        # コマンドの実行と結果の表示
        #----------------------------------------
        #----------------------------------------
        # DioInit
        #----------------------------------------
        if command.value == COMMAND_DIO_INIT:
            #----------------------------------------
            # DioInitを実行
            #----------------------------------------
            lret.value = cdio.DioInit(buf.encode(), ctypes.byref(id))
            #----------------------------------------
            # エラーコードの文字列を取得
            #----------------------------------------
            cdio.DioGetErrorString(lret, err_str)
            #----------------------------------------
            # 関数の実行結果を表示
            #----------------------------------------
            print(f"DioInit = {lret.value}: {err_str.value.decode('sjis')}")
            #----------------------------------------
            # DioInitがエラーならコマンド入力に戻る
            #----------------------------------------
            if lret.value != cdio.DIO_ERR_SUCCESS:
                continue
            #----------------------------------------
            # DioGetMaxCountChannelsを実行
            #----------------------------------------
            lret.value = cdio.DioGetMaxCountChannels(id, ctypes.byref(channel_num))
            #----------------------------------------
            # DioGetMaxCountChannelsがエラーならエラーコードを表示
            #----------------------------------------
            if lret.value != cdio.DIO_ERR_SUCCESS:
                #----------------------------------------
                # エラーコードの文字列を取得
                #----------------------------------------
                cdio.DioGetErrorString(lret, err_str)
                #----------------------------------------
                # 関数の実行結果を表示
                #----------------------------------------
                print(f"DioGetMaxCountChannels = {lret.value}: {err_str.value.decode('sjis')}")
                continue
            #----------------------------------------
            # カウンタチャネル数が最大チャネル数より大きければ最大チャネル数に更新
            #----------------------------------------
            if channel_num.value > MAX_CHANNEL:
                channel_num.value = MAX_CHANNEL
        #----------------------------------------
        # DioSetCountEdge
        #----------------------------------------
        elif command.value == COMMAND_DIO_SETCOUNTEDGE:
            #----------------------------------------
            # カウント方向を配列に格納
            #----------------------------------------
            for i in range(0, channel_num.value):
                count_edge[i] = ctypes.c_short(int(buf))
            #----------------------------------------
            # DioSetCountEdgeを実行
            #----------------------------------------
            lret.value = cdio.DioSetCountEdge(id, channel_no, channel_num, count_edge)
            #----------------------------------------
            # エラーコードの文字列を取得
            #----------------------------------------
            cdio.DioGetErrorString(lret, err_str)
            #----------------------------------------
            # 関数の実行結果を表示
            #----------------------------------------
            print(f"DioSetCountEdge = {lret.value}: {err_str.value.decode('sjis')}")
        #----------------------------------------
        # DioSetCountMatchValue
        #----------------------------------------
        elif command.value == COMMAND_DIO_SETCOUNTMATCHVALUE:
            #----------------------------------------
            # 比較値を配列に格納
            #----------------------------------------
            for i in range(0, channel_num.value):
                compare_reg_no[i] = 0
                compare_count[i] = ctypes.c_uint(int(buf))
            #----------------------------------------
            # DioSetCountMatchValueを実行
            #----------------------------------------
            lret.value = cdio.DioSetCountMatchValue(id, channel_no, channel_num, compare_reg_no, compare_count)
            #----------------------------------------
            # エラーコードの文字列を取得
            #----------------------------------------
            cdio.DioGetErrorString(lret, err_str)
            #----------------------------------------
            # 関数の実行結果を表示
            #----------------------------------------
            print(f"DioSetCountMatchValue = {lret.value}: {err_str.value.decode('sjis')}")
        #----------------------------------------
        # DioStartCount
        #----------------------------------------
        elif command.value == COMMAND_DIO_STARTCOUNT:
            #----------------------------------------
            # DioStartCountを実行
            #----------------------------------------
            lret.value = cdio.DioStartCount(id, channel_no, channel_num)
            #----------------------------------------
            # エラーコードの文字列を取得
            #----------------------------------------
            cdio.DioGetErrorString(lret, err_str)
            #----------------------------------------
            # 関数の実行結果を表示
            #----------------------------------------
            print(f"DioStartCount = {lret.value}: {err_str.value.decode('sjis')}")
        #----------------------------------------
        # DioReadCount
        #----------------------------------------
        elif command.value == COMMAND_DIO_READCOUNT:
            #----------------------------------------
            # DioReadCountを実行
            #----------------------------------------
            lret.value = cdio.DioReadCount(id, channel_no, channel_num, count)
            #----------------------------------------
            # エラーコードの文字列を取得
            #----------------------------------------
            cdio.DioGetErrorString(lret, err_str)
            #----------------------------------------
            # 関数の実行結果を表示
            #----------------------------------------
            print(f"DioReadCount = {lret.value}: {err_str.value.decode('sjis')}")
            #----------------------------------------
            # DioReadCountがエラーならコマンド入力に戻る
            #----------------------------------------
            if lret.value != cdio.DIO_ERR_SUCCESS:
                continue
            #----------------------------------------
            # カウント値を表示
            #----------------------------------------
            print('====================')
            print('Input Data(10進数)')
            print('====================')
            for i in range(0, channel_num.value):
                print(f"Channel{i}: {count[i]}")
        #----------------------------------------
        # DioGetCountStatus
        #----------------------------------------
        elif command.value == COMMAND_DIO_GETCOUTNSTATUS:
            #----------------------------------------
            # DioGetCountStatusを実行
            #----------------------------------------
            lret.value = cdio.DioGetCountStatus(id, channel_no, channel_num, count_status)
            #----------------------------------------
            # エラーコードの文字列を取得
            #----------------------------------------
            cdio.DioGetErrorString(lret, err_str)
            #----------------------------------------
            # 関数の実行結果を表示
            #----------------------------------------
            print(f"DioGetCountStatus = {lret.value}: {err_str.value.decode('sjis')}")
            #----------------------------------------
            # DioGetCountStatusがエラーならコマンド入力に戻る
            #----------------------------------------
            if lret.value != cdio.DIO_ERR_SUCCESS:
                continue
            #----------------------------------------
            # ステータスを表示
            #----------------------------------------
            print('====================')
            print('Status')
            print('====================')
            for i in range(0, channel_num.value):
                print(f"Channel{i}: {count_status[i]:x}")
        #----------------------------------------
        # DioCountPreset
        #----------------------------------------
        elif command.value == COMMAND_DIO_COUNTPRESET:
            #----------------------------------------
            # プリセット値を配列に格納
            #----------------------------------------
            for i in range(0, channel_num.value):
                preset_count[i] = ctypes.c_uint(int(buf))
            #----------------------------------------
            # DioCountPresetを実行
            #----------------------------------------
            lret.value = cdio.DioCountPreset(id, channel_no, channel_num, preset_count)
            #----------------------------------------
            # エラーコードの文字列を取得
            #----------------------------------------
            cdio.DioGetErrorString(lret, err_str)
            #----------------------------------------
            # 関数の実行結果を表示
            #----------------------------------------
            print(f"DioCountPreset = {lret.value}: {err_str.value.decode('sjis')}")
        #----------------------------------------
        # DioStopCount
        #----------------------------------------
        elif command.value == COMMAND_DIO_STOPCOUNT:
            #----------------------------------------
            # DioStopCountを実行
            #----------------------------------------
            lret.value = cdio.DioStopCount(id, channel_no, channel_num)
            #----------------------------------------
            # エラーコードの文字列を取得
            #----------------------------------------
            cdio.DioGetErrorString(lret, err_str)
            #----------------------------------------
            # 関数の実行結果を表示
            #----------------------------------------
            print(f"DioStopCount = {lret.value}: {err_str.value.decode('sjis')}")
        #----------------------------------------
        # DioExit
        #----------------------------------------
        elif command.value == COMMAND_DIO_EXIT:
            #----------------------------------------
            # DioExitを実行
            #----------------------------------------
            lret.value = cdio.DioExit(id)
            #----------------------------------------
            # エラーコードの文字列を取得
            #----------------------------------------
            cdio.DioGetErrorString(lret, err_str)
            #----------------------------------------
            # 関数の実行結果を表示
            #----------------------------------------
            print(f"DioExit = {lret.value}: {err_str.value.decode('sjis')}")
        #----------------------------------------
        # Exitコマンドが選択されたら終了する
        #----------------------------------------
        if command.value == COMMAND_EXIT:
            break
    sys.exit()


#----------------------------------------
# main関数呼び出し
#----------------------------------------
if __name__ == "__main__":
    main()

