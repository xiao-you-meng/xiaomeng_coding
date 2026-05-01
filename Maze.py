
import random
import os
import time

EPSILON = 0.1       #探索率
GAMMA = 0.9         #折扣因子
ALPHA = 0.1         #学习率
EPISODES = 1000     #训练轮数

print("输入迷宫高度：")
m = int(input())
print("输入迷宫宽度：")
n =int(input())
maze = []

print("请输入迷宫(1:墙 2:终点 0:路径):")
for i in range(m):
    row = list(map(int, input().split()))
    maze.append(row)

#####小测试
# n=7
# m=7
# maze=[[0,0,0,0,0,0,0],
#       [0,1,1,1,0,1,0],
#       [0,0,0,1,0,0,0],
#       [0,1,0,0,0,1,0],
#       [0,0,0,1,0,0,0],
#       [1,0,1,0,0,0,0],
#       [1,0,0,0,0,0,2]]

#转成一维坐标
def coord_to_state(x,y):
    return y*n+x

#转成二维坐标
def state_to_coord(state):
    return (state%n,state//n)

#创建Q表
q = [[0 for k in range(4)] for i in range(m*n)]

#选择行动
def choose_action(state):
    if random.random() < EPSILON:
        return random.randint(0,3)
    else:
        temp = max(q[state])
        con = 0
        for i in q[state]:
            if temp == i:
                return con
            con+=1

#采取行动
def take_action(state,action):
    x,y = state_to_coord(state)
    new_x = x
    new_y = y
    reward = 0

    if action==0:
        new_y-=1
    elif action==1:
        new_y+=1
    elif action==2:
        new_x-=1
    else:
        new_x+=1
    
    if new_x<0 or new_y<0 or new_x>=n or new_y>=m or maze[new_y][new_x]==1:
        reward = -10
        return state,reward
    
    new_state = coord_to_state(new_x,new_y)
    if maze[new_y][new_x]==2 :
        reward = 100
    else:
        reward = -1
    return new_state,reward

#更新Q表
def update_q(state,action,new_state,reward):
    q[state][action] += ALPHA * (reward + GAMMA * max(q[new_state])-q[state][action])
    return

#输出迷宫
def print_maze(agent_x,agent_y):
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(m):
        for j in range(n):
            if i==agent_y and j==agent_x:
                print('A',end=' ')
            elif maze[i][j]==0:
                print('.',end=' ')
            elif maze[i][j]==1:
                print('#',end=' ')
            else:
                print('G',end=' ')
        print("")

#训练
def train():
    ep = 0
    while ep<EPISODES:
        ep+=1
        state = coord_to_state(0,0)
        while 1:
            action = choose_action(state)
            new_state,reward=take_action(state,action)
            update_q(state,action,new_state,reward)
            state = new_state
            now_x,now_y = state_to_coord(state)
            if maze[now_y][now_x]==2:
                break

#展示
def demo():
    state = coord_to_state(0,0)
    steps = 0
    while 1:
        x,y=state_to_coord(state)
        print_maze(x,y)
        print("步骤：",steps)
        steps+=1
        if maze[y][x]==2:
            print("到达目标!")
            break

        action=0
        max_q = max(q[state])
        for i in q[state]:
            if i==max_q:
                break
            action+=1
        state,reward = take_action(state,action)
        time.sleep(0.5)

train()
demo()