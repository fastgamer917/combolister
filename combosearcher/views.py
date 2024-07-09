import os

from django.http import HttpResponse
from django.shortcuts import render
import time
from combosearcher.models import Combos
import glob
from django.conf import settings


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def search(request):
    if request.method == "GET":
        return render(request,'combosearcher/search-combos-form.html')
    elif request.method == "POST":
        search_term = request.POST.get('searchTerm','')
        found_results = Combos.objects.filter(combo__contains=search_term).values()
        context = {'found_results': found_results,
                   'search_term': search_term,
                   'total_results':len(found_results)}
        return render(request,'combosearcher/search-results-page.html',context=context)


def upload_combos(request):
    if request.method == "GET":
        return render(request,"combosearcher/upload-combos.html")
    elif request.method == "POST":
        combo_source = request.POST.get('source','')
        files_list = glob.glob(settings.UPLOAD_DIR+'/*')
        start_time = time.time()
        for file in files_list:
            with open(file, 'r',encoding="utf8") as csvfile:
                lines = csvfile.readlines()
            chunks = [lines[x:x + 1000] for x in range(0, len(lines), 1000)]
            running_chunk = 0
            for chunk in chunks:
                running_chunk += 1
                print(f"Running Chunks: {running_chunk}/{len(chunks)}")
                to_bulk_create = []
                for line in chunk:
                    to_bulk_create.append(Combos(combo=line,source=combo_source))
                objs = Combos.objects.bulk_create(to_bulk_create)
                print("--- %s seconds Lapsed---" % (time.time() - start_time))
            os.remove(file)
        return HttpResponse("All data uploaded successfully. \n --- %s seconds Lapsed---" % (time.time() - start_time))
