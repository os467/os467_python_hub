import pygame
import sys
import random
import time
from pygame.locals import *

black_color = pygame.Color(0,0,0)
white_color = pygame.Color(255, 255, 255)
red_color = pygame.Color(255,0,0)
green_color = pygame.Color(0,255,0)
blue_color = pygame.Color(0,150,255)
grey_color = pygame.Color(150, 150, 150)
orange_color = pygame.Color(255,165,0)

def destory(li,tag_id):
        "删除列表被标记对象"
        del_num = 0
        for i in range(len(li)):
            if li[i][0] == 'destory':
                del_num+=1
        for i in range(del_num):
            li.remove(tag_id)
        return None
            
def tag_destory(li):
    "对li列表标记替换并返回li列表"
    for i in range(len(li)):
        li[i] = 'destory'
    return li
            
def gamestart():
    "游戏开始界面"
    pygame.init()
    pygame.time.Clock()
    ftpsClock = pygame.time.Clock()
    #创建窗口
    #设置窗口尺寸
    gamesurface = pygame.display.set_mode((1920,1080), FULLSCREEN, HWSURFACE)
    pygame.display.set_caption('测试游戏')
###############################################################################
    while True:
        "开始游戏"
        gameshow_font = pygame.font.SysFont('MicrosoftYaHei',25)
        gameshow_color = gameshow_font.render("Press 'q' Start Game",True,white_color)
        gameshow_location = gameshow_color.get_rect()
        gameshow_location.midtop = (740,320)
        gamesurface.blit(gameshow_color,gameshow_location)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.type == QUIT:
                   return 1
                if event.key == K_q:
                    return 0
        pygame.display.update()
            
def gameover(score):
    pygame.init()
    pygame.time.Clock()
    ftpsClock = pygame.time.Clock()
    #创建窗口
    #设置窗口尺寸
    gamesurface = pygame.display.set_mode((1920,1080), FULLSCREEN, HWSURFACE)
    pygame.display.set_caption('测试游戏')
###############################################################################
    while True:
        "游戏结算"
        score_ = str(score)
        gameshow_font = pygame.font.SysFont('MicrosoftYaHei',25)
        gameshow_color = gameshow_font.render("Game Over",True,white_color)
        gameshow_location = gameshow_color.get_rect()
        gameshow_location.midtop = (770,320)
        gamesurface.blit(gameshow_color,gameshow_location)
        gameshow_color = gameshow_font.render(f"Your score:{score_}",True,white_color)
        gameshow_location = gameshow_color.get_rect()
        gameshow_location.midtop = (770,400)
        gamesurface.blit(gameshow_color,gameshow_location)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return 1
                elif event.key == K_q:
                    return 0
        pygame.display.update()
        
def main():
    pygame.init()
    pygame.mixer.init()
    #初始化音效
    s_fire = pygame.mixer.Sound("voice_fire.mp3")
    pygame.mixer.music.load("DarkSeaSide.mp3")
    pygame.mixer.music.play(-1,1)
    pygame.time.Clock()
    ftpsClock = pygame.time.Clock()
    #创建窗口
    #设置窗口尺寸
    gamesurface = pygame.display.set_mode((1920,1080),FULLSCREEN,HWSURFACE)
    pygame.display.set_caption('测试游戏')
    agentSize = [[690,740],[710,740],[730,740]]
    boss = []
    bulletsize = []
    enemy_bulletsize = []
    enemy = []
    reward = []
    bosslevel = 1
    bossdirection = 0
    bosslife = 100
    bossbulletsize = []
    #游戏初始boss等级
    press_tag = 0
    score = 0
    #游戏得分
    enemy_limit = 2
    enemy_speed = 5
    #最大敌人数
    enemy_summon_limit = 10
    #敌人生成时间间隔
    buff = [0,0,0]
    #是否获得弹数加成
    fire_buff = 0
    #是否获得连发加成
    life = 5
    MouseButton = 0
    skill_down = 0
    #生命值
    change_direction = [0,0,0,0]
    gametick= [0,0,0,0,0,0,0,0,0,0,0,0,20,0]
    #游戏时间计数器,0:子弹发射间隔，1:敌人生成间隔，2:游戏存活时间,3:敌人子弹刷新时间,4:奖励存活时间,5:buff存活时间,6:受伤免疫时间,7:敌人位移决定时间
    #8:buff3火力时间,9:buff3声音参数,10:游戏累计时间,11:群军进攻时间,12:skill技能冷却,13:boss受到攻击的频率上限
    press_order = []
    #记录玩家历史输入方向
    color_tag = 0
    r = 255
    add = 1
    black_color = pygame.Color(0,0,0)
    white_color = pygame.Color(255, 255, 255)
