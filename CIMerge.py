#!/usr/bin/env python3
import os
import csv
import sys
# from operator import itemgetter


def get_source_data(csv_file):
    # 返回一个由csv内容组成的list
    # 内容只包括有限的几类

    types = ['AI', 'AO', 'DI', 'DO', 'CIM', 'CI', 'CO']
    with open(csv_file, 'r', encoding='gbk') as file:
        reader = csv.reader(file, delimiter=',')
        data = [data for data in reader if data[4] in types]

    print('return get_source_data')
    return data


def csv_query(query_data, source, flag):
    # data可能是ai_sheet中的一行，或是di_sheet中的一行数据
    # 在ai_sheet中，`2`列是Tag信号名，`9`列是DeviceID站号(格式纯数字),`11`列放value值
    # 在di_sheet中，`2`列是Tag信号名，`10`列是DeviceID站号(格式纯数字)，`12`列放value值
    # source是一个list组成的list，`1`列是Name信号名，`10`列是Station站号（格式YJ5_数字）,`8`列是Value值
    # 如果source中的value值是空的，则返回字符串invalid.
    # 如果没有找到对应的点，则返回字符串notfound
    notfound = True

    for line in source:
        # 点名相同，而且站号相同

        if flag == 'ai':
            if line[1] == query_data[2] and line[10].split('_')[1] == query_data[9]:
                return line[8]
        if flag == 'di':
            if line[1] == query_data[2] and line[10].split('_')[1] == query_data[10]:
                print('line[8] is %s' % line[8])
                return line[8]

    if notfound:
        return 'notfound'


def targets_handler(targets, source_data):
    # targets是一个由tuple组成的list，source_data是一个源数据的list
    for in_file, out_file in targets:
        # 打开in和out
        # 把in_file的第一行到最后一行，存成一个list
        # 遍历list
        # - 在source_data中找点
        #   - 有这个点:
        #       - 把它的value，写到in_file的数据中
        #   - 没有这个点:
        #       - 把这个点的信息写到一个lost_found的list中
        # - 把准备好的数据写到out_file里

        # flag，是csv_query()的第三个参数。
        if 'ai_sheet' in in_file:
            flag = 'ai'
        else:
            flag = 'di'

        with open(in_file, 'r', encoding='gbk') as csv_in,\
                open(out_file, 'w', encoding='gbk') as csv_out:

            reader = csv.reader(csv_in, delimiter=',')
            writer = csv.writer(csv_out, delimiter=',')

            csv_in_data = list(reader)
            csv_out_data = []

            print('开始处理文件 %s，可能需要几分钟，请稍候...' % os.path.basename(in_file))
            for query_data in csv_in_data:
                # 如果点名单元格中的内容长度<4，说明这一列不是数据列
                # 原封不动写到输出文件里
                if len(query_data[2]) < 4:
                    writer.writerow(query_data)
                # 否则，说明是数据列
                else:
                    csv_out_data = query_data[:]
                    value = csv_query(query_data, source_data, flag)
                    # print(value)
                    # value有两种可能：正常值, 或 'notfound'

                    # ai_sheet和di_sheet中，存放value的位置是不一样的，所以:
                    if flag == 'ai':
                        csv_out_data[11] = value
                    elif flag == 'di':
                        csv_out_data[12] = value

                    writer.writerow(csv_out_data)
            print('处理完成！')


def main():

    # csv文件，存放在程序根目录内一个叫CI的目录下
    csv_dir = 'CI'

    if not os.path.isdir(csv_dir):
        input('没有发现 %s 文件夹，已为你新建。\n请将csv文件放入其中，再运行本程序。\n按任意键退出...' % csv_dir)
        os.mkdir(csv_dir)
        sys.exit(1)

    # 遍历给定文件夹内的所有文件
    # 如果是csv文件，则：
    #   - 挨个处理
    csvfiles = [item for item in os.listdir(csv_dir) if '.csv' == item[-4:].lower()]

    # 在offset文件夹中没有csv文件
    if len(csvfiles) == 0:
        input('%s 文件夹中缺少相关csv文件，按任意键退出...' % csv_dir)
        sys.exit(1)

    # 为csv文件分类
    # 如果命名不正确（说明文件内容可能也有问题），则要退出运行
    source = []
    targets = []
    for csvfile in csvfiles:

        # 对源文件的判断：文件名中包含"exportIC"
        if 'exportic' in csvfile.lower():
            source.append(os.path.join(os.getcwd(), csv_dir, csvfile))

        # 对目标文件的判断：文件名由"ai"或者"di"开头
        if csvfile[:2].lower() == 'ai' or csvfile[:2].lower() == 'di':
            in_file = os.path.join(os.getcwd(), csv_dir, csvfile)
            out_file = os.path.join(os.getcwd(), csv_dir, 'sync_' + csvfile)
            # targets是一系列（in_file, out_file）组成的tuple
            targets.append((in_file, out_file))

    # 如果源文件存在，且至少存在一个目标文件：
    # 开始处理文件
    if len(targets) > 0 and len(source) > 0:
        #1. 读源文件
        source_data = get_source_data(source[0])
        #2. 处理目标文件
        # targets是一个由tuple组成的list，source_data是一个源数据的list
        targets_handler(targets, source_data)
        #3. 所有文件处理完成，cue一下用户
        input('按任意键退出...')
        sys.exit(0)

    elif len(targets) == 0:
        input('%s 文件夹中缺少ai_sheet.csv或di_sheet.csv，请检查。\n按任意键退出...' % csv_dir)
        sys.exit(1)
    elif len(source) == 0:
        input('%s 文件夹中缺少exportIC.csv文件，请检查。\n按任意键退出...' % csv_dir)
        sys.exit(1)


if __name__ == '__main__':
    main()
