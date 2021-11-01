import cv2,subprocess,time,os,re

devs = os.listdir('/dev')
vid_indices = [int(dev[-1]) for dev in devs 
if dev.startswith('video')]
vid_indices = sorted(vid_indices)
clener = re.sub("[],*[\r\n]*","", str(vid_indices))
clear_number_cam = re.sub("[0-1] ","", str(clener))
resolution_1080p= [1920,1080] #1080p
resolution_768p=[1366,768] #768p
resolution_720p=[1280,720] #720p
resolution_480p=[856,480]#480p
cap = cv2.VideoCapture(int(clear_number_cam[0])) 
cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution_480p[0]) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution_480p[1]) 
ptime=0  
nome = "video capture"
subprocess.call('pactl load-module module-loopback latency_msec=1', shell=True) 
while(cap.isOpened()):
    ret,frame = cap.read()
    #calc fps
    ctime = time.time() 
    fps = 1//(ctime-ptime)
    ptime = ctime
    #video processor
    output_video = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)   
    resized = cv2.resize(output_video,(resolution_768p[0],resolution_768p[1])) 
    cv2.namedWindow(nome, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(nome,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)    
    cv2.putText(resized,f'fps:{int(fps)}',(10,55),cv2.FONT_HERSHEY_TRIPLEX,1,(0,160,28)) 
    cv2.imshow(nome, resized)
    k = cv2.waitKey(1)
    if k == 27:
     # ESC pressed
     subprocess.call('pactl unload-module module-loopback', shell=True)
     time.sleep(1)
     cv2.destroyAllWindows()
     break
cap.release()
cv2.destroyAllWindows()