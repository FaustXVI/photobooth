import time

from flash import Flash

def main():
    with Flash(37) as flash:
        flash.turn_on()
        time.sleep(1)
        flash.turn_off()
        time.sleep(1)


if __name__ == '__main__':
    main()
