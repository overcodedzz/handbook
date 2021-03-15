---
title:  "Blockchain"
categories: Technology
toc: true
tags:
    - distributed system
---

## **Blockchain là gì ?**

Blockchain là một trong những công nghệ sổ cái phân tán (*). Việc truyền thông tin từ node này sang node khác chính là việc tạo ra transaction. Các transaction này sẽ được xác thực rồi lưu trữ trong  block. Mỗi block sẽ được nối với nhau tạo thành chain of blocks (nguồn gốc tên gọi blockchain). Nhờ cơ chế đồng thuận, chain of blocks này sẽ được đồng bộ giữa các bên tham gia.

(*) Distributed ledger technology (công nghệ sổ cái phân tán): công nghệ cho phép các bên tham gia mạng lưới phân tán có thể trao đổi và lưu trữ thông tin với sự giúp đỡ của thuật toán đồng thuận. Ưu điểm là công nghệ có thể hoạt động không cần có trung tâm điều phối (centralized authority), điều này giúp cho mạng lưới trở nên đáng tin cậy.

### Comparison between Blockchain and Database

| Blockchain                                                                  | Database                                                                                   |
|-----------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Distributed ledger                                                          | Centralized ledger                                                                         |
| Hỗ trợ read và write dữ liệu dựa trên sự đồng thuận của các bên tham gia    | Hỗ trợ read và write dữ liệu đối với đối tượng được cấp phép.                              |
| Có thể lưu trữ nhiều bản copy dữ liệu (được thực hiện bởi các bên tham gia) | Có thể lưu trữ nhiều bản copy dữ liệu (được thực hiện bởi admin)                           |
| Thông tin lưu trữ đáng tin cậy, có thể verify nhờ các bên tham gia          | Thông tin lưu trữ chưa đáng tin cậy, có thể bị thay đổi bởi người lấy được quyền truy cập. |
| Tốc độ thực thi bị giới hạn bởi cơ chế đồng thuận và xác thực               | Tốc độ thực thi nhanh chóng                                                                |
| Dữ liệu được minh bạch giữa các bên tham gia                                | Dữ liệu có thể không minh bạch vì admin là người quyết định điều đó                        |


Khi nói về các ứng dụng của Blockchain người ta lấy Bitcoin làm hệ quy chiếu. Để hiểu sâu về blockchain, bạn cần hiểu các mà mạng Bitcoin hoạt động. 

Tìm hiểu thêm về Bitcoin tại [đây](/technology/bitcoin/).


## References
- Book: Mastering Bitcoin 2nd
- [https://101blockchains.com/blockchain-vs-database-the-difference/](https://101blockchains.com/blockchain-vs-database-the-difference/)

## Contributor
- [minhdq99hp](mailto:minhdq99hp@gmail.com)
