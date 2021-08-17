from django.shortcuts import render

# Create your views here.

def getGraph(request):
    """
    plot graphs with matlibplot and send a picture
    :param request: POST or GET??
    :return: jpg?
    """

    context = {}

    # Render list page with the documents and the form
    return render(request, "matlibplot.html", context)
