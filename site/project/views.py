import csv
import time
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import (
    HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
    )
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from django.contrib.flatpages.models import FlatPage

from zinnia.models.entry import Entry

from project.tasks import send_initial_password_mail
from services.instapage import InstapageSubmission as Instapage
from shareholder.models import Company, Operator
from utils.pdf import render_to_pdf


def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request, {})
    if Entry.published.all().exists():
        context['latest_blog_entry'] = Entry.published.all()[0]
    context['flatpages'] = FlatPage.objects.all()
    return HttpResponse(template.render(context))


@login_required
def start(request):
    template = loader.get_template('start.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


def instapage(request):
    """
    import user data from instapage
    instapage?submission=30122798
    create user and login
    """
    if not request.GET.get('submission'):
        return HttpResponseBadRequest('invalid data')

    # get and extract data
    sub = int(request.GET.get('submission'))
    instapage = Instapage()
    instapage.get(sub)
    name = instapage._get_value_by_field_name('Name').split(' ')
    email = instapage._get_value_by_field_name('Email')
    ip = instapage._get_value_by_field_name('ip')
    password = User.objects.make_random_password()

    if len(name) == 2:
        first_name, last_name = name
    elif len(name) == 1:
        first_name, last_name = '', name[0]
    else:
        first_name, last_name = name[0], ' '.join(name[1:])

    kwargs = dict(
        first_name=first_name, last_name=last_name, email=email,
        is_active=True, username=email[:29],
        )

    # save data
    user = User.objects.create(**kwargs)
    user.set_password(password)
    user.save()
    profile = user.userprofile
    profile.ip = ip
    profile.tnc_accepted = True
    profile.save()

    # authenticate user
    user = authenticate(username=email, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)

    # send password email
    send_initial_password_mail.delay(user=user, password=password)

    return redirect(reverse('start'))


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
        _(u'shareholder number'), _(u'last name'), _(u'first name'),
        _(u'email'), _(u'share count'), _(u'votes share percent'),
        _(u'language ISO'), _('language full')
    ])
    for shareholder in company.get_active_shareholders():
        row = [
            shareholder.number,
            shareholder.user.last_name,
            shareholder.user.first_name,
            shareholder.user.email,
            shareholder.share_count(),
            shareholder.share_percent() or '--',
            shareholder.user.userprofile.language,
            shareholder.user.userprofile.get_language_display()
        ]
        writer.writerow([unicode(s).encode("utf-8") for s in row])

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
