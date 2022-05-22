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
#以上是全局变量用来设置配置的RGB颜色
def destory(li,tag_id):
        '''
        li为存储敌人的列表，tag_id为标记的敌人对象列表样式,以提供remove函数的参数
        删除列表被标记对象
        del_num用于统计被标记对象的个数，便于后续设置删除循环上限次数
        '''
        del_num = 0
        for i in range(len(li)):
            if li[i][0] == 'destory':
                del_num+=1
        for i in range(del_num):
            li.remove(tag_id)
        return None
            
def tag_destory(li):
    "对li列表标记替换并返回li列表,作用：标记可迭代对象所有值为destory"
    for i in range(len(li)):
        li[i] = 'destory'
    return li
            
def gamestart():
    '''
    游戏开始界面
    p键进入游戏
    注释了渲染页面的方法，以及更新游戏帧方法
    '''
    pygame.init()
    #pygame模块初始化
    pygame.time.Clock()
    #pygame模块提供的时钟方类，初始化
    ftpsClock = pygame.time.Clock()
    #创建时钟类的对象
    gamesurface = pygame.display.set_mode((1920,1080), FULLSCREEN, HWSURFACE)
    #设置窗口尺寸,全屏
    pygame.display.set_caption('测试游戏')
    #设置窗口名字
###############################################################################
    while True:
        "开始游戏函数主循界面"
        gameshow_font = pygame.font.SysFont('MicrosoftYaHei',25)
        #设置字体格式
        gameshow_color = gameshow_font.render("Press 'q' Start Game",True,white_color)
        #设置显示样式与字符串
        gameshow_location = gameshow_color.get_rect()
        #调用处理矩形图样处理方法
        gameshow_location.midtop = (740,320)
        #设置显示坐标
        gamesurface.blit(gameshow_color,gameshow_location)
        #绘制渲染内容
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.type == QUIT:
                   return 1
                if event.key == K_q:
                    return 0
        #监听游戏，如果接收到按键按下操作，对按键进行判断，q键开始游戏，esc退出游戏
        pygame.display.update()
        #更新当前循环页面，刷帧，更新帧    
    return None
def gameover(score):
    '''
    游戏结算页面，返回b值，用于主函数判断是否退出游戏程序
    原理同gamestart函数
    '''
    pygame.init()
    pygame.time.Clock()
    ftpsClock = pygame.time.Clock()
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
    #以上代码同理开始游戏函数注释
        
def main():
    pygame.init()
    #初始化pygame模块
    pygame.mixer.init()
    #初始化pygame音效模块
    s_fire = pygame.mixer.Sound("voice_fire.mp3")
    #调用音效模块sound方法，调用程序所在同级文件夹内的MP3资源文件，s_fire作为次方法的实例
    pygame.mixer.music.load("DarkSeaSide.mp3")
    #调用音效模块music类load方法，用于布局背景音乐
    pygame.mixer.music.play(-1,1)
    #播放载入的背景音乐，-1参数不断循环播放
    pygame.time.Clock()
    ftpsClock = pygame.time.Clock()
    #创建游戏时钟对象
    gamesurface = pygame.display.set_mode((1920,1080),FULLSCREEN,HWSURFACE)
    #创建窗口,设置窗口尺寸
    pygame.display.set_caption('测试游戏')
    agentSize = [[690,740],[710,740],[730,740]]
    #游戏用户，列表对象，存有每个渲染像素块的坐标，20pix为一个大的渲染区块
    boss = []
    #boss定义，初始化为空列表
    bulletsize = []
    #玩家子弹列表，初始化
    enemy_bulletsize = []
    #敌人子弹列表，初始化
    enemy = []
    #敌人对象列表，初始化
    reward = []
    #奖励道具列表，初始化
    bosslevel = 1
    #游戏boss等级，计分板
    bossdirection = 0
    #游戏boss位移方向变量，bool类型，初始化
    bosslife = 100
    #boss初始生命值
    bossbulletsize = []
    #boss子弹列表，初始化
    press_tag = 0
    #用于记录当前用户方向键是否全部弹起，初始化，0：全部弹起
    score = 0
    #游戏得分计数器，初始化
    enemy_limit = 2
    #游戏生成敌人数量限制
    enemy_speed = 5
    #敌人移动速度，沿y轴向下5pix每帧，初始化
    enemy_summon_limit = 10
    #敌人生成时间间隔
    buff = [0,0,0]
    #buff触发开关列表，0：是否获得弹数加成，1：生命值buff，2：连发buff
    fire_buff = 0
    #是否获得连发加成
    life = 5
    #玩家生命值，初始化
    MouseButton = 0
    #记录鼠标是否按下，布尔值，初始化
    skill_down = 0
    #记录技能是否使用，按键Space，布尔值，初始化
    change_direction = [0,0,0,0]
    #方向值开关列表，序列0，1，2，3映射上下左右
    gametick= [0,0,0,0,0,0,0,0,0,0,0,0,20,0]
    #计数器列表集，时间相关,0:子弹发射间隔，1:敌人生成间隔，2:游戏存活时间,3:敌人子弹刷新时间,4:奖励存活时间,5:buff存活时间,6:受伤免疫时间,7:敌人位移决定时间
    #8:buff3火力时间,9:buff3声音参数,10:游戏累计时间,11:群军进攻时间,12:skill技能冷却,13:boss受到攻击的频率上限
    press_order = []
    #记录玩家历史输入方向列表，初始化
    color_tag = 0
    #记录是否渐变的标签，布尔值，初始化
    r = 255
    #颜色rgb通道值，初始化
    add = 1
    #渐变方向，1代表递减，布尔值，初始化
    black_color = pygame.Color(0,0,0)
    white_color = pygame.Color(255, 255, 255)
    #颜色局部变量，游戏main主体作用域使用
