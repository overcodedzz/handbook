---
title: "Django Channels"
categories:
  - Computer science
tags:
    - django
    - channels
    - websockets
---
## Introduction
     
Channels wraps Django’s native asynchronous view support, allowing Django projects to handle not only HTTP, but protocols that require long-running connections too - WebSockets, MQTT, chatbots, amateur radio, and more.

In this post, we will consider using Channels for WebSockets only.

Why WebSockets ? It is the modern protocol allowing bi-directional connection between server and clients. You want a real-time web application ? You better use WebSockets.
 
### Glossary:

- ASGI: asynchronous server specification
    - Channels in built on ASGI

Channels and ASGI split up incoming connections into two components: a scope and a series of events

- Scope: set of details about a signle incofming connection - such as the path a web request was made from, or the originating IP address of a WebSocket, or the user messaging a chatbot - and persists throughout the connection.
    - For HTTP, the scope just lasts a single request. For WS, it lasts for the lifetime of the socket (but changes if the socket closes and reconnects). For other protocols, it varies based on how the protocol's ASGI spec is written;
- Events: a series of events occur during the lifetime of this scope.

### Consumer

A consumer (consume events) is the basic unit of Channels code.

Tương tự với HTTP request, khi channel nhận được kết nối websocket, nó sẽ tìm routing configuration để lookup thằng consumer, rồi gọi hàm tương ứng trên consumer đó để handle event từ kết nối. Khác là kết nối đó là long-running. (Tất nhiên là cũng có thể tạo short-running, vd như cho HTTP)

```python
class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.username = "Anonymous"
        self.accept()
        self.send(text_data="[Welcome %s!]" % self.username)

    def receive(self, *, text_data):
        if text_data.startswith("/name"):
            self.username = text_data[5:].strip()
            self.send(text_data="[set your username to %s]" % self.username)
        else:
            self.send(text_data=self.username + ": " + text_data)

    def disconnect(self, message):
        pass
```

Mỗi protocol sẽ có các event khác nhau, mỗi loại sẽ tương ứng với một method.

Nếu viết kiểu kia thì Channels sẽ chạy các event handler ở synchronous thread. Tức là có thể thực hiện các blocking operations như là gọi Django ORM.

Nếu muốn viết async functions thì cần sử dụng fully async consumer. (xem trong docs)

```python
application = URLRouter([
    url(r"^chat/admin/$", AdminChatConsumer.as_asgi()),
    url(r"^chat/$", PublicChatConsumer.as_asgi(),
])
```

Consumers cũng khá giống với Django views. Bất kỳ user nào kết nối tới app sẽ được thêm vào Group, và sẽ nhận được message gửi bởi server. Khi mà user disconnect thì Channel sẽ bị xóa khỏi group và user không nhận được message nữa.

### Cross-Process Communication (Channel layer)

Mỗi socket hay kết nối đến application sẽ được handle thông qua *application instance*. Khi cần xây dựng một hệ thống phức tạp thì cần có các để liên lạc giữa các application instances. Điều này có thể giải quyết bằng cách poll database, tuy nhiên Channels đưa ra luôn khái niệm *channel layer*. (A low-level abstraction around a set of transports that allow you to send information between different processes).

Each application instance has a unique channel name, and can join groups, allowing both point-to-point and broadcast messaging.

```python
# In a consumer
self.channel_layer.send(
    "myproject.thumbnail_notifications",
    {
        "type": "thumbnail.generate",
        "id": 90902949,
    },
)
```

A channel layer is a kind of communication system. It allows multiple consumer instances to talk with each other, and with other parts of Django.

A channel layer provides the following abstractions:

- A channel is a mailbox where messages can be sent to. Each channel has a name. Anyone who has the name of a channel can send a message to channel.
- A group is a group of related channels. A group has a name. Anyone who has the name of a group can add/remove a channel to the group by name and send a message to all channels in the group. It is not possible to enumerate what channels are in a particular group.

Xem code chi tiết tại: [https://channels.readthedocs.io/en/stable/tutorial/part_2.html](https://channels.readthedocs.io/en/stable/tutorial/part_2.html)

### Django integration

```python
from django.urls import re_path
from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r"^front(end)/$", consumers.AsyncChatConsumer.as_asgi()),
        ])
    ),
})
```

## References:

- [https://channels.readthedocs.io/en/stable/](https://channels.readthedocs.io/en/stable/)