###############################################################################
    "图像渲染"
    block_img = pygame.image.load("block.png")
    # enemy_img = pygame.image.load("enemy.png")
    
###############################################################################   
    while True:
        #击杀boss界面颜色渐变功能
        if color_tag:
            if add:
                r -=1
                if r == 0:
                    color_tag = 0
                    add = 0
            if not add:
                r += 1
                if r == 255:
                    color_tag = 0
                    add = 1
            black_color = pygame.Color(255-r,255-r,255-r)
            white_color = pygame.Color(r, r, r)
###############################################################################
        gametick = list(map(lambda x:x+1, gametick))
        if gametick[2]> 150:
            enemy_limit+=1
            gametick[2] = 0
        
        if gametick[10] > 2000 * (enemy_limit - 1) and enemy_limit < 30:
            enemy_limit+=1
###############################################################################
        "玩家控制模块"
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                MouseButton = 0
            if event.type == MOUSEBUTTONDOWN and gametick[0] > 8:
                MouseButton = 1
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                if event.key == K_SPACE:
                    skill_down = 0
                if event.key == K_RIGHT or event.key == K_d:
                    change_direction[3] = 0
                    try:
                        press_order.remove('3')
                    except:
                        ""
                if event.key == K_LEFT or event.key == K_a:
                    try:
                        press_order.remove('2')
                    except:
                        ""
                    change_direction[2] = 0
                if event.key == K_DOWN or event.key == K_s:
                    change_direction[1] = 0
                    try:
                        press_order.remove('1')
                    except:
                        ""
                if event.key == K_UP or event.key == K_w:
                    change_direction[0] = 0
                    press_order.remove('0')
                if change_direction == [0,0,0,0]:
                    press_tag = 0
                #只有当所有控制键全部弹起才判断为完全静止
            elif event.type == KEYDOWN:
                press_tag = 1
                
                if event.key == K_RIGHT or event.key == K_d:
                    change_direction[3] = 1
                    press_order.append('3')
                if event.key == K_LEFT or event.key == K_a:
                    change_direction[2] = 1
                    press_order.append('2')
                if event.key == K_DOWN or event.key == K_s:
                    change_direction[1] = 1
                    press_order.append('1')
                if event.key == K_UP or event.key == K_w:
                    change_direction[0] = 1
                    press_order.append('0')
                if event.key == K_SPACE and gametick[12] > 15:
                    skill_down = 1
                if event.key == K_ESCAPE:
                    return score
###############################################################################
        "奖励生成"
        if  gametick[4] > 600:
            x = random.randrange(1,70)*20
            y = random.randrange(40,50)*15
            t = random.randrange(1,4)*1
            reward.insert(0,[x,y,t])
            gametick[4] = 0
        "敌人生成"
        if len(enemy)<enemy_limit and gametick[1] > enemy_summon_limit:
            x = random.randrange(1,70)*20
            y = -10 
            t = -1
            enemy.insert(0,[x,y,t])
            gametick[1] = 0
            if random.randrange(1,100)>60:
                enemy_bulletsize.insert(0,[enemy[0][0]+20,enemy[0][1]+40])
        "boss生成"
        if gametick[10] > 3000 and score - bosslevel*200 > 0 and not boss:
            bosslevel+=1
            boss = [[690,140],[710,140],[730,140],bossdirection,bosslife]
            enemy_speed = 5
        
        "敌人随机发射子弹"
        if len(enemy) > 3 and gametick[3] > 10:
            index = random.randrange(0,len(enemy)-1)
            if random.randrange(1,100)>80:
                enemy_bulletsize.insert(0,[enemy[index][0]+20,enemy[index][1]+40])
            gametick[3] = 0
        "boss发射子弹"
        if boss and gametick[3] > 5:
            if random.randrange(1,100)>80:
                bossbulletsize.insert(0, [boss[1][0]+10,boss[1][1]+30])
            if random.randrange(1,200) > 190:
                bossbulletsize.insert(0, [boss[0][0]+10,boss[0][1]+30])
                bossbulletsize.insert(0, [boss[2][0]+10,boss[2][1]+30])
