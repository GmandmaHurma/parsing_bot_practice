from celery import shared_task
from .pars import fetch_resume_data

@shared_task
def fetch_resumes_task(query, min_salary):
    all_resumes = fetch_resume_data(query=query, min_salary=min_salary)
    return all_resumes
