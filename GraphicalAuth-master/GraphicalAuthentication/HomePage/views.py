from genericpath import exists
from django.core.files import images
from django.http import JsonResponse
from django.shortcuts import render
from .models import Details
import cv2
from PIL import Image
import blowfish, numpy as np, distance, hashlib, string, random


# Create your views here.


def home(request):
    return render(request, 'homepage.html')

def authWelcome(request):
    return render(request, 'graphinfo.html')

def failInformation(request):
    return render(request, 'failauth.html')


def signup(request):
    if request.method == "POST":
        Username=request.POST['Username']
        email = request.POST['email']
        phone = request.POST['phone']
        img_index = request.POST['img_index']
        images = request.session['images']
        try:
            userObj = Details(img_index=img_index, Username=Username, email=email, phone=phone, images=images)
            userObj.save()
            return render(request, 'homepage.html')
        except:
            pass
        # print("data entered")

    return render(request, 'signup.html', {'h':'hello'})


def dum(request):
    pixelString = request.POST.get('pixelString', None)
    passwordKey = request.POST.get('passwordKey', None)
    phone = request.POST.get('phone', None)
    imagePath = request.POST.get('imagePath', None).replace('http://127.0.0.1:8000', '.')
    try:
        encry = steganographyEncrypt(phone, imagePath, pixelString, passwordKey)
        # encry2 = encry.split('./')
        images = encry
        print(images)
        request.session['images'] = images
    except:
        pass
    
    # stegFile = Image.open(stegFileName)
    #userObj = Details(img_index=0, Username=username, email=email, phone=phone, imageBytes=stegFileBinary)
    #userObj.save()

    return JsonResponse({})
    

def steganographyEncrypt(username, imagePath, pixelString, passwordKey):
    d = {}
    c = {}

    for i in range(255):
        d[chr(i)] = i
        c[i] = chr(i)

    x = cv2.imread(imagePath)
    i = x.shape[0]
    j = x.shape[1]
    # print(i, j)

    # blowfishKey = bytes(pixelString[:4], 'utf-8')
    # temPlainText = bytes(pixelString, 'utf-8')
    key = passwordKey
    text = pixelString
    
    # cipher = blowfish.Cipher(key=blowfishKey)
    # cipherText = b"".join(cipher.encrypt_ecb_cts(temPlainText))
    # cipherText = str(cipherText)


    kl = 0
    z = 0  
    n = 0  
    m = 0  

    l = len(text)

    for i in range(l):
        x[n, m, z] = d[text[i]] ^ d[key[kl]]
        n = n + 1
        m = m + 1
        m = (m + 1) % 3  
        kl = (kl + 1) % len(key)
    
    finalCombo = ''.join(random.choices(string.ascii_uppercase+string.digits, k = 20))
    hashDum = hashlib.sha256(finalCombo.encode()).hexdigest()
    newImagePath = 'static/images_db/'+hashDum+'.png'
    cv2.imwrite(newImagePath, x)
    print(newImagePath)
    return newImagePath

    
def signin(request):
    if request.method == "get":
        stud = Details.objects.all()
        print("Myoutput",stud)
        return render(request, 'signin.html',{'stu': stud})
    return render(request, 'signin.html')
    

def getImage(request): 
    print(request.GET.get("username", None))
    receivedUsername = request.GET.get("username", None)
    try:
        imagePath = Details.objects.all().filter(Username=receivedUsername).values()[0]["images"]
    except: imagePath = 0
    return JsonResponse({'image': imagePath})


def checkAuth(request):
    pixelString = request.POST.get('pixelString', None)
    passwordKey = request.POST.get('passwordKey', None)
    phone = request.POST.get('phone', None)
    username = request.POST.get('username', None)
    imagePath = request.POST.get('imagePath', None).replace('http://127.0.0.1:8000', '.')
    
    key = passwordKey
    text = pixelString

    d = {}
    c = {}

    for i in range(255):
        d[chr(i)] = i
        c[i] = chr(i)
    
    l = len(text)

    x=cv2.imread(imagePath)

    kl = 0
    tln = len(text)
    z = 0  
    n = 0  
    m = 0  

    decrypt = ""
    for i in range(l):
        decrypt += c[x[n, m, z] ^ d[key[kl]]]
        n = n + 1
        m = m + 1
        m = (m + 1) % 3
        kl = (kl + 1) % len(key)
    # print("Encrypted text was : ", decrypt)

    print(distance.nlevenshtein(decrypt, pixelString, method=1))
    if distance.nlevenshtein(decrypt, pixelString, method=1) < 0.5:
        finalCombo = decrypt+username+key
        hashDum = hashlib.sha256(finalCombo.encode()).hexdigest()
        isEncrypted = {'encrypt': True, 'token': hashDum}
    else: 
        isEncrypted = {'encrypt': False}
    return JsonResponse(isEncrypted)


def checkUser(request):
    username = request.GET.get('username', None)
    querySet = Details.objects.all().filter(Username=username).count()
    if querySet:
        exists = True
    else: exists = False
    return JsonResponse({'exists': exists})





    