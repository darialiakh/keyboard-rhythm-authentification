from pynput.keyboard import Key, Listener
from time import time, sleep
from math import fsum, sqrt
import pickle
from os import mkdir, listdir

attempts = 10
temp = []
table_student_coef = {3: 2.353363, 4: 2.131847,5:2.015048,6:1.943180,7:1.894579,8:1.859548,9:1.833113,10:1.812461}
valid = {4:1,5:2,6:2,7:2,8:3,9:3,10:3,11:4,12:4}
intervals = []
y = []


def intervals_without_i_interval(intervals, i):
    y = []
    for j in range(len(intervals)):
        if i != j:
            y.append(intervals[j])
    # print(y)
    return y

def expected_value_calc(y):
    int_sum = fsum(y)
    exp_value = int_sum/len(y)
    return exp_value

def varience_calc(intervals, exp_value):
    # print([(intervals[i]-exp_value) for i in range(len(intervals))])
    int_sum = fsum([((intervals[i]-exp_value) ** 2) for i in range(len(intervals))])
    varience = int_sum/(len(intervals)-1)
    return varience

def varience_d_calc(intervals, exp_value):
    # print([(intervals[i]-exp_value) for i in range(len(intervals))])
    int_sum = fsum([((intervals[i]-exp_value) ** 2) for i in range(len(intervals))])
    varience = int_sum/(len(intervals)-1)
    return varience

def deviation_calc(varience):
    deviation = sqrt(varience)
    return deviation

def student_coef_calc(interval, exp_value, deviation):
    coef = abs((interval-exp_value)/deviation)
    return coef

