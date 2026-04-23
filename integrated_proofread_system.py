# -*- coding: utf-8 -*-
"""
HWP 통합 교정 시스템 - 최종본
모든 교정 기능을 통합한 단일 실행 파일

기능:
1. 의존명사 띄어쓰기 교정 (것, 수, 데, 바, 지, 뿐, 적, 등, 때, 중, 상...)
2. 지명 변환 (나라→조, 황주→황해도)
3. 따옴표 변환 (""→'')
4. 보조용언 띄어쓰기 (고 있다, 해 보다...)
5. 복합 표현 (뿐만 아니라, 수 있다/없다...)
6. 문맥 기반 띄어쓰기
7. 바이너리 + COM 이중 교정
"""

import sys, os, re, struct, zlib, hashlib, time, shutil, stat, argparse
from datetime import datetime
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import olefile
except ImportError:
    print("olefile 패키지 필요: pip install olefile")
    sys.exit(1)

try:
    import win32com.client
    import pythoncom
    HAS_COM = True
except ImportError:
    HAS_COM = False
    print("win32com 없음 - COM 교정 비활성화")

from hwp_proofread.constants import PROVINCE_ABBREV, SECTIONS, DEPENDENT_NOUNS, DEPENDENT_NOUN_PHRASES
from hwp_proofread.spacing_rules import (
    SpacingCorrector, apply_dependent_noun_inspection, apply_text_corrections,
    build_all_rules, BOTH_FORMS_DEP_NOUNS
)

RULES_CHINA_PLACE = r"C:\AMD\AJ\hwp_proofreading_package\rules_china_place.txt"

GEOT_NOSPLIT = {"이것","그것","저것","이것저것","그것저것","보잘것","옛것","새것","별것","모든것","어느것","어떤것","들것","말것"}

SU_NOSPLIT = {
    "장수","교수","척수","우수","선수","준수","주파수","정수","함수","감수","인수","순수","특수","기수","접수","군수","죄수","다수",
    "가수","수수","보수","점수","완수","지수","호수","분수","박수","불수","할수록","매수","차수","상수","변수","소수","횟수",
    "갈수","본수","갈수록","될수록","역수","약수","공수","출수","생수","화수","해수","강수","풍수",
    "수술","수도","수원","수산","수입","수출","수면","수련","수렵","수호","수비","수색","수송","수확","수집","수여","수행","수반",
    "수습","수용","수치","수필","수분","수명","수단","수리","치수","속임수","복수","흡수","급수","한수","운수","어수",
    "계수","도수","액수","건수","명수","회수","층수","권수","징수","산수","홀수","단수","밀수","검수","입수",
    "포수","묘수","암수","추수","낙수","유수","조수","배수","누수","탈수","양수","음수",
    "총수","평균수","최대수","최소수","합계수","누계수","증감수","옥수수","기본주파수","교통운수","머리수","파수","고수",
    "목수","방수","부수","금수","취수","거수","무수","근수","독수","대수","압수","몰수","담수","혼수","홍수","전수",
    "령수","옥수","철수","국수","적수","야수","엄수","차단주파수","실수","침수","헛수","간수","충수","저수","락수","랭수",
    "어쩔수","얻을수","볼수","떨어질수","할수","알수","이십팔수","말수","골수","필수","원심탈수","문화재밀수","률수","예술수",
    "생활수","지방일수","찰수","연수","진수","경수","뇌수","평수","광수","난수","세수","의수","치수",
}

TTAWI_NOSPLIT = {"따위","따위의","따위로","따위를","따위는","따위가","따위도"}
SAI_NOSPLIT = {"강사이","수사이","두사이","그사이","이사이","중간사이"}
PPUN_NOSPLIT = {"뿐만","뿐이다","뿐이었다","뿐이고","뿐이며","뿐이니","사뿐사뿐","사뿐"}

CHUK_NOSPLIT_PREFIXES = ("개척","세척","척추","척결","척도","척골","질척","부척","권척","곡척","협척","률척","고정척","진촌퇴척","척박","간척","투척")

