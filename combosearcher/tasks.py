from celery import shared_task
from .search_controller import search_folder_files_v2
import time
from .models import SearchResult,SearchProgress
from datetime import datetime

@shared_task()
def search_task(keyword:str, task_progress_obj_pk):
    try:
        task_progress_obj = SearchProgress.objects.get(pk=task_progress_obj_pk)
        start_time = time.time()
        total_found = search_folder_files_v2(keyword)
        exec_time = time.time() - start_time
        # Below Update is not working.. showing no update attribute for object. fix it later
        # task_progress_obj.update(
        #     total_found=len(total_found),
        #     run_time=exec_time,
        #     search_status = "Completed",
        #     search_completed_time = datetime.now()
        # )
        task_progress_obj.total_found=len(total_found)
        task_progress_obj.run_time=exec_time
        task_progress_obj.search_status = "Completed"
        task_progress_obj.search_completed_time = datetime.now()
        task_progress_obj.save()
        for result in total_found:
            SearchResult.objects.create(
                search_id = task_progress_obj,
                found_string = result.get('combo'),
                found_in_file = result.get('source'),
            )
    except Exception as e:
        print(e)
        task_progress_obj.search_status = e
        task_progress_obj.save()


