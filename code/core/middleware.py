# from django.utils.timezone import now

# from models import DyadUser

# class SetLastVisitMiddleware(object):



#     def process_response(self, request, response):
#         # assert hasattr(request, 'username')
#         if request.user.is_authenticated():
#             DyadUser.objects.filter(pk=request.user.pk).update(last_vist=now())
#         return response 