CHUK_NOSPLIT = {
    "배척하다","배척하고","배척당하고","무척","지척","인척","세척","개척하다","인기척","척하다","척하고","척추","척수","척도","진척하다","간척","수척","기척",
    "친한척","사람인척","아는척하면","척추뼈","진척","척박한","간척하다","질척질척한","수척해","지척거리다","공사진척","척하여",
}

DE_NOSPLIT = {"어데","여데","그데","이데","저데","구데","어느데","어떤데","모든데","아무데","김데","옛데","새데","별데","좋은데","나쁜데"}

JI_NOSPLIT = {"세지","네지","두지","한지","이지","저지","그지","어느지","어떤지","모든지","아무지","별지","옛지","새지","굳은지","큰지","작은지","많은지","적은지","좋은지","나쁜지"}

JUNGDWAE_NOSPLIT = {"공중","수중","의중","귀중","민중","대중","집중","신중","시중","논중","중중","과중","적중","궁중","열중","상중","진중","영중","운중","연중","년중","월중","일중","시중","속중","그중","이중","저중","어느중","어떤중","모든중","아무중","별중","옛중","새중"}

NOSPLIT_SETS = {
    '것': GEOT_NOSPLIT, '수': SU_NOSPLIT, '따위': TTAWI_NOSPLIT, '사이': SAI_NOSPLIT,
    '뿐': PPUN_NOSPLIT, '척': CHUK_NOSPLIT, '데': DE_NOSPLIT, '지': JI_NOSPLIT,
    '중': JUNGDWAE_NOSPLIT,
}

DAERO_NOSPLIT = {
    "이대로","그대로","저대로","어느대로","어떤대로","모든대로","아무대로","별대로","옛대로","새대로","굳이대로","크대로","작대로","많대로","적대로","좋대로","나쁘대로",
    "바로대로","그냥대로","있는대로","없는대로","보는대로","듣는대로","아는대로","모르는대로","가는대로","오는대로","하는대로","되는대로","주는대로","받는대로",
    "생각대로","마음대로","뜻대로","소원대로","요구대로","명령대로","지시대로","계획대로","약속대로","기대대로","예상대로","희망대로","바람대로","의도대로",
    "순서대로","차례대로","순서대로","순서대로","순서대로","순서대로","순서대로","순서대로","순서대로","순서대로","순서대로","순서대로","순서대로","순서대로",
}

MANKEUM_NOSPLIT = {
    "이만큼","그만큼","저만큼","어느만큼","어떤만큼","모든만큼","아무만큼","별만큼","옛만큼","새만큼","굳이만큼","크만큼","작만큼","많만큼","적만큼","좋만큼","나쁘만큼",
    "있는만큼","없는만큼","보는만큼","듣는만큼","아는만큼","모르는만큼","가는만큼","오는만큼","하는만큼","되는만큼","주는만큼","받는만큼",
    "생각만큼","마음만큼","뜻만큼","소원만큼","요구만큼","명령만큼","지시만큼","계획만큼","약속만큼","기대만큼","예상만큼","희망만큼","바람만큼","의도만큼",
}

JUL_NOSPLIT = {
    "이줄","그줄","저줄","어느줄","어떤줄","모든줄","아무줄","별줄","옛줄","새줄","굳이줄","크줄","작줄","많줄","적줄","좋줄","나쁘줄",
    "있는줄","없는줄","보는줄","듣는줄","아는줄","모르는줄","가는줄","오는줄","하는줄","되는줄","주는줄","받는줄",
    "생각줄","마음줄","뜻줄","소원줄","요구줄","명령줄","지시줄","계획줄","약속줄","기대줄","예상줄","희망줄","바람줄","의도줄",
    "줄알다","줄모르다","줄알았다","줄몰랐다","줄알고","줄모르고","줄알면","줄모르면",
}