###############################################################################
    "图像渲染"
    block_img = pygame.image.load("block.png")
    # enemy_img = pygame.image.load("enemy.png")
    #贴图资源文件载入
###############################################################################   
    while True:
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
        #击杀boss界面颜色渐变功能，color_tag为渐变开关，add为渐变方向开关，直到达到r值达到0或255结束渐变
###############################################################################
        gametick = list(map(lambda x:x+1, gametick))
        #对时间计数器列表每项+1，调用lambda函数
        if gametick[2]> 150:
            enemy_limit+=1
            gametick[2] = 0
        #每隔150个循环，敌人数量上限加1
        if gametick[10] > 2000 * (enemy_limit - 1) and enemy_limit < 30:
            enemy_limit+=1
        
###############################################################################
        "玩家控制模块"
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                MouseButton = 0
            #监听鼠标按键是否弹起
            if event.type == MOUSEBUTTONDOWN and gametick[0] > 8:
                MouseButton = 1
            #监听鼠标按键是否按下，8帧检测记录一次
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #监听esc键，判断是否退出
            elif event.type == KEYUP:
                #监听键盘弹起项目
                if event.key == K_SPACE:
                    skill_down = 0
                #监听空格键是否弹起，记录
                if event.key == K_RIGHT or event.key == K_d:
                    change_direction[3] = 0
                    try:
                        press_order.remove('3')
                    except:
                        ""
                    #监听按键d或者按键右是否弹起，记录，尝试从键位记录内的历史记录，3序列代表右
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
                #以上同理按键d，右
                if change_direction == [0,0,0,0]:
                    press_tag = 0
                #只有当所有控制键全部弹起才判断为完全静止，记录完全静止状态
            elif event.type == KEYDOWN:
                press_tag = 1
                #监听到按键按下项目，记录按键按下状态
                if event.key == K_RIGHT or event.key == K_d:
                    change_direction[3] = 1
                    press_order.append('3')
                #监听到按键d或按键右被按下，记录，并添加进按键历史记录
                if event.key == K_LEFT or event.key == K_a:
                    change_direction[2] = 1
                    press_order.append('2')
                if event.key == K_DOWN or event.key == K_s:
                    change_direction[1] = 1
                    press_order.append('1')
                if event.key == K_UP or event.key == K_w:
                    change_direction[0] = 1
                    press_order.append('0')
                #以上同理按键d，右
                if event.key == K_SPACE and gametick[12] > 15:
                    skill_down = 1
                #15帧监听一次空格键，记录
                if event.key == K_ESCAPE:
                #监听到esc，返回当前分数，结束main函数
                    return score
