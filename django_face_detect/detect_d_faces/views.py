from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage



filename = None


# Create your views here.
def index(request):


    if request.method=='POST' and request.FILES['myfile']:

        myfile=request.FILES['myfile']
        fs=FileSystemStorage()
        filename=fs.save(myfile.name,myfile)
        print(fs.url(filename))

        print("@@file recieved")
        fs.delete(filename)

        print(fs.url(filename))

        




    return render(request,'index.html')
