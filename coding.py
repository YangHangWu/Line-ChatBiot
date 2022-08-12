def solution(A):
    result=0
    count_list=[0,0,0,0,0]
    for i in range(len(A)):
        count_list[A[i]]+=1
    print(count_list)
    for i in range(1,5):
        step=0
        for j in range(1,5):
            step+=abs(count_list[j]*(j-i))
        if(i==1):
            result=step
        print(step)
        result=min(result,step)
    
    print(result)
solution([4,1,4,1])