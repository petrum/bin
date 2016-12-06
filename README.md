# bin

```
$> sudo nmap -sP 192.168.1.1/24 | ./nmap2descr.py -s
               ip                     dn
0     192.168.1.1          machine1.home
1     192.168.1.2              roku.home
//...

$> sudo nmap -sP 192.168.1.1/24 | ./nmap2descr.py
               ip                     dn                mac                      company
0     192.168.1.1          machine1.home  18:1B:EB:12:34:56        Actiontec Electronics
1     192.168.1.2              roku.home  00:18:01:12:34:56                         Roku

$> head mac-addresses.csv
mac,desc,expected
00:18:01:12:34:56,Fios main ch 6,1
0C:89:10:12:34:56,TV,1

$> sudo nmap -sP 192.168.1.1/24 | ./nmap2descr.py -d mac-addresses.csv
               ip                     dn                mac                      company               desc  expected
0     192.168.1.1          machine1.home  18:1B:EB:12:34:56        Actiontec Electronics     Fios main ch 6         1
1     192.168.1.2              roku.home  00:18:01:12:34:56                         Roku               roku         1

```
