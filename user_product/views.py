from rest_framework.response import Response
from .serializers import ProductReviewSerializer
from rest_framework.views import APIView
from superadmin.custompermissions import CustomEndUserPermission
from superadmin.tokengeneratedecode import get_decoded_payload


class AddProductReview(APIView):

    permission_classes = [CustomEndUserPermission]

    def post(self, request, *args, **kwargs):
        payload = get_decoded_payload(request)
        product_review_serializer = ProductReviewSerializer(data=request.data)
        if product_review_serializer.is_valid(raise_exception=True):
            review = product_review_serializer.save()
            print(review)
            return Response({"result":"Review added"})
        