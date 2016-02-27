import csv
import time
import datetime

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

from shareholder.models import Company, Operator
from utils.pdf import render_to_pdf


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
def captable_csv(request, company_id):
    """ returns csv with active shareholders """

    # perm check
    if not Operator.objects.filter(
        user=request.user, company__id=company_id
    ).exists():
        return HttpResponseForbidden()

    company = get_object_or_404(Company, id=company_id)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = u'attachment; filename='
    u'"{}_captable_{}.csv"'.format(
        time.strftime("%Y-%m-%d"), slugify(company.name))

    writer = csv.writer(response)
    writer.writerow([
        'shareholder number', 'last name', 'first name',
        'email', 'share count', 'share percent'])
    for shareholder in company.get_active_shareholders():
        writer.writerow([
            shareholder.number,
            shareholder.user.last_name,
            shareholder.user.first_name,
            shareholder.user.email,
            shareholder.share_count(),
            shareholder.share_percent()
        ])

    return response


@login_required
def captable_pdf(request, company_id):

    # perm check
    if not Operator.objects.filter(
        user=request.user, company__id=company_id
    ).exists():
        return HttpResponseForbidden()

    company = get_object_or_404(Company, id=company_id)

    response = render_to_pdf(
        'active_shareholder_captable.pdf.html',
        {
            'pagesize': 'A4',
            'company': company,
            'today': datetime.datetime.now().date,
            'total_capital': company.get_total_capital,
            'currency': 'CHF',
            'provisioned_capital': company.get_provisioned_capital(),
        }
    )

    # Create the HttpResponse object with the appropriate PDF header.
    # if not DEBUG
    if not settings.DEBUG:
        response['Content-Disposition'] = 'attachment; filename="'
        '{}_captable_{}.pdf"'.format(
            time.strftime("%Y-%m-%d"), company.name)

    return response
