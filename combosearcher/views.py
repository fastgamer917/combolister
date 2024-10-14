# TODO: Cleanup useless code from other branches

import os
import time
from django.http import HttpResponse
from django.shortcuts import render, redirect
import time
from combosearcher.models import Combos
import glob
from django.conf import settings
from .search_controller import search_folder_files
from django.contrib.auth.decorators import login_required
from .tasks import search_task
from .models import SearchProgress, SearchResult
from datetime import datetime


def index(request):
    #TODO; Add buttons that redirect to different pages
    return HttpResponse("Hello, world. You're at the polls index.")

@login_required()
def submit_search(request):
    if request.method == 'GET':
        return render(request,'combosearcher/submit-search.html')
    if request.method == "POST":
        search_term = request.POST.get('searchTerm',None)
        if not search_term:
            return render(request, 'combosearcher/submit-search.html')
        requested_user = request.user
        #create a search progress obj to update it later
        search_progress_obj = SearchProgress.objects.create(
            submitted_user=requested_user,
            search_term=search_term,
            submitted_time=datetime.now(),
            search_status="In Progress",
        )
        search_task.delay(search_term,search_progress_obj.pk)
        return redirect('search_progress')


def search_progress(request):
    all_searches_progress = SearchProgress.objects.all()
    return render(request,'combosearcher/search_progress.html',context={"all_searches_progress":all_searches_progress})

def search_results(request):
    search_progress_id = request.GET.get('search_progress_id', None)
    search_progress_obj = SearchProgress.objects.get(pk=search_progress_id)
    search_results = SearchResult.objects.filter(search_id=search_progress_id)
    context = {'found_results': search_results,
               'search_term': search_progress_obj.search_term,
               'exec_time': search_progress_obj.run_time,
               'total_results': search_progress_obj.total_found}

    return render(request,'combosearcher/search-results-page_v2.html',context=context)

def searchv2(request):
    """
    This search implements searching the keyword in all the files of folder instead of any db.
    #TODO: Change combo folder location appropriately.
    """
    if request.method == "GET":
        return render(request,'combosearcher/search-combos-form.html')
    elif request.method == "POST":
        start_time = time.time()
        folder_path_for_search = "<Combo folder location full path>"
        search_term = request.POST.get('searchTerm','')
        found_results = search_folder_files(folder_path_for_search, search_term)
        context = {'found_results': found_results,
                   'search_term': search_term,
                   'exec_time': time.time() - start_time,
                   'total_results':len(found_results)}
        return render(request,'combosearcher/search-results-page.html',context=context)


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