###############################################################################
        "奖励生成"
        if  gametick[4] > 600:
            x = random.randrange(1,70)*20
            y = random.randrange(40,50)*15
            t = random.randrange(1,4)*1
            reward.insert(0,[x,y,t])
            gametick[4] = 0
            #每600游戏帧生成一次奖励，(x,y)随机获取坐标，t为随机生成的奖励类型标签，有3种类型
            #将生成的奖励插入奖励列表内，重置计时器
        "敌人生成"
        if len(enemy)<enemy_limit and gametick[1] > enemy_summon_limit:
            x = random.randrange(1,70)*20
            y = -10 
            t = -1
            enemy.insert(0,[x,y,t])
            gametick[1] = 0
            if random.randrange(1,100)>60:
                enemy_bulletsize.insert(0,[enemy[0][0]+20,enemy[0][1]+40])
            #同理奖励生成，t标签记录敌人位移方向，初始化为-1，40%概率发射子弹，插入敌人子弹列表
        "boss生成"
        if gametick[10] > 3000 and score - bosslevel*200 > 0 and not boss:
            bosslevel+=1
            boss = [[690,140],[710,140],[730,140],bossdirection,bosslife]
            enemy_speed = 5
        #3k游戏帧后生成，满足不存在boss并且积分达到对应bosslevel值时触发生成，对敌人减速，boss等级增加1以备下次生成boss使用新的参数
        "敌人随机发射子弹"
        if len(enemy) > 3 and gametick[3] > 10:
            index = random.randrange(0,len(enemy)-1)
            if random.randrange(1,100)>80:
                enemy_bulletsize.insert(0,[enemy[index][0]+20,enemy[index][1]+40])
            gametick[3] = 0
        #满足超过3个敌人，每10游戏帧触发，抽取1名敌人，发射指定的敌人序列随机获取，20%概率触发，插入敌人子弹列表，重置计时器
        "boss发射子弹"
        if boss and gametick[3] > 5:
            if random.randrange(1,100)>80:
                bossbulletsize.insert(0, [boss[1][0]+10,boss[1][1]+30])
            if random.randrange(1,200) > 190:
                bossbulletsize.insert(0, [boss[0][0]+10,boss[0][1]+30])
                bossbulletsize.insert(0, [boss[2][0]+10,boss[2][1]+30])
        #如果存在boss，每5游戏帧触发，20%概率发射子弹，5%触发双连射，插入boss子弹列表
