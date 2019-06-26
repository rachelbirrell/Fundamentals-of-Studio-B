import numpy as np
import cv2
import time
import boto3
import os

#import the cascade for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
max = 3
filenum = max
i = 1
x = 1



def TakeSnapshotAndSave():
    # access the webcam (every webcam has a number, the default is 0)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    num = 0 
    while num<2:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # to detect faces in video
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

        x = 0
        y = 20
        text_color = (0,255,0)

        cv2.imwrite('opencv'+str(num)+'.jpeg',frame)
        num = num+1

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    CheckSimilarity()


def CheckSimilarity():
    global i
    b = max
    while i<max and i!=0:
         
        sourceFile='Customer'+str(i)+'.jpeg'
        image = sourceFile
        targetFile='opencv1.jpeg'
        client=boto3.client('rekognition')
           
        imageSource=open(sourceFile,'rb')
        imageTarget=open(targetFile,'rb')

        response=client.compare_faces(SimilarityThreshold=70,
                                        SourceImage={'Bytes': imageSource.read()},
                                        TargetImage={'Bytes': imageTarget.read()})
        


        for faceMatch in response['FaceMatches']:
            position = faceMatch['Face']['BoundingBox']
            similarity = str(faceMatch['Similarity'])
            #print ('Comparing with ' + image)
            #print('-->The face at ' +
                   #str(position['Left']) + ' ' +
                   #str(position['Top']) +
                   #' matches with ' + similarity + '% confidence')
            global x 
            x = i
            i = 0
            break

        else:
            #print ('Comparing with ' + image)
            #print('-->These faces do not match')
            i = i+1
    imageSource.close()
    imageTarget.close()   
    
    if i == 0:
        openfile()
    else: 
        print('Sorry, we cant find an account, would you like to create a new one?') 
        options()

def openfile():
    os.startfile("Customer"+str(x)+".txt")
    print('We found your account!')

def options():
    op = input("y/n> ")
    print ("You selected ", op)
    if op == 'y':
        newfile()
    elif op == 'n':
        print('okay, bye bye!')
    else: 
        print('Sorry, please pick y or n')
        options()

def newfile():
    filenum = max
    print('we are making you a new account')
    f = open("Customer" +str(filenum)+ ".txt", "w+")
    print('Please type your name')
    name = input(">")
    f.write("name: %s" %name)
    f.close()
    savephoto()


def addone():
    global max
    max = max + 1

def savephoto():
    global x 
    print('Smile! we are going to take a photo of you')
    input("Press Enter when you are ready")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    ret, frame = cap.read()
    cv2.imwrite('Customer'+str(i)+'.jpeg',frame)
    print('Thanks! account has been made')
    cap.release()
    cv2.destroyAllWindows()
    print('')
    addone()
    Startup()

def Startup(): 
    print('Welcome to Pi Cafe!')
    input("Press Enter to continue...")
    TakeSnapshotAndSave()

if __name__ == "__main__":
    Startup()


   