TEO_NOSPLIT = {
    "이터","그터","저터","어느터","어떤터","모든터","아무터","별터","옛터","새터","굳이터","크터","작터","많터","적터","좋터","나쁘터",
    "있는터","없는터","보는터","듣는터","아는터","모르는터","가는터","오는터","하는터","되는터","주는터","받는터",
    "생각터","마음터","뜻터","소원터","요구터","명령터","지시터","계획터","약속터","기대터","예상터","희망터","바람터","의도터",
}

CHAE_NOSPLIT = {
    "이체","그체","저체","어느체","어떤체","모든체","아무체","별체","옛체","새체","굳이체","크체","작체","많체","적체","좋체","나쁘체",
    "있는체","없는체","보는체","듣는체","아는체","모르는체","가는체","오는체","하는체","되는체","주는체","받는체",
    "생각체","마음체","뜻체","소원체","요구체","명령체","지시체","계획체","약속체","기대체","예상체","희망체","바람체","의도체",
    "아는체하다","모르는체하다","있는체하다","없는체하다","아는체하고","모르는체하고","있는체하고","없는체하고",
}

JEOK_NOSPLIT = {
    "이적","그적","저적","어느적","어떤적","모든적","아무적","별적","옛적","새적","굳이적","크적","작적","많적","적적","좋적","나쁘적",
    "있는적","없는적","보는적","듣는적","아는적","모르는적","가는적","오는적","하는적","되는적","주는적","받는적",
    "생각적","마음적","뜻적","소원적","요구적","명령적","지시적","계획적","약속적","기대적","예상적","희망적","바람적","의도적",
    "한적","간적","본적","들은적","먹은적","받은적","했던적","했었던적","살았던적","다녔던적","갔던적","왔던적","읽었던적","썼던적","만났던적",
}

JI_NOSPLIT = {
    "이지","그지","저지","어느지","어떤지","모든지","아무지","별지","옛지","새지","굳이지","크지","작지","많지","적지","좋지","나쁘지",
    "있는지","없는지","보는지","듣는지","아는지","모르는지","가는지","오는지","하는지","되는지","주는지","받는지",
    "생각지","마음지","뜻지","소원지","요구지","명령지","지시지","계획지","약속지","기대지","예상지","희망지","바람지","의도지",
    "한지","간지","본지","들은지","먹은지","받은지","했던지","했었던지","살았던지","다녔던지","갔던지","왔던지","읽었던지","썼던지","만났던지",
}

BA_NOSPLIT = {
    "이바","그바","저바","어느바","어떤바","모든바","아무바","별바","옛바","새바","굳이바","크바","작바","많바","적바","좋바","나쁘바",
    "있는바","없는바","보는바","듣는바","아는바","모르는바","가는바","오는바","하는바","되는바","주는바","받는바",
    "생각바","마음바","뜻바","소원바","요구바","명령바","지시바","계획바","약속바","기대바","예상바","희망바","바람바","의도바",
    "할바","있을바","없을바","볼바","들을바","알바","모를바","갈바","올바","할바","될바","줄바","받을바",
}

IHA_NOSPLIT = {
    "이하","그이하","저이하","어느이하","어떤이하","모든이하","아무이하","별이하","옛이하","새이하","굳이이하","크이하","작이하","많이하","적이하","좋이하","나쁘이하",
    "명이하","개이하","원이하","kg이하","g이하","m이하","cm이하","mm이하","km이하","L이하","ml이하","%이하","도이하",
}

SANG_NOSPLIT = {
    "이상","그이상","저이상","어느이상","어떤이상","모든이상","아무이상","별이상","옛이상","새이상","굳이이상","크이상","작이상","많이상","적이상","좋이상","나쁘이상",
    "명이상","개이상","원이상","kg이상","g이상","m이상","cm이상","mm이상","km이상","L이상","ml이상","%이상","도이상",
    "이상하다","이상한","이상하게","이상스럽다","이상스러운","이상스럽게",
}

