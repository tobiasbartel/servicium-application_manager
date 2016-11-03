from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from models import *
from pprint import pprint
import pydotplus
import re
from servicecatalog import graphgenerator
from instance_manager.models import Instance
from contact_manager.views import contact_box


from main.settings import TEMPLATE_NAME

def index(request):
    return HttpResponseRedirect('/module/')


def module_overview(request):
    return render_to_response('%s/module_overview.tpl.html' % TEMPLATE_NAME, {'request': request,})


def module_detail(request, module_name):
    my_module = Module.objects.get(slug=module_name)
    my_contacts = ModuleContact.objects.all().filter(parent=my_module)
    my_instances = Instance.objects.all().filter(module=my_module)

    my_payment_methods = set([])
    for connection in ModuleWritesToModule.objects.all().filter(from_module=my_module):
        for pm in connection.payment_methods.iterator():
            my_payment_methods.add(pm)

    my_contact_boxes = contact_box(request, my_contacts)
    my_payment_methods = sorted(my_payment_methods, key=lambda k: k.name)

    return render_to_response('%s/module.tpl.html' % TEMPLATE_NAME, {'request': request, 'my_module': my_module, 'my_instances':my_instances, 'my_contact_boxes':my_contact_boxes, 'my_payment_methods': my_payment_methods, })


def module_graph(request, my_module_name, my_payment_method_name=None, raw=False):
    if my_payment_method_name is not None:
        my_graph = graphgenerator.module(my_module_name, my_payment_method_name.split(","))
    else:
        my_graph = graphgenerator.module(my_module_name)

    if raw:
         return my_graph
    else:
        response = HttpResponse(my_graph, content_type='image/svg+xml')
        response['Content-Length'] = len(my_graph)
        return response

def all_module_graph(request, raw=False):
    my_graph = graphgenerator.module(None)

    if raw:
         return my_graph
    else:
        response = HttpResponse(my_graph, content_type='image/svg+xml')
        response['Content-Length'] = len(my_graph)
        return response

def license(request, ):
    return render_to_response('%s/license.tpl.html' % TEMPLATE_NAME, {'request': request, })
