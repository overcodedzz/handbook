---
title: "Async with Django 3.1"
categories:
  - Computer science
tags:
    - django
    - async
    - asynchronous programming
toc: true
---

## Introduction

Từ phiên bản 3.1, Django đã hỗ trợ hoàn toàn tính năng async. 

- Có thể tạo async views
- Entirely backward-compatible: có thể dùng song song sync và async view.
- Hỗ trợ cả ASGI và WSGI nhưng mà dùng ASGI sẽ đảm bảo hiệu năng tốt nhất và đầy đủ tính năng nhất.

Ví dụ:

```python
def simple_middleware(get_response):
  async def middleware(request):
    # do something interesting
    response = await get_response(request)
    return response
  return middleware
```

Compare WSGI Server request flow vs ASGI Server request flow:

![/handbook/assets/images/async-with-django-3-1/Untitled.png](/handbook/assets/images/async-with-django-3-1/Untitled.png)

Synchronous programming is safe.

Asynchronous programming is hard. But it does worth.

The way asynchronous programming works in Python is called cooperative multitasking.

Bad example:

```python
async def main_view(request, book_id):
		book = Book.objects.get(id=book_id)

		return render(request, 'book.html', {'book': book})
```

→ Về bản chất thì nó sẽ block event loop, một điều không mong muốn chút nào với async programming. Có thể sẽ cho ra performance tệ hơn cả sync programming.

→ Tuy nhiên Django detect được và sẽ raise SynchronousOnlyException (có thể là do ORM - database accessing khi trong chạy trong async context) → yêu cầu sử dụng thread hoặc sync_to_async adapter. → Đây là tính năng guardrail của Django.

→ Chuyển từ silent failure → explicit failure. Dễ debug hơn

```python
async def main_view(request, book_id):
		# Note: get_async is not supported yet !
		# This is just a demo code for async ORM
		book = await Book.objects.get_async(id=book_id)

		return render(request, 'book.html', {'book': book})
```

→ Dùng keyword `await` để "nói với" event loop là nó có thể tiếp tục

## When to use Async view ?

- Sử dụng nhiều HTTP calls hoặc là long-polling, slow streaming calls trong view.
- 

## Where you can’t use async in Django yet ?

- ORM (coming soon)
- 

## How to write Async view ?

Mục tiêu là parallelize code. Chia nhỏ đoạn code thành các task độc lập với nhau và cho chạy bất đồng bộ.

Tuy nhiên, không phải lúc nào cũng nên parallelize code. Bởi việc chạy bất đồng bộ không đảm bảo 2 yếu tố: thứ tự thực thi và sự đảm bảo thực thi.

→ Khó để handle lỗi nếu xảy ra.

- Thêm `async` để biến function thành coroutine.
- Sử dụng `await` để give up control to the event loop.

VD: chạy bất đồng bộ 2 task.

```python
async def main_view_async(request):
		start_time = time.time()
		# task1 = asyncio.ensure_future(get_movies_async())
		# task2 = asyncio.ensure_future(get_stories_async())
		# await asyncio.wait([task1, task2])
		
		# or in 1 line
		asyncio.gather(get_movie_async(), get_stories_async())

		return HTTPResponse('OK')
```

### The `sync_to_async` decorator

```python
@sync_to_async
def create_user_account():
		User.objects.create(...) 

result = await create_user_account()

# --------- #

from asgiref.sync import sync_to_async

results = await sync_to_async(Blog.objects.get, thread_sensitive=True)(pk=123)

# --------- #

from asgiref.sync import sync_to_async

def _get_blog(pk):
    return Blog.objects.select_related('author').get(pk=pk)

get_blog = sync_to_async(_get_blog, thread_sensitive=True)
```

`thread_sensitive=True`(default): the sync function will run in the same thread as all other thread_sensitive functions. This will be the main thread, if the main thread is synchronous and you are using the async_to_sync() wrapper.

`thread_sensitive=False`: the sync function will run in a brand new thread which is then closed once the invocation completes.

