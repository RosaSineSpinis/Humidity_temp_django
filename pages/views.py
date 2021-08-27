from django.shortcuts import render

# Create your views here.


def home_view(request, *args, **kwargs):
    # print(args, kwargs)
    # print(request.user)
    # return HttpResponse("<h1>Hello World</h1>")
    context = {

    }
    return render(request, "home.html", context)


def about_program_view(request, *args, **kwargs):
    context = {}
    return render(request, "about_program.html", context)


