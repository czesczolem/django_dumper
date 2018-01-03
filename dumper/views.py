from django.shortcuts import render
from django.http import HttpResponse
import time
from .forms import DumpForm
import datetime

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
            return render(request, 'dumper/start_dumping.html', {'form': form ,'message' : 'Server is busy now. Please try again in few minutes'})
        else:
            form = DumpForm(request.POST)
            if form.is_valid():
                dump_item = form.save(commit=False)
                dump_item.date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dump_item.save()
            # if request.form['filename']:
            #     timestamp = str(int(time.time()))
            #     filename = request.form['filename'] + "_" + timestamp
            #     tcp_dump = True
            #     print(tcp_dump)
            #     return redirect(url_for('stop_dumping'))
            # else:
            #     return render_template('start_dumping.html', message='Filename is empty!')
            return HttpResponse('<p>ok</p>')
