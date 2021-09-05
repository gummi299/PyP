from os import name
from urllib.parse import urlencode, quote_plus #인터넷 관련
from bs4 import BeautifulSoup
from discord import file 
from discord.ext import commands #디스코드 봇 커맨드 관련
from datetime import datetime,timedelta
import matplotlib
import requests #인터넷에서 값 받아오는 모듈
import pandas as pd #DATAFRAME
import bs4 #XML 관련
import asyncio #디스코드 관련 모듈
import discord #디스코드 관련 모듈
import matplotlib.pyplot as plt #차트 관련
import seaborn as sns #차트 관련
import time as t
import random as r
 
nameList = ['확진자','확진율','생성날짜','치명률','사망','사망률','구분','번호','업데이트'] #통계에 쓰일 배열
indexList=['0-9','10-19','20-29','30-39','40-49','50-59','60-69','70-79','80+','여성','남성'] #구분에 쓰일 배열
chartList_1=['성별','연령별'] #차트에 쓰일 배열
chartList_2=['확진율','사망률','치명률'] #차트에 쓰일 배열
s_list=['남성','여성'] # 성별에 쓰일 배열
ag_list=['0-9','10-19','20-29','30-39','40-49','50-59','60-69','70-79','80+'] # 연령별에 쓰일 배열
emojiList=[':baby:',':child:',':boy:',':adult:',':adult:',':adult:',':older_adult:',':older_adult:',':older_adult:',':woman:',':man:'] #구분 이모지

rowList = []
columnList = []
apinameList=[]

apidate=''
displaydate=''

result=pd.DataFrame()

ratio=[1,1]
ratio_1=0
ratio_2=0
ratio_1_1=0
ratio_1_2=0
ratio_1_3=0
ratio_1_4=0
ratio_1_5=0
ratio_1_6=0
ratio_1_7=0
ratio_1_8=0
ratio_1_9=0
filename=''
ratio_list=[]

def pltconfig_default():
    sns.reset_defaults()

def xy(x,y): # 성별 pie 차트 함수
    pltconfig_default()
    print(ratio)
    labels = [s_list[0],s_list[1]]
    plt.rc('font', family='Malgun Gothic')
    colors = ['#ff9999', '#ffc000', '#8fd9b6', '#d395d0','#17becf','#bcbd22','#7f7f7f','#e377c2','#8c564b']
    wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}
    plt.rcParams['font.size']=20
    plt.rc('axes', labelsize=60)
    plt.title('<코로나 '+chartList_1[x]+' '+chartList_2[y]+' 차트>')
    plt.pie(ratio, labels=labels, autopct='%.1f%%', startangle=260, counterclock=False, colors=colors, wedgeprops=wedgeprops)
    plt.legend(bbox_to_anchor=(0.12,0.225))
    plt.savefig(filename)
    plt.close()

def xy_2(x,y): # 연령별 pie 차트 함수
    pltconfig_default()
    print(ratio)
    labels = [ag_list[0],ag_list[1],ag_list[2],ag_list[3],ag_list[4],ag_list[5],ag_list[6],ag_list[7],ag_list[8]]
    plt.rc('font', family='Malgun Gothic')
    colors = ['#ff9999', '#ffc000', '#8fd9b6', '#d395d0','#17becf','#bcbd22','#7f7f7f','#e377c2','#8c564b']
    wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}
    plt.rcParams['font.size']=11
    plt.title('<코로나 '+chartList_1[x]+' '+chartList_2[y]+' 차트>')
    plt.pie(ratio, labels=labels, autopct='%.1f%%', startangle=260, counterclock=False, colors=colors, wedgeprops=wedgeprops)
    plt.legend(bbox_to_anchor=(0,0.5))
    plt.savefig(filename)
    plt.close()

