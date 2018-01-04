from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import DumpForm
import datetime
from django.utils.encoding import smart_str
from .models import Dump
import os

# Create your views here.

tcp_dump = False
filename = ''

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
                filename = dump_item.filename
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
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(str(file_id))
    response['X-Sendfile'] = smart_str('user_data/' + file_id)
    return response

def file_list(request):
    user_file_path = 'user_data'
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_list = os.listdir(dir_path + '/' + user_file_path)
    return render(request, 'dumper/table.html', {'file_list': file_list})

def server_state(request):
    global tcp_dump
    if request.method == "GET":
        return JsonResponse({"tcp_flag": tcp_dump, 'filename': filename})
    elif request.method == "POST":
        tcp_dump = False
        return JsonResponse({"tcp_flag": tcp_dump})

def dump_timeout(request):
    global tcp_dump
    tcp_dump = False
    return JsonResponse({"tcp_flag": tcp_dump})