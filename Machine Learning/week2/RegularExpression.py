import re

thongtin = "TRẦN MẠNH CƯỜNG tranmanhcuong@hotmail.com Nguyễn An Ninh phường Tương Mai quận Hoàng Mai  0999970000"
compile_email = re.compile('(\S+@[a-z]+\.[a-z]{2,6})')
compile_phone = re.compile('([0-9]{10,11})')

email = compile_email.search(thongtin)
phone = compile_phone.search(thongtin)
other = re.split('\S+@[a-z]+\.[a-z]{2,6}', thongtin)

'''

/S     matches any non-whitespace character
.      matches any character including a newline.
\      ko lấy các kí tự đặc biệt
{2,6}  lấy từ 2 => 6 kí tự
[a-z]  will match any lowercase
+      to match 1 or more repetitions of the preceding RE. ab+ will match ‘a’ followed by any non-zero number of ‘b’s; it will not match just ‘a’.
(...)  Matches whatever regular expression is inside the parentheses, and indicates the start and end of a group; the contents of a group can be retrieved after a match has been performed, and can be matched later in the string with the \number special sequence, described below. To match the literals '(' or ')', use \( or \), or enclose them inside a character class: [(] [)].
.sub   Thay the, Return the string obtained by replacing the leftmost non-overlapping occurrences of pattern in string by the replacement repl
'''
print("\nEmail: " ,email.group(),"\nPhone: ",phone.group(),"\nTen: ",other[0],"\nDia Chi: ",compile_phone.sub("",other[1].strip()))