###############################################################################
        "玩家事件"
        "发射子弹"
        if MouseButton == 1 and gametick[0] > 8:
            s_fire.play()
            bulletsize.insert(0,[agentSize[1][0]+10,agentSize[1][1]-20])
            if buff[0] == 1:
                buff_bull_time+=1
                bulletsize.insert(0,[agentSize[0][0]+10,agentSize[0][1]-20])
                bulletsize.insert(0,[agentSize[2][0]+10,agentSize[2][1]-20])
            gametick[0] = 0
        #检测到鼠标按下记录，每8游戏帧触发，播放开火音效，插入子弹列表，如果buff0触发，计数器+1，将双轨子弹插入子弹列表，重置计时器                                
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
        #对敌人列表遍历，对玩家子弹列表遍历，判断敌人与子弹之间的距离，如果x，y满足在规定范围内判断击毁敌人
        #将当前敌人元素呈递给tag_destory函数处理，返回处理后的tag_id,玩家积分+1，打破循环，尝试将敌人列表与tag_id呈递给destory函数处理
        #删除被标记的敌人元素
        "攻击boss"
        if gametick[13] >1:
            for pix_e in boss[0:3]:
                for pix_b in bulletsize:
                    if ((pix_e[0]+20 - pix_b[0])**2)**0.5 < 22 and ((pix_e[1]+7.5 - pix_b[1])**2)**0.5 < 15:
                        bosslife-=1
            gametick[13] = 0
        #每隔1帧游戏帧触发，对boss列表切片取前三项遍历，判定玩家子弹与boss坐标距离，满足规定距离范围则boss生命值-1，重置计时器
        "boss死亡"
        if boss and bosslife < 0:
            boss = []
            bosslife = bosslevel* 100
            enemy_speed = 10
            color_tag = 1
        #如果存在boss并且生命值小于0，则清空boss列表，boss生命值更新，敌人速度恢复，背景颜色渐变开关开启
        "吃到奖励"
        for pix in reward:
            if ((agentSize[1][0] -pix[0])**2)**0.5 < 40 and ((agentSize[1][1] - pix[1])**2)**0.5 < 30:
                
                if pix[2] == 1:
                    score+=15
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
                #对奖励列表遍历，检测玩家与奖励距离，满足距离规定范围则判定奖励列表内元素类型，积分增加15，启用buff，重置buff子弹数
                #对buff时间状态进行判断，在buff时效内继续累计buff时间，超出buff时效，重置buff时效，时效累计叠加状态下可以继续累加buff时效
                #对奖励对象进行标记并返回tag_id
                if pix[2] == 2:
                    score+=15
                    buff[1] = 1
                    tag_id = tag_destory(pix)
                #同上
                if pix[2] == 3:
                    score+=15
                    buff[2] = 1
                    if gametick[8] >=0 and gametick[8] <= 500:
                        gametick[8] -= 500
                    elif gametick[8] >500:
                        gametick[8] = 0
                    elif gametick[8] <0:
                        gametick[8] -= 500
                    tag_id = tag_destory(pix)
                #同上
        try:
            destory(reward,tag_id)
        except:
            ""
           #将奖励列表与tag_id呈递给destory函数处理，删除被标记奖励     
        "buff过期"
        if gametick[5] > 500:
            buff[0] = 0
            gametick[5] = 0
        if gametick[8] > 500:
            fire_buff = 0
            gametick[8] = 0
        #对过期的buff进行buff开关的关闭，赋值为0，重置计时器
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
        #玩家受伤，每50游戏帧检测一次，对敌人，敌人子弹，boss子弹，boss切片，进行遍历，与玩家进行距离判断决定生命值是否减少，重置计时器
        "奖励生效2"
        if buff[1] == 1:
            life+=1
            buff[1] = 0
        #奖励内容，生命值+1，立即生效，奖励开关关闭
        "奖励生效3"
        if buff[2] == 1:
            fire_buff = 1
            buff[2] = 0
        #奖励内容，开启连射buff开关。奖励开关关闭   
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
        #奖励3具体内容，每5帧自动发射子弹，如果在奖励1叠加状态下自动连发双规子弹，插入子弹列表    
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
        #每50帧触发，如果存在敌人元素，遍历，30%概率触发位移，左右方向各50%概率，标记决定位移标签t的值，重置计时器
        #如果存在boss，30%概率触发位移，左右位移概率各50%，标记标签
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
         #敌人群体攻击事件，触发概率为1/2000，在1k游戏帧后触发
         #持续200游戏帧，如果敌人生成限制为1，敌人数限制减小，敌人速度设置为10，敌人生成限制设置为10
        "使用技能"
        if skill_down == 1:
            s_fire.play()
            skill_down = 0
            gametick[12] = 0
            bulletsize.insert(0,[agentSize[1][0]+30,agentSize[1][1]-20])
            bulletsize.insert(0,[agentSize[1][0]+60,agentSize[1][1]-20])
            bulletsize.insert(0,[agentSize[1][0]-10,agentSize[1][1]-20])
            bulletsize.insert(0,[agentSize[1][0]-40,agentSize[1][1]-20])
        #播放音效，重置开关，重置计时器，生成4枚并排子弹，插入子弹列表
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
        #如果玩家处于地图边界，对向边界外位移的方向开关进行关闭
        for pix in bulletsize:
            if pix[1]<=0:
                bulletsize.pop()
        for pix in enemy:
            if pix[1]>=760:
                enemy.pop()
        for pix in bossbulletsize:
            if pix[1] <=0:
                bossbulletsize.pop()
        #对超出边界的子弹元素进行清理 