U_NOSPLIT = {
    "이우","그우","저우","어느우","어떤우","모든우","아무우","별우","옛우","새우","굳이우","크우","작우","많우","적우","좋우","나쁘우",
    "있는우","없는우","보는우","듣는우","아는우","모르는우","가는우","오는우","하는우","되는우","주는우","받는우",
}

JUNG_NOSPLIT = {
    "이중","그중","저중","어느중","어떤중","모든중","아무중","별중","옛중","새중","굳이중","크중","작중","많중","적중","좋중","나쁘중",
    "있는중","없는중","보는중","듣는중","아는중","모르는중","가는중","오는중","하는중","되는중","주는중","받는중",
    "회의중","작업중","수술중","진행중","검토중","개발중","수리중","운행중","영업중","수업중","회담중","면담중","통화중","진료중","조사중","연구중","학습중","훈련중","실험중","관측중","관찰중","측정중","분석중","평가중","검사중","심사중","심의중","논의중","협의중","협상중","교섭중","타결중","결정중","판단중","선택중","선정중","선발중","모집중","채용중","임용중","승진중","승급중","승격중","강등중","파면중","해임중","면직중","사임중","퇴직중","은퇴중","퇴거중","이사중","이전중","이동중","이송중","운송중","운반중","운수중","운전중","주행중","비행중","항해중","항공중","철도중","도로중","해상중","수상중","수중","지상중","공중","우주중","우주공간중",
}

GAT_NOSPLIT = {
    "이같","그같","저같","어느같","어떤같","모든같","아무같","별같","옛같","새같","굳이같","크같","작같","많같","적같","좋같","나쁘같",
    "있는같","없는같","보는같","듣는같","아는같","모르는같","가는같","오는같","하는같","되는같","주는같","받는같",
    "이같이","그같이","저같이","어느같이","어떤같이","모든같이","아무같이","별같이","옛같이","새같이","굳이같이","크같이","작같이","많같이","적같이","좋같이","나쁘같이",
    "이같은","그같은","저같은","어느같은","어떤같은","모든같은","아무같은","별같은","옛같은","새같은","굳이같은","크같은","작같은","많같은","적같은","좋같은","나쁘같은",
}

NARA_RULES = [
    ("나라때", "조 때"), ("나라말기", "조 말기"), ("나라시기", "조 시기"),
    ("나라중기", "조 중기"), ("나라초기", "조 초기"),
    ("나라", "조"),
]

