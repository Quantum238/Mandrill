from django.contrib import admin
from send.models import *

# Register your models here.
admin.site.register(Message)
admin.site.register(Recipient)
admin.site.register(Template)
admin.site.register(TemplateContent)
admin.site.register(Merge)
admin.site.register(GlobalMerge)
admin.site.register(Tags)
admin.site.register(GoogleAnalytics)
admin.site.register(Metadata)
admin.site.register(RecipientMetadata)
admin.site.register(Attachments)
admin.site.register(Images)
admin.site.register(Headers)
admin.site.register(SendTo)
admin.site.register(MandrillInfo)
admin.site.register(TemplateForMessage)