Ví dụ sử dụng httpx để gọi concurrently:

```python
**async def async_home(request):
    """Display homepage by calling two services asynchronously (proper concurrency)"""
    context = {}
    try:
        async with httpx.AsyncClient() as client:
            response_p, response_r = await asyncio.gather(
                client.get(PROMO_SERVICE_URL), client.get(RECCO_SERVICE_URL)
            )

            if response_p.status_code == httpx.codes.OK:
                context["promo"] = response_p.json()
            if response_r.status_code == httpx.codes.OK:
                context["recco"] = response_r.json()
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}.")
    return render(request, "index.html", context)**
```

## How to debug async code ?

Set environment variable:

```bash
PYTHONASYNCIODEBUG=1
```

- Detect slow coroutines: 100ms
- Detect unawaited coroutines
- Slow I/O and thread-safety

 

> Make it work, then make it fast

Viết sync rồi test kỹ rồi mới chuyển sang async.

## Related Topics

[ASGI vs WSGI](https://www.notion.so/ASGI-vs-WSGI-5fbc2bf24ebb44fcbb67cc2983f74ac2)

[Coroutine](https://www.notion.so/Coroutine-cf7a3330e9064a8d861e32db112f679a)

### Asyncio

Threading in Python is inefficient because of the [GIL](https://wiki.python.org/moin/GlobalInterpreterLock) (Global Interpreter Lock) which means that multiple threads cannot be run in parallel as you would expect on a multi-processor system. Plus you have to rely on the interpreter to switch between threads, this adds to the inefficiency.

asyc/[asyncio](https://docs.python.org/3/library/asyncio.html#module-asyncio) allows concurrency within a single thread. This gives you, as the developer, much more fine grained control of the task switching and can give much better performance for concurrent I/O bound tasks than Python threading.

### Why asyncio is faster than multi-threading ?

It’s because asyncio is more robust with task scheduling and provides the user with full control of code execution. You can pause the code by using the await keyword and during the wait, you could run nothing or go ahead executing other code. As a result, resources are not locked down during the wait.

### Blocking Event Loop

Như chúng ta đã biết thì Event Loop sẽ liên tục tìm kiếm trong call stack những gì cần thực thi cho đến khi call stack rỗng nhưng Event Loop sẽ không dừng ở đó, nó sẽ bắt đầu đọc tiếp Event Queue để nhặt ra những gì được nhét vào đó và lôi ra để thực thi.

Thế nên là khi chạy một tác vụ lâu thì call stack sẽ không trống → block event loop.

Giải thích Event loop trong JS một cách trực quan: [https://dev.to/lydiahallie/javascript-visualized-event-loop-3dif](https://dev.to/lydiahallie/javascript-visualized-event-loop-3dif)

### Requests vs httpx ?

Với synchronous mode thì performance hai thằng khá tương đồng nhau.

Điểm mạnh của httpx có là: "Built in async capabilities while offering a request-like interface."

- Có giao diện dễ dùng (gần với requests) → tốt hơn aiohttp
- Thư viện khá mới, hỗ trợ HTTP/2

## Resources:

- Official documentation: [https://docs.djangoproject.com/en/3.2/topics/async/](https://docs.djangoproject.com/en/3.2/topics/async/)
- [https://deepsource.io/blog/django-async-support/](https://deepsource.io/blog/django-async-support/)
- Một seminar khá chi tiết về async view trong DjangoCon 2020: [https://www.youtube.com/watch?v=19Uh_PA_8Rc](https://www.youtube.com/watch?v=19Uh_PA_8Rc)
- Compare the performance between sync and async: [https://www.youtube.com/watch?v=YneIutRhmgo](https://www.youtube.com/watch?v=YneIutRhmgo)
- Ví dụ sử dụng httpx gọi API concurrently với async view: [https://dev.to/arocks/better-examples-of-django-async-views-295d](https://dev.to/arocks/better-examples-of-django-async-views-295d)