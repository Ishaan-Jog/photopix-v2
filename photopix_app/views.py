from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from photopix_app.forms import ImageUploadForm
from photopix_app.models import UploadedImage
from django.contrib import messages


def index(request):
    return render(request, "index.html")

def aboutus(request):
    return render(request, "aboutus.html")

def contactus(request):
    return render(request, "contactus.html")

@login_required(login_url='/login/')
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Image uploaded successfully!")
            return redirect('upload_image')
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})

def ourclicks(request):
    clean_missing_images()
    images = UploadedImage.objects.all()
    return render(request, 'ourclicks.html', {'images': images})

def login_(request):
    if request.user.is_authenticated:
        return redirect('upload_image')

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)
            return redirect('upload_image')
        else:
            messages.error(request, "Invalid credentials! Try again.")
            return redirect('login')
    return render(request, 'login.html')

def logout_(request):
    logout(request)
    return redirect('/')

def clean_missing_images():
    for img in UploadedImage.objects.all():
        if not default_storage.exists(img.image.name):  # Check if file exists
            img.delete()  # Delete record if file is missing
