from django.shortcuts import render, redirect

# Create your views here.
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Document
from .forms import DocumentForm


def list_view(request):
    # Handle file
    message = 'Upload as many files as you want!'
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            print("we are here")
            # Redirect to the document list after POST
            # return HttpResponseRedirect(reverse('myapp.views.list'))
            return redirect('uploader:list')
        else:
            message = 'The form is not valid. Fix the following error:'

    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    print("documents", documents)

    context = {'documents': documents, 'form': form, 'message': message}

    # Render list page with the documents and the form
    return render(request, "load_file.html", context)


from django.views.generic.edit import FormView
from .forms import FileFieldForm
from django.urls import reverse_lazy
from django.middleware.csrf import CsrfViewMiddleware

class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = 'load_file_multiple.html'  # Replace with your template.
    success_url = reverse_lazy('uploader:multiple_load')  # Replace with your URL or reverse().
    form = form_class

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        print("files", files)
        if form.is_valid():
            print("form is valid")
            for f in files:
                print('f', f)
                newdoc = Document(docfile=f)
                newdoc.save()


        documents = Document.objects.all()
        print("documents", documents)
        context = {
            'documents': documents,
            'form': form,
        }
        # return self.form_valid(form)
        return render(request, "load_file_multiple.html", context)


from django.core.files.uploadhandler import MemoryFileUploadHandler
from  django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import sys
from .forms import DirectoryFieldForm

class CustomMemoryFileUploadHandler(MemoryFileUploadHandler):
    def new_file(self, *args, **kwargs):
        args = (args[0], args[1].replace('/', '-').replace('\\', '-')) + args[2:]
        super(CustomMemoryFileUploadHandler, self).new_file(*args, **kwargs)


class CustomTemporaryFileUploadHandler(TemporaryFileUploadHandler):
    def new_file(self, *args, **kwargs):
        args = (args[0], args[1].replace('/', '-').replace('\\', '-')) + args[2:]
        super(CustomTemporaryFileUploadHandler, self).new_file(*args, **kwargs)


@csrf_exempt
def my_view(request):
    # replace upload handlers. This depends on FILE_UPLOAD_HANDLERS setting. Below code handles the default in Django 1.10
    request.upload_handlers = [CustomMemoryFileUploadHandler(request), CustomTemporaryFileUploadHandler(request)]
    return _my_view(request)


@csrf_protect
def _my_view(request):
    # if the path of the uploaded file was "test/abc.jpg", here it will be "test-abc.jpg"
    blah = request.FILES[0].name


def directory_load_view(request):
    """Function responsible for loading whole directory of files"""
    # Handle file
    message = 'Upload whole directory which you want!'
    if request.method == 'POST':
        form = DirectoryFieldForm(request.POST, request.FILES)
        print("form error", form.errors)
        files = request.FILES.getlist('directory')
        # print("files", files)
        print("Name of file is ", sys.stderr)
        form.non_field_errors()
        field_errors = [(field.label, field.errors) for field in form]
        print("field_errors, ", field_errors)
        print("form.data", form.data)
        print("form.data", form.files)
        if form.is_valid():
            print("form is valid")
            Document.objects.all().delete()
            # newdoc = Document(docfile=request.FILES['docfile'])
            # newdoc.save()
            # print("we are here")
            for f in files:
                print('f', f)
                newdoc = Document(docfile=f)
                newdoc.save()

            return redirect('uploader:directory_load')
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = DirectoryFieldForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    print("documents", documents)

    context = {'documents': documents, 'form': form, 'message': message}

    # Render list page with the documents and the form
    return render(request, "load_directory2.html", context)
