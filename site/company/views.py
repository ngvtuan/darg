from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from shareholder.models import Company

@login_required
def company(request, company_id):
    template = loader.get_template('company.html')
    company = get_object_or_404(Company, id=int(company_id))
    context = RequestContext(request, {'company': company})
    return HttpResponse(template.render(context))
