from openpyxl import Workbook


wb = Workbook()
wb.create_sheet('rtt汇总',index=0)

sheet = wb['rtt汇总']
sheet.append(["total_rtt","total_lost","total_maxbr","total_fail"])


filename = "f://logs/nstest_log.txt"
result = "f://logs/nstest_log.xlsx"
with open(filename) as f:
    lines = f.readlines()

total_rtt, total_lost, total_maxbr, total_fail = 0, 0, 0, 0
for line in lines:
    # print(line.rstrip())
    if 'nstest set nstest' in line:
        # print("total_rtt","total_lost","total_maxbr","total_fail")
        # print(total_rtt, total_lost, total_maxbr, total_fail)
        sheet.append([total_rtt, total_lost, total_maxbr, total_fail])
        total_rtt, total_lost, total_maxbr, total_fail = 0, 0, 0, 0
    if 'nstest set info rtt' in line:
        s = line.split(" ")
        total_rtt += int(s[10])
        total_lost += int(s[12])
        total_maxbr += int(s[14])
        total_fail += int(s[16])
        # print(s[10],s[12],s[14],s[16])
        # print(s)
        # print(total_rtt, total_lost, total_maxbr, total_fail)
wb.save(result)