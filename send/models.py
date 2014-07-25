from django.db import models

# Create your models here.
class Recipient(models.Model):
    to_email = models.EmailField()
    to_name = models.CharField(max_length = 100, blank = True)
    to_type_choices = (('to','To'),
                       ('cc','cc'),
                       ('bcc','bcc'))
    to_type = models.CharField(max_length = 3,
                               choices = to_type_choices,
                               default = 'to')

    def __str__(self):
        if self.to_name:
            return self.to_email + ' : ' + self.to_name
        return self.to_email
    
    
    

    

class Message(models.Model):

    text = models.TextField(blank = True)
    html = models.TextField(blank = True)
    subject = models.CharField(max_length = 200)
    from_email = models.EmailField()
    from_name = models.CharField(max_length = 200, blank = True)
    track_opens = models.BooleanField(default = True)
    
    track_clicks = models.BooleanField(default = True)
    important = models.BooleanField(default = False)
    auto_text = models.BooleanField(default = True)
    auto_html = models.BooleanField(default = True)
    inline_css = models.BooleanField(default = False)
    url_strip_qs = models.BooleanField(default = False)
    preserve_recipients = models.BooleanField(default = False)
    view_content_link = models.BooleanField(default = False)
    bcc_address = models.EmailField(blank = True)
    tracking_domain = models.URLField(blank = True)
    signing_domain = models.URLField(blank = True)
    return_path_domain = models.URLField(blank = True)
    sub_account = models.CharField(blank = True, max_length = 200)
    google_analytics_campaign = models.CharField(blank = True, max_length = 200)


    def __iter__(self):

        for x in self._meta.get_all_field_names():
            if hasattr(self,x):
                yield(x, getattr(self,x))

    def __str__(self):
        return self.subject + ' - from ' + self.from_email

            
    def get_global_merge_vars(self):
        g_merge_objs = GlobalMerge.objects.filter(message = self)

        if len(g_merge_objs) == 0: return None

        inner_dic = {}
        for x in g_merge_objs:
            inner_dic[x.name] = x.content
        return [inner_dic]

    def get_recipients(self):
        send_obj = SendTo.objects.filter(message = self)
        rcpt_list = []
        for send in send_obj:
            rcpt = send.recipient
            dic  = {}
            dic['email'] = rcpt.to_email
            dic['name'] = rcpt.to_name
            dic['type'] = rcpt.to_type
            rcpt_list.append(dic)

        return rcpt_list

    def get_google_analytics_domains(self):

        gad_objs = GoogleAnalytics.objects.filter(message = self)
        if len(gad_objs) == 0: return None
        
        gads_list = []
        for x in gad_objs:
            gads_list.append(x.google_analytics_domain)

        return gads_list

    def get_headers(self):

        header_objs = Headers.objects.filter(message = self)

        if len(header_objs) == 0: return None

        headers = {}
        for x in header_objs:
            headers[x.header] = x.value

        return headers

    def get_images(self):

        image_objs = Images.objects.filter(message = self)
        if len(image_objs) == 0: return None

        image_list = []
        for x in image_objs:
            dic = {}
            dic['content'] = x.content
            dic['name'] = x.name
            dic['type'] = x._type
            image_list.append(dic)

        return image_list

    def get_merge_vars(self):

        merge_objs = Merge.objects.filter(message = self)
        #these are all merge objects that are specific to this message

        if len(merge_objs) == 0: return None

        merge_list = []
        rcpts = get_recipients()
        #these are the recipients of this message

        for rcpt in rcpts:
            rcpt_merge_objs = merge.filter(recipient__to_name = rcpt[name])
            #these are all the merges from this message that pertain to
            #this recipient
            if len(rcpt_merge_objs) == 0: continue

            dic = []
            dic['rcpt'] = rcpt['email']
            dic['vars'] = [{}]
            
            for merge_obj in rcpt_merge_objs:
                dic['vars'][0][merge_obj.name] = merge_obj.content

            merge_list.append(dic)

        return merge_list

    def get_metadata(self):

        meta_objs = Metadata.objects.filter(message = self)
        if len(meta_objs) == 0: return None

        dic = {}
        for x in meta_objs:
            dic[x.metadata_key] = x.metadata_value

        return dic

    def get_recipient_metadata(self):

        rcpt_meta_objs = RecipientMetadata.objects.filter(message = self)
        if len(rcpt_meta_objs) == 0: return None

        rcpts = get_recipients()
        rcpt_meta_list = []

        for rcpt in rcpts:
            meta_obj = rcpt_meta_objs.filter(recipient__to_name = rcpt[name])
            if len(meta_obj) == 0: continue
            dic = {}
            dic['rcpt'] = rcpt['email']
            dic['values'] = {}
            for x in meta_obj:
                dic['values'][metadata_key] = metadata_value

            rcpt_meta_list.append(dic)

        return rcpt_meta_list

    def get_tags(self):

        tag_objs = Tags.objects.filter(message = self)
        if len(tag_objs) == 0: return None

        tags = []
        for x in tag_objs:
            tags.append(x.tag)

        return tags

    def get_attachments(self):

        attach_objs = Attachments.objects.filter(message = self)
        if len(attach_objs) == 0: return None

        attach_list = []
        for x in attach_objs:
            dic = {}
            dic['content'] = x.content
            dic['name'] = x.name
            dic['type'] = x._type

            attach_list.append(dic)

        return attach_list


    def prepare_message_call(self):

        message = {}
        for key,val in self:
            if val:
                message[key] = val

        message['to'] = self.get_recipients()


        callables = {'attachments':self.get_attachments,
                     'globale_merge_vars':self.get_global_merge_vars,
                     'google_analytics domains':self.get_google_analytics_domains,
                     'headers':self.get_headers,
                     'images':self.get_images,
                     'merge_vars':self.get_merge_vars,
                     'metadata':self.get_metadata,
                     'recipient_metadata':self.get_recipient_metadata,
                     'tags':self.get_tags}

        for key in callables.keys():
            temp = callables[key]()
            if temp is not None:
                message[key] = temp


        return message
    
        
        
