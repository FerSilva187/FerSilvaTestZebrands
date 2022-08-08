from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

class BaseViewSet(viewsets.GenericViewSet):
    def ok(self, **args):
        args["ok"] = True
        return Response(args)

    def error(self, status=None, **args):
        args["ok"] = False
        return Response(args, status=status)


        

PREVENT_DELETE_MIXINS = [
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    BaseViewSet,
]