#!/bin/bash
D="$HOME/so_seminars/seminar02/data" && mkdir -p "$D/weirdnames"
cat > "$D/web.log" << 'L'
192.168.1.10 - - [17/Mar/2026:09:15:22 +0000] "GET /api/users HTTP/1.1" 200 1234
10.0.0.5 - - [17/Mar/2026:09:15:23 +0000] "POST /api/login HTTP/1.1" 302 0
172.16.0.3 - - [17/Mar/2026:09:15:24 +0000] "GET /admin HTTP/1.1" 403 287
192.168.1.42 - - [17/Mar/2026:09:15:25 +0000] "GET /missing.html HTTP/1.1" 404 123
172.16.0.3 - - [17/Mar/2026:09:15:26 +0000] "POST /api/submit HTTP/1.1" 500 0
10.0.0.5 - - [17/Mar/2026:09:15:27 +0000] "GET /api/data?id=12 HTTP/1.1" 200 5678
192.168.1.10 - - [17/Mar/2026:09:15:28 +0000] "GET /api/status HTTP/1.1" 200 89
172.16.0.3 - - [17/Mar/2026:09:15:29 +0000] "GET /api/data?id=42 HTTP/1.1" 500 0
192.168.1.42 - - [17/Mar/2026:09:15:30 +0000] "GET /favicon.ico HTTP/1.1" 404 0
10.0.0.5 - - [17/Mar/2026:09:15:31 +0000] "GET /api/health HTTP/1.1" 200 15
L
printf '%s\n' "Hello World" "this is a lowercase line" \
"Line with 42 numbers inside" "UPPERCASE LINE HERE" \
" multiple spaces here" \
"Another line with digits 7 and 99" "" "Mixed Case Line" \
"Report from 2026: all systems go" "" "last line" > "$D/text.txt"
printf 'user=%s token=%s\n' ana ABCD-1234-XYZ bob EFGH-5678-UVW \
carol IJKL-9012-RST dan MNOP-3456-QRS > "$D/creds.txt"
printf '%s\n' "id, name, amount" "1,alice, 250" "2 ,bob,300" \
"3, carol , 175" "4,dan, 420" > "$D/messy.csv"
touch "$D/weirdnames/file with spaces.txt"
echo "odd" > "$D/weirdnames/-weirdname.txt"
echo "secret" > "$D/secret.txt" && chmod 600 "$D/secret.txt"
echo "Dataset: $(find "$D" -type f | wc -l) files in $D"
