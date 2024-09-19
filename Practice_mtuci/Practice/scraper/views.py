from django.shortcuts import render
from django.views.decorators.http import require_POST
from .forms import ScrapeForm
from .pars import fetch_resume_data
from .mod import Resume
from .forms import ScrapeForm
from .deal import fetch_resumes_task

def scraper_home(request):
    form = ScrapeForm()
    return render(request, 'scraper/scrape.html', {'form': form})


def scrape_view(request):
    if request.method == 'POST':
        form = ScrapeForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            min_salary = form.cleaned_data['min_salary']


            resumes = fetch_resume_data(query=query, min_salary=min_salary)
            total_resumes = len(resumes)

            return render(request, 'scrape.html', {'form': form, 'resumes': resumes, 'total_resumes': total_resumes})
    else:
        form = ScrapeForm()

    return render(request, 'scrape.html', {'form': form})

