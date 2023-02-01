import datetime as dt
import glob
import os


def merge():
    data_obj = str(dt.datetime.now().strftime('%Y-%m-%d')) + '.csv'
    input_path = r'./nowon/tms/'
    o_path = r'./nowon/tms/merged/'
    output_path = o_path + data_obj

    file_list = glob.glob(input_path + '*.csv')
    print(file_list)

    with open(output_path, 'w', encoding='UTF-8') as f:
        for i, file in enumerate(file_list):
            if i == 0:
                with open(file, 'r', encoding='UTF-8') as f2:
                    while True:
                        line = f2.readline()
                        if not line:
                            break
                        f.write(line)
                    print(file.split('\\')[-1])

            else:
                with open(file, 'r', encoding='UTF-8') as f2:
                    n = 0
                    while True:
                        line = f2.readline()
                        if n != 0:
                            f.write(line)
                        if not line:
                            break
                        n += 1
                    print(file.split('\\')[-1])

    file_num = len(next(os.walk(input_path))[2])
    print(file_num, 'Merging data is completed...')


if __name__ == '__main__':
    merge()
