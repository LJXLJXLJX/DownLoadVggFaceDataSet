import requests
import os
import cv2
from multiprocessing import Pool
import time
import numpy as np

AllFileList = os.listdir('files')
AllPeopleList = os.listdir('images')
AllFileList = list(set(AllFileList) - set(AllPeopleList))  # 本次下载队列去掉已经下载的
AllFileNum = len(AllFileList)
quarter = AllFileNum // 4
fileList1 = AllFileList[0:quarter]
fileList2 = AllFileList[quarter:2 * quarter]
fileList3 = AllFileList[2 * quarter:3 * quarter]
fileList4 = AllFileList[3 * quarter:]


def download_1(fileList1):
    fileNum = len(fileList1)
    for i in range(fileNum):
        print(i + 1, '/', fileNum)
        peopleName = fileList1[i][0:fileList1[i].find('.txt')]
        peopleDir = 'images/' + peopleName
        if not os.path.exists(peopleDir):
            os.mkdir(peopleDir)
        with open('files/' + fileList1[i], 'r') as f:
            lines = f.readlines()
            count = 0
            for line in lines:
                count += 1
                print('  ', count)
                line = line.split(' ')
                num = str(int(line[0]))
                if int(num) > 200:  # 后面基本上都是错的，只取200张
                    break
                url = line[1]
                x1 = int(float(line[2]))
                y1 = int(float(line[3]))
                x2 = int(float(line[4]))
                y2 = int(float(line[5]))
                imagePath = peopleDir + '/' + num + '.jpg'
                time.sleep(0.6)
                try:
                    r = requests.get(url, timeout=10)
                    s = requests.session()
                    s.keep_alive = False

                    if r.status_code == 200:
                        with open(imagePath, 'wb') as f:
                            for chunk in r:
                                f.write(chunk)
                        image = cv2.imread(imagePath)
                        image = image[y1:y2, x1:x2]
                        cv2.imwrite(imagePath, image)
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    pool = Pool(processes=4)
    pool.map(download_1, [fileList1, fileList2, fileList3, fileList4])
    pool.close()
    pool.join()
