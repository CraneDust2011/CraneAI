import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from tkinter.font import Font
import json
import os
import logging
from datetime import datetime
import requests
import string
import threading
import time
import webbrowser

# 屏蔽requests SSL警告
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# ========== 全局配置常量 ==========
ARK_API_KEY = "e62aaf16-40b4-467b-b7ec-ff36ed23160c"

APP_NAME = "CraneAI 客户端 | 信阳市平桥区外国语中学23届杨家旭作品"
APP_FULL_DESCRIPTION = "CraneAI 客户端 | 信阳市平桥区外国语中学23届杨家旭作品\n本程序的图标的版权为CraneDust（杨家旭）的“筱赫” 版权登记号：豫作登字-2025-F-00085274"
COPYRIGHT_REG_URL = "http://hnbq.cn/henanuser/user/show-work/picture?serialNum=202512Z1100014216"

APP_VERSION = "v1.0.0"
APP_AUTHOR = "CraneAI Team"
APP_COPYRIGHT = "Copyright © 2026 CraneDust. All Rights Reserved."
APP_UPDATE_URL = "https://example.com/update"
APP_HELP_URL = "https://example.com/help"
APP_LOGO = "icons/CraneAI.ico"
APP_ICON_SMALL = "icons/icon_16x16.ico"
APP_ICON_MEDIUM = "icons/icon_32x32.ico"
APP_ICON_LARGE = "icons/icon_64x64.ico"

# 窗口配置（增大默认尺寸和最小尺寸，避免内容挤压）
WINDOW_DEFAULT_WIDTH = 1200  # 更宽敞的默认宽度
WINDOW_DEFAULT_HEIGHT = 850  # 更充足的默认高度
WINDOW_MIN_WIDTH = 900       # 增大最小宽度，防止过度缩小
WINDOW_MIN_HEIGHT = 700      # 增大最小高度，保证底部版权不被遮挡
WINDOW_MAX_WIDTH = 1920
WINDOW_MAX_HEIGHT = 1080
WINDOW_START_X = 100
WINDOW_START_Y = 100
WINDOW_RESIZABLE = True
WINDOW_TITLE_BAR = True
WINDOW_BACKGROUND = "#f7f8fa"

# 字体配置
FONT_FAMILY_MAIN = "Microsoft YaHei"
FONT_FAMILY_MONO = "Consolas"
FONT_FAMILY_TITLE = "Microsoft YaHei Bold"
FONT_SIZE_TITLE = 15
FONT_SIZE_NORMAL = 12
FONT_SIZE_SMALL = 10
FONT_SIZE_TINY = 8
FONT_SIZE_LARGE = 14
FONT_SIZE_XLARGE = 16
FONT_WEIGHT_NORMAL = "normal"
FONT_WEIGHT_BOLD = "bold"
FONT_WEIGHT_LIGHT = "light"

# 颜色配置
COLOR_PRIMARY = "#1677ff"
COLOR_PRIMARY_LIGHT = "#4096ff"
COLOR_PRIMARY_DARK = "#0958d9"
COLOR_SECONDARY = "#f0f2f5"
COLOR_SECONDARY_LIGHT = "#f7f8fa"
COLOR_SECONDARY_DARK = "#e5e7eb"
COLOR_TEXT_MAIN = "#333333"
COLOR_TEXT_SECONDARY = "#666666"
COLOR_TEXT_GRAY = "#999999"
COLOR_TEXT_WHITE = "#ffffff"
COLOR_SUCCESS = "#52c41a"
COLOR_SUCCESS_LIGHT = "#73d13d"
COLOR_ERROR = "#ff4d4f"
COLOR_ERROR_LIGHT = "#ff7875"
COLOR_WARNING = "#faad14"
COLOR_WARNING_LIGHT = "#ffc53d"
COLOR_INFO = "#1890ff"
COLOR_INFO_LIGHT = "#40a9ff"

# 聊天配置
CHAT_MESSAGE_MAX_LENGTH = 10000
CHAT_HISTORY_MAX_COUNT = 100
CHAT_INPUT_MIN_ROWS = 1
CHAT_INPUT_MAX_ROWS = 6
CHAT_SCROLL_SPEED = 10
CHAT_BUBBLE_PADDING_X = 16
CHAT_BUBBLE_PADDING_Y = 12
CHAT_BUBBLE_RADIUS = 12
CHAT_TIME_FORMAT = "%H:%M:%S"
CHAT_DATE_FORMAT = "%Y-%m-%d"
CHAT_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# API配置
API_REQUEST_TIMEOUT = 60
API_MAX_RETRY_COUNT = 3
API_RETRY_INTERVAL = 1
API_CONTENT_TYPE = "application/json; charset=utf-8"
API_AUTHORIZATION_PREFIX = "Bearer"
API_ENDPOINT_BEIJING = "https://ark.cn-beijing.volces.com/api/v3"
API_ENDPOINT_SHANGHAI = "https://ark.cn-shanghai.volces.com"
API_ENDPOINT_GUANGZHOU = "https://ark.cn-guangzhou.volces.com"
API_PATH_MODELS = "/api/v3/models"
API_PATH_COMPLETIONS = "/api/v3/chat/completions"

# 加载配置
PRESET_DELAY_TIME = 0.8
API_LOADING_TEXT = "CraneAI 正在思考中... 🤔"

# 测试常量列表/字典
DUMMY_CONST_LIST_1 = [f"dummy_value_{str(i).zfill(2)}" for i in range(1, 21)]
DUMMY_CONST_LIST_2 = [i for i in range(1001, 1031)]
DUMMY_CONST_LIST_3 = [True if i % 2 == 0 else False for i in range(20)]

DUMMY_CONST_DICT_1 = {f"key_{str(i).zfill(2)}": f"value_{str(i).zfill(2)}" for i in range(1, 21)}
DUMMY_CONST_DICT_2 = {f"num_key_{str(i).zfill(2)}": 1000 + i for i in range(1, 21)}

# ========== 模型映射与配置 ==========
MODEL_NAME_MAP = {
    "CraneAI-Pro 旗舰版": "doubao-seed-1-8-251228",
    "CraneAI-Lite 轻量版": "doubao-lite-128k-240428"
}
SUPPORTED_MODELS_DISPLAY = list(MODEL_NAME_MAP.keys())
INVALID_MODELS = [
    "doubao-seedance-1-0-lite-i2v-250428",
    "doubao-seed-1-0"
]

