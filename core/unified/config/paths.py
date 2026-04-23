# -*- coding: utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_DIR = r"C:\Users\doris\.agent-skills"

RULES_CHINA_PLACE = r"C:\AMD\AJ\hwp_proofreading_package\rules_china_place.txt"
RULES_DOCUMENTATION = r"C:\AMD\AJ\hwp_proofreading_package\rules_documentation.txt"
PROOFREAD_RULES = r"C:\AMD\AJ\hwp_proofreading_package\hwp_proofreading\config\proofread_rules.txt"

BACKUP_DIR = r"C:\Users\doris\AppData\Local\Temp\hwp_backup"
LOG_DIR = r"C:\Users\doris\AppData\Local\Temp\hwp_logs"

FILES = {
    "J": {
        "orig": r"C:\Users\doris\Desktop\【大中朝 14】J 1419-1693--275--20240920_original_copy.hwp",
        "work": r"C:\Users\doris\Desktop\J_spacing_fixed.hwp",
    },
    "L": {
        "orig": r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920.hwp",
        "work": r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920__v1.hwp",
    },
    "K": {
        "orig": r"C:\Users\doris\Desktop\新词典\【大中朝 15】K 1694-1786--93--20240920.hwp",
        "work": r"C:\Users\doris\Desktop\xwechat_files\WORD\K 1694-1786--93--20240920_교정본_상세로그_20260418_재실행_작업본_최근규칙_작업본_20260418_3차.hwp",
    },
}

DYNASTIES = [
    "당(唐)", "송(宋)", "명(明)", "청(淸)", "원(元)", "수(隋)", "진(秦)", "한(漢)",
    "위(魏)", "촉(蜀)", "오(吴)", "진(晉)", "동진(東晉)", "서진(西晉)",
    "남송(南宋)", "북송(北宋)", "서하(西夏)", "요(遼)", "금(金)",
    "제(齊)", "초(楚)", "량(梁)", "진(陳)",
]

DYN_SUFFIXES = ["때", "시기", "말기", "초기", "중기", "시기에", "때의", "의", "에", "가", "를", "이후에는", "사람으로서"]