###############################################################################
        "改变坐标,移动轨迹"
        #判断是移动时按下空格还是静止时按下空格
        for pix in bossbulletsize:
            pix[1]+=15
        for pix in enemy_bulletsize:
            pix[1]+=20
        for pix in bulletsize:
            pix[1]-=10
        #对各种子弹坐标进行修改
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
        #对buff0的双轨子弹进行坐标改变，x坐标改变
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
        #对玩家方向记录进行检测，按照对应方向开关项改变坐标，控制上下左右
        #对敌人位移坐标进行改变
        "敌人位移"
        if enemy:
            for pix in enemy:
                if pix[0] > 10 and pix[0] < 1490:
                    if pix[2] == 1:
                        pix[0]+=5
                    elif not pix[2]:
                        pix[0]-=5
        #如果存在敌人元素，对游戏界面范围内的敌人进行x坐标改变，左右移动
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
        #如果存在boss，对boss的x坐标进行检测，超出游戏界面范围则执行方向修正
        #按照位移方向对boss进行坐标改变
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
        #如果上下同时按住，尝试查看历史按键记录，index0记录上按键历史序列值，index1记录下按键历史序列值
        #将旧的方向开关设置为0，保留新的方向开关
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
        #同上
###############################################################################
        "绘制图像"
        gamesurface.fill(black_color)
        #填充背景颜色
        if boss:
            pygame.draw.polygon(gamesurface,red_color,[[boss[0][0],boss[0][1]],
                                                         [boss[0][0]+20,boss[0][1]],
                                                         [boss[0][0]+20,boss[0][1]+20]])
            pygame.draw.polygon(gamesurface,red_color,[[boss[2][0],boss[2][1]],
                                                         [boss[2][0]+20,boss[2][1]],
                                                         [boss[2][0],boss[2][1]+20]])
            pygame.draw.rect(gamesurface,red_color,Rect(boss[1][0],boss[1][1]+5,20,10))
        #绘制boss图像，用pygame的不规则图形与矩形方法绘制boss简图
        if enemy:
            for pix in enemy:
                pygame.draw.polygon(gamesurface,white_color,[[pix[0],pix[1]],[pix[0]+40,pix[1]],[pix[0]+20,pix[1]+15]])
        #对敌人列表里的所有敌人元素进行绘制简图
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
        #对子弹进行绘制
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
        #对不同奖励按照不同颜色进行绘制
        score_ = str(score)
        life_ = str(life)
        bosslife_ = str(bosslife)
        #将整型数据字符串化
        gameshow_font = pygame.font.SysFont('MicrosoftYaHei',20)
        gameshow_color = gameshow_font.render(f"Now Score:{score_}",True,orange_color)
        gameshow_location = gameshow_color.get_rect()
        gameshow_location.midtop = (80,40)
        gamesurface.blit(gameshow_color,gameshow_location)
        #渲染显示的字符串内容
        gameshow_color = gameshow_font.render(f"Now Life:{life_}",True,green_color)
        gameshow_location = gameshow_color.get_rect()
        gameshow_location.midtop = (80,80)
        gamesurface.blit(gameshow_color,gameshow_location)
        #渲染显示的字符串内容
        gamesurface.blit(block_img,[agentSize[0][0]-10,agentSize[0][1]-10])
        #用载入的飞船贴图文件渲染玩家飞船
        if boss:
            gameshow_font = pygame.font.SysFont('MicrosoftYaHei',20)
            gameshow_color = gameshow_font.render(f"BossLife:{bosslife_}",True,red_color)
            gameshow_location = gameshow_color.get_rect()
            gameshow_location.midtop = (710,10)
            gamesurface.blit(gameshow_color,gameshow_location)
        #如果存在boss，渲染显示boss生命值       
        pygame.display.update()
        #更新当前帧
        ftpsClock.tick(40)
        #设置游戏帧数
        if life < 0:
            return score
        #玩家生命值耗尽，返回积分，进入游戏结算
"主程序"
while True:
    gamestart()
    #启动游戏界面
    score = main()
    #进入main函数开始游戏主题循环，游戏结束返回分数
    b = gameover(score)
    #进入gameover界面，显示得分，并返回一个是否退出的bool值b
    if b:
        pygame.quit()
        sys.exit()
        break
    #判断是否退出游戏