###############################################################################
        "事件"
        "发射子弹"
        if MouseButton == 1 and gametick[0] > 8:
            s_fire.play()
            bulletsize.insert(0,[agentSize[1][0]+10,agentSize[1][1]-20])
            if buff[0] == 1:
                buff_bull_time+=1
                bulletsize.insert(0,[agentSize[0][0]+10,agentSize[0][1]-20])
                bulletsize.insert(0,[agentSize[2][0]+10,agentSize[2][1]-20])
            gametick[0] = 0
                                        
        "击毁敌人"
        for pix_e in enemy:
            for pix_b in bulletsize:
                if ((pix_e[0]+20 - pix_b[0])**2)**0.5 < 22 and ((pix_e[1]+7.5 - pix_b[1])**2)**0.5 < 15:
                    tag_id = tag_destory(pix_e)
                    score+=1
                    break
                    #对于当前pix_e，即敌人个体弹出列表后应当打断内层次个体与子弹对撞的判定
        try:
            destory(enemy,tag_id)
        except:
            ""
        "攻击boss"
        if gametick[13] >1:
            for pix_e in boss[0:3]:
                for pix_b in bulletsize:
                    if ((pix_e[0]+20 - pix_b[0])**2)**0.5 < 22 and ((pix_e[1]+7.5 - pix_b[1])**2)**0.5 < 15:
                        bosslife-=1
            gametick[13] = 0
        "boss死亡"
        if boss and bosslife < 0:
            boss = []
            bosslevel+=1
            bosslife = bosslevel* 100
            enemy_speed = 10
            color_tag = 1
        "吃到奖励"
        for pix in reward:
            if ((agentSize[1][0] -pix[0])**2)**0.5 < 40 and ((agentSize[1][1] - pix[1])**2)**0.5 < 30:
                
                if pix[2] == 1:
                    score+=30
                    buff[0] = 1
                    buff_bull_time = 0
                    if gametick[5] >=0 and gametick[5] <= 500:
                        gametick[5] -= 500
                    elif gametick[5] >500:
                        gametick[5] = 0
                    elif gametick[5] <0:
                        gametick[5] -= 500
                    #重置buff时间,叠加buff时间
                    tag_id = tag_destory(pix)
                    
                if pix[2] == 2:
                    score+=10
                    buff[1] = 1
                    tag_id = tag_destory(pix)
                
                if pix[2] == 3:
                    score+=10
                    buff[2] = 1
                    if gametick[8] >=0 and gametick[8] <= 500:
                        gametick[8] -= 500
                    elif gametick[8] >500:
                        gametick[8] = 0
                    elif gametick[8] <0:
                        gametick[8] -= 500
                    tag_id = tag_destory(pix)
        try:
            destory(reward,tag_id)
        except:
            ""
                
        "buff过期"
        if gametick[5] > 500:
            buff[0] = 0
            gametick[5] = 0
        if gametick[8] > 500:
            fire_buff = 0
            gametick[8] = 0
        "受伤"
        if gametick[6] >50:
            for pix in enemy:
                if ((agentSize[1][0] -pix[0])**2)**0.5 < 40 and ((agentSize[1][1] - pix[1])**2)**0.5 <20:
                    life-=1
                    gametick[6] = 0
            for pix in enemy_bulletsize:
                if ((agentSize[1][0] -pix[0])**2)**0.5 < 40 and ((agentSize[1][1] - pix[1])**2)**0.5 <20:
                    life-=1
                    gametick[6] = 0
            for pix in bossbulletsize:
                if ((agentSize[1][0] -pix[0])**2)**0.5 < 40 and ((agentSize[1][1] - pix[1])**2)**0.5 <20:
                    life-=1
                    gametick[6] = 0
            for pix in boss[0:3]:
                if ((agentSize[1][0] -pix[0])**2)**0.5 < 40 and ((agentSize[1][1] - pix[1])**2)**0.5 <20:
                    life-=1
                    gametick[6] = 0
        "奖励生效2"
        if buff[1] == 1:
            life+=1
            buff[1] = 0
        "奖励生效3"
        if buff[2] == 1:
            fire_buff = 1
            buff[2] = 0
            
        "奖励3内容"
        if fire_buff == 1:
            if gametick[9] > 5:
                s_fire.play()
                gametick[9] = 0
            bulletsize.insert(0,[agentSize[1][0]+10,agentSize[1][1]-20])
            if buff[0] == 1:
                buff_bull_time+=1
                bulletsize.insert(0,[agentSize[0][0]+10,agentSize[0][1]-20])
                bulletsize.insert(0,[agentSize[2][0]+10,agentSize[2][1]-20])
            
        "敌人位移决定"
        if gametick[7] > 50:
            if enemy:
                for pix in enemy:
                    if random.randrange(1,100)>70:
                        if random.randrange(1,100)>50:
                            pix[2] = 1
                        else:
                            pix[2] = 0
                    gametick[7] = 0
                    "boss位移决定"
                    if boss:
                        if random.randrange(1,100)>70:
                            if random.randrange(1,100)>50:
                                boss[3] = 1
                            else:
                                boss[3] = 0
        "群军"
        if random.randrange(0,2000) == 1 and gametick[10] > 1000:
            enemy_speed = 15
            enemy_limit += 2*enemy_limit
            enemy_summon_limit = 1
            gametick[11] = 0
        if gametick[11] > 200 and enemy_summon_limit == 1:
            enemy_limit -= 2*enemy_limit
            enemy_speed = 10
            enemy_summon_limit = 10
            
        "使用技能"
        if skill_down == 1:
            s_fire.play()
            skill_down = 0
            gametick[12] = 0
            bulletsize.insert(0,[agentSize[1][0]+30,agentSize[1][1]-20])
            bulletsize.insert(0,[agentSize[1][0]+60,agentSize[1][1]-20])
            bulletsize.insert(0,[agentSize[1][0]-10,agentSize[1][1]-20])
            bulletsize.insert(0,[agentSize[1][0]-40,agentSize[1][1]-20])
