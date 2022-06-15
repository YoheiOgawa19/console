#================================================================
#================================================================
# API-DIO(LNX)
# 割り込みサンプル
#                                                CONTEC Co., Ltd.
#================================================================
#================================================================

import ctypes
import sys
import cdio

#================================================================
# コールバック関数
#================================================================
def int_callback(dev_id, msg, bit_no, logic, param):
    #----------------------------------------
    # 割り込みメッセージの処理
    #----------------------------------------
    if msg == cdio.DIOM_INTERRUPT:
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
        # 割り込み要因表示
        #----------------------------------------
        print(f'Interrupt:id={dev_id}, bit = {bit_no}, logic = {up_down}: {c_char_ptr.value.decode()}')
    #----------------------------------------
    # それ以外
    #----------------------------------------
    else:
        print(f'msg = {msg}')
    return


pint_callback = cdio.PDIO_INT_CALLBACK(int_callback)


#================================================================
# main関数
#================================================================
def main():
    dio_id = ctypes.c_short()
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
    # デジタルフィルタの設定
    #----------------------------------------
    lret = cdio.DioSetDigitalFilter(dio_id, 20)
    if lret != cdio.DIO_ERR_SUCCESS:
        cdio.DioGetErrorString(lret, err_str)
        print(f"DioSetDigitalFilter = {lret}: {err_str.value.decode('sjis')}")
    #----------------------------------------
    # 割り込みイベント要因の設定
    #----------------------------------------
    for bit_no in range(4):
        lret = cdio.DioSetInterruptEvent(dio_id, bit_no, cdio.DIO_INT_RISE)
        if lret != cdio.DIO_ERR_SUCCESS:
            cdio.DioGetErrorString(lret, err_str)
            print(f"DioSetInterruptEvent = {lret}: {err_str.value.decode('sjis')}")
            sys.exit()
    #----------------------------------------
    # 割り込みコールバックの設定
    #----------------------------------------
    param = ("input 'q' + 'enter' to quit").encode()
    lret = cdio.DioSetInterruptCallBackProc(dio_id, pint_callback, param)
    if lret != cdio.DIO_ERR_SUCCESS:
        cdio.DioGetErrorString(lret, err_str)
        print(f"DioSetInterruptCallBackProc = {lret}: {err_str.value.decode('sjis')}")
        sys.exit()
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