DEFAULT_CONFIG = {
    "temperature": 0.7,
    "max_tokens": 4000,
    "top_p": 0.9,
    "stream": False,
    "stop": None
}
REQUEST_TIMEOUT = 60
HISTORY_FILE = "craneai_chat_history_fixed.json"
SETTINGS_FILE = "craneai_settings.json"
DEFAULT_ENDPOINT = "https://ark.cn-beijing.volces.com"
API_PATH = "/api/v3/chat/completions"
SUPPORTED_ENDPOINTS = [
    "https://ark.cn-beijing.volces.com",
    "https://ark.cn-shanghai.volces.com",
    "https://ark.cn-guangzhou.volces.com"
]

# ========== 预设问答库 ==========
PRESET_ANSWERS = {
    # 基础身份类
    "你是谁": "我是CraneAI，一款智能助手，致力于为你提供高效、便捷的服务~",
    "你的名字是什么": "我的名字是CraneAI呀！很高兴认识你~",
    "你叫什么": "我叫CraneAI，随时为你待命哦！",
    "你叫啥": "我叫CraneAI，是不是很好记呀~",
    "你是谁啊": "我是CraneAI呀，你的专属智能小助手~",
    "介绍一下你自己": "大家好，我是CraneAI，一款专注于提供优质服务的智能助手，当前版本v1.0.0~",
    "自我介": "我是CraneAI，由CraneAI Team开发维护，版权归CraneDust所有~",
    "who are you": "I am CraneAI, an intelligent assistant dedicated to providing you with efficient services.",
    "what's your name": "My name is CraneAI, nice to meet you!",
    "what is your name": "My name is CraneAI, and I'm here to help you anytime.",
    "introduce yourself": "Hello, I'm CraneAI, a smart assistant developed by the CraneAI Team, version v1.0.0.",

    # 版本/开发者类
    "你是什么版本": "我当前的版本是 CraneAI v1.0.0，由 CraneAI Team 开发维护~",
    "谁开发的你": "我是由 CraneAI Team 开发的智能助手，版权归 CraneDust 所有哦~",
    "你的开发者是谁": "我的开发者是 CraneAI Team，感谢你的关注与支持！",
    "你是哪个公司的": "我是CraneDust旗下的智能助手，由CraneAI Team负责开发和迭代~",
    "你的版权归谁": "我的版权归CraneDust所有，未经允许请勿商用哦~",
    "你什么时候更新": "我的更新由CraneAI Team统一规划，有新版本会在客户端内通知大家~",
    "which version are you": "I'm currently CraneAI v1.0.0, developed and maintained by the CraneAI Team.",
    "who developed you": "I was developed by the CraneAI Team, and the copyright belongs to CraneDust.",
    "which company are you from": "I'm a smart assistant under CraneDust, developed by the CraneAI Team.",

    # 功能类
    "你能做什么": "我可以陪你聊天、解答疑问、提供信息查询、整理思路等服务，有什么需求都可以告诉我~",
    "你的功能有哪些": "我的功能包括日常聊天、问题解答、信息检索、文案润色等，快来试试吧！",
    "你会什么": "我会的可多啦！聊天、答疑、帮你梳理知识点、甚至陪你吐槽，有需要尽管开口~",
    "你能帮我做什么": "我可以帮你解答各类常见问题、整理信息、提供简单的建议，具体可以直接跟我描述你的需求~",
    "你会聊天吗": "当然会啦！我很擅长和人聊天哦，不管是日常唠嗑还是专业问题，都可以和我交流~",
    "你能解答数学题吗": "我可以帮你解答基础的数学问题哦，复杂的难题也可以尝试帮你梳理思路~",
    "你能写作文吗": "我可以帮你构思作文框架、润色语句、提供写作灵感，助力你完成优质作文~",
    "what can you do": "I can chat with you, answer questions, provide information retrieval and other services.",
    "what functions do you have": "My functions include daily chat, Q&A, information retrieval, copy polishing, and more.",
    "can you help me with math": "I can help you solve basic math problems and sort out ideas for complex problems.",
    "can you write an essay": "I can help you conceive an essay framework, polish sentences, and provide writing inspiration.",

    # 特色/定位类
    "你和其他ai有什么区别": "我是专为 CraneAI 客户端打造的智能助手，界面简洁、响应快速、占用资源少，体验更流畅~",
    "你是免费的吗": "我是 CraneAI 客户端的内置智能助手，当前版本可免费使用所有基础功能哦~",
    "你收费吗": "当前版本的CraneAI基础功能全部免费，后续若推出增值服务，会提前在客户端内公示~",
    "你比其他ai好用吗": "我专注于提供轻量化、高效率的服务，在日常聊天和基础答疑场景下，会给你不错的体验哦~",
    "你有什么优势": "我的优势是响应快、界面简洁、操作简单，而且是专为CraneAI客户端优化的，适配性更好~",
    "can you help me": "Of course! I'm here to help you with whatever you need, just let me know.",
    "are you free to use": "I'm a built-in smart assistant of the CraneAI client, and all basic functions are free to use currently.",
    "what are your advantages": "My advantages are fast response, simple interface, and better adaptability to the CraneAI client.",

    # 使用帮助类
    "怎么清空聊天记录": "你可以点击界面上方的「清空对话」按钮，就能一键清空所有聊天记录啦~",
    "怎么测试连接": "界面上方有个「测试连接」按钮，点击它就能检测API连接是否正常哦~",
    "聊天记录会保存吗": "会的哦！你的聊天记录会自动保存到本地文件中，下次打开客户端还能查看~",
    "怎么更换模型": "界面上方的模型下拉框，点击后可以选择不同的CraneAI版本模型哦~",
    "快捷键是什么": "发送消息可以使用「Ctrl+Enter」快捷键，更快捷地提交你的问题~",
    "how to clear chat history": "You can click the \"Clear Chat\" button at the top of the interface to clear all chat records with one click.",
    "how to test the connection": "There is a \"Test Connection\" button at the top of the interface, click it to check if the API connection is normal.",

    # 语气互动类
    "你好": "你好呀！我是CraneAI，很高兴能和你交流~",
    "哈喽": "哈喽哈喽！有什么可以帮到你的吗~",
    "早上好": "早上好呀！新的一天也要元气满满哦~",
    "晚上好": "晚上好呀！忙碌了一天，要不要和我聊聊天放松一下~",
    "谢谢": "不客气哦！能帮到你我也很开心~",
    "thank you": "You're welcome! I'm glad I could help you.",
    "hello": "Hello! How can I assist you today?",
    "good morning": "Good morning! Wish you a wonderful day ahead.",

    # 常见疑问类
    "你需要联网吗": "是的哦，我需要联网调用API才能为你提供完整的服务，确保网络畅通即可~",
    "你的回答准确吗": "我会尽力为你提供准确的回答，不过对于一些专业领域的深度问题，建议你参考权威资料哦~",
    "你能记住我的对话吗": "在当前会话中，我可以记住我们的聊天内容，关闭客户端后，仅会保存聊天记录，不会记忆会话上下文哦~",
    "can you remember our chat": "I can remember our chat content in the current session. After closing the client, only the chat records will be saved.",
    "do you need internet": "Yes, I need to connect to the Internet to call the API and provide you with complete services.",

    # 故障排查类
    "为什么发送失败": "发送失败可能是网络问题或API连接异常，你可以先点击「测试连接」检测，再检查网络畅通~",
    "为什么没有回复": "没有回复可能是网络延迟或API请求超时，你可以稍等片刻，或重新发送问题哦~",
    "why can't I send messages": "Failed to send messages may be due to network problems or abnormal API connections. Please check your network and test the connection first."
}

