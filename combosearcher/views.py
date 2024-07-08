from django.http import HttpResponse
from combosearcher.models import Combos
from django.shortcuts import render
import time
from combosearcher.models import Combos


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def search(request):
    if request.method == "GET":
        return render(request,'combosearcher/search-combos-form.html')
    elif request.method == "POST":
        search_term = request.POST.get('searchTerm','')
        search_position = request.POST.get('searchPosition','')
        if search_position=='url':
            found_results = Combos.objects.filter(url__contains=search_term).values()
        else:
            found_results = Combos.objects.filter(username__contains=search_term).values()
        context = {'found_results': found_results,
                   'search_position': search_position,
                   'search_term': search_term,
                   'total_results':len(found_results)}
        return render(request,'combosearcher/search-results-page.html',context=context)


def upload_combos(request):
    start_time = time.time()
    with open('toupload.csv', 'r',encoding="utf8") as csvfile:
        lines = csvfile.readlines()

    chunks = [lines[x:x + 1000] for x in range(0, len(lines), 1000)]
    running_chunk = 0
    for chunk in chunks:
        running_chunk += 1
        print(f"Running Chunks: {running_chunk}/{len(chunks)}")
        to_bulk_create = []
        for line in chunk:
            try:
                line_split = line.split(',')
                url = line_split[0]
                username = line_split[1]
                password = line_split[2]
            except IndexError:
                continue
            to_bulk_create.append(Combos(url=url, username=username, password=password))
        objs = Combos.objects.bulk_create(to_bulk_create)
        print("--- %s seconds Lapsed---" % (time.time() - start_time))
    return HttpResponse("All data uploaded successfully")
