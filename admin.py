from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User,TermsAndCondition,  PrivacyPolicy, AboutParagraph, Feedback,Transaction,Referral,Message, Account, Statement,Notification,Address,FAQ,FactAtAGlance,Objective,SocialNetwork

class AddressAdmin(admin.ModelAdmin):
    list_display = ('address_line_1','phone','email')

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('email','tel','message','can_be_contacted')

class FactAtAGlanceAdmin(admin.ModelAdmin):
    list_display = ('term','definition','fact_order')

class FAQAdmin(admin.ModelAdmin):
    list_display = ('keyword','question','faq_order')

# Register your models here.
admin.site.register(Feedback,FeedbackAdmin)
admin.site.register(Transaction)
admin.site.register(Referral)
admin.site.register(Message)
admin.site.register(Statement)
admin.site.register(Notification)
admin.site.register(Account)
admin.site.register(Address,AddressAdmin)
admin.site.register(FAQ,FAQAdmin)
admin.site.register(FactAtAGlance,FactAtAGlanceAdmin)
admin.site.register(Objective)
admin.site.register(SocialNetwork)
admin.site.register(AboutParagraph)
admin.site.register(PrivacyPolicy)
admin.site.register(TermsAndCondition)


# Re-register UserAdmin
admin.site.register(User, UserAdmin)