from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import DumpForm
import datetime
from django.utils.encoding import smart_str
from .models import Dump

# Create your views here.

tcp_dump = False
filename = None

def index(request):
    global tcp_dump, filename
    if request.method == 'GET':
        form = DumpForm()
        return render(request, 'dumper/start_dumping.html', {'form': form})
    else:
        if tcp_dump:
            form = DumpForm()
            return render(request, 'dumper/start_dumping.html', {'form': form,'message': 'Server is busy now. Please try again in few minutes'})
        else:
            form = DumpForm(request.POST)
            if form.is_valid():
                tcp_dump = True
                dump_item = form.save(commit=False)
                dump_item.date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return redirect('stop')

def stop(request):
    global tcp_dump
    if request.method == 'GET':
        return render(request, 'dumper/stop_dumping.html')
    else:
        tcp_dump = False
        return redirect('file_list')


def download_file(request, file_id):
    response = HttpResponse(
        content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('tests.py')
    response['X-Sendfile'] = smart_str('tests.py')
    return response

def file_list(request):
    all_files = Dump.objects.all()
    return render(request, 'dumper/table.html', {'all_files': all_files})