###############################################################################
        "边界判定"
        for pix in agentSize:
            if pix[1]==0:
                if change_direction[0] == 1:
                    change_direction[0] = 0
            if pix[1]==740:
                if change_direction[1] == 1:
                    change_direction[1] = 0
            if pix[0]==10:
                if change_direction[2] == 1:
                    change_direction[2] = 0
            if pix[0]==1490:
                if change_direction[3] == 1:
                    change_direction[3] = 0
        for pix in bulletsize:
            if pix[1]<=0:
                bulletsize.pop()
        for pix in enemy:
            if pix[1]>=760:
                enemy.pop()
        for pix in bossbulletsize:
            if pix[1] <=0:
                bossbulletsize.pop()
         
###############################################################################
        "改变坐标,移动轨迹"
        #判断是移动时按下空格还是静止时按下空格
        for pix in bossbulletsize:
            pix[1]+=15
        for pix in enemy_bulletsize:
            pix[1]+=20
        for pix in bulletsize:
            pix[1]-=10
        if buff[0] == 1 and bulletsize:
            try:
                index1 = 0
                index2 = 1
                for i in range(buff_bull_time):
                    bulletsize[index1][0]+=5
                    bulletsize[index2][0]-=5
                    index1+=3
                    index2+=3
            except:
                ""
        if press_tag == 1:
            #正常移动，和按下开火时的移动
            if change_direction[3] == 1:
                for pix in agentSize:
                    pix[0]+=20
            if change_direction[2] == 1:
                for pix in agentSize:
                    pix[0]-=20
            if change_direction[1] == 1:
                for pix in agentSize:
                    pix[1]+=10
            if change_direction[0] == 1:
                for pix in agentSize:
                    pix[1]-=10
        for pix in enemy:
            pix[1]+=enemy_speed
        
        "敌人位移"
        if enemy:
            for pix in enemy:
                if pix[0] > 10 and pix[0] < 1490:
                    if pix[2] == 1:
                        pix[0]+=5
                    elif not pix[2]:
                        pix[0]-=5
        "boss位移"
        if boss:
            if boss[0][0] <= 20:
                boss[3] = 1
            if boss[2][0] >= 1440:
                boss[3] = 0
            for pix in boss[0:3]:
                if boss[3] == 1:
                    pix[0]+=5
                if not boss[3]:
                    pix[0]-=5
            
        "修复卡顿"
        #原理：在同时按住相反两个键位的时候，通过press_order列表存储的键位顺序判断先后，自动覆盖老的键位
        if press_tag == 1:
            if change_direction[0] == 1 and change_direction[1] == 1:
                try:
                    index0 = 0
                    index1 = 1
                    for i in range(len(press_order)):
                        if press_order[i] == '0':
                            index0 = i
                        if press_order[i] == '1':
                            index1 = i
                    if index0 > index1:
                        change_direction[1] = 0
                    else:
                        change_direction[0] = 0
                except:
                    ""
            if change_direction[2] == 1 and change_direction[3] == 1:
                try:
                    index2 = 0
                    index3 = 0
                    for i in range(len(press_order)):
                        if press_order[i] == '2':
                            index2 = i
                        if press_order[i] == '3':
                            index3 = i
                    if index2 > index3:
                        change_direction[3] = 0
                    else:
                        change_direction[2] = 0
                except:
                    ""
        