# ========== 辅助类 ==========
class DummyHelperClass01:
    def __init__(self):
        self.attr_01 = "attr_01"
        self.attr_02 = 100
        self.attr_03 = True
        self.attr_04 = []
        self.attr_05 = {}
    
    def dummy_method_01(self):
        self.attr_02 += 1
    
    def dummy_method_02(self):
        self.attr_04.append(self.attr_01)
    
    def dummy_method_03(self):
        self.attr_05[self.attr_01] = self.attr_02

class DummyHelperClass02:
    def __init__(self):
        self.dummy_attr_01 = None
        self.dummy_attr_02 = None
        self.dummy_attr_03 = None
    
    def dummy_method_04(self):
        pass
    
    def dummy_method_05(self):
        pass

class DummyHelperClass03:
    def __init__(self):
        self.helper_01 = DummyHelperClass01()
        self.helper_02 = DummyHelperClass02()
    
    def dummy_method_06(self):
        self.helper_01.dummy_method_01()
    
    def dummy_method_07(self):
        self.helper_02.dummy_method_04()

# ========== 冗余测试函数 ==========
def dummy_function_001():
    a = 1
    b = 2
    c = a + b
    d = c * 2
    e = d - 1

def dummy_function_002():
    text = "dummy text"
    text_upper = text.upper()
    text_lower = text.lower()
    text_len = len(text)

def dummy_function_003():
    lst = [1, 2, 3, 4, 5]
    lst.append(6)
    lst.remove(1)
    lst_len = len(lst)

def dummy_function_004():
    dic = {"a": 1, "b": 2}
    dic["c"] = 3
    dic.pop("a")
    dic_len = len(dic)

def dummy_function_005():
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day

def dummy_function_006():
    dummy_function_001()
    dummy_function_002()

def dummy_function_007():
    dummy_function_003()
    dummy_function_004()

def dummy_function_008():
    x = 10
    y = 20
    z = x if x > y else y

def dummy_function_009():
    for i in range(5):
        j = i * 2

def dummy_function_010():
    k = 0
    while k < 5:
        k += 1

def dummy_function_011(): pass
def dummy_function_012(): pass
def dummy_function_013(): pass
def dummy_function_014(): pass
def dummy_function_015(): pass
def dummy_function_016(): pass
def dummy_function_017(): pass
def dummy_function_018(): pass
def dummy_function_019(): pass
def dummy_function_020(): pass

def dummy_function_021(): pass
def dummy_function_022(): pass
def dummy_function_023(): pass
def dummy_function_024(): pass
def dummy_function_025(): pass
def dummy_function_026(): pass
def dummy_function_027(): pass
def dummy_function_028(): pass
def dummy_function_029(): pass
def dummy_function_030(): pass

def dummy_function_031(): pass
def dummy_function_032(): pass
def dummy_function_033(): pass
def dummy_function_034(): pass
def dummy_function_035(): pass
def dummy_function_036(): pass
def dummy_function_037(): pass
def dummy_function_038(): pass
def dummy_function_039(): pass
def dummy_function_040(): pass

def dummy_function_041(): pass
def dummy_function_042(): pass
def dummy_function_043(): pass
def dummy_function_044(): pass
def dummy_function_045(): pass
def dummy_function_046(): pass
def dummy_function_047(): pass
def dummy_function_048(): pass
def dummy_function_049(): pass
def dummy_function_050(): pass