def xy_3(x,y): # 연령별 막대 차트 함수
    pltconfig_default()
    print(ratio)
    labels = [ag_list[0],ag_list[1],ag_list[2],ag_list[3],ag_list[4],ag_list[5],ag_list[6],ag_list[7],ag_list[8]]
    plt.rc('font', family='Malgun Gothic')
    colors = sns.color_palette('hls',len(labels))

    plt.rc('xtick', labelsize=70)
    plt.rc('ytick', labelsize=70)
    plt.rc('axes', labelsize=90)
    plt.rc('legend', fontsize=60)

    fig= plt.figure(figsize=(30,30))
    ax = fig.add_subplot() 
    xtick_label_position = list(range(len(labels)))
    plt.xticks(xtick_label_position, labels)
    bars= plt.bar(xtick_label_position, ratio, color=colors, edgecolor=colors, alpha=0.7, linewidth=4)
    for i, b in enumerate(bars):
        ax.text(b.get_x()+b.get_width()*(1/2),b.get_height()+0.1, \
                ratio[i],ha='center',fontsize=55)

    plt.title('<코로나 '+chartList_1[x]+' '+chartList_2[y]+' 차트>', fontsize=110,)
    plt.xlabel(chartList_1[x]) 
    plt.ylabel(chartList_2[y]+"%")
    ax.legend(handles=bars,labels=list(labels))
    plt.savefig(filename)
    plt.close()

##---API 함수 시작---##
def GetAPI(setDate):
    global nameList
    global indexList
    global emojiList
    global rowList
    global columnList
    global apinameList
    global apidate
    global result
    global displaydate
    global chartList_1
    global chartList_2
    global ratio
    global ratio_1
    global ratio_2

    if setDate==True:
    #API 불러올 날짜 설정
        if datetime.today().hour>=15:
            apidate=datetime.today().strftime("%Y%m%d")
        else:
            yesterday = datetime.today() - timedelta(1)
            apidate=yesterday.strftime("%Y%m%d")
    displaydate=datetime.strptime(apidate,"%Y%m%d").strftime("%Y-%m-%d")
    #API 호출 링크
    apikey="API_KEY"
    Url ='http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19GenAgeCaseInfJson?serviceKey=' + apikey + '&pageNo=1&numOfRows=10&startCreateDt=' + apidate + '&endCreateDt=' +apidate

    #API 받아오기
    res = requests.get(Url).text

    #API XML로 변환
    xmlobj = bs4.BeautifulSoup(res, 'lxml-xml')
    rows = xmlobj.findAll('item')

    #API 세부 값 받아올 배열
    rowList = []
    columnList = []
    apinameList=[]

    #API 세부 값 불러오기
    rowsLen = len(rows)
    for i in range(0, rowsLen):
        columns = rows[i].find_all()
        columnsLen = len(columns)
        for j in range(0, columnsLen):
            if i == 0:
                apinameList.append(columns[j].name)
            eachColumn = columns[j].text
            columnList.append(eachColumn)
        rowList.append(columnList)
        columnList = []    

    #결과값 변수 = result
    result = pd.DataFrame(rowList, columns=nameList,index=indexList)
##---API 함수 끝---##

#API 불러오기
GetAPI(True)

#디스코드 봇
client= commands.Bot(command_prefix='/') #명령어 접두어
token="BOT_TOKEN"

#디스코드 봇 로그인 부분
@client.event
async def on_ready():
    print("다음으로 로그인 합니다")
    print(client.user.name)
    print(client.user.id)

