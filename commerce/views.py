from django.shortcuts import render

# Create your views here.
def main(request):
    
    return render(request, 'index.html')

def auctions(request):
    
    return render(request, 'auctions.html')

def product(request, id):
    
    return render(request, 'product.html')

def comment(request, id):
    
    return render(request, 'product.html')

def new_product(request):
    
    return render(request, 'new.html')

def login(request):
    
    return render(request, 'registration/login.html')

