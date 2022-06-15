#================================================================
#================================================================
# API-DIO(LNX)
# トリガサンプル
#                                                CONTEC Co., Ltd.
#================================================================
#================================================================

import ctypes
import sys
import cdio

#================================================================
# コールバック関数
#================================================================
def trg_callback(dev_id, msg, bit_no, logic, param):
    #----------------------------------------
    # トリガメッセージの処理
    #----------------------------------------
    if msg == cdio.DIOM_TRIGGER:
        #----------------------------------------
        # アップカウント
        #----------------------------------------
        if logic == cdio.DIO_INT_RISE:
            up_down = 'UP'
        #----------------------------------------
        # ダウンカウント
        #----------------------------------------
        elif logic == cdio.DIO_INT_FALL:
            up_down = 'DOWN'
        else:
            up_down = 'NONE'
        c_char_ptr = ctypes.cast(param, ctypes.c_char_p)
        #----------------------------------------
        # トリガ要因表示
        #----------------------------------------
        print(f'Trigger:id={dev_id} bit = {bit_no}, logic = {up_down}: {c_char_ptr.value.decode()}')
    #----------------------------------------
    # それ以外
    #----------------------------------------
    else:
        print(f'msg = {msg}')
    return


ptrg_callback = cdio.PDIO_TRG_CALLBACK(trg_callback)


#================================================================
# main関数
#================================================================
def main():
    dio_id = ctypes.c_short()
    in_port_num = ctypes.c_short()
    out_port_num = ctypes.c_short()
    err_str = ctypes.create_string_buffer(256)

    #----------------------------------------
    # ドライバ初期化処理
    #----------------------------------------
    dev_name = input('Input device name: ')
    lret = cdio.DioInit(dev_name.encode(), ctypes.byref(dio_id))
    if lret != cdio.DIO_ERR_SUCCESS:
        cdio.DioGetErrorString(lret, err_str)
        print(f"DioInit = {lret}: {err_str.value.decode('sjis')}")
        sys.exit()
    #----------------------------------------
    # ビット数の取得
    #----------------------------------------
    lret = cdio.DioGetMaxPorts(dio_id, ctypes.byref(in_port_num), ctypes.byref(out_port_num))
    if lret != cdio.DIO_ERR_SUCCESS:
        cdio.DioGetErrorString(lret, err_str)
        print(f"DioGetMaxPorts = {lret}: {err_str.value.decode('sjis')}")
        sys.exit()
    max_trg = 8 * in_port_num.value
    if max_trg == 0:
        print(f'Input bit number = 0')
        sys.exit()
    else:
        print(f'Trigger bit = 0 to {max_trg - 1}')
    #----------------------------------------
    # トリガコールバックの設定
    #----------------------------------------
    param = ("input 'q' + 'enter' to quit").encode()
    lret = cdio.DioSetTrgCallBackProc (dio_id, ptrg_callback, param)
    if lret != cdio.DIO_ERR_SUCCESS:
        cdio.DioGetErrorString(lret, err_str)
        print(f"DioSetTrgCallBackProc = {lret}: {err_str.value.decode('sjis')}")
        sys.exit()
    #----------------------------------------
    # トリガを有効にする
    #----------------------------------------
    for bit_no in range(max_trg):
        lret = cdio.DioSetTrgEvent ( dio_id, bit_no, cdio.DIO_TRG_RISE | cdio.DIO_TRG_FALL, 100)
        if lret != cdio.DIO_ERR_SUCCESS:
            cdio.DioGetErrorString(lret, err_str)
            print(f"DioSetTrgEvent = {lret}: {err_str.value.decode('sjis')}")
            sys.exit()
    print("Waiting for trigger...")
    #----------------------------------------
    # 入力待ちループ
    #----------------------------------------
    while True:
        print("Input 'q' + 'enter' to quit")
        buf = input()
        #----------------------------------------
        # 終了
        #----------------------------------------
        if buf == 'q':
            print(f'quit.')
            break
    #----------------------------------------
    # ドライバ終了処理
    #----------------------------------------
    lret = cdio.DioExit(dio_id)
    if lret != cdio.DIO_ERR_SUCCESS:
        cdio.DioGetErrorString(lret, err_str)
        print(f"DioExit = {lret}: {err_str.value.decode('sjis')}")
    #----------------------------------------
    # アプリケーション終了
    #----------------------------------------
    sys.exit()


#----------------------------------------
# main関数呼び出し
#----------------------------------------
if __name__ == "__main__":
    main()
