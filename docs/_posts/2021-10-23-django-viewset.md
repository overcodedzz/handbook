---
title: "Django Viewset"
categories:
  - Computer science
tags:
    - django
    - api
    - drf
toc: true
---

# Django Viewset

Modified: October 23, 2021 4:36 PM

## Introduction

Tại sao phải dùng viewset ?

- Để code được clean, tránh việc reinvent the wheel.

### APIView

Trước khi tìm hiểu về Viewset thì mình sẽ nói qua về APIView.

Hỗ trợ override các method: get, post, put, patch, delete,...

Hỗ trợ các API policy như: authentication_classes, throttle_classes, permission_classes,... Thường thì thiết lập các static API policy kể trên là khá đủ trong nhiều trường hợp rồi, tuy nhiên nếu muốn tuỳ chỉnh nhiều hơn nữa thì có thể thiết lập dynamic policy bằng cách override các hàm get_authenticators(), get_permissions(),...

### GenericAPIView

APIView là lớp đơn giản nhất, có khả năng tuỳ chỉnh dễ dàng. Tuy nhiên vì là xử lý ở mức low-level như vậy thì sẽ khiến code dài, nhiều pattern bị lặp lại. Để xử lý vấn đề này thì DRF sinh ra thằng GenericAPIView nhằm trừu tượng hoá các pattern đó.

→ GenericAPIView chứa một số attribute và method như: get_serializer_class(), pagination_class, filter_backends, get_queryset(), get_object(),...

Ngoài ra, thay vì tác động vào các hàm HTTP method handlers thì generic views cung cấp các mixins được implement sẵn các hàm abstract như: list, retrieve, create,...

**GenericViews**: một số view extend từ GenericAPIView và các mixins

- E.g: ListCreateAPIView, RetrieveUpdateDestroyAPIView

Đọc thêm:

- [https://github.com/MattBroach/DjangoRestMultipleModels](https://github.com/MattBroach/DjangoRestMultipleModels)

## Viewsets

DRF cho phép gộp một số view liên quan đến nhau thành 1 class duy nhất gọi là viewset. Ở một số framework khác, bạn cũng sẽ thấy cách implementation tương tự nhưng với tên gọi khác như Resources hay Controllers.

ViewSet cung cấp một số action như list và create thay vì các method handlers như get hay post. Việc binding các action với các method handler chỉ xảy ra khi sử dụng .as_view().

Và thay vì phải khai báo trực tiếp các views trong viewset ở urlconf thì mình sẽ đăng ký viewset với router class.

Ví dụ:

```python
class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
```

Chúng ta có thể bind viewset này thành 2 views khác nhau như sau:

```python
user_list = UserViewSet.as_view({'get': 'list'})
user_detail = UserViewSet.as_view({'get': 'retrieve'})
```

Rồi thêm 2 view vào urlconfig như thêm APIView.

Nhưng mà bình thường thì sẽ không cần làm thế, mà mình sẽ đi đăng ký viewset với router, để nó tự sinh urlconfig cho mình

```python
from myapp.views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
urlpatterns = router.urls
```

Các action trong một viewset:

```python
class UserViewSet(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    def list(self, request)
    def create(self, request)
    def retrieve(self, request, pk=None)
    def update(self, request, pk=None)
    def partial_update(self, request, pk=None)
    def destroy(self, request, pk=None)
```

Customize viewset:

```python
def get_permissions(self):
    """
    Instantiates and returns the list of permissions that this view requires.
    """
    if self.action == 'list':
        permission_classes = [IsAuthenticated]
    else:
        permission_classes = [IsAdmin]
    return [permission() for permission in permission_classes]
```

### ModelViewSet

Viewset dành cho một model cụ thể

```python
class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
```

Thường thì mình sẽ đi customize hàm get_queryset để filter theo query params.

- Raise ValidationError để trả về 400
- Raise NotFound để trả về 404

## Conclusion

Có thể thấy là viewset tiến một bước trong việc trừu tượng hoá so với genericview.

Mà trừu tượng hoá hơn thì sẽ có những trade-off nhất định như là tuỳ chỉnh sẽ không được thoải mái lắm, phức tạp hơn trong việc binding method với action. Cơ mà cũng không thể phủ nhận tính hữu dụng của viewset khi giúp code clean hơn, đúng chuẩn hơn.

Cách tốt nhất để hiểu viewset là thực hành, mò thẳng vào trong source code của DRF và đọc.

## References:

- [https://www.django-rest-framework.org/api-guide/viewsets/](https://www.django-rest-framework.org/api-guide/viewsets/)