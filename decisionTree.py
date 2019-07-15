'''
    决策树系统
'''
import pickle
from math import *

# 计算数据信息熵, 值越小越好
def calcshan(dataSet):   
    lenDataSet = len(dataSet)
    p = {}
    H = 0.0
    for data in dataSet:
        currentLabel = data[-1]  # 获取类别标签
        if currentLabel not in p.keys():  # 若字典中不存在该类别标签, 则创建
            p[currentLabel] = 0
        p[currentLabel] += 1    # 递增类别标签的值
    for key in p:
        px = float(p[key])/float(lenDataSet)  #计算某个标签的概率
        H -= px*log(px,2)  #计算信息熵
    return H
    
# 根据某一特征分类数据集, 提取满足axis的value的数据
# dataSet为要划分的数据集, axis为给定的特征, value为给定特征的具体值
def spiltData(dataSet, axis, value):
    subDataSet = []
    for data in dataSet:
        subData = []
        if data[axis] == value:
            # 把第axis个特征从数据集中去掉
            subData = data[:axis] 
            subData.extend(data[axis + 1:])
            subDataSet.append(subData)
    return subDataSet
    
# 遍历所有特征, 选择信息熵最小的特征, 即为最好的分类特征    
def chooseBestFeature(dataSet):
    lenFeature = len(dataSet[0]) - 1
    shanInit = calcshan(dataSet)      # 原始数据的信息熵
    feature = []
    inValue = 0.0
    bestFeature = 0
    # 遍历每个特征
    for i in range(lenFeature):
        shanCarry = 0.0
        feature = [example[i] for example in dataSet]  #提取第i个特征的所有数据
        feature = set(feature)  # 得到第i个特征所有的状态，如'0'和'1'
        # 遍历每个特征的每种情况, subData是特征i的j情况下的数据
        for feat in feature:  
            # 把数据集根据该特征可能出现的情况分成几类
            # 计算该特征的信息熵时要去除该特征本身, 计算余下信息的信息熵
            subData = spiltData(dataSet, i, feat)
            prob = float(len(subData))/float(len(dataSet))
            # 计算第i个特征的信息熵, 计算方法: 总信息熵 = 各部分信息熵的加权总和
            shanCarry += prob * calcshan(subData)
        outValue = shanInit - shanCarry  #原始数据信息熵与循环中的信息熵的差
        # 初始熵比参数的熵大outValue, 若存在一个参数的熵与初始熵相差的值大于outValue, 说明新参数更优
        # outValue是新参数的熵的差值, inValue是上一个最优参数的熵的差值
        if (outValue > inValue):
            inValue = outValue
            bestFeature = i     # 第i个参数最优
    # 返回的是最优特征的序号, 不是特征的名称
    return bestFeature

# 创建决策树
def createTree(dataSet, label):
    classList = [example[-1] for example in dataSet]
    # 一个分支遍历完成后, 生成叶子classList[0]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    featBest = chooseBestFeature(dataSet)  # 选择最好的分类特征
    feature = [example[featBest] for example in dataSet]  # 使用该分类特征进行分类
    featValue = set(feature)  # 得到该特征所有的分类值，如'0'和'1'
    newLabel = label[featBest]
    del(label[featBest])
    Tree = {newLabel:{}}  # 创建一个多重字典，存储决策树分类结果
    # 递归函数使得Tree不断创建分支，直到分类结束
    for value in featValue:
        subLabel = label[:]
        Tree[newLabel][value] = createTree(spiltData(dataSet, featBest, value), subLabel)
    return Tree
    
# 使用决策树执行分类，返回分类结果
# tree为createTree()函数返回的决策树；label为特征的标签值；testVec为测试数据
def classify(tree, label, testVec):
    firstFeat = list(tree.keys())[0]      # 取出tree的第一个键
    secondDict = tree[firstFeat]          # 取出tree第一个键的值，即tree的第二个字典
    labelIndex = label.index(firstFeat)   # 得到第一个特征firstFeat在标签label中的索引
    for key in secondDict.keys():         # 遍历第二个字典的键
        if testVec[labelIndex] == key:    # 如果第一个特征的测试值与第二个字典的键相对
            if type(secondDict[key]).__name__ == 'dict':  # 如果第二个字典的值还是一个字典, 说明分类还没结束, 递归执行classify函数
                return classify(secondDict[key], label, testVec)
            else:
                return secondDict[key]  # 最后将得到的分类值赋给classLabel输出
    
# 使用pickle模块存储决策树
def storeTree(tree, filename):
    # 二进制写入
    fw = open(filename,'wb')
    pickle.dump(tree, fw)
    fw.close()

# 打开文件取出决策树
def loadTree(filename):
    fr = open(filename,'rb')
    return pickle.load(fr)
    