SPACING_RULES = [
    ("고있다", "고 있다"), ("고있는", "고 있는"), ("고있었", "고 있었"),
    ("고있어", "고 있어"), ("고있겠", "고 있겠"), ("고있지", "고 있지"),
    ("고있고", "고 있고"), ("고있음", "고 있음"),
    ("해보다", "해 보다"), ("해본", "해 본"), ("해봐", "해 봐"),
    ("해봤", "해 봤"), ("해보려", "해 보려"), ("해보고", "해 보고"),
    ("살펴보다", "살펴 보다"), ("살펴본", "살펴 본"), ("살펴봐", "살펴 봐"),
    ("생각해보다", "생각해 보다"), ("생각해본", "생각해 본"), ("생각해봐", "생각해 봐"),
    ("먹어보다", "먹어 보다"), ("읽어보다", "읽어 보다"),
    ("흥정해본", "흥정해 본"), ("시탐해보다", "시탐해 보다"),
    ("조사해보다", "조사해 보다"), ("검사해보다", "검사해 보다"),
    ("역할따위", "역할 따위"), ("갈등따위", "갈등 따위"),
    ("넘어질번", "넘어질 번"), ("한번도", "한 번도"),
    ("한번은", "한 번은"), ("두번다시", "두 번 다시"),
    ("세번째", "세 번째"), ("첫번째", "첫 번째"), ("몇번", "몇 번"),
    ("수있다", "수 있다"), ("수있는", "수 있는"), ("수있었", "수 있었"),
    ("수있겠", "수 있겠"), ("수있어", "수 있어"), ("수있고", "수 있고"),
    ("수있음", "수 있음"), ("수있지", "수 있지"),
    ("것같다", "것 같다"), ("것같은", "것 같은"), ("것같이", "것 같이"),
    ("것같다", "것 같다"), ("것같음", "것 같음"), ("것같고", "것 같고"),
    ("척했다", "척했다"), ("척하는", "척하는"),
    ("할수", "할 수"), ("할수록", "할 수록"), ("될수", "될 수"),
    ("있을수", "있을 수"), ("없을수", "없을 수"), ("하는수", "하는 수"),
    ("할뿐", "할 뿐"), ("있을뿐", "있을 뿐"), ("뿐만아니라", "뿐만 아니라"),
    ("한적", "한 적"), ("간적", "간 적"), ("받은적", "받은 적"),
    ("먹은적", "먹은 적"), ("본적", "본 적"), ("들은적", "들은 적"),
    ("한지", "한 지"), ("된지", "된 지"), ("간지", "간 지"),
    ("지난지", "지난 지"), ("만난지", "만난 지"),
    ("할바", "할 바"), ("있는바", "있는 바"), ("아는바", "아는 바"),
    ("본바", "본 바"), ("들은바", "들은 바"),
    ("할것", "할 것"), ("있을것", "있을 것"), ("하는것", "하는 것"),
    ("된것", "된 것"), ("갈것", "갈 것"), ("올것", "올 것"),
    ("없는것", "없는 것"), ("있는것", "있는 것"), ("하는것", "하는 것"),
    ("갈데", "갈 데"), ("있을데", "있을 데"), ("없을데", "없을 데"),
    ("볼데", "볼 데"), ("쉴데", "쉴 데"),
    ("회의중", "회의 중"), ("작업중", "작업 중"), ("수술중", "수술 중"),
    ("진행중", "진행 중"), ("검토중", "검토 중"), ("개발중", "개발 중"),
    ("수리중", "수리 중"), ("운행중", "운행 중"), ("영업중", "영업 중"),
    ("명이상", "명 이상"), ("개이상", "개 이상"), ("원이상", "원 이상"),
    ("명이하", "명 이하"), ("개이하", "개 이하"), ("원이하", "원 이하"),
    ("이상의", "이상 의"), ("이하의", "이하 의"),
    ("사과등", "사과 등"), ("배등", "배 등"), ("포도등", "포도 등"),
    ("학생등", "학생 등"), ("교사등", "교사 등"),
    ("그때", "그 때"), ("이때", "이 때"), ("그때부터", "그 때부터"),
    ("그때에", "그 때에"), ("이때에", "이 때에"),
    ("아는척하다", "아는 척하다"), ("모르는척하다", "모르는 척하다"),
    ("있는척하다", "있는 척하다"), ("없는척하다", "없는 척하다"),
    ("아는척했다", "아는 척했다"), ("모르는척했다", "모르는 척했다"),
]

QUOTE_RULES = [
    (""", "'"), (""", "'"),
    ("「", "'"), ("」", "'"),
    ("『", "'"), ("』", "'"),
]

def load_china_rules(filepath):
    rules = []
    if not os.path.exists(filepath):
        return rules
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '→' in line:
                parts = line.split('→')
                if len(parts) == 2:
                    src = parts[0].strip()
                    dst = parts[1].strip()
                    if src and dst:
                        rules.append((src, dst))
    return rules

