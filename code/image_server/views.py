from django.http import HttpResponse
from django.shortcuts import render, redirect
from image_server.forms import ImageForm
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def imageView(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            img_obj = form.instance
            return render(request, 'imageform.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()
    return render(request, 'imageform.html', {'form': form})

def uploadSuccessView(request):
    return HttpResponse('Upload Success')