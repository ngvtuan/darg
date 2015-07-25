import csv
import time

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

from shareholder.models import Company


def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


@login_required
def start(request):
    template = loader.get_template('start.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


@login_required
def captable_csv(requesti, company_id):
    """ returns csv with active shareholders """

    company = get_object_or_404(Company, id=company_id)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}_captable_{}.csv"'.format(
        time.strftime("%Y-%m-%d"), company.name)

    writer = csv.writer(response)
    writer.writerow(['shareholder number', 'last name', 'first name', 'email', 'share count', 'share percent'])
    for shareholder in company.get_active_shareholders():
        writer.writerow([
            shareholder.number,
            shareholder.user.last_name,
            shareholder.user.first_name,
            shareholder.user.email,
            shareholder.share_count(),
            "{:.2f}".format(shareholder.share_percent())
        ])

    return response


@login_required
def captable_pdf(request, company_id):

    response = ""

    return response