def save_obj(obj):
    with open('data\\' + 'userdata' + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj():
    with open('data\\' + 'userdata' + '.pkl', 'rb') as f:
        return pickle.load(f)

def on_press(key):
    # print('{0} pressed'.format(
    #  key))
    temp.append(time())

def on_release(key):
    temp.append(time())
    if key == Key.enter:
        # Stop listener
        return False

def listen_phrase(key_phrase):
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

    this_phrase = input()
    if this_phrase == key_phrase:
        valid_phrase = True
    else:
        valid_phrase = False
    time_intervals = []
    for i in range(0, 2 * (len(this_phrase) - 1) - 1, 2):
        time_intervals.append((temp[i + 2] - temp[i + 1])*100)
    temp.clear()
    return time_intervals, valid_phrase

def collect_data(key_phrase):
    num_valid_phrase = 0
    while num_valid_phrase != attempts:
        time_intervals, valid_phrase = listen_phrase(key_phrase)
        if valid_phrase:
            num_valid_phrase += 1
            intervals.append(time_intervals)
        else:
            print('Please write correct password.')

    print('intervals: ')
    for i in range(attempts):
        print(intervals[i])

def clear_data(key_phrase):
    y = [[] for j in range(attempts)]
    exp_value = [[] for j in range(attempts)]
    varience = [[] for j in range(attempts)]
    deviation = [[] for j in range(attempts)]
    student_coef = [[] for j in range(attempts)]
    for i in range(attempts):
        for j in range(len(intervals[i])):
            y[i].append(intervals_without_i_interval([intervals[k][j] for k in range(attempts)], i))
    # print('y: ', y)
    for i in range(attempts):
        for j in range(len(intervals[i])):
            exp_value[i].append(expected_value_calc(y[i][j]))
    # print('exp value: ', exp_value)
    # print('exp value: ')
    # for i in range(attempts):
    #     print(exp_value[i])
    for i in range(attempts):
        for j in range(len(intervals[i])):
            varience[i].append(varience_calc(y[i][j], exp_value[i][j]))
    # print('varience: ')
    # for i in range(attempts):
    #     print(varience[i])
    for i in range(attempts):
        for j in range(len(intervals[i])):
            deviation[i].append(deviation_calc(varience[i][j]))
    # print('deviation: ')
    # for i in range(attempts):
    #     print(deviation[i])
    # print('varience: ', varience)
    # print('deviation: ', deviation)
    for i in range(attempts):
        for j in range(len(intervals[i])):
            student_coef[i].append(student_coef_calc(intervals[i][j], exp_value[i][j], deviation[i][j]))
            if student_coef[i][j] > table_student_coef[attempts-2]:
                intervals[i][j] = -1
    # print('student_coef: ', student_coef)
    # print('student coef: ')
    # for i in range(attempts):
    #     print(student_coef[i])
    print('study: ')
    for i in range(attempts):
        print(intervals[i])

    exp_value_d = []
    varience_d = []
    deviation_d = []
    t_min = []
    t_max = []
    v = []
    for i in range(len(key_phrase)-1):
        intervals_d = []
        count_correct_value = 0
        for k in range(attempts):
            if intervals[k][i] != -1:
                count_correct_value += 1
                intervals_d.append(intervals[k][i])
        print(count_correct_value)
        exp_value_d.append(expected_value_calc(intervals_d))
        varience_d.append(varience_d_calc(intervals_d, exp_value_d[i]))
        deviation_d.append(deviation_calc(varience_d[i]))
        t_min.append(exp_value_d[i] - table_student_coef[count_correct_value-1] * deviation_d[i])
        t_max.append(exp_value_d[i] + table_student_coef[count_correct_value-1] * deviation_d[i])
        v.append(t_min[i])
        v.append(t_max[i])

        # print('v:     ', v)
    print("exp_value_d: ", exp_value_d)
    print('varience_d:  ', varience_d)
    print('t_min: ', t_min)
    print('t_max: ', t_max)
    return t_min, t_max


def study():
    print("Please enter your login: ")
    user_login = input()
    sleep(0.5)
    print("Please enter key phrase: ")
    key_phrase = input()
    sleep(0.5)
    print('You are in learning mode.')
    print('Please enter key phrase 10 times.')
    collect_data(key_phrase)
    t_min, t_max = clear_data(key_phrase)
    print('The learning mode is finished.')

    try:
        user_data = load_obj()
    except:
        user_data = {}
        save_obj(user_data)

    user_data[user_login] = [key_phrase, t_min, t_max]
    save_obj(user_data)
    print(user_data)


def identification():
    try:
        user_data = load_obj()
    except FileNotFoundError:
        print('Зарегистрируйте сначала пользователя!')
        user_data = {}
        save_obj(user_data)
        quit()

    print('You are in identification mode.')
    print("Please enter your login: ")
    ident_user_login = input()
    sleep(0.5)
    if ident_user_login not in user_data.keys():
        print("This is incorrect login. Please try again.", user_data.keys())
        return
    else:
        print("Please enter your password: ")
        ident_intervals, valid_password = listen_phrase(user_data[ident_user_login][0])
        if not valid_password:
            print("This is incorrect password. Please try again.", user_data[ident_user_login][0])
        else:
            # print("Correct login and password.")
            error_counter = 0

            for i in range(len(ident_intervals)):
                if ident_intervals[i] < user_data[ident_user_login][1][i] or ident_intervals[i] > user_data[ident_user_login][2][i]:
                    error_counter += 1
            print('errror counter:', error_counter)
            print('valid error counter:', valid[len(ident_intervals)])
            print('t min:  ', user_data[ident_user_login][1])
            print('my int: ', ident_intervals)
            print('t max:  ', user_data[ident_user_login][2])
            if error_counter <= valid[len(ident_intervals)]:
                print('Congratulations! ')
            else:
                print('Ohh no.')




def menu():
    try:
        i = True
        while (i):
            print("Please enter your choice: ")
            print("1. Study ")
            print("2. Identification ")
            print('3. Exit')
            print("Your choice: ")
            choice = input()
            if int(choice) == 1:
                study()
            elif int(choice) == 2:
                identification()
            elif int(choice) == 3:
                i = False
            else:
                print('You entered incorrect value.')
    except:
        print('Error!\nPlease try again.')
        menu()



if 'data' not in listdir():
    mkdir('data')

menu()