#디스코드 봇 명령어 처리 부분
@client.command()
async def 코로나(ctx,*txt):
    commandtype=txt[0]
    gubun=txt[1]
    if commandtype=='구분':
        #입력된 구분의 통계가 존재하면
        if gubun in indexList:
            embed=discord.Embed(title='코로나 ' + emojiList[indexList.index(gubun)] + gubun +  ' 통계')
            embed.set_footer(text='코로나알리미👀')
            embed.set_author(name=displaydate + '기준')
            embed.add_field(name='확진자',value=result.loc[gubun]['확진자'],inline=True)
            embed.add_field(name='확진율',value=result.loc[gubun]['확진율'] + '%',inline=True)
            embed.add_field(name='치명률',value=result.loc[gubun]['치명률'] + '%',inline=True)
            embed.add_field(name='사망',value=result.loc[gubun]['사망'],inline=True)
            embed.add_field(name='사망률',value=result.loc[gubun]['사망률'] + '%',inline=True)
            await ctx.send(embed=embed)
        elif gubun=='전체':
            col=len(result['확진자'])
            row=len(result.loc['0-9'])
            embed=discord.Embed(title='코로나 전체 통계')
            embed.set_footer(text='코로나알리미👀')
            embed.set_author(name=displaydate + '기준')

            for s in range(col):
                txt=''
                for i in [0,1,3,4,5]:
                    txt=txt + '\n' + nameList[i] + ': ' + result.loc[indexList[s]][nameList[i]]
                embed.add_field(name=emojiList[s] + indexList[s],value=txt,inline=True)
            await ctx.send(embed=embed)
        else: #존재하지 않으면
            embed=discord.Embed(title='아쉽지만 ' + gubun + ' 라는 구분은 존재하지 않습니다...')
            embed.add_field(name="사용 가능한 구분",value='`' + "`, `".join(indexList) + '`')
            embed.set_footer(text='코로나알리미👀')
            await ctx.send(embed=embed)
    
    
    if commandtype=='통계':
        #입력된 구분의 통계가 존재하면
        if gubun in nameList:
            lis=result[gubun]
            embed=discord.Embed(title='코로나 ' + gubun + ' 통계')
            embed.set_footer(text='코로나알리미👀')
            embed.set_author(name=displaydate + '기준')
            for s in range(len(lis)):
                embed.add_field(name=emojiList[s] + indexList[s],value=lis[s],inline=True)
            await ctx.send(embed=embed)
        elif gubun=='전체':
            col=len(result['확진자'])
            row=len(result.loc['0-9'])
            embed=discord.Embed(title='코로나 전체 통계')
            embed.set_author(name=displaydate + '기준')
            embed.set_footer(text='코로나알리미👀')

            for s in [0,1,3,4,5]:
                txt=''
                for i in range(col):
                    txt=txt + '\n' + emojiList[i] + indexList[i] + ': ' + result.loc[indexList[i]][nameList[s]]
                embed.add_field(name=nameList[s],value=txt,inline=True)
            await ctx.send(embed=embed)
        else: #존재하지 않으면       
            embed=discord.Embed(title='아쉽지만 ' + gubun + ' 에 대한 통계는 존재하지 않습니다...')
            embed.add_field(name="사용 가능한 통계",value='`' + "`, `".join(nameList) + '`')
            embed.set_footer(text='코로나알리미👀')
            await ctx.send(embed=embed)
    if len(txt)==3:       
        if commandtype=='차트':
                global filename
        global ratio
        chart_1=txt[1]
        chart_2=txt[2]
        if commandtype=='차트':
            #입력된 구분의 차트가 존재하면
            if chart_1 in chartList_1: 
                if chart_2 in chartList_2:
                    if chart_1==chartList_1[0]: #CHART_1==성별 
                        x=0
                        for q in range(3):
                            q_2=q
                            if chart_2==chartList_2[q_2]:
                                y=q_2   
                                ratio_1=float(str(result.loc['여성',chartList_2[y]]))
                                ratio_2=float(str(result.loc['남성',chartList_2[y]]))
                                            
                                ratio = [ratio_1,ratio_2]      
                                print(ratio)
                                filename = 'Coronavirus_Chart'+str(r.randint(0,1000))+str(r.randint(0,1000))+".png"      
                                xy(x,y)
                                t.sleep(1)
                                image = discord.File(filename)
                                embed = discord.Embed(title='코로나 '+chartList_1[x]+' '+chartList_2[y]+' 차트')
                                embed.set_author(name=displaydate + '기준')
                                embed.set_footer(text='코로나알리미👀')
                                print(filename,type(filename))
                                print(filename)
                                embed.set_image(url="attachment://"+filename)
                                await ctx.send(embed = embed,file=image)
                
                    elif chart_1==chartList_1[1]: #CHART_1=연령별 
                        ratio_list=[]
                        x=1
                        for q in range(3):
                            q_3=q
                            if chart_2==chartList_2[q_3]:
                                y=q_3
                                if chart_2==chartList_2[0] or chart_2==chartList_2[1]:


                                    for i in range(len(ag_list)):
                                        
                                        confCaseRate=float(str(result.loc[ag_list[i],chartList_2[y]]))
                                        ratio_list.insert(i,float(confCaseRate)) 

                                                
                                    print(ratio_list)           
                                    ratio = [ratio_list[0],ratio_list[1],ratio_list[2],ratio_list[3],ratio_list[4],ratio_list[5],ratio_list[6],ratio_list[7],ratio_list[8]]      
                                    print(ratio)
                                    filename = 'Coronavirus_Chart'+str(r.randint(0,1000))+str(r.randint(0,1000))+".png"     
                                    xy_2(x,y)
                                    t.sleep(1)
                                    image = discord.File(filename)
                                    embed = discord.Embed(title='코로나 '+chartList_1[x]+' '+chartList_2[y]+' 차트')
                                    embed.set_author(name=displaydate + '기준')
                                    embed.set_footer(text='코로나알리미👀')
                                    print(filename,type(filename))
                                    print(filename)
                                    embed.set_image(url="attachment://"+filename)
                                    await ctx.send(embed = embed,file=image)
                                    

                                elif chart_2==chartList_2[2]:     #치명률 차트
                                    for i in range(len(ag_list)):
                                                                        
                                        criticalRate=float(str(result.loc[ag_list[i],chartList_2[2]]))
                                        ratio_list.insert(i,float(criticalRate)) 
                                        
                                    print(ratio_list)           
                                    ratio = [ratio_list[0],ratio_list[1],ratio_list[2],ratio_list[3],ratio_list[4],ratio_list[5],ratio_list[6],ratio_list[7],ratio_list[8]]      
                                    print(ratio)
                                    filename = 'Coronavirus_Chart'+str(r.randint(0,1000))+str(r.randint(0,1000))+".png"     
                                    xy_3(x,y)
                                    t.sleep(1)
                                    image = discord.File(filename)
                                    embed = discord.Embed(title='코로나 '+chartList_1[x]+' '+chartList_2[y]+' 차트')
                                    embed.set_author(name=displaydate + '기준')
                                    embed.set_footer(text='코로나알리미👀')
                                    print(filename,type(filename))
                                    print(filename)
                                    embed.set_image(url="attachment://"+filename)
                                    await ctx.send(embed = embed,file=image)
                else: #존재하지 않으면       
                        embed=discord.Embed(title='아쉽지만 ' + gubun + ' 에 대한 차트는 존재하지 않습니다...')
                        embed.add_field(name="사용 가능한 통계",value='`' + "`, `".join(chartList_2) + '`')
                        embed.set_footer(text='코로나알리미👀')
                        await ctx.send(embed=embed)
            else: #존재하지 않으면       
                    embed=discord.Embed(title='아쉽지만 ' + gubun + ' 에 대한 차트는 존재하지 않습니다...')
                    embed.add_field(name="사용 가능한 통계",value='`' + "`, `".join(chartList_1) + '`')
                    embed.set_footer(text='코로나알리미👀')
                    await ctx.send(embed=embed)


#도움말 명령어
@client.command()
async def 도움말(ctx):
    embed=discord.Embed(title='도움말')
    embed.set_footer(text='코로나알리미👀')
    embed.add_field(name="/코로나 구분 `[구분]`",value='`전체`, `' + "`, `".join(indexList) + '`',inline=False)
    embed.add_field(name="/코로나 통계 `[통계]`",value='`전체`, `' + "`, `".join(nameList) + '`',inline=False)
    embed.add_field(name="/코로나 차트 `[구분]` `[통계]`",value='`구분:`, `' + "`, `".join(chartList_1) + '`'"\n" + '`통계:`, `' + "`, `".join(chartList_2) + '`',inline=False)
    embed.add_field(name='/도움말',value='`/도움말`',inline=False)
    embed.add_field(name='/api show `[...]`',value='`dataframe` : api 데이터를 보여줍니다. \n `date` : api 데이터의 날짜를 보여줍니다.',inline=False)
    embed.add_field(name='/api setdate `[date]`',value='api로 받아올 데이터의 날짜를 설정합니다. \n `YYYYMMDD` 형식으로 입력해야 합니다. (예시:`' + apidate +'`)',inline=False)
    await ctx.send(embed=embed)

#api 명령어
@client.command()
async def api(ctx,commandtype,param):
    global apidate
    if commandtype=='show':
        if param=='dataframe':
            await ctx.send(pd.DataFrame(rowList, columns=apinameList,index=indexList))
        if param=='date':
            await ctx.send(apidate)
    if commandtype=='setdate':
        apidate=datetime.strptime(param,"%Y%m%d").strftime("%Y%m%d")
        GetAPI(False)
        embed=discord.Embed(title='api 날짜가 변경되었습니다.',description='`' + displaydate + '`')
        embed.set_footer(text='코로나알리미👀')
        await ctx.send(embed=embed)


#명령어 오류 처리
@코로나.error
async def 코로나_error(ctx,error):
    embed=discord.Embed(title='`/도움말`을 참고해주세요.',description=str(error))
    embed.set_footer(text='코로나알리미👀')
    await ctx.send(embed=embed)
@api.error
async def api_error(ctx,error):
    embed=discord.Embed(title='오류입니다.',description='`' + str(error) + '`')
    embed.set_footer(text='코로나알리미👀')
    await ctx.send(embed=embed)

#디스코드 봇 실행
client.run(token)

