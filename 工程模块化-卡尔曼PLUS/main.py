from package import *

def main(roomId = 1):
    #这么沙雕的命名法也只有我这样的辣鸡会干了
    go = gos.gogogo("https://goldennumber.aiedu.msra.cn/", "/swagger/v1/swagger.json",roomId)
    go.start()

if __name__ == '__main__':
    #以下为参数传递模块的功能，用于在外面打开这个程序时，可调用参数，显得逼格无限
    parser = argparse.ArgumentParser()
    parser.add_argument('--room', type=int, help='Room ID', required=False)
    args = parser.parse_args()

    main(args.room)
