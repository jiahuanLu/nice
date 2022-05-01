from socket import *
import numpy as np
import cv2
import base64
import os
import detect

detect_api = detect.DetectAPI(exist_ok=True)


# 提供yolov5检测图片的服务（这里实现的是socket）
class Yolov5DetectServer:
    host = "127.0.0.1"
    port = 12345
    bufferSize = 1024 * 20

    def __init__(self, host, port, buffer_size):
        self.host = host
        self.port = port
        self.bufferSize = buffer_size

    def main(self):
        socketAddress = (self.host, self.port)
        tcpSerSock = socket(AF_INET, SOCK_STREAM)
        tcpSerSock.bind(socketAddress)
        tcpSerSock.listen(5)
        while True:
            receiveData = bytes([])
            print('waiting for connection...')
            tcpCliSock, clientAddress = tcpSerSock.accept()
            print('...connected from:', clientAddress)

            while True:
                data = tcpCliSock.recv(self.bufferSize)
                if not data or len(data) == 0:
                    break
                else:
                    receiveData = receiveData + data
            receiveData = base64.b64decode(receiveData)

            np_arr = np.frombuffer(receiveData, np.uint8)
            image = cv2.imdecode(np_arr, 1)

            path = '/Users/lujiahuan/4projects/yolov5+javaweb/yolov5/runs/detect/myexp_source_imgs/'
            cv2.imwrite(os.path.join(path, 'test.jpg'), image)

            responseResult = detect_api.run()
            print(responseResult)   # 包含标框点坐标、识别结果和置信度值

            image_detect = cv2.imread('/Users/lujiahuan/4projects/yolov5+javaweb/yolov5/runs/detect/myexp/test.jpg', flags=1)
            # cv2.imshow("image", image_detect)
            #
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            # cv2.waitKey(1)
            # cv2.waitKey(1)
            # cv2.waitKey(1)
            # cv2.waitKey(1)

            tcpCliSock.send("0001".encode())  # tcpCliSock.send("返回值")
            tcpCliSock.close()
        tcpSerSock.close()

    def detect_img(image):
        result, names = a.detect([image])
        img = result[0][0]  # 第一张图片的处理结果图片
        '''
        for cls,(x1,y1,x2,y2),conf in result[0][1]: #第一张图片的处理结果标签。
            print(cls,x1,y1,x2,y2,conf)
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0))
            cv2.putText(img,names[cls],(x1,y1-20),cv2.FONT_HERSHEY_DUPLEX,1.5,(255,0,0))
        '''
        print(result[0][1])
        cv2.imshow("image", img)


if __name__ == "__main__":
    detectObj = Yolov5DetectServer("127.0.0.1", 12345, 1024 * 20)
    detectObj.main()
