import threading
import time

count = 0

strList: list[str] = []

for i in range(10):
    strList.append(str(i))

thr_num = 3


def do_task():
    try:
        if len(strList) == 0:
            print('end of list')
            return
        head = strList[0]

        time.sleep(1)
        print(head)

        if len(strList) > 0:
            strList.pop(0)

        if len(strList) > 0:
            do_task()
    except NameError:
        pass


for _ in range(thr_num):
    threading.Thread(target=do_task, args=()).start()