class SendTo(models.Model):
    message = models.ForeignKey(Message)
    recipient = models.ForeignKey(Recipient)

    

    
    
class Template(models.Model):
    template_name = models.CharField(max_length = 200)

    def prepare_template_call(self):

        content_obj = TemplateContent.objects.filter(template = self)
        template_content = []
        for x in content_obj:
            dic = {}
            dic['content'] = x.content
            dic['name'] = x.name
            template_content.append(dic)
            
        return self.template_name,template_content

class TemplateContent(models.Model):
    template = models.ForeignKey(Template)
    name = models.CharField(max_length = 200)
    content = models.CharField(max_length = 200)
    
class TemplateForMessage(models.Model):
    template = models.ForeignKey(Template)
    message = models.ForeignKey(Message)
    
class Merge(models.Model):
    message = models.ForeignKey(Message)
    recipient = models.ForeignKey(Recipient)
    name = models.CharField(max_length = 200)
    content = models.CharField(max_length = 200)
    

class GlobalMerge(models.Model):
    message = models.ForeignKey(Message)
    name = models.CharField(max_length = 200)
    content = models.CharField(max_length = 200)
    
class Tags(models.Model):
    message = models.ForeignKey(Message)
    tag = models.CharField(max_length = 200)

class GoogleAnalytics(models.Model):
    message = models.ForeignKey(Message)
    google_analytics_domain = models.CharField(max_length = 200)

class Metadata(models.Model):
    message = models.ForeignKey(Message)
    metadata_key = models.CharField(max_length = 200)
    metadata_value = models.CharField(max_length = 200)

class RecipientMetadata(models.Model):
    message = models.ForeignKey(Message)
    recipient = models.ForeignKey(Recipient)
    metadata_key = models.CharField(max_length = 200)
    metadata_value = models.CharField(max_length = 200)

class Attachments(models.Model):
    message = models.ForeignKey(Message)
    _type = models.CharField(max_length = 200)
    name = models.CharField(max_length = 200)
    content = models.CharField(max_length = 200)

class Images(models.Model):
    message = models.ForeignKey(Message)
    _type = models.CharField(max_length = 200)
    name = models.CharField(max_length = 200)
    content = models.CharField(max_length = 200)

class Headers(models.Model):
    message = models.ForeignKey(Message)
    header = models.CharField(max_length = 200)
    value = models.CharField(max_length = 200)

class MandrillInfo(models.Model):
    message = models.ForeignKey(Message)
    _id = models.CharField(max_length = 200)
    json = models.TextField(blank = True)

    def __str__(self):
        return self.message.subject + ' - from ' + self.message.from_email
    
