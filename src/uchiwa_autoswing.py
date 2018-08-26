# うちわ動かすやつ
import RPi.GPIO as GPIO
import time
# 温度取るやつ
import smbus
import time
# 温度用の定数
i2c = smbus.SMBus(1)
address = 0x5c
 

def get_discomfort(i2c, address):
    # センサsleep解除
    try:
        i2c.write_i2c_block_data(address,0x00,[])
    except:
        pass
    # 読み取り命令
    time.sleep(0.003)
    i2c.write_i2c_block_data(address,0x03,[0x00,0x04])

    # データ受取
    time.sleep(0.015)
    block = i2c.read_i2c_block_data(address,0,6)
    shitudo = float(block[2] << 8 | block[3])/10
    ondo = float(block[4] << 8 | block[5])/10

    # 不快指数を算出
    discomfort = (0.81 * ondo) + (0.01 * shitudo) * (0.99 * ondo - 14.3 ) + 46.3
    print(shitudo) # 湿度表示
    print(ondo) # 温度表示
    print(discomfort)

    return discomfort

def move_servo(servo)
    # パルス出力の開始
    servo.start(0)

    # サーボを動作させる
    servo.ChangeDutyCycle(2)
    time.sleep(0.5)
    servo.ChangeDutyCycle(7)
    time.sleep(0.5)

    # 後処理
    servo.stop()

# メイン関数
def main():
    i2c = smbus.SMBus(1)
    address = 0x5c
    
    # GPIOのモード設定
    GPIO.setmode(GPIO.BCM)

    # GPIO18を制御パルスの出力に設定
    gp_out = 18
    GPIO.setup(gp_out, GPIO.OUT)

    # サーボの制御パルスと周波数の設定
    servo = GPIO.PWM(gp_out, 50)

    # 以下、無限ループ
		try:
        while true:
            discomfort = get_discomfort(i2c, address)

            if(discomfort > 75) # 不快指数のしきい値を一度75とする
                #print('disconfort')
                move_servo(servo)

            time.sleep(5)
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == '__main__':
    main()