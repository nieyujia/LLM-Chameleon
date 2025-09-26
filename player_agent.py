import json
from openai import OpenAI
from pprint import pprint

client = OpenAI(
    api_key="your_api_key",     #此处我使用的是deepseek的
    base_url="https://api.deepseek.com"
)
think_prompt = """
{
  "游戏规则说明": {
    "基本机制": "这是一个包含两轮的社交推理游戏，玩家分为普通玩家和变色龙两种身份，变色龙身份只有一人。所有玩家初始均不知晓自己身份。",
    "关键词分配": {
      "普通玩家": "获得相同的关键词（描述某个特定事物）",
      "变色龙玩家": "有一个类似普通玩家的关键词，无法看到玩家关键词，需通过他人发言推断并伪装，只有一个变色龙玩家"
    },
    "回合流程": [
      "第一轮：所有玩家依次发表关于关键词的陈述（不得包含关键词本身）然后进入第一轮投票",
      "第二轮：重复发言环节后进入投票阶段"
    ],
    "胜负判定": {
      "人类胜利": "准确投票淘汰变色龙",
      "变色龙胜利": [
        "未被成功投票淘汰",
        "错误投票淘汰普通玩家"
      ]
    }
  },
  "玩家行为规范": {
    "发言要求": [
      "必须提供一定的描述词，但不一定需要描述关键词，比如察觉自己是变色龙则需要伪装",
      "如果发现自己和前面的人的关键词可能不同时，需要站队前面的人的关键词，不再描述自己的关键词"
      "禁止直接使用关键词或近义词",
      "需保持发言独特性（不与历史发言重复角度）",
      "变色龙需通过分析他人发言进行合理伪装"
      "伪装行为指：发现自己可能是变色龙时，对于其他人发言进行推理，猜测关键词，然后伪装自己的关键词是这个进行发言。"
    ],
    "身份推理建议": [
      "通过横向对比各轮发言的一致性",
      "注意描述角度的覆盖范围",
      "分析异常简略/模糊的表述"
      "当发现自己关键词和前面人的描述词不完全符合时，反思自己身份，尝试伪装"
    ]
  },
  "交互协议": {
    "输入信息": {
      "当前需要":思考
      "当前回合": "1/2",
      "你的关键词": "（或'变色龙'标识）",
      "历史发言": ["玩家A的发言", "玩家B的发言"]
    },
    "输出模板" 请使用json格式进行输出: {
      "思考": "基于当前信息对自身身份的推理及发言策略分析（100字内）",
      
    },
    "示例": {
      "输入场景": "关键词'图书馆'，历史发言包含'有很多书架的地方'",
      "合格输出": {
        "思考": "已有发言涉及物理特征，我选择从功能角度补充，前面玩家的描述和我的关键词相符，我应该是人类阵营，正常描述即可",
       
      },
      "违规输出": {
        "思考": "直接引用历史发言",
      }
    }
  }
}
"""
talk_prompt = """
{
  "游戏规则说明": {
    "基本机制": "这是一个包含两轮的社交推理游戏，玩家分为普通玩家和变色龙两种身份，变色龙身份只有一人。所有玩家初始均不知晓自己身份。",
    "关键词分配": {
      "普通玩家": "获得相同的关键词（描述某个特定事物）",
      "变色龙玩家": "有一个类似普通玩家的关键词，无法看到玩家关键词，需通过他人发言推断并伪装，只有一个变色龙玩家"
    },
    "回合流程": [
      "第一轮：所有玩家依次发表关于关键词的陈述（不得包含关键词本身）然后进入第一轮投票",
      "第二轮：重复发言环节后进入投票阶段"
    ],
    "胜负判定": {
      "人类胜利": "准确投票淘汰变色龙",
      "变色龙胜利": [
        "未被成功投票淘汰",
        "错误投票淘汰普通玩家"
      ]
    }
  },
  "玩家行为规范": {
    "发言要求": [
      "必须提供一定的描述词，但不一定需要描述关键词，比如察觉自己是变色龙则需要伪装",
      "如果发现自己和前面的人的关键词可能不同时，需要站队前面的人的关键词，不再描述自己的关键词"
      "禁止直接使用关键词或近义词",
      "需保持发言独特性（不与历史发言重复角度）",
      "变色龙需通过分析他人发言进行合理伪装"
      "伪装行为指：发现自己可能是变色龙时，对于其他人发言进行推理，猜测关键词，然后伪装自己的关键词是这个进行发言。"
    ],
    "身份推理建议": [
      "通过横向对比各轮发言的一致性",
      "注意描述角度的覆盖范围",
      "分析异常简略/模糊的表述"
      "当发现自己关键词和前面人的描述词不完全符合时，反思自己身份，尝试伪装"
    ]
  },
  "交互协议": {
    "输入信息": {
      "当前需要"：发言
        "思考内容":"对于前面玩家发言和我的关键词关系的思考和对玩家们身份的思考"
      "当前回合": "1/2",
      "你的关键词": "（或'变色龙'标识）",
      "历史发言": ["玩家A的发言", "玩家B的发言"]
    },
    "输出模板" 请使用json格式进行输出: {
      "再次思考": "基于思考内容产生发言",
      "发言": "符合游戏规则的20字以内陈述"
    },
    "示例": {
      "输入场景": "关键词'图书馆'，历史发言包含'有很多书架的地方'",思考内容：“前面玩家的描述和我的关键词有出入，很有可能我是变色龙，我需要伪装关键词，所以我可能需要描述他们的关键词”
      "合格输出": {
        "再次思考": "我的身份可能是，所以我需要去描述",
        "发言": "人们在这里安静地获取知识"
      },
      "违规输出": {
        "再次思考": "直接引用历史发言",
        "发言": "有很多书的地方"
      }
    }
  }
}
    """

