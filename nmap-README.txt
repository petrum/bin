1. recent ts, active = True: do nothing
2. recent ts, active = False: send email when it was last seen + active = True + lastEmailTS = Now()
3, old ts < 5 min ago, active = True: send email about how long it was online + active = False + lastEmailTS = Now()
4. old ts < 5 min ago, active = False: do nothing
