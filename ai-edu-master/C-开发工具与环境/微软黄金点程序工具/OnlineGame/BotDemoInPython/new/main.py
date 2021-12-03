from package import *

def main(roomId):
    pass
    # go = go.gogogo("https://goldennumber.aiedu.msra.cn/", "/swagger/v1/swagger.json", None)
    # go.start()
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--room', type=int, help='Room ID', required=False)
    args = parser.parse_args()

    main(args.room)