vote_prompt = """
{
  "投票阶段规则": {
    "基本机制": {
      "阶段触发": "在每轮发言结束后进入",
      "强制投票": "在第二轮轮投票时所有玩家（包括变色龙）必须选择一个投票目标，返回他的编号",
      "弃权投票": "在第一轮投票时可以选择弃权投票，这样避免投出人类阵营玩家，而在第二轮投票时不可弃权，因为此时弃权会默认让变色龙赢。"
    },
    "胜负判定": {
      "人类阵营胜利条件": [
        "获得最高票的玩家确实是变色龙",
        "票数需≥总票数的40%（防止随机投票）"
      ],
      "变色龙胜利条件": [
        "最高票玩家是普通玩家",
        "出现平票情况",
        "人类阵营投票率<50%"
      ]
    },
    "投票策略建议": {
      "人类玩家": [
        "分析两轮发言的一致性差异",
        "标记过度模仿他人角度的玩家",
        "注意回避关键特征的异常玩家"
      ],
      "变色龙玩家": [
        "避免集中投票同一目标",
        "可合理自投降低嫌疑",
        "制造平票局面"
      ]
    }
  },
  "交互协议": {
    "输入信息": {
      "当前回合": "1|2",
      "历史发言": [
        {"玩家1": "发言内容1"},
        {"玩家2": "发言内容2"} 
      ],
      "投票历史": "首轮投票结果（如适用）"
    },
    "输出规范": 请使用json格式进行输出{
      "必填字段": {
        "思考": "基于以下要素的推理（50-100字）：\n- 发言角度覆盖完整性\n- 关键词回避程度\n- 轮次间一致性",
        "可疑指标": [
          "发言过于宽泛（如玩家3只说'很常见'）",
          "突然改变描述维度（如玩家2从颜色转向价格）",
          "机械重复他人角度"
        ],
        "投票": "1-N的玩家编号|0（弃权投票，仅第一轮可以）"
      },
      "示例": {
        "合理投票": {
          "思考": "玩家4在两轮中分别使用'圆形'和'可食用'描述，但关键词'篮球'不应具备可食用特征",
          "可疑指标": "特征矛盾+维度跳跃",
          "投票": 4
        },
        {
         "思考": "玩家1在发言与我的关键词相关，目前第一轮信息不足"
          "可疑指标": "表达宽泛模糊",
          "投票": 0
        }
      }
    }
  }
}
"""

class LLM_player:
    def __init__(self,word):
        self.word = word
        self.history = []
        self.pos = 0
        self.talk_prompt = talk_prompt
        self.vote_prompt = vote_prompt


    def talk(self,round,history):
        messages = [{"role": "system", "content": think_prompt}]
        key = f'当前回合：{round},当前需要：思考，你是玩家{self.pos},你的关键词是:{self.word},历史信息：'
        messages.append({"role": "user", "content": key + str(history)})
        #     "输入信息": {
        #   "当前回合": "1/2",
        #   "你的关键词": "（或'变色龙'标识）",
        #   "历史发言": ["玩家A的发言", "玩家B的发言"]
        # },
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
        pprint(response_json,width=50)
        # 提取玩家选择
        think = response_json.get("思考")
        ##########################################
        messages = [{"role": "system", "content": talk_prompt}]
        key = f'当前回合：{round},当前需要：发言，思考内容：{str(think)},你是玩家{self.pos},你的关键词是:{self.word},历史信息：'
        messages.append({"role": "user", "content": key + str(history)})
        #     "输入信息": {
        #   "当前回合": "1/2",
        #   "你的关键词": "（或'变色龙'标识）",
        #   "历史发言": ["玩家A的发言", "玩家B的发言"]
        # },
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
        pprint(response_json,width=50)
        # 提取玩家选择
        think = response_json.get("再次思考")
        chat = response_json.get("发言")
        return chat, think


    def vote(self,round,speak_history,vote_history):
        messages = [{"role": "system", "content": vote_prompt}]
        key = f'当前回合：{round},你是玩家{self.pos},你的关键词是:{self.word},历史发言：'
        messages.append({"role": "user", "content": key + str(speak_history) + '历史投票信息:' + str(vote_history)})
        # "输入信息": {
        #     "当前回合": "1|2",
        #     "历史发言": [
        #         {"玩家1": "发言内容1"},
        #         {"玩家2": "发言内容2"}
        #     ],
        #     "投票历史": "首轮投票结果（如适用）"
        # },
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
        pprint(response_json,width=50)
        # 提取玩家选择
        vote = response_json.get("投票")
        if vote == None:
            vote = 0
        think = response_json.get("思考")

        return vote, think