###############################################################################
        "绘制图像"
        gamesurface.fill(black_color)
        if boss:
            pygame.draw.polygon(gamesurface,red_color,[[boss[0][0],boss[0][1]],
                                                         [boss[0][0]+20,boss[0][1]],
                                                         [boss[0][0]+20,boss[0][1]+20]])
            pygame.draw.polygon(gamesurface,red_color,[[boss[2][0],boss[2][1]],
                                                         [boss[2][0]+20,boss[2][1]],
                                                         [boss[2][0],boss[2][1]+20]])
            pygame.draw.rect(gamesurface,red_color,Rect(boss[1][0],boss[1][1]+5,20,10))
        if enemy:
            for pix in enemy:
                pygame.draw.polygon(gamesurface,white_color,[[pix[0],pix[1]],[pix[0]+40,pix[1]],[pix[0]+20,pix[1]+15]])
        if bulletsize:
                for pix in bulletsize:
                    pygame.draw.circle(gamesurface,white_color,[pix[0],pix[1]],radius=4)
        if enemy_bulletsize:
            for pix in enemy_bulletsize:
                pygame.draw.circle(gamesurface,red_color,[pix[0],pix[1]],radius=4)
        if bossbulletsize:
            if enemy_bulletsize:
                for pix in bossbulletsize:
                    pygame.draw.circle(gamesurface,red_color,[pix[0],pix[1]],radius=4)
        if reward:
            for pix in reward:
                if pix[2] == 1:
                    pygame.draw.polygon(gamesurface,blue_color,[[pix[0]-10,pix[1]],
                                                                [pix[0],pix[1]+10],
                                                                [pix[0]+10,pix[1]],
                                                                [pix[0],pix[1]-10]])
                if pix[2] == 2:
                    pygame.draw.polygon(gamesurface,green_color,[[pix[0]-10,pix[1]],
                                                                [pix[0],pix[1]+10],
                                                                [pix[0]+10,pix[1]],
                                                                [pix[0],pix[1]-10]])
                if pix[2] == 3:
                    pygame.draw.polygon(gamesurface,red_color,[[pix[0]-10,pix[1]],
                                                                [pix[0],pix[1]+10],
                                                                [pix[0]+10,pix[1]],
                                                                [pix[0],pix[1]-10]])

        score_ = str(score)
        life_ = str(life)
        bosslife_ = str(bosslife)
        
        gameshow_font = pygame.font.SysFont('MicrosoftYaHei',20)
        gameshow_color = gameshow_font.render(f"Now Score:{score_}",True,orange_color)
        gameshow_location = gameshow_color.get_rect()
        gameshow_location.midtop = (80,40)
        gamesurface.blit(gameshow_color,gameshow_location)
        
        gameshow_color = gameshow_font.render(f"Now Life:{life_}",True,green_color)
        gameshow_location = gameshow_color.get_rect()
        gameshow_location.midtop = (80,80)
        gamesurface.blit(gameshow_color,gameshow_location)
        
        gamesurface.blit(block_img,[agentSize[0][0]-10,agentSize[0][1]-10])
        
        if boss:
            gameshow_font = pygame.font.SysFont('MicrosoftYaHei',20)
            gameshow_color = gameshow_font.render(f"BossLife:{bosslife_}",True,red_color)
            gameshow_location = gameshow_color.get_rect()
            gameshow_location.midtop = (710,10)
            gamesurface.blit(gameshow_color,gameshow_location)
               
        pygame.display.update()
        ftpsClock.tick(40)
        if life < 0:
            return score

"主程序"
while True:
    gamestart()
    #启动游戏界面
    score = main()
    #进入main函数开始游戏主题循环，游戏结束返回分数
    b = gameover(score)
    #进入gameover界面，显示得分，并返回一个是否退出的bool值b
    #以下为是否退出游戏判定
    if b:
        pygame.quit()
        sys.exit()
        break