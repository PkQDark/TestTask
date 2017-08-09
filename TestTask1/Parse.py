def decode_text(num_of_param1, num_of_param2):
    f = open('34300.01.01.2016.01.01.2017.1.0.0.ru.csv', 'rb')
    line_parse = []
    split_line = []
    date_and_second_param = []
    for line in f:
        line_parse.append(line)
    f.close()
    line_parse = line_parse[7:]
    for i in line_parse:
        i = i.split(b';')
        split_line.append(i)
    for i in split_line:
        try:
            date_and_second_param.append(i[num_of_param1].decode())
            date_and_second_param.append(i[num_of_param2].decode())
        except UnicodeError:
            date_and_second_param.append('0.0')
    return date_and_second_param


def intermediate_calculate(cut_size, decode_list, int_or_float):
    for i in range(len(decode_list)):
        if not i % 2:
            decode_list[i] = decode_list[i][cut_size:10]
    date = []
    not_date = []
    for i in range(len(decode_list)):
        if not i % 2:
            date.append(decode_list[i])
        else:
            not_date.append(decode_list[i])
    temp = date[0]
    count = 0
    not_date_rep_time = []
    not_date_rep_time.append(0.0)
    if int_or_float:
        for i in range(len(date)):
            if date[i] == temp:
                not_date_rep_time[count] += int(not_date[i])
            else:
                count += 1
                not_date_rep_time.append(0.0)
                not_date_rep_time[count] += int(not_date[i])
                temp = date[i]
    else:
        for i in range(len(date)):
            if date[i] == temp:
                not_date_rep_time[count] += float(not_date[i])
            else:
                count += 1
                not_date_rep_time.append(0.0)
                not_date_rep_time[count] += float(not_date[i])
                temp = date[i]
    unique_date = []
    temp = date[0]
    count = 0
    list_of_date = []
    list_of_date.append(date[0])
    unique_date.append(0)
    for i in range(len(date)):
        if temp == date[i]:
            unique_date[count] += 1
        else:
            count += 1
            unique_date.append(0)
            list_of_date.append(date[i])
            temp = date[i]
    devide = []
    for i in range(len(unique_date)):
        devide.append(not_date_rep_time[i] / unique_date[i])
    return devide, list_of_date


def task1():
    devide, list_of_date = intermediate_calculate(3, decode_text(0, 7), True)
    maximum = max(devide)
    print(list_of_date[devide.index(maximum)])


def task2():
    devide, list_of_date = intermediate_calculate(3, decode_text(0, 1), False)
    minimum = min(devide)
    print(list_of_date[devide.index(minimum)])


def task3():
    devide, list_of_date = intermediate_calculate(0, decode_text(0, 1), False)
    maximum = max(devide)
    print(list_of_date[devide.index(maximum)])


def task4():
    devide, list_of_date = intermediate_calculate(3, decode_text(0, 1), False)
    maximum = max(devide)
    print(list_of_date[devide.index(maximum)])


def task5():
    devide, list_of_date = intermediate_calculate(0, decode_text(0, 1), False)
    minimum = min(devide)
    print(list_of_date[devide.index(minimum)])


def main():
    task1()
    task2()
    task3()
    task4()
    task5()

if __name__ == '__main__':
    main()