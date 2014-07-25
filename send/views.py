from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
from send.models import *
import mandrill

def index(request):

    message_list = Message.objects.all()
    context = {'message_list':message_list}
    
    return render(request,'send/index.html',context)

def detail(request, message_id):

    message = get_object_or_404(Message,pk = message_id)
    return render(request, 'send/detail.html', {'message':message})

def confirmation(request,message_id):
    m = get_object_or_404(Message, pk = message_id)
    args = m.prepare_message_call()

    template_obj = TemplateForMessage.objects.filter(message = m)
    if len(template_obj) !=0 :
        template = template_obj[0]
        template_name,template_content = template.prepare_template_call()
    
    
    
    try:
        client = mandrill.Mandrill('bp2Lk5PopOmLPwMpZN0t4g')
        if len(template_obj) != 0:
            res = client.messages.send(message = args,
                                       template_name = template_name,
                                       template_content = template_content)
        else:
            res = client.messages.send(message = args)
            error = 'All Good'
            msg_id = MandrillInfo(message = m, _id = res[0]['_id'])
            msg_id.save()

    except mandrill.Error as e:
        res = 'No Results'
        error = e
        
    return render(request, 'send/confirmation.html',{'args':args,
                                                     'res':res,
                                                     'error' : error})
    
@csrf_exempt
def get_stats(request):
    #get posts from mandrill,
    #print em out here
    json_res = request.POST['mandrill_events']
    data = json.loads(json_res)
    message_id = data['msg']['_id']
    info_obj = MandrillInfo.objects.get(_id = message_id)
    info_obj.json = json_res
    info_obj.save()
    return render(request,'send/index.html')
    
    


def see_stats(request,message_id):
    message = get_object_or_404(Message,pk = message_id)
    info_obj = MandrillInfo.objects.filter(message = message)
    json_res = []
    for x in info_obj:
        json_res.append(x.json)

    return render(request,'send/see_stats.html',{'json':json_res})
    
