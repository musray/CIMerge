# CIMerge

## 规则
根据站号和点名，将AIO点同步至`ai_sheet.csv`，将DIO点同步至`di_sheet.csv`

## 开发思路

### 源文件分析
在源文件里找到相应数据，写到目标文件中。
- 源文件：命名类似于`current_IC0213test_exportIC.csv`
- 目标文件：`ai_sheet.csv`和`di_sheet.csv`

内容：
- 在源文件中，根据`1`和`10`两列（Name和Station）确定唯一的信号
- 该信号`2`列的信号，是变量类型（varType）;`8`列的内容，即目标数据（Value）
- 如果变量类型（varType）是`AIO`：
    - 在`ai_sheet.csv`中，根据Station和Name，找到对应的点
    - 将源文件中的value值，填写到`11`列（TestValue）中
- 如果变量类型（varType）是`DIO`：
    - 在`di_sheet.csv`中，根据State和Name，找到对应的点
    - 将源文件中的value值，填写到`11`列（TestValue）中


### 程序执行过程
1. 环境校验及准备
    - 是否有指定文件夹? 继续运行 : 新建+提示+退出
    - 文件夹内是否有指定文件? 继续运行 : 提示+退出
2. 打开源文件
    - 打开源文件(csv)
    - 获得数据
3. 打开目标文件
    - 逐行遍历：
        - 获得Station和Name
        - 在源文件数据中，找到该Station和Name，并获得Value
        - 将Value写入目标文件数据中
    - 保存新的输出文件

### 可能存在的问题
1. value列的值，看起来是数字，但要看实际上倒出的csv中，value到底是字符串还是数字。