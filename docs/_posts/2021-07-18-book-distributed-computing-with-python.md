---
title: "[Book] Distributed Computing with Python"
categories:
  - Computer science
tags:
    - book
    - python
toc: true
---

# Distributed Computing with Python
Modified: July 18, 2021 4:19 PM

## Introduction

Đây là note tóm tắt các ý chính trong cuốn Distributed Computing with Python (PacktPub 2016)

Trên tổng cộng 8 chapter, các chapter được tóm tắt bao gồm: 1-4, 7 và 8. Các chapter còn lại nói về cách setup distributed Python application trên cloud và HPC.

Nội dung chính:

- Multithreading programming vs Async programming.
- Giới thiệu qua về coroutine - thành phần không thể thiếu trong async programming.
- Working with multithreading
- Working with multiprocessing
- Giới thiệu qua về celery
- Test and debug distributed application

Để đơn giản hoá thì sẽ assume phiên bản của Python là 3.5+ với các feature chính:

- couroutine via yield expressions.
- library asyncio
- true coroutine types vai async def and await

## Multithread

- Python đã hỗ trợ thread từ lâu, sử dụng thư viện threading để làm việc với thread.
- Python threads là OS-native threads.
- Vấn đề lớn nhất đối với threading là race condition.
- Queue trong Python là thread-safe vì nó sử dụng lock để đồng bộ.
    - Hàm join() sẽ đợi cho đến khi tất cả kết quả được lấy về (chính xác thì là khi hàm get() được gọi rồi đến task_done() được gọi).

Sử dụng threads với Python chỉ hiệu quả với I/O-bound tasks, còn với CPU-bound thì có khi còn cho kết quả tệ hơn. Điều này là vì standard Python interpreter sử dụng Global Interpreter Lock (GIL) → chỉ cho phép một thread có thể active tại một thời điểm.

### GIL

Global Interpreter Lock (GIL): được sử dụng chính để đồng bộ reference counting.

- Không phải interpreter nào cũng dùng GIL, ví dụ là Jython.
- Một cách khác để tránh GIL là sử dụng những thư viện đã được compile để chạy thread song song. VD: numpy (dựa vào thư viện BLAS).
- Ngoài ra thì cũng nên tìm hiểu về Cython, a Python-like language to create C modules. Cython can allows programmers to easily multithread their code.

![/handbook/assets/images/book-distributed-computing-with-python/Untitled.png](/handbook/assets/images/book-distributed-computing-with-python/Untitled.png)

Example: working with threading

```python
from threading import Thread
from queue import Queue
import urllib.request

URL = 'http://finance.yahoo.com/d/quotes.csv?s={}=X&f=p'

def get_rate(pair, outq, url_tmplt=URL):
    with urllib.request.urlopen(url_tmplt.format(pair)) as res:
        body = res.read()
    outq.put((pair, float(body.strip())))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('pairs', type=str, nargs='+')
    args = parser.parse_args()
		
		outputq = Queue()

		for pair in args.pairs:
		    t = Thread(target=get_rate,
		               kwargs={'pair': pair,
		                       'outq': outputq})
		    t.daemon = True
		    t.start()

		for _ in args.pairs:
		    pair, rate = outputq.get()
		    print(pair, rate)
		    outputq.task_done()

		outputq.join()
```

## Multiple processes

- Với CPU-bound task trong Python thì nên dùng multiprocessing.
- Điểm trừ là overhead về startup time và memory usage khi dùng nhiều process cùng lúc.
- Điểm cộng là nó sử dụng share-nothing architecture → dể chuyển đổi từ single-machine sang distributed application, dễ hiểu cách access data hơn.
- Tìm hiểu thêm: multiprocessing hỗ trợ việc chạy process ở các máy khác nhau, kết nối thông qua socket server, quản lý bởi class Manager.
- Vấn đề cần giải quyết: chia sẻ thông tin giữa các process.

Có 2 modules có thể sử dụng là multiprocessing và concurrent.futures (built on top of multiprocessing and the threading module and provides a powerful high-level interface to them).

### Module: `concurrent.futures`

Example: 

```python
import concurrent.futures as cf

with cf.ProcessPoolExecutor(max_workers=args.n) as pool:
        results = pool.map(fib, [args.number] * args.n)
```

Cả 2 class ProcessPoolExecutor và ThreadPoolExecutor đều có chung API:

- submit(f, *args, **kwargs): this is used to schedule an asynchronous call to f(*args, **kwargs) and return a Future instance as a result placeholder.
- map(f, *arglist, timeout=None, chunksize=1): this is the equivalent to the built-in map(f, *arglist) method. It returns a list of Future objects rather than a list of actual results, as map would do.
- shutdown(wait=True) is used to free the resources used by the Executor object as soon as all currently scheduled functions are done.

Executor objects can also be used as context managers (as in the above example). We would get results rather than Future instances once the context manager exits.

Khi sử dụng multiprocessing thì vấn đề nảy sinh ra là làm thế nào để share thông tin giữa các worker. Thư viện multiprocessing có hỗ trợ Queue (modeled after queue.Queue) with the additional twist that items stored in the multiprocessing queue need to be pickable.

## Distributed Applications with Celery

![/handbook/assets/images/book-distributed-computing-with-python/Untitled%201.png](/handbook/assets/images/book-distributed-computing-with-python/Untitled%201.png)

- Celery is distributed task queue application.
    - Distributed task queue: has a form of master-worker architecture with a middleware layer that uses a set of queues for work requests (the task queues) and a queues, or a storage area, to hold the results (the result backend).
    - The master process (also called a client or producer) puts work requests (tasks) into one of the task queues and fetches results from the result backend. Worker processes, on the other hand, subscribe to some or all of the task queues and put results into the result backend.
- Very easy to scale and prioritize
- Celery task support timeout and retry.
- Sử dụng group để run the individual independent tasks as a unit of work. Tuy nhiên cũng nên tránh vì nó tạo ra overhead do celery pooling.
- Có thể chạy multithreads với Celery thay vì multiprocessing. hoặc kể cả là async với gevent.
- Có thể thêm ignore_result=True đối với các task không phải track kết quả.
- Cần quyết định start workers như nào, ở đâu, làm thế nào để đảm bảo nó chạy. Celery hỗ trợ supervisord để quản lý worker processes. Để monitor thì có thể sử dụng flower.

Alternatives to Celery: Python-RQ, Pyro

## Testing and Debugging Distributed Applications

Vấn đề về clock & time:

- Nên thống nhất chung chuẩn UTC giữa các service
- Điều chỉnh timing đối với các periodic (polling loops or cronjob) để tránh overload system

Vấn đề về environment:

- Dùng venv và docker

Vấn đề về vận hành:

- Có thể rất khó phát hiện ra ngay. Cách tốt nhất là logging & setup cơ chế fallback về state ban đầu nếu có lỗi xảy ra.
- Môi trường dev cũng cần giống production nhất có thể. Điều này không phải bao giờ cũng đạt được đối với team bé.
- Sử dụng monitor: Sentry, Flower (for celery)
- Chạy giả lập để test hệ thống.

## References:

- Book: Distributed Computing with Python (PacktPub 2016)