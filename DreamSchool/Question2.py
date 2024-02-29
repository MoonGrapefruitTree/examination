import sys
'''
给你一个字符串，如果一个字符在它前面k个字符中已经出现过了，就把这个字符改成’-’。
比如
Input: abcdefaxc 10
Output abcdef-x-

Input: abcdefaxcqwertba 10
Output abcdef-x-qw-rtb-
'''
if __name__ == '__main__':
    sentence, num = str(sys.argv[1]), int(sys.argv[2])
    # 遍历字符串，逐个判断是否需要修改成'-' 如果需要就修改否则不变
    new_sentence = [sentence[i] if not sentence[max(i-10, 0):i].__contains__(sentence[i]) else '-' for i in range(len(sentence))]
    # list 转换成string 并输出
    new_sentence = ''.join(new_sentence)
    print(new_sentence)