import random
from player_agent import LLM_player
import json
from openai import OpenAI

client = OpenAI(
    api_key="sk-ebd93d5dc05c4c81a589037f7b85fcd1",
    base_url="https://api.deepseek.com"
)


prompt = """
{
  "随机词生成系统": {
    "随机化引擎": {
      "种子来源": [
        "系统时间毫秒级哈希",
        "公开API实时数据（如天气/股价最后一位）",
        "维基百科随机页面标题首字符ASCII码"
      ],
      "分类轮盘": {
        "基础类别": ["生活用品", "自然现象", "职业", "抽象概念", "科技产品"],
        "筛选条件": "排除专业术语（频率<100万/Google搜索结果）"
      }
    },
    "词语配对算法": {
      "相似维度": [
        {"物理特征": "形状/材质/颜色相似度≥60%"},
        {"功能属性": "使用场景重叠度40-70%"},
        {"情感联想": "激发同类情绪（如浪漫/恐惧）"}
      ],
      "差异锚点": [
        "核心功能差异",
        "文化认知冲突",
        "规模量级差异"
      ],
      "娱乐性强化": [
        "包含意外反转",
        "存在经典误解",
        "触发联想竞赛"
      ]
    },
    "输出规范": {
      "必含字段": {
        "玩家词": "符合大众认知的高频词",
        "卧底词": "满足相似但可辩驳的关联词",
        "关联说明": "20字内解释相似点+差异点"
      },
  },

请使用json格式输出结果,且仅给出以下格式的输出
      "玩家词": 
      "卧底词": 
      "关联说明": 
}
"""

def game_res_judge(votes):
    if not votes:
        return -1

        # 统计每个数字出现的频率
    frequency = {}
    for num in votes:
        if num in frequency:
            frequency[num] += 1
        else:
            frequency[num] = 1

    # 找出最高频率
    max_freq = max(frequency.values())

    # 找出所有出现次数等于max_freq的数字
    most_frequent_numbers = [num for num, count in frequency.items() if count == max_freq]

    # 检查条件：多个最高频数字，或者最高频数字是0
    if len(most_frequent_numbers) > 1 or (len(most_frequent_numbers) == 1 and most_frequent_numbers[0] == 0):
        return -1
    else:
        return most_frequent_numbers[0]

def game(n,chameleons,word,chameleon_word):
    rounds = 2  #总轮数
    print(f'玩家词：{word},变色龙词：{chameleon_word}')
    players = []
    speak_history = []
    vote_history = []
    c_pos = 0
    for i in range(n):
        if i < chameleons:
            p = LLM_player(chameleon_word)

        else:
            p = LLM_player(word)
        players.append(p)
    random.shuffle(players)

    for i, p in enumerate(players):
        p.pos = i+1
        if p.word == chameleon_word:
            print(f'\033[31m变色龙是{p.pos}号\033[0m') # "\033[31m这是红色文本\033[0m"
            c_pos = p.pos


    for i in range(rounds):
        s = f'第{i+1}轮开始'
        print(s)
        speak_history.append(s)
        ###回答环节
        for p in players:
            chat, think = p.talk(i, speak_history)
            s = f'玩家{p.pos}:{chat}'
            #print(s)
            speak_history.append(s)

        votes = []
        for p in players:
            r,think = p.vote(i, speak_history, vote_history)
            votes.append(r)
        vote_history.append(votes)

        ###需要判断投票结果
        print(f'第{i+1}轮投票结果是:{votes}')
        res = game_res_judge(votes)


        if res == -1 and i+1 != rounds:
            s = f'第{i+1}轮投票没有结果！'
            print(s)
            speak_history.append(s)
            continue
        elif res == -1 and i+1 == rounds:
            s = f'最后一轮投票未投出变色龙！变色龙获胜！'
            print(s)
            speak_history.append(s)
        else:
            s = f'第{i+1}轮投票结果：被投出的是{res}号！'
            print(s)
            speak_history.append(s)
            if res == c_pos:
                s = f'{res}号是变色龙！玩家阵营获胜！'

                print(s)
                speak_history.append(s)
                break
            else:
                s = f'{res}号不是变色龙！变色龙阵营获胜！'

                print(s)
                speak_history.append(s)
                break


def word_initer():
    messages = [{"role": "system", "content": prompt}]
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=True,
        response_format={
            'type': 'json_object'
        },
    )

    collected_chunks = []
    for chunk in response:
        if chunk.choices[0].delta.content:
            collected_chunks.append(chunk.choices[0].delta.content)

    # 合并所有块内容
    full_response = "".join(collected_chunks)

    # 解析JSON
    response_json = json.loads(full_response)
    print(response_json)
    # 提取玩家选择
    word = response_json.get("玩家词")
    chameleon_word = response_json.get("卧底词")
    return word, chameleon_word

def word_initer1():
    return '公园', '马路'

if __name__ == "__main__":
    print('游戏开始')
    word, chameleon_word = word_initer1()

    n = 4
    chameleons = 1
    game(n, chameleons, word, chameleon_word)
    print('游戏结束！')