def file_hash(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def extract_text_from_records(records):
    text_parts = []
    for rec in records:
        if rec.get('type') == 'text':
            text_parts.append(rec.get('text', ''))
    return '\n'.join(text_parts)

def parse_records(text):
    records = []
    lines = text.split('\n')
    for line in lines:
        if line.strip():
            records.append({'type': 'text', 'text': line})
    return records

def process_hwp_binary(in_path, out_path, all_fixes, log_fn=print):
    OUT_TMP = out_path + '.tmp'

    ole_info = olefile.OleFileIO(in_path)
    streams = ole_info.listdir()

    bodytext_streams = []
    for s in streams:
        name = '/'.join(s)
        if name.startswith('BodyText/'):
            bodytext_streams.append(name)

    if not bodytext_streams:
        log_fn("BodyText 스트림 없음")
        ole_info.close()
        return None, [], 0

    shutil.copy2(in_path, OUT_TMP)

    total_changes = 0
    change_log = []

    with open(OUT_TMP, 'r+b') as f:
        for stream_name in bodytext_streams:
            try:
                entry = ole_info.getentry(stream_name)
                if not entry:
                    continue

                start_sector = entry['SecID']
                size = entry['Size']

                f.seek(512 + start_sector * 512)
                data = f.read(size)

                try:
                    text = data.decode('utf-16-le', errors='ignore')
                except:
                    continue

                original_text = text
                changes_in_stream = 0

                for src, dst, category, cnt in all_fixes:
                    if src in text:
                        occurrences = text.count(src)
                        text = text.replace(src, dst)
                        changes_in_stream += occurrences
                        change_log.append({
                            'stream': stream_name,
                            'category': category,
                            'before': src,
                            'after': dst,
                            'count': occurrences
                        })

                if changes_in_stream > 0:
                    new_data = text.encode('utf-16-le', errors='ignore')
                    compressed_data = zlib.compress(new_data, 6)

                    f.seek(512 + start_sector * 512)
                    f.write(compressed_data)

                    total_changes += changes_in_stream
                    log_fn(f"  [{stream_name}] {changes_in_stream}건 교정")

            except Exception as e:
                log_fn(f"  [{stream_name}] 오류: {e}")
                continue

    ole_info.close()

    if os.path.exists(out_path):
        os.chmod(out_path, stat.S_IWRITE | stat.S_IREAD)
        os.remove(out_path)
    os.rename(OUT_TMP, out_path)

    log_fn(f"\n  출력 파일: {out_path}")
    log_fn(f"  총 교정: {total_changes}건")

    return out_path, change_log, total_changes

class IntegratedProofreadSystem:
    def __init__(self, log_dir=None):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_dir = log_dir or os.path.join(os.path.dirname(__file__), 'logs')
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_path = os.path.join(self.log_dir, f"integrated_proofread_{self.timestamp}.txt")
        self.log_fh = None
        self.china_rules = load_china_rules(RULES_CHINA_PLACE)
        self.all_results = {}

    def log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] {msg}"
        print(line, flush=True)
        if self.log_fh:
            try:
                self.log_fh.write(line + "\n")
                self.log_fh.flush()
            except:
                pass

    def _collect_all_fixes(self, text):
        all_fixes = []

        for src, dst in NARA_RULES:
            cnt = text.count(src)
            if cnt > 0:
                all_fixes.append((src, dst, "나라→조", cnt))

        for src, dst in self.china_rules:
            if src in text:
                all_fixes.append((src, dst, "중한규칙", src))

        for src, dst in SPACING_RULES:
            cnt = text.count(src)
            if cnt > 0:
                all_fixes.append((src, dst, "띄어쓰기", cnt))

        for src, dst in QUOTE_RULES:
            cnt = text.count(src)
            if cnt > 0:
                all_fixes.append((src, dst, "따옴표", cnt))

        dep_results, both_forms = apply_dependent_noun_inspection(text)
        for noun, items in dep_results.items():
            for item in items:
                if len(item) == 3:
                    word, spaced, cnt = item
                    if word in text:
                        all_fixes.append((word, spaced, f"의존명사_{noun}", cnt))

        all_fixes.sort(key=lambda r: len(r[0]), reverse=True)

        return all_fixes

    def proofread_file(self, in_path, use_binary=True, use_com=True):
        self.log(f"\n{'=' * 70}")
        self.log(f"  파일 교정 시작")
        self.log(f"{'=' * 70}")

        if not os.path.exists(in_path):
            self.log(f"  파일 없음: {in_path}")
            return None

        base_name = os.path.basename(in_path)
        name_no_ext = os.path.splitext(base_name)[0]
        out_dir = os.path.dirname(in_path)
        out_path = os.path.join(out_dir, f"{name_no_ext}_교정완료_{self.timestamp}.hwp")

        with open(in_path, 'rb') as f:
            data = f.read()
        text = data.decode('utf-16-le', errors='ignore')

        self.log(f"  텍스트: {len(text):,}자")

        all_fixes = self._collect_all_fixes(text)
        self.log(f"  총 수정 항목: {len(all_fixes)}종")

        if not all_fixes:
            self.log(f"  수정 불필요 - 모든 규칙 이미 적용됨")
            return None

        total_changes = 0

        if use_binary:
            self.log(f"\n  --- 1단계: 바이너리 수준 교정 ---")
            result_path, change_log, changes = process_hwp_binary(in_path, out_path, all_fixes, self.log)
            if result_path:
                total_changes += changes
                in_path = result_path

        if use_com and HAS_COM:
            self.log(f"\n  --- 2단계: COM 자동화 교정 ---")
            try:
                pythoncom.CoInitialize()
                hwp = win32com.client.Dispatch("HWPFrame.HwpObject")
                hwp.RegisterModule("FilePathCheckDLL", "AutomationModule")
                hwp.Open(in_path, "", "")

                for src, dst, category, cnt in all_fixes:
                    try:
                        hwp.HAction.GetDefault("Replace", hwp.HParameterSet.HFindReplace.HSet)
                        hwp.HParameterSet.HFindReplace.FindString = src
                        hwp.HParameterSet.HFindReplace.ReplaceString = dst
                        hwp.HParameterSet.HFindReplace.ReplaceMode = 1
                        hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
                        hwp.HParameterSet.HFindReplace.Direction = 0
                        hwp.HAction.Execute("Replace", hwp.HParameterSet.HFindReplace.HSet)
                    except:
                        pass

                hwp.SaveAs(out_path, "", "")
                hwp.Quit()
                pythoncom.CoUninitialize()
                self.log(f"  COM 교정 완료")
            except Exception as e:
                self.log(f"  COM 교정 오류: {e}")

        self.log(f"\n  총 교정: {total_changes}건")
        self.log(f"  출력 파일: {out_path}")

        return out_path

    def run(self, files=None):
        self.log_fh = open(self.log_path, 'w', encoding='utf-8')
        self.log(f"HWP 통합 교정 시스템 시작")
        self.log(f"시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        if files:
            for f in files:
                if os.path.exists(f):
                    self.proofread_file(f)
        else:
            for key, section in SECTIONS.items():
                orig = section.get('orig')
                if orig and os.path.exists(orig):
                    self.proofread_file(orig)

        self.log(f"\n완료: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log_fh.close()

def main():
    parser = argparse.ArgumentParser(description="HWP 통합 교정 시스템")
    parser.add_argument("files", nargs="*", help="교정할 HWP 파일들")
    parser.add_argument("--no-binary", action="store_true", help="바이너리 교정 건너뛰기")
    parser.add_argument("--no-com", action="store_true", help="COM 교정 건너뛰기")
    parser.add_argument("--analyze", action="store_true", help="분석만 수행")
    args = parser.parse_args()

    system = IntegratedProofreadSystem()

    if args.analyze:
        for f in args.files:
            if os.path.exists(f):
                with open(f, 'rb') as fh:
                    data = fh.read()
                text = data.decode('utf-16-le', errors='ignore')
                fixes = system._collect_all_fixes(text)
                print(f"\n[{f}]")
                print(f"  텍스트: {len(text):,}자")
                print(f"  수정 항목: {len(fixes)}종")
                for src, dst, cat, cnt in fixes[:20]:
                    print(f"    [{cat}] '{src}' → '{dst}' ({cnt}건)")
    else:
        system.run(args.files if args.files else None)

if __name__ == "__main__":
    main()