# ========== 主GUI类 ==========
class CraneAIStyleGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # 初始化应用属性
        self.app_name = APP_NAME
        self.app_version = APP_VERSION
        self.app_author = APP_AUTHOR
        self.app_copyright = APP_COPYRIGHT
        self.app_update_url = APP_UPDATE_URL
        self.app_help_url = APP_HELP_URL
        
        # 窗口属性
        self.window_default_width = WINDOW_DEFAULT_WIDTH
        self.window_default_height = WINDOW_DEFAULT_HEIGHT
        self.window_min_width = WINDOW_MIN_WIDTH
        self.window_min_height = WINDOW_MIN_HEIGHT
        self.window_max_width = WINDOW_MAX_WIDTH
        self.window_max_height = WINDOW_MAX_HEIGHT
        self.window_start_x = WINDOW_START_X
        self.window_start_y = WINDOW_START_Y
        self.window_resizable = WINDOW_RESIZABLE
        self.window_title_bar = WINDOW_TITLE_BAR
        
        # 颜色属性
        self.color_primary = COLOR_PRIMARY
        self.color_primary_light = COLOR_PRIMARY_LIGHT
        self.color_primary_dark = COLOR_PRIMARY_DARK
        self.color_secondary = COLOR_SECONDARY
        self.color_secondary_light = COLOR_SECONDARY_LIGHT
        self.color_secondary_dark = COLOR_SECONDARY_DARK
        self.color_text_main = COLOR_TEXT_MAIN
        self.color_text_secondary = COLOR_TEXT_SECONDARY
        self.color_text_gray = COLOR_TEXT_GRAY
        self.color_text_white = COLOR_TEXT_WHITE
        self.color_success = COLOR_SUCCESS
        self.color_error = COLOR_ERROR
        self.color_warning = COLOR_WARNING
        self.color_info = COLOR_INFO
        
        # 字体属性
        self.font_family_main = FONT_FAMILY_MAIN
        self.font_family_mono = FONT_FAMILY_MONO
        self.font_size_title = FONT_SIZE_TITLE
        self.font_size_normal = FONT_SIZE_NORMAL
        self.font_size_small = FONT_SIZE_SMALL
        self.font_weight_bold = FONT_WEIGHT_BOLD
        self.font_weight_normal = FONT_WEIGHT_NORMAL
        
        # 聊天属性
        self.chat_message_max_length = CHAT_MESSAGE_MAX_LENGTH
        self.chat_history_max_count = CHAT_HISTORY_MAX_COUNT
        self.chat_input_min_rows = CHAT_INPUT_MIN_ROWS
        self.chat_input_max_rows = CHAT_INPUT_MAX_ROWS
        self.chat_bubble_padding_x = CHAT_BUBBLE_PADDING_X
        self.chat_bubble_padding_y = CHAT_BUBBLE_PADDING_Y
        self.chat_time_format = CHAT_TIME_FORMAT
        
        # 辅助类实例
        self.dummy_helper_01 = DummyHelperClass01()
        self.dummy_helper_02 = DummyHelperClass02()
        self.dummy_helper_03 = DummyHelperClass03()
        
        # 测试数据
        self.dummy_list_01 = DUMMY_CONST_LIST_1.copy()
        self.dummy_list_02 = DUMMY_CONST_LIST_2.copy()
        self.dummy_dict_01 = DUMMY_CONST_DICT_1.copy()
        self.dummy_dict_02 = DUMMY_CONST_DICT_2.copy()
        
        # API相关变量
        self.endpoint = tk.StringVar(value=DEFAULT_ENDPOINT)
        self.current_model_display = tk.StringVar(value=SUPPORTED_MODELS_DISPLAY[0])
        self.message_list = []
        self.chat_history = []
        self.is_loading = False
        
        # 设置相关变量
        self.current_api_key = tk.StringVar(value=ARK_API_KEY)
        self.temperature_var = tk.DoubleVar(value=DEFAULT_CONFIG["temperature"])
        self.max_tokens_var = tk.IntVar(value=DEFAULT_CONFIG["max_tokens"])
        self.top_p_var = tk.DoubleVar(value=DEFAULT_CONFIG["top_p"])
        
        # ========== 初始化日志 ==========
        self.init_logger()
        
        # 后续初始化流程
        self.settings = self.load_settings()
        self.settings_visible = tk.BooleanVar(value=False)
        self.check_api_key_valid()
        self.setup_font_and_style()
        self.create_all_widgets()
        self.create_copyright_label()
        self.bind_window_events()
        self.load_chat_history()
        
        # 测试操作
        self.dummy_initialization_ops()
        
        # 窗口最终配置
        self.title(APP_NAME)
        self.geometry(f"{WINDOW_DEFAULT_WIDTH}x{WINDOW_DEFAULT_HEIGHT}")
        self.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.configure(bg=WINDOW_BACKGROUND)
        
        # ========== 主布局自适应配置 ==========
        self.grid_rowconfigure(1, weight=1)  # 聊天区域占满垂直空间
        self.grid_columnconfigure(0, weight=1)  # 水平方向自适应
        
        # 日志输出
        self.log_info("CraneAIUI初始化完成")
        self.log_info(f"应用版本：{self.app_version}")

    # ========== 日志核心方法 ==========
    def init_logger(self):
        """初始化日志系统"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("craneai.log", encoding="utf-8"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def log_info(self, msg):
        """记录info级别日志"""
        if hasattr(self, 'logger'):
            self.logger.info(msg)
    
    def log_error(self, msg):
        """记录error级别日志"""
        if hasattr(self, 'logger'):
            self.logger.error(msg)

    # ========== 聊天消息渲染核心方法 ==========
    def show_message(self, sender, content, send_time, is_user=True):
        """在聊天框显示消息"""
        self.text_chat.config(state=tk.NORMAL)
        
        # 消息头部
        header = f"[{sender}] {send_time}\n"
        self.text_chat.insert(tk.END, header, "time")
        
        # 消息内容
        self.text_chat.insert(tk.END, content + "\n\n", "user_msg" if is_user else "ai_msg")
        
        # 滚动到底部
        self.text_chat.see(tk.END)
        self.text_chat.config(state=tk.DISABLED)

    # ========== 初始化辅助操作 ==========
    def dummy_initialization_ops(self):
        self.dummy_helper_01.dummy_method_01()
        self.dummy_helper_01.dummy_method_02()
        self.dummy_helper_03.dummy_method_06()
        
        self.dummy_list_01.append("dummy_extra_01")
        self.dummy_dict_01["extra_key_01"] = "extra_value_01"
        
        dummy_function_001()
        dummy_function_002()
        dummy_function_003()

    def dummy_widget_config_ops(self, widget):
        widget_name = widget.winfo_name()
        widget_width = widget.winfo_width()
        widget_height = widget.winfo_height()

    def dummy_message_post_process(self, sender, content):
        sender_len = len(sender)
        content_len = len(content)
        content_first_10 = content[:10] if len(content) >= 10 else content

    def dummy_log_extra(self, msg):
        msg_prefix = "[DUMMY LOG] "
        full_msg = msg_prefix + msg
        msg_len = len(full_msg)

    # ========== API Key 验证 ==========
    def check_api_key_valid(self):
        api_key = self.current_api_key.get().strip()
        if api_key == "your_ark_api_key_here" or not api_key:
            error_title = "API Key未配置"
            error_message = "请在代码顶部ARK_API_KEY变量中填写真实API Key！\n"
            error_message += "当前配置为默认值，无法正常调用接口。"
            messagebox.showerror(error_title, error_message)
            self.quit()

    # ========== 字体和样式设置 ==========
    def setup_font_and_style(self):
        self.font_title = Font(family=self.font_family_main, size=self.font_size_title, weight=self.font_weight_bold)
        self.font_normal = Font(family=self.font_family_main, size=self.font_size_normal)
        self.font_mono = Font(family=self.font_family_mono, size=self.font_size_small)
        self.font_small = Font(family=self.font_family_main, size=self.font_size_small)
        
        style = ttk.Style(self)
        style.theme_use("clam")
        
        style.configure("Primary.TButton",
                        font=self.font_normal,
                        padding=(12, 6),
                        background=self.color_primary,
                        foreground=self.color_text_white,
                        relief=tk.FLAT)
        style.map("Primary.TButton",
                  background=[("active", self.color_primary_light)])
        
        style.configure("Secondary.TButton",
                        font=self.font_small,
                        padding=(8, 4),
                        background=self.color_secondary,
                        foreground=self.color_text_main,
                        relief=tk.FLAT)
        style.map("Secondary.TButton",
                  background=[("active", self.color_secondary_dark)])
        
        style.configure("TEntry",
                        padding=8,
                        font=self.font_normal,
                        fieldbackground=self.color_text_white,
                        relief=tk.FLAT,
                        borderwidth=1)
        
        style.configure("Setting.TLabel",
                        font=self.font_small,
                        padding=(4, 2),
                        foreground=self.color_text_secondary)
        
        self.widget_style = style

    # ========== 全局组件创建 ==========
    def create_all_widgets(self):
        # 主分栏容器
        self.main_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.main_paned.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # 左侧聊天容器
        self.chat_container = ttk.Frame(self.main_paned)
        self.chat_container.grid_rowconfigure(1, weight=1)
        self.chat_container.grid_columnconfigure(0, weight=1)
        self.main_paned.add(self.chat_container, weight=4)
        
        # 右侧设置容器
        self.settings_container = ttk.Frame(self.main_paned)
        self.settings_container.grid_rowconfigure(0, weight=0)
        self.settings_container.grid_rowconfigure(1, weight=1)
        self.settings_container.grid_columnconfigure(0, weight=1)
        
        # 创建顶部栏、聊天区域、输入区域、设置面板
        self.create_top_bar()
        self.create_chat_area(self.chat_container)
        self.create_input_area(self.chat_container)
        self.create_settings_panel(self.settings_container)
        
        # 初始隐藏设置面板
        self.toggle_settings_panel()
        
        # 测试组件配置
        self.all_widget_frames = [self.top_frame, self.chat_frame, self.input_frame, self.settings_container]
        for frame in self.all_widget_frames:
            self.dummy_widget_config_ops(frame)

    # ========== 顶部栏创建 ==========
    def create_top_bar(self):
        self.top_frame = ttk.Frame(self, style="Secondary.TButton")
        self.top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        self.top_frame.grid_columnconfigure(4, weight=1)
        
        # 模型选择
        ttk.Label(self.top_frame, text="模型：", font=self.font_normal).grid(
            row=0, column=0, padx=5, pady=8, sticky="w"
        )
        
        self.combo_model = ttk.Combobox(
            self.top_frame,
            textvariable=self.current_model_display,
            values=SUPPORTED_MODELS_DISPLAY,
            state="readonly",
            width=20
        )
        self.combo_model.grid(row=0, column=1, padx=5, pady=8, sticky="w")
        
        # 测试连接按钮
        self.btn_test = ttk.Button(
            self.top_frame,
            text="测试连接",
            style="Primary.TButton",
            command=self.test_ark_connection
        )
        self.btn_test.grid(row=0, column=2, padx=5, pady=8)
        
        # 清空对话按钮
        self.btn_clear = ttk.Button(
            self.top_frame,
            text="清空对话",
            style="Secondary.TButton",
            command=self.clear_chat_history
        )
        self.btn_clear.grid(row=0, column=3, padx=5, pady=8)
        
        # 设置开关按钮
        self.btn_toggle_settings = ttk.Button(
            self.top_frame,
            text="⚙️ 设置",
            style="Secondary.TButton",
            command=self.toggle_settings_panel
        )
        self.btn_toggle_settings.grid(row=0, column=5, padx=5, pady=8, sticky="e")
        
        # 关于按钮
        self.btn_about = ttk.Button(
            self.top_frame,
            text="ℹ️ 关于",
            style="Secondary.TButton",
            command=self.show_about_dialog
        )
        self.btn_about.grid(row=0, column=6, padx=5, pady=8, sticky="e")

    # ========== 聊天区域创建 ==========
    def create_chat_area(self, parent):
        self.chat_frame = ttk.Frame(parent)
        self.chat_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.chat_frame.grid_rowconfigure(0, weight=1)
        self.chat_frame.grid_columnconfigure(0, weight=1)
        
        self.text_chat = scrolledtext.ScrolledText(
            self.chat_frame,
            font=self.font_normal,
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg=self.color_text_white,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.text_chat.grid(row=0, column=0, sticky="nsew")
        
        # 聊天消息标签样式
        self.text_chat.tag_configure(
            "user_msg",
            foreground=self.color_text_white,
            background=self.color_primary,
            lmargin1=100,
            lmargin2=100,
            rmargin=10,
            spacing1=8,
            spacing3=8
        )
        self.text_chat.tag_configure(
            "ai_msg",
            foreground=self.color_text_main,
            background=self.color_secondary,
            lmargin1=10,
            lmargin2=10,
            rmargin=100,
            spacing1=8,
            spacing3=8
        )
        self.text_chat.tag_configure(
            "time",
            foreground=self.color_text_gray,
            font=self.font_small
        )
        self.text_chat.tag_configure(
            "loading",
            foreground=self.color_info,
            background=self.color_secondary_light,
            lmargin1=10,
            lmargin2=10,
            rmargin=100,
            spacing1=8,
            spacing3=8
        )

    # ========== 输入区域创建 ==========
    def create_input_area(self, parent):
        self.input_frame = ttk.Frame(parent, style="Secondary.TButton")
        self.input_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        self.entry_input = tk.Text(
            self.input_frame,
            font=self.font_normal,
            height=4,
            wrap=tk.WORD,
            bg=self.color_text_white,
            relief=tk.FLAT,
            padx=10,
            pady=10,
            bd=1,
            highlightthickness=1,
            highlightbackground=self.color_secondary_dark
        )
        self.entry_input.grid(row=0, column=0, sticky="ew", padx=5, pady=8)
        
        # 快捷键绑定
        self.entry_input.bind("<Control-Return>", lambda e: self.send_chat_message())
        self.entry_input.bind("<FocusIn>", lambda e: self.entry_input.config(
            highlightbackground=self.color_primary
        ))
        self.entry_input.bind("<FocusOut>", lambda e: self.entry_input.config(
            highlightbackground=self.color_secondary_dark
        ))
        
        # 发送按钮
        self.btn_send = ttk.Button(
            self.input_frame,
            text="发送 (Ctrl+Enter)",
            style="Primary.TButton",
            command=self.send_chat_message
        )
        self.btn_send.grid(row=0, column=1, padx=5, pady=8, sticky="ns")

    # ========== 设置面板创建 ==========
    def create_settings_panel(self, parent):
        # 设置标题
        self.settings_title_frame = ttk.Frame(parent)
        self.settings_title_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        ttk.Label(self.settings_title_frame, text="⚙️ CraneAI 设置", font=self.font_title).grid(
            row=0, column=0, sticky="w"
        )
        
        # 滚动容器
        self.settings_canvas = tk.Canvas(parent, bg=self.color_secondary_light, relief=tk.FLAT)
        self.settings_scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.settings_canvas.yview)
        self.settings_scrollable_frame = ttk.Frame(self.settings_canvas)
        
        self.settings_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.settings_canvas.configure(scrollregion=self.settings_canvas.bbox("all"))
        )
        self.settings_canvas.create_window((0, 0), window=self.settings_scrollable_frame, anchor="nw")
        self.settings_canvas.configure(yscrollcommand=self.settings_scrollbar.set)
        
        self.settings_canvas.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.settings_scrollbar.grid(row=1, column=1, sticky="ns", padx=0, pady=5)
        
        # 配置项
        row_idx = 0
        
        # API Key配置
        ttk.Label(self.settings_scrollable_frame, text="API Key 配置", style="Setting.TLabel", font=(self.font_family_main, 11, "bold")).grid(
            row=row_idx, column=0, columnspan=2, sticky="w", padx=10, pady=(20, 10)
        )
        row_idx += 1
        
        ttk.Label(self.settings_scrollable_frame, text="API Key：", style="Setting.TLabel").grid(
            row=row_idx, column=0, sticky="w", padx=15, pady=5
        )
        self.api_key_entry = ttk.Entry(
            self.settings_scrollable_frame,
            textvariable=self.current_api_key,
            width=30,
            show="*"
        )
        self.api_key_entry.grid(row=row_idx, column=1, sticky="w", padx=5, pady=5)
        row_idx += 1
        
        # 对话参数配置
        ttk.Label(self.settings_scrollable_frame, text="对话参数配置", style="Setting.TLabel", font=(self.font_family_main, 11, "bold")).grid(
            row=row_idx, column=0, columnspan=2, sticky="w", padx=10, pady=(20, 10)
        )
        row_idx += 1
        
        # 温度系数
        ttk.Label(self.settings_scrollable_frame, text="温度系数 (0.0-1.0)：", style="Setting.TLabel").grid(
            row=row_idx, column=0, sticky="w", padx=15, pady=5
        )
        self.temperature_scale = ttk.Scale(
            self.settings_scrollable_frame,
            from_=0.0,
            to=1.0,
            variable=self.temperature_var,
            orient=tk.HORIZONTAL,
            length=150
        )
        self.temperature_scale.grid(row=row_idx, column=1, sticky="w", padx=5, pady=5)
        self.temperature_label = ttk.Label(self.settings_scrollable_frame, text=f"{self.temperature_var.get():.1f}", style="Setting.TLabel")
        self.temperature_label.grid(row=row_idx, column=2, sticky="w", padx=5, pady=5)
        self.temperature_var.trace("w", lambda *args: self.temperature_label.config(text=f"{self.temperature_var.get():.1f}"))
        row_idx += 1
        
        # 最大令牌数
        ttk.Label(self.settings_scrollable_frame, text="最大令牌数：", style="Setting.TLabel").grid(
            row=row_idx, column=0, sticky="w", padx=15, pady=5
        )
        self.max_tokens_spinbox = ttk.Spinbox(
            self.settings_scrollable_frame,
            textvariable=self.max_tokens_var,
            from_=100,
            to=8000,
            increment=100,
            width=10
        )
        self.max_tokens_spinbox.grid(row=row_idx, column=1, sticky="w", padx=5, pady=5)
        row_idx += 1
        
        # Top P参数
        ttk.Label(self.settings_scrollable_frame, text="Top P (0.0-1.0)：", style="Setting.TLabel").grid(
            row=row_idx, column=0, sticky="w", padx=15, pady=5
        )
        self.top_p_scale = ttk.Scale(
            self.settings_scrollable_frame,
            from_=0.0,
            to=1.0,
            variable=self.top_p_var,
            orient=tk.HORIZONTAL,
            length=150
        )
        self.top_p_scale.grid(row=row_idx, column=1, sticky="w", padx=5, pady=5)
        self.top_p_label = ttk.Label(self.settings_scrollable_frame, text=f"{self.top_p_var.get():.1f}", style="Setting.TLabel")
        self.top_p_label.grid(row=row_idx, column=2, sticky="w", padx=5, pady=5)
        self.top_p_var.trace("w", lambda *args: self.top_p_label.config(text=f"{self.top_p_var.get():.1f}"))
        row_idx += 1
        
        # 保存按钮
        self.save_settings_btn = ttk.Button(
            self.settings_scrollable_frame,
            text="保存设置",
            style="Primary.TButton",
            command=self.save_settings
        )
        self.save_settings_btn.grid(row=row_idx, column=0, columnspan=3, sticky="ew", padx=15, pady=(30, 20))
        row_idx += 1

    # ========== 版权声明创建（完整显示优化） ==========
    def create_copyright_label(self):
        """优化版权声明显示，确保完整不截断"""
        self.copyright_label = ttk.Label(
            self,
            text=self.app_copyright,
            font=(self.font_family_main, FONT_SIZE_TINY),
            foreground=self.color_text_gray,
            wraplength=200,  # 自动换行，防止文字溢出
            justify="center" # 居中对齐，提升美观度
        )
        self.copyright_label.grid(
            row=3, column=0, sticky="se",
            padx=20, pady=10,
            ipadx=10  # 内边距，防止文字贴边
        )
        self.grid_rowconfigure(3, weight=0)

    # ========== 设置相关方法 ==========
    def load_settings(self):
        default_settings = {
            "api_key": ARK_API_KEY,
            "temperature": DEFAULT_CONFIG["temperature"],
            "max_tokens": DEFAULT_CONFIG["max_tokens"],
            "top_p": DEFAULT_CONFIG["top_p"]
        }
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    loaded_settings = json.load(f)
                    self.current_api_key.set(loaded_settings.get("api_key", ARK_API_KEY))
                    self.temperature_var.set(loaded_settings.get("temperature", DEFAULT_CONFIG["temperature"]))
                    self.max_tokens_var.set(loaded_settings.get("max_tokens", DEFAULT_CONFIG["max_tokens"]))
                    self.top_p_var.set(loaded_settings.get("top_p", DEFAULT_CONFIG["top_p"]))
                    return loaded_settings
            except Exception as e:
                self.log_error(f"加载设置失败：{e}")
                return default_settings
        else:
            return default_settings

    def save_settings(self):
        try:
            self.settings = {
                "api_key": self.current_api_key.get().strip(),
                "temperature": self.temperature_var.get(),
                "max_tokens": self.max_tokens_var.get(),
                "top_p": self.top_p_var.get()
            }
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
            DEFAULT_CONFIG["temperature"] = self.temperature_var.get()
            DEFAULT_CONFIG["max_tokens"] = self.max_tokens_var.get()
            DEFAULT_CONFIG["top_p"] = self.top_p_var.get()
            messagebox.showinfo("成功", "设置已保存，重启后生效！")
        except Exception as e:
            self.log_error(f"保存设置失败：{e}")
            messagebox.showerror("错误", f"保存设置失败：{str(e)}")

    def toggle_settings_panel(self):
        self.settings_visible.set(not self.settings_visible.get())
        if self.settings_visible.get():
            self.main_paned.add(self.settings_container, weight=1)
            self.btn_toggle_settings.config(text="🔼 隐藏设置")
        else:
            try:
                self.main_paned.forget(self.settings_container)
                self.btn_toggle_settings.config(text="⚙️ 显示设置")
            except:
                pass

    # ========== 关于弹窗（核心版权描述完整显示优化） ==========
    def show_about_dialog(self):
        """关于弹窗：长文本自动换行，核心版权描述完整无截断"""
        about_window = tk.Toplevel(self)
        about_window.title(f"关于 {self.app_name}")
        # 增大弹窗尺寸，提供充足展示空间（500x350 → 650x380）
        about_window.geometry("650x380")
        about_window.resizable(False, False)
        about_window.configure(bg=WINDOW_BACKGROUND)
        about_window.transient(self)
        about_window.grab_set()
        
        content_frame = ttk.Frame(about_window, padding=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 拆分完整描述
        full_desc_lines = APP_FULL_DESCRIPTION.split('\n')
        main_title = full_desc_lines[0]
        copyright_detail = full_desc_lines[1]  # 核心长文本版权描述
        
        # 主标题
        ttk.Label(
            content_frame,
            text=main_title,
            font=self.font_title,
            foreground=self.color_primary
        ).pack(pady=(10, 15), anchor="w")
        
        # 核心优化：长文本自动换行，完整展示无截断
        copyright_label = ttk.Label(
            content_frame,
            text=copyright_detail,
            font=self.font_normal,
            foreground=self.color_text_main,
            wraplength=600,  # 600像素内自动换行，适配弹窗宽度
            justify="left"   # 左对齐，保持排版规整
        )
        copyright_label.pack(pady=(0, 20), anchor="w")
        
        # 版本信息
        ttk.Label(
            content_frame,
            text=f"版本：{self.app_version}",
            font=self.font_normal
        ).pack(pady=5, anchor="w")
        
        # 开发者信息
        ttk.Label(
            content_frame,
            text=f"开发者：{self.app_author}",
            font=self.font_normal
        ).pack(pady=5, anchor="w")
        
        # 版权声明
        ttk.Label(
            content_frame,
            text=self.app_copyright,
            font=self.font_small,
            foreground=self.color_text_gray
        ).pack(pady=20, anchor="w")
        
        # 说明文本
        ttk.Label(
            content_frame,
            text="一款轻量级智能对话客户端，专为高效交互设计。",
            font=self.font_small,
            foreground=self.color_text_secondary
        ).pack(pady=5, anchor="w")
        
        # 确认按钮
        ttk.Button(
            content_frame,
            text="确认",
            style="Primary.TButton",
            command=about_window.destroy
        ).pack(pady=(30, 10), anchor="center")

    # ========== 预设回答展示 ==========
    def show_preset_answer(self, user_input, preset_answer):
        time.sleep(PRESET_DELAY_TIME)
        current_time = datetime.now().strftime(self.chat_time_format)
        self.show_message("CraneAI", preset_answer, current_time, is_user=False)
        self.message_list.append({"role": "user", "content": user_input})
        self.message_list.append({"role": "assistant", "content": preset_answer})
        self.save_chat_history()
        self.btn_send.config(state=tk.NORMAL)
        self.is_loading = False

    # ========== API 请求线程 ==========
    def api_request_thread(self, user_input, actual_model, api_key):
        """API请求线程，避免阻塞UI"""
        # 显示加载提示
        self.text_chat.config(state=tk.NORMAL)
        loading_time = datetime.now().strftime(self.chat_time_format)
        loading_header = f"[CraneAI] {loading_time}\n"
        self.text_chat.insert(tk.END, loading_header, "time")
        self.text_chat.insert(tk.END, API_LOADING_TEXT + "\n\n", "loading")
        self.text_chat.see(tk.END)
        self.text_chat.config(state=tk.DISABLED)

        try:
            headers = {
                "Content-Type": API_CONTENT_TYPE,
                "Authorization": f"{API_AUTHORIZATION_PREFIX} {api_key}"
            }
            data = {
                "model": actual_model,
                "messages": self.message_list,
                "temperature": self.temperature_var.get(),
                "max_tokens": self.max_tokens_var.get(),
                "top_p": self.top_p_var.get(),
                "stream": DEFAULT_CONFIG["stream"]
            }
            
            response = requests.post(
                f"{self.endpoint.get()}{API_PATH}",
                headers=headers,
                json=data,
                timeout=REQUEST_TIMEOUT,
                verify=False
            )
            
            # 移除加载提示
            self.text_chat.config(state=tk.NORMAL)
            self.text_chat.delete("end-2l linestart", "end")
            self.text_chat.config(state=tk.DISABLED)

            if response.status_code == 200:
                ai_reply = response.json()["choices"][0]["message"]["content"]
                self.message_list.append({"role": "assistant", "content": ai_reply})
                current_time = datetime.now().strftime(self.chat_time_format)
                self.show_message("CraneAI", ai_reply, current_time, is_user=False)
                self.save_chat_history()
            else:
                error_msg = f"请求失败：{response.status_code} {response.text[:200]}"
                current_time = datetime.now().strftime(self.chat_time_format)
                self.show_message("系统", error_msg, current_time, is_user=False)
                messagebox.showerror("错误", error_msg)
        except Exception as e:
            # 异常处理：移除加载提示
            self.text_chat.config(state=tk.NORMAL)
            self.text_chat.delete("end-2l linestart", "end")
            self.text_chat.config(state=tk.DISABLED)

            error_msg = f"异常：{str(e)}"
            current_time = datetime.now().strftime(self.chat_time_format)
            self.show_message("系统", error_msg, current_time, is_user=False)
            messagebox.showerror("错误", error_msg)
        finally:
            # 恢复按钮状态
            self.btn_send.config(state=tk.NORMAL)
            self.is_loading = False

    # ========== 发送消息 ==========
    def send_chat_message(self):
        """发送用户消息，匹配预设回答或调用API"""
        if self.is_loading:
            return
        
        user_input = self.entry_input.get("1.0", tk.END).strip()
        api_key = self.current_api_key.get().strip()
        
        if not user_input:
            return
        
        # 清空输入框
        self.entry_input.delete("1.0", tk.END)
        self.btn_send.config(state=tk.DISABLED)
        self.is_loading = True
        
        # 显示用户消息
        current_time = datetime.now().strftime(self.chat_time_format)
        self.show_message("用户", user_input, current_time, is_user=True)
        self.message_list.append({"role": "user", "content": user_input})
        
        # 处理用户输入（移除标点和语气词）
        modal_words = ["啊", "呀", "哦", "呢", "吧", "啦", "咩", "哈"]
        user_input_clean = user_input.strip().lower()
        user_input_clean = user_input_clean.translate(str.maketrans('', '', string.punctuation))
        for word in modal_words:
            user_input_clean = user_input_clean.replace(word, "")
        
        # 匹配预设回答或调用API
        if user_input in PRESET_ANSWERS:
            preset_answer = PRESET_ANSWERS[user_input]
            threading.Thread(
                target=self.show_preset_answer,
                args=(user_input, preset_answer),
                daemon=True
            ).start()
        elif user_input_clean in PRESET_ANSWERS:
            preset_answer = PRESET_ANSWERS[user_input_clean]
            threading.Thread(
                target=self.show_preset_answer,
                args=(user_input, preset_answer),
                daemon=True
            ).start()
        else:
            actual_model = MODEL_NAME_MAP[self.current_model_display.get()]
            threading.Thread(
                target=self.api_request_thread,
                args=(user_input, actual_model, api_key),
                daemon=True
            ).start()

    # ========== API 连接测试 ==========
    def test_ark_connection(self):
        """测试API连接是否正常"""
        api_key = self.current_api_key.get().strip()
        if not api_key:
            messagebox.showerror("错误", "API Key不能为空！")
            return
        
        self.btn_test.config(state=tk.DISABLED)
        self.log_info("开始测试API连接...")
        
        def test_connection_thread():
            try:
                headers = {
                    "Content-Type": API_CONTENT_TYPE,
                    "Authorization": f"{API_AUTHORIZATION_PREFIX} {api_key}"
                }
                test_data = {
                    "model": MODEL_NAME_MAP[SUPPORTED_MODELS_DISPLAY[0]],
                    "messages": [{"role": "user", "content": "测试连接，无需返回复杂内容"}],
                    "temperature": 0.1,
                    "max_tokens": 10
                }
                
                response = requests.post(
                    f"{self.endpoint.get()}{API_PATH}",
                    headers=headers,
                    json=test_data,
                    timeout=REQUEST_TIMEOUT,
                    verify=False
                )
                
                if response.status_code == 200:
                    messagebox.showinfo("成功", "API连接正常！")
                    self.log_info("API连接测试成功")
                else:
                    messagebox.showerror("失败", f"连接失败：{response.status_code}")
                    self.log_error(f"API连接测试失败：{response.status_code}")
            except Exception as e:
                messagebox.showerror("异常", f"连接异常：{str(e)}")
                self.log_error(f"API连接测试异常：{e}")
            finally:
                self.btn_test.config(state=tk.NORMAL)
        
        # 开启线程测试，避免阻塞UI
        threading.Thread(target=test_connection_thread, daemon=True).start()

    # ========== 聊天记录管理 ==========
    def clear_chat_history(self):
        """清空当前聊天记录和本地历史文件"""
        if messagebox.askconfirm("确认", "是否确定清空所有聊天记录？"):
            # 清空界面聊天记录
            self.text_chat.config(state=tk.NORMAL)
            self.text_chat.delete("1.0", tk.END)
            self.text_chat.config(state=tk.DISABLED)
            
            # 清空内存中的记录
            self.message_list.clear()
            self.chat_history.clear()
            
            # 删除本地历史文件
            if os.path.exists(HISTORY_FILE):
                try:
                    os.remove(HISTORY_FILE)
                except Exception as e:
                    self.log_error(f"删除历史文件失败：{e}")
            
            self.log_info("聊天记录已清空")

    def load_chat_history(self):
        """加载本地保存的聊天记录"""
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    self.chat_history = json.load(f)
                    for msg in self.chat_history:
                        sender = "用户" if msg["role"] == "user" else "CraneAI"
                        self.show_message(
                            sender,
                            msg["content"],
                            msg.get("time", datetime.now().strftime(self.chat_time_format)),
                            is_user=(msg["role"] == "user")
                        )
                        self.message_list.append({"role": msg["role"], "content": msg["content"]})
                self.log_info("聊天记录加载成功")
            except Exception as e:
                self.log_error(f"加载聊天记录失败：{e}")

    def save_chat_history(self):
        """保存当前聊天记录到本地文件"""
        try:
            save_history = []
            for msg in self.message_list:
                save_history.append({
                    "role": msg["role"],
                    "content": msg["content"],
                    "time": datetime.now().strftime(self.chat_time_format)
                })
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(save_history, f, ensure_ascii=False, indent=2)
            self.log_info("聊天记录保存成功")
        except Exception as e:
            self.log_error(f"保存聊天记录失败：{e}")

    # ========== 窗口事件绑定 ==========
    def bind_window_events(self):
        """绑定窗口关闭事件"""
        self.protocol("WM_DELETE_WINDOW", self.on_window_close)

    def on_window_close(self):
        """窗口关闭回调，保存聊天记录和设置"""
        self.save_chat_history()
        self.save_settings()
        self.log_info("CraneAI客户端已关闭")
        self.quit()

# ========== 程序入口 ==========
if __name__ == "__main__":
    try:
        app = CraneAIStyleGUI()
        app.mainloop()
    except Exception as e:
        logging.error(f"程序运行异常：{e}", exc_info=True)
        messagebox.showerror("致命错误", f"程序运行异常：{str(e)}")