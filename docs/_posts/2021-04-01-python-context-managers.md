---
title: "Python Context Managers"
categories: 
  - Computer science
toc: true
---

## Introduction

Motivation of Context Manager: resource management.

- Yêu cầu resource → cấp cho resource (open)
- Resource là hữu hạn → phải nhả (close) khi dùng xong.

Cách thông thường là sử dụng try/catch/finally để đảm bảo việc cấp phát, sử dụng resource "có kiểm soát". Python thì có cơ chế hay hơn, "pythonic" hơn là đó là sử dụng context manager.

### Resource management without Context Managers

E.g. Bad practice:

```python
opened_file = open('readme.txt')
text = opened_file.read()
...
opened_file.close()
```

- Nếu có vấn đề gì xảy ra giữa quá trình open và close (exception) thì sẽ dẫn đến resource leak.

E.g. Improved way

```python
try:
	opened_file = open('readme.txt')
	text = opened_file.read()
	...
else:
# finally:
	opened_file.close()
```

- Statements trong else sẽ đảm bảo được chạy.

## Implementing Context Managers

### Method 1: defining class

A context manager is a class with 2 special methods:

- `__enter__`: the method that gets called when we open the resource, or technically "enter" the runtime context.
- `__exit__`: contains clean-up code which must be executed after we're done with the resource, no matter what.

Example:

```python
class FileManager:
		def __init__(self, filename):
				self.filename = filename

		def __enter__(self):
				self.opened_file = open(self.filename)
				return self.opened_file

		def __exit__(self, *exc):
				self.opened_file.close()

...

with FileManager('readme.txt') as file:
		text = file.read()
```

- Một instance mới của `FileManager` được tạo ra khi sử dụng `with`

statement, sau đó nó gọi hàm `__enter__` và gán giá trị trả về vào biến `file`.

Conclusion:

1. The object passed to the `with` statement must have `__enter__` and `__exit__` methods
2. The `__enter__` method must return the resource that's to be used in the `with` block.

### Method 2: using contextlib

```python
from contextlib import contextmanager

@contextmanager
def open_file(filename):
		opened_file = open(filename)
		try:
				yield opened_file
		finally:
				opened_file.close()
```

Ngoài hỗ trợ decorator như trên thì contextlib còn có `AbstractContextManager` (Python 3.6+).

## References:

- [https://stackabuse.com/python-context-managers/](https://stackabuse.com/python-context-managers/)
- [https://everyday.codes/python/python-context-managers-in-depth/](https://everyday.codes/python/python-context-managers-in-depth/)

## Contributors:

- minhdq99hp $\dagger$