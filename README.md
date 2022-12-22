## Để biên dịch chương trình trên, gõ lệnh:
`gcc -Wall -pthread -g -o <Tên chương trình> <Tên file chạy> –lwiringPi -lstdc++`
- Ví dụ: `gcc -Wall -pthread -g -o main main.cpp –lwiringPi -lstdc++`
- Wall : Tất cả warning sẽ được in lên terminal.
- pthread : Biên dịch kèm thư viện `pthead`. Thư viện `pthread` để khởi chạy đa luồng trong cùng một chương trình.

## Chạy chương trình bằng lệnh: 
`sudo ./<Tên chương trình>`
- Ví dụ: `sudo ./demo`