# -*- coding: utf-8 -*-
import sys, os, io, re, struct, zlib, shutil, hashlib, stat, time
from collections import Counter
from datetime import datetime

sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import olefile
from hwp_ollama_proofread import extract_text_from_hwp_binary

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PY312 = r"C:\Users\doris\AppData\Local\Programs\Python\Python312\python.exe"

FILES = {
    "J": r"C:\Users\doris\Desktop\新词典\【大中朝 14】J 1419-1693--275--20240920_original_copy.hwp",
    "L": r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920.hwp",
}

OUT_DIR = r"c:\Users\doris\.agent-skills\output"
BACKUP_DIR = r"c:\Users\doris\.agent-skills\backups"
LOG_DIR = r"c:\Users\doris\.agent-skills\logs"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

GEOT_NOSPLIT = {
    "이것", "그것", "저것", "이것저것", "그것저것", "보잘것", "옛것", "새것",
    "별것",
    "보잘것없다", "보잘것없는", "보잘것없이", "보잘것없음",
    "아무것도", "아무것이", "아무것을", "아무것은", "아무것과",
}

SU_NOSPLIT = {
    "장수", "교수", "척수", "우수", "선수", "준수", "주파수", "정수", "함수",
    "감수", "인수", "순수", "특수", "기수", "접수", "군수", "죄수", "다수",
    "가수", "수수", "보수", "점수", "완수", "지수", "호수", "분수",
    "박수", "불수", "할수록", "매수", "차수", "상수", "변수", "소수", "횟수",
    "역수", "약수", "공수", "출수", "생수", "화수", "해수", "강수", "풍수",
    "수술", "수도", "수원", "수산", "수입", "수출", "수면", "수련", "수렵",
    "수호", "수비", "수색", "수송", "수확", "수집", "수여", "수행", "수반",
    "수습", "수용", "수치", "수필", "수분", "수명", "수단", "수리",
    "치수", "속임수", "복수", "흡수", "급수", "한수", "운수", "어수",
    "계수", "도수", "액수", "건수", "명수", "회수", "층수", "권수",
    "징수", "산수", "홀수", "단수", "밀수", "검수", "입수",
    "포수", "묘수", "암수", "추수", "낙수", "유수", "조수",
    "배수", "누수", "탈수", "양수", "음수",
    "총수", "평균수", "최대수", "최소수", "합계수", "누계수", "증감수",
    "옥수수", "기본주파수", "교통운수", "머리수", "파수", "고수",
    "목수", "방수", "부수", "금수", "취수", "거수", "무수", "근수",
    "독수", "대수", "압수", "몰수", "담수", "혼수", "홍수", "전수",
    "령수", "옥수", "철수", "국수", "적수", "야수", "엄수", "차단주파수",
    "실수", "침수", "헛수", "간수", "충수", "저수", "락수", "랭수",
    "이십팔수", "말수", "골수", "필수", "원심탈수", "문화재밀수",
    "률수", "예술수", "생활수", "지방일수", "찰수", "연수", "진수",
    "경수", "뇌수", "평수", "광수", "난수", "세수", "의수",
    "갈수록", "될수록", "할수록",
}

PPUN_NOSPLIT = {"뿐만", "뿐이다", "뿐이었다", "뿐이고", "뿐이며", "뿐이니", "사뿐사뿐", "사뿐", "가뿐", "가뿐하다", "가뿐하게", "가뿐한", "이뿐", "고우나뿐"}

BA_NOSPLIT = {
    "바다", "바람", "바늘", "바깥", "바구니", "바닥", "바탕",
    "바위", "바이러스", "바이올린", "바코드", "바람직",
    "김바", "밭바", "산바", "들바",
    "바꾸다", "바꾸어", "바꾸면",
    "바라다", "바라고", "바라면",
    "바로", "바르다", "바르게",
    "바치다", "바치고", "바치면",
    "바라", "바래", "바랍",
    "어바", "가바", "하바", "자바",
    "우바", "좌바", "대바", "명바",
    "바깥", "바깥쪽", "바깥으로",
    "거울바", "문바", "길바",
    "곧바로", "똑바로", "올바르다", "옳바르다",
    "뒤바뀌다", "뒤바뀌", "뒤바뀐",
    "거꾸로바뀌다", "서로바뀌다",
    "바삭바삭", "반짝반짝",
    "곧바", "똑바", "옳바", "뒤바",
    "지르바", "울바", "낯바", "밑바",
    "고무바", "손바", "가을바",
    "룸바", "견인바", "쇠바", "골덴바",
    "회오리바", "돌개바", "류산바", "장바", "막바",
    "바탕", "바람", "바다", "바느질",
}

JEOK_DEP_NOSPLIT = {
    "적성", "적자", "적중", "적응", "적극", "적법", "적당",
    "적색", "적소", "적임", "적요", "적의", "적합", "적활",
    "부적", "부적절", "부적당", "부적합",
    "적극적", "소극적", "적극적으로", "소극적으로",
    "적극성", "적성검사", "적자결산", "적자운행",
    "근본적", "기본적", "일반적", "구체적", "객관적", "주관적",
    "절대적", "상대적", "적대적",
    "특수적", "개별적", "전체적", "국부적",
    "순간적", "영구적", "일시적", "지속적", "정치적",
    "경제적", "사회적", "문화적", "역사적", "과학적",
    "시간적", "공간적", "물리적", "화학적", "생물적",
    "원적", "본적지", "본적을", "본적이", "본적의",
    "시간적구간", "공간적인", "순간적으로", "순간적인",
    "근본적으로", "기본적으로", "일반적으로", "구체적으로",
    "적혈구", "적기", "적령", "적막", "적산", "적선",
    "적의", "적조", "적토",
}

DE_NOSPLIT = {
    "가운데", "한가운데", "그가운데", "포름알데", "놀포름알데",
    "메타알데", "아쎄트알데", "알데", "데굴데", "번데", "한데", "아데",
    "데려", "데리고", "데려가", "데려오", "데릴",
    "앙데", "지데", "놀이데", "춤데",
    "수데", "김데", "빛데", "밤데", "길데", "밭데",
    "어데", "여데", "제데", "참데", "집데",
    "껍데기", "껍데", "껍질데",
    "사람가운데", "것가운데", "곳가운데", "땅가운데",
    "집가운데", "물가운데", "산가운데", "길가운데",
    "또래가운데", "세계가운데", "국민소득가운데",
    "데구르르", "데굴데굴", "데미지", "데시벨",
    "데탕트", "데투라", "데우다", "데워",
}

SANG_DIR_NOSPLIT = {
    "세상", "항상", "현상", "리상", "이상", "예상", "사상", "로상",
    "조상", "책상", "증상", "감상", "륙상", "고상", "진상", "대상",
    "린상", "정상", "수상", "기상", "해상", "손상", "호상", "인상",
    "앙상", "지상", "추상", "중상", "가상", "화상", "령상", "살상",
    "일상", "관상", "걸상", "련쇄상", "립상",
    "상하", "상대", "상황", "상태", "상식", "상류", "상반", "상쇄",
    "상한", "상처", "상실", "상쾌", "상쾌하다",
    "예상하다", "예상하고", "예상한",
    "감상하다", "감상하고",
    "진상하다", "진상하고",
    "림상", "화장상", "중개상", "빙상", "가격상", "매상",
    "돌묵상", "도리상", "유유상", "련립상", "대나무침상",
    "실상", "린편상", "류상", "랭상", "침상", "거상",
    "소상", "노상", "백상", "문상", "탁상", "연상",
    "상인", "상업", "상점", "상품", "상공", "상류",
    "투상", "조상", "명상", "운상", "외상", "내상",
    "인간세상", "노벨물리학상", "둘이상",
}

HA_DIR_NOSPLIT = {
    "비유하다", "속하다", "형용하다", "못하다", "말하다",
    "청렴하다", "사용하다", "일하다", "처리하다",
    "로련하다", "대하다", "다하다", "련결하다",
    "리용하다", "리해하다", "생각하다", "피로하다",
    "랭담하다", "좋아하다", "그리워하다", "쌀쌀하다",
    "정리하다", "어수선하다", "비슷하다", "시원하다",
    "발생하다", "계속하다", "당하다", "조심하다",
    "정직하다", "민첩하다", "란잡하다", "깨끗하다",
    "침착하다", "안내하다", "이야기하다", "진행하다",
    "실행하다", "싫어하다", "단정하다",
    "하다", "하고", "하여", "해서", "하였다", "한다", "한", "하세요",
    "하기", "함", "할", "했", "하는",
    "강하다", "강하게", "강하고",
    "경사하다", "경사하고",
    "하천", "하류", "하반", "하부", "하층",
    "하늘", "하기", "하지", "하숙", "하숙집",
    "포기하다", "포기하고",
    "시작하다", "시작하고",
    "연구하다", "연구하고",
    "노력하다", "노력하고",
    "준비하다", "준비하고",
    "결정하다", "결정하고",
    "출발하다", "출발하고",
    "도착하다", "도착하고",
    "이동하다", "이동하고",
    "변경하다", "변경하고",
    "수정하다", "수정하고",
    "확인하다", "확인하고",
    "요구하다", "요구하고",
    "제출하다", "제출하고",
    "보고하다", "보고하고",
    "신고하다", "신고하고",
    "경고하다", "경고하고",
    "권고하다", "권고하고",
    "견고하다", "견고하고", "견고하여",
    "확고하다", "확고하고", "확고하여",
    "숭고하다", "숭고하고",
    "고고하다", "고고하고",
    "허락하다", "허락하고",
    "거절하다", "거절하고",
    "승인하다", "승인하고",
    "부정하다", "부정하고",
    "긍정하다", "긍정하고",
    "인정하다", "인정하고",
    "부인하다", "부인하고",
    "주장하다", "주장하고",
    "주동하다", "주동하고",
    "강조하다", "강조하고",
    "설명하다", "설명하고",
    "해석하다", "해석하고",
    "분석하다", "분석하고",
    "비판하다", "비판하고",
    "평가하다", "평가하고",
    "판단하다", "판단하고",
    "선택하다", "선택하고",
    "채택하다", "채택하고",
    "거절하다", "거절하고",
    "반대하다", "반대하고",
    "찬성하다", "찬성하고",
    "동의하다", "동의하고",
    "협조하다", "협조하고",
    "지시하다", "지시하고",
    "지도하다", "지도하고",
    "지원하다", "지원하고",
    "보호하다", "보호하고",
    "방어하다", "방어하고",
    "공격하다", "공격하고",
    "방어하다", "방어하고",
    "수비하다", "수비하고",
    "수호하다", "수호하고",
    "수정하다", "수정하고",
    "개선하다", "개선하고",
    "개량하다", "개량하고",
    "발전하다", "발전하고",
    "진보하다", "진보하고",
    "퇴보하다", "퇴보하고",
    "향상하다", "향상하고",
    "향상되다", "향상되고",
    "제고하다", "제고하고",
    "증가하다", "증가하고",
    "감소하다", "감소하고",
    "증대하다", "증대하고",
    "감소하다", "감소하고",
    "확대하다", "확대하고",
    "축소하다", "축소하고",
    "확장하다", "확장하고",
    "축소하다", "축소하고",
    "성공하다", "성공하고",
    "실패하다", "실패하고",
    "완성하다", "완성하고",
    "달성하다", "달성하고",
    "도달하다", "도달하고",
    "도착하다", "도착하고",
    "완료하다", "완료하고",
    "종료하다", "종료하고",
    "시작하다", "시작하고",
    "개시하다", "개시하고",
    "착수하다", "착수하고",
    "착공하다", "착공하고",
    "준공하다", "준공하고",
    "운행하다", "운행하고",
    "운영하다", "운영하고",
    "관리하다", "관리하고",
    "운영하다", "운영하고",
    "경영하다", "경영하고",
    "운전하다", "운전하고",
    "조작하다", "조작하고",
    "조절하다", "조절하고",
    "통제하다", "통제하고",
    "감독하다", "감독하고",
    "감시하다", "감시하고",
    "관찰하다", "관찰하고",
    "검사하다", "검사하고",
    "검토하다", "검토하고",
    "조사하다", "조사하고",
    "연구하다", "연구하고",
    "탐구하다", "탐구하고",
    "탐색하다", "탐색하고",
    "발견하다", "발견하고",
    "발명하다", "발명하고",
    "창조하다", "창조하고",
    "창작하다", "창작하고",
    "제작하다", "제작하고",
    "생산하다", "생산하고",
    "제조하다", "제조하고",
    "가공하다", "가공하고",
    "건설하다", "건설하고",
    "축조하다", "축조하고",
    "조립하다", "조립하고",
    "설치하다", "설치하고",
    "배치하다", "배치하고",
    "배열하다", "배열하고",
    "정렬하다", "정렬하고",
    "분류하다", "분류하고",
    "구분하다", "구분하고",
    "구별하다", "구별하고",
    "식별하다", "식별하고",
    "판별하다", "판별하고",
    "감별하다", "감별하고",
    "선별하다", "선별하고",
    "선발하다", "선발하고",
    "선거하다", "선거하고",
    "투표하다", "투표하고",
    "당선하다", "당선하고",
    "낙선하다", "낙선하고",
    "임명하다", "임명하고",
    "지명하다", "지명하고",
    "추천하다", "추천하고",
    "천거하다", "천거하고",
    "파면하다", "파면하고",
    "해임하다", "해임하고",
    "면직하다", "면직하고",
    "사임하다", "사임하고",
    "은퇴하다", "은퇴하고",
    "퇴직하다", "퇴직하고",
    "퇴임하다", "퇴임하고",
    "취임하다", "취임하고",
    "취직하다", "취직하고",
    "입사하다", "입사하고",
    "퇴사하다", "퇴사하고",
    "전근하다", "전근하고",
    "승진하다", "승진하고",
    "강등하다", "강등하고",
    "진급하다", "진급하고",
    "졸업하다", "졸업하고",
    "입학하다", "입학하고",
    "퇴학하다", "퇴학하고",
    "수료하다", "수료하고",
    "이수하다", "이수하고",
    "학습하다", "학습하고",
    "연구하다", "연구하고",
    "교육하다", "교육하고",
    "훈련하다", "훈련하고",
    "련습하다", "련습하고",
    "실천하다", "실천하고",
    "실행하다", "실행하고",
    "실시하다", "실시하고",
    "시행하다", "시행하고",
    "시행되다", "시행되고",
    "적용하다", "적용하고",
    "적용되다", "적용되고",
    "운용하다", "운용하고",
    "활용하다", "활용하고",
    "리용하다", "리용하고",
    "사용하다", "사용하고",
    "사용되다", "사용되고",
    "이용하다", "이용하고",
    "이용되다", "이용되고",
    "채용하다", "채용하고",
    "채용되다", "채용되고",
    "채택하다", "채택하고",
    "채택되다", "채택되고",
    "채점하다", "채점하고",
    "채집하다", "채집하고",
    "채색하다", "채색하고",
    "채우다", "채워", "채운",
    "채소", "채널", "채팅",
    "채권", "채무", "채석",
}

JUNG_NOSPLIT = {
    "신중", "대중", "이중", "관중", "귀중", "공중", "랑중", "집중",
    "소중", "존중", "도중", "진중", "정중", "엄중", "명중", "적중",
    "궁중", "하중", "시중", "군중", "장중", "출중", "과중", "기중",
    "일반대중", "무의식중", "한밤중", "어중이떠중", "부지중",
    "그중", "나중", "산중", "밤중", "한중", "위중", "고대중",
    "세기중", "압연과정중",
    "중간", "중심", "중앙", "중요", "중복", "중단", "중지", "중계",
    "중량", "중소", "중순", "중세", "중기", "중류", "중합", "중화",
    "중독", "중상", "중년", "중국", "중부", "중층", "중형",
    "집중하다", "집중하고", "집중하여",
    "신중하다", "신중하고", "신중한",
    "대중적", "대중화",
    "비중", "민중", "인장하중", "인중", "다중", "삼중",
    "상중", "랭중", "찬중", "리중", "중얼중", "소장중", "십중",
    "압축하중", "인장하중", "전단하중", "비틀림하중",
    "휨하중", "축하중", "경하중", "활하중",
    "집중하중", "등분포하중", "분포하중",
    "수중", "우중", "둔중", "까마중", "하늘공중",
    "일중", "오중", "려정도중", "려행도중",
    "수중에", "수중의", "수중에서",
    "공중에", "공중의", "공중에서",
    "우중에", "우중의",
    "둔중한", "둔중하다", "둔중하고",
    "까마중에", "까마중의",
    "하늘공중에", "하늘공중의",
    "일중에", "일중의",
    "오중에", "오중의",
    "려정도중에", "려정도중의",
    "려행도중에", "려행도중의",
    "령도도중", "사업도중", "작업도중", "회의도중",
    "수업도중", "식사도중", "수송도중", "이동도중",
    "전투도중", "훈련도중", "시험도중", "조사도중",
    "공사도중", "건설도중", "운전도중", "운행도중",
    "집회도중", "행사도중", "관람도중", "관광도중",
    "비중에", "비중의", "비중이", "비중을",
    "민중에", "민중의", "민중이",
    "체중", "체중을", "체중이", "체중의",
    "심중", "심중을", "심중에", "심중의",
    "안중", "안중에", "안중의",
    "좌중", "좌중의", "좌중에",
    "취중", "취중에", "취중의",
    "옥중", "옥중의", "옥중에",
    "은연중", "은연중에", "은연중의",
    "말중", "말중에", "말중의",
    "극중", "극중의", "극중에",
    "전중", "전중을", "전중에",
    "주중", "야중",
}

ISANG_NOSPLIT = {"이상", "이상의", "이상으로", "이상하다", "이상하게", "이상한", "정상이상", "비정상이상"}
IHA_NOSPLIT = {
    "가까이하다", "가까이하고", "가까이하여", "가까이해서", "가까이한",
    "기이하다", "기이하고", "기이한", "기이하여",
    "되풀이하다", "되풀이하고", "되풀이하여", "되풀이한",
    "해이하다", "해이하고", "해이한", "해이하여",
    "같이하다", "같이하고", "같이하여",
    "괴이하다", "괴이하고", "괴이한", "괴이하여",
    "특이하다", "특이하고", "특이한", "특이하여",
    "용이하다", "용이하고", "용이한",
    "부득이하다", "부득이하고", "부득이한",
    "맞이하다", "맞이하고", "맞이하여", "맞이한",
    "수준이하", "생리적령점이하", "령이하", "영도이하", "류행성이하",
    "상이하다", "상이하고", "상이한",
    "중동무이하다", "중동무이하고",
    "되풀이", "고기잡이", "기이", "용이", "가까이", "해이", "괴이", "매갈이", "돈벌이",
}

AP_NOSPLIT = {
    "앞날", "앞문", "앞바다", "앞발", "앞서다", "앞세우다",
    "앞장", "앞장서다", "앞뒤", "앞뒤가", "앞뒤를",
    "앞니", "앞가슴", "앞꿈치", "앞마당", "앞머리",
    "앞바퀴", "앞발", "앞부분", "앞쪽", "앞쪽의",
    "맨앞", "제일앞", "오른앞", "왼앞",
}

DDUT_NOSPLIT = {
    "뜻하지", "뜻밖에", "뜻밖의", "뜻밖",
    "본뜻", "원뜻", "참뜻", "속뜻", "첫뜻",
    "큰뜻", "작은뜻", "깊은뜻",
}

MODU_NOSPLIT = {
    "모두", "모두가", "모두를", "모두의", "모두는", "모두도",
}


def file_hash(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def parse_records(data):
    records = []
    offset = 0
    while offset < len(data) - 4:
        raw = struct.unpack_from('<I', data, offset)[0]
        tag_id = raw & 0x3FF
        level = (raw >> 10) & 0x3FF
        size = (raw >> 20) & 0xFFF
        if size == 0xFFF:
            if offset + 8 > len(data):
                break
            size = struct.unpack_from('<I', data, offset + 4)[0]
            header_size = 8
        else:
            header_size = 4
        if offset + header_size + size > len(data):
            break
        payload = data[offset + header_size:offset + header_size + size]
        records.append({
            "tag_id": tag_id,
            "level": level,
            "size": size,
            "header_size": header_size,
            "payload": payload,
        })
        offset += header_size + size
    return records


def rebuild_stream(records):
    parts = []
    for rec in records:
        payload = rec["payload"]
        size = len(payload)
        level = rec["level"]
        tag_id = rec["tag_id"]
        if size < 0xFFF:
            header = struct.pack('<I', tag_id | (level << 10) | (size << 20))
        else:
            header = struct.pack('<I', tag_id | (level << 10) | (0xFFF << 20)) + struct.pack('<I', size)
        parts.append(header + payload)
    return b''.join(parts)


def extract_text_from_records(records):
    texts = []
    for rec in records:
        if rec["tag_id"] != 67:
            continue
        try:
            texts.append(rec["payload"].decode("utf-16-le", errors="replace"))
        except Exception:
            continue
    return ''.join(texts)


def extract_text(filepath):
    ole = olefile.OleFileIO(filepath, write_mode=False)
    try:
        all_texts = []
        for sp in ole.listdir():
            if sp[0] == "BodyText":
                raw = ole.openstream('/'.join(sp)).read()
                try:
                    dec = zlib.decompress(raw, -15)
                except zlib.error:
                    continue
                records = parse_records(dec)
                all_texts.append(extract_text_from_records(records))
    finally:
        ole.close()
    return '\n'.join(all_texts)


def generate_context_rules(text):
    changes = []
    seen = {}

    def add(src, dst, cat):
        if src in seen:
            return
        cnt = text.count(src)
        if cnt > 0:
            changes.append((src, dst, cat, cnt))
            seen[src] = True

    # 1. 것 - 의존명사 (정밀 패턴: 그룹 캡처 사용)
    geot_suffixes = [
        '은', '이', '을', '으로', '과', '와', '도', '만', '까지', '처럼',
        '같이', '이라', '이란', '인데', '인지', '이나', '이라도', '이든', '이야',
        '이어서', '이어야', '이어도', '이어만',
    ]
    geot_pattern = re.compile(
        r'([가-힣]+)(것(?:' + '|'.join(s for s in geot_suffixes) + r'))'
    )
    for m in geot_pattern.finditer(text):
        before = m.group(1)
        geot_part = m.group(2)
        full = m.group(0)
        base = before + '것'
        if base in GEOT_NOSPLIT or full in GEOT_NOSPLIT or base == '것':
            continue
        suffix = geot_part[1:]
        add(full, f"{before} 것{suffix}", "것")

    geot_pattern2 = re.compile(r'([가-힣]+)(것(?:같다|같은|같이|같고))')
    for m in geot_pattern2.finditer(text):
        before = m.group(1)
        geot_part = m.group(2)
        full = m.group(0)
        base = before + '것'
        if base in GEOT_NOSPLIT or full in GEOT_NOSPLIT:
            continue
        suffix = geot_part[1:]
        add(full, f"{before} 것{suffix}", "것 같은")

    # 2. 수 - 의존명사
    su_stems = ['할', '될', '있을', '없을', '갈', '볼', '알', '쓸', '칠', '먹을',
                '걸을', '탈', '받을', '만들', '달릴', '부를', '지낼', '닦을', '뛸',
                '읽을', '찾을', '살', '열', '뽑을', '고를', '고칠', '넣을',
                '빚을', '깎을', '줄', '막을', '지을', '지킬', '따를', '이길',
                '느낄', '바꿀', '뗄', '놓을', '빼앗을', '깨울', '빨',
                '그릴', '누릴', '다닐', '돕', '맡을', '묻', '빌',
                '쏠', '외울', '일으킬', '팔', '핥']
    for stem in su_stems:
        for suffix in ['수', '수도', '수밖에']:
            orig = stem + suffix
            if orig in SU_NOSPLIT:
                continue
            cnt = text.count(orig)
            if cnt > 0:
                add(orig, f"{stem} {suffix}", "수")

    # 3. 데 - 의존명사 (문맥 구분)
    de_dep_patterns = [
        (r'할데(가|는|로|서|에|를|이)', '할 데\\1'),
        (r'한데(가|로|서|에|를|이)', '한 데\\1'),
        (r'된데(가|로|서|에|를|이)', '된 데\\1'),
        (r'좋은데(가|로|서|에|를|이)', '좋은 데\\1'),
        (r'많은데(가|로|서|에|를|이)', '많은 데\\1'),
        (r'적은데(가|로|서|에|를|이)', '적은 데\\1'),
        (r'큰데(가|로|서|에|를|이)', '큰 데\\1'),
        (r'작은데(가|로|서|에|를|이)', '작은 데\\1'),
        (r'높은데(가|로|서|에|를|이)', '높은 데\\1'),
        (r'낮은데(가|로|서|에|를|이)', '낮은 데\\1'),
        (r'있는데(가|로|서|에|를|이)', '있는 데\\1'),
        (r'없는데(가|로|서|에|를|이)', '없는 데\\1'),
    ]
    for pat, repl in de_dep_patterns:
        for m in re.finditer(pat, text):
            orig = m.group(0)
            fixed = m.expand(repl)
            if orig not in DE_NOSPLIT:
                add(orig, fixed, "데")

    # 추가 데 의존명사 패턴 (관형사형 + 데)
    de_dep_extra = [
        (r'쓸데(가|는|로|서|에|를|이)', '쓸 데\\1'),
        (r'이를데(가|로|서|에|를|이)', '이를 데\\1'),
        (r'비할데(가|로|서|에|를|이)', '비할 데\\1'),
        (r'갈데(가|로|서|에|를|이)', '갈 데\\1'),
        (r'먹을데(가|로|서|에|를|이)', '먹을 데\\1'),
        (r'볼데(가|로|서|에|를|이)', '볼 데\\1'),
        (r'알데(가|로|서|에|를|이)', '알 데\\1'),
        (r'살데(가|로|서|에|를|이)', '살 데\\1'),
        (r'놀데(가|로|서|에|를|이)', '놀 데\\1'),
        (r'다닐데(가|로|서|에|를|이)', '다닐 데\\1'),
        (r'지낼데(가|로|서|에|를|이)', '지낼 데\\1'),
        (r'기대할데(가|로|서|에|를|이)', '기대할 데\\1'),
        (r'쉴데(가|로|서|에|를|이)', '쉴 데\\1'),
        (r'묵을데(가|로|서|에|를|이)', '묵을 데\\1'),
        (r'배울데(가|로|서|에|를|이)', '배울 데\\1'),
    ]
    for pat, repl in de_dep_extra:
        for m in re.finditer(pat, text):
            orig = m.group(0)
            fixed = m.expand(repl)
            if orig not in DE_NOSPLIT:
                add(orig, fixed, "데")

    # 4. 뿐 - 의존명사
    ppun_pattern = re.compile(r'([가-힣]+)(뿐(?:이다|이고|이며|이니|만|만아니라|만더러|더러))')
    for m in ppun_pattern.finditer(text):
        before = m.group(1)
        ppun_suffix = m.group(2)
        full = m.group(0)
        if before + '뿐' in PPUN_NOSPLIT:
            continue
        add(full, f"{before} {ppun_suffix}", "뿐")

    ppun_only = re.compile(r'([가-힣]+)뿐(?![이다이고이며이니만])')
    for m in ppun_only.finditer(text):
        before = m.group(1)
        full = m.group(0)
        if before + '뿐' in PPUN_NOSPLIT:
            continue
        if full.endswith('뿐만'):
            continue
        add(full, f"{before} 뿐", "뿐")

    # 5. 바 - 의존명사
    ba_dep_stems = ['할', '한', '될', '하는', '있는', '없는', '볼', '들은', '아는', '기대할', '바랄']
    for stem in ba_dep_stems:
        for suffix in ['바', '바를', '바가', '바는', '바이다', '바와']:
            orig = stem + suffix
            base = stem + '바'
            if orig in BA_NOSPLIT or base in BA_NOSPLIT:
                continue
            cnt = text.count(orig)
            if cnt > 0:
                add(orig, f"{stem} {suffix}", "바")

    # 6. 적 - 의존명사 (본 적, 간 적, 한 적, 할 적)
    jeok_dep_stems = ['본', '간', '한', '할', '만난', '읽은', '들은', '쓴', '먹은', '갈', '볼', '알', '살', '다닌', '느낀']
    for stem in jeok_dep_stems:
        for suffix in ['적', '적이', '적도', '적만']:
            orig = stem + suffix
            base = stem + '적'
            if orig in JEOK_DEP_NOSPLIT or base in JEOK_DEP_NOSPLIT:
                continue
            cnt = text.count(orig)
            if cnt > 0:
                add(orig, f"{stem} {suffix}", "적")

    # 7. 상/하 - 방위 의존명사 (문맥 확인 결과 대부분 복합어이므로 제외)
    # 강하→강하게, 산하→청산하다, 집하→고집하다 등 모두 복합어
    # 방위 의존명사로 쓰이는 경우만 극히 제한적으로 처리
    # 현재 사전에서는 방위 의존명사 "상/하" 교정 대상 없음

    # 8. 두발 → 두 발 (단, "진두발" 등 복합어는 제외)
    dubal_pattern = re.compile(r'(?<![가-힣])두발(?![가-힣])')
    for m in dubal_pattern.finditer(text):
        add("두발", "두 발", "두발")

    # 9. 중 - 의존명사 (매우 제한적 적용)
    # 주의: "나중", "체중", "심중", "비중", "하중", "좌중", "취중", "옥중" 등은 복합명사
    # 오직 명확한 의존명사 패턴만 교정
    jung_dep_patterns = [
        '하는중', '있는중', '된중', '가는중', '오는중',
        '만드는중', '진행중', '작업중', '수행중',
        '려행중', '출장중', '회의중', '수업중', '식사중', '운전중',
        '관람중', '관광중', '조사중', '시험중', '훈련중', '전투중',
        '공사중', '건설중', '운행중', '수송중', '이동중',
        '근무중', '사용중', '재학중', '도주중', '수감중', '활주중',
        '부화중', '반응중', '개혁중', '실행중',
    ]
    for pat in jung_dep_patterns:
        if pat in JUNG_NOSPLIT:
            continue
        cnt = text.count(pat)
        if cnt > 0:
            idx = pat.index('중')
            before = pat[:idx]
            after = pat[idx+1:]
            add(pat, f"{before} 중{after}", "중")

    # "진행 중인", "진행 중에" 등 명확한 활동+중+조사 패턴
    # 오직 위 jung_dep_patterns의 기본형+조사만 처리
    jung_base_words = ['진행','작업','수행','려행','출장','회의','수업','식사','운전',
                       '관람','관광','조사','시험','훈련','전투','공사','건설','운행',
                       '수송','이동','근무','사용','재학','도주','수감','활주','부화',
                       '반응','개혁','실행','하는','있는','된','가는','오는','만드는']
    for base in jung_base_words:
        for josa in ['중인', '중에', '중에서', '중의', '중이', '중을', '중은', '중도', '중만']:
            orig = base + josa
            if orig in JUNG_NOSPLIT:
                continue
            cnt = text.count(orig)
            if cnt > 0:
                add(orig, f"{base} {josa[:0]}중{josa[1:]}", "중")

    # "급한중에" 등 서술어+중 패턴 (매우 제한적)
    jung_adj_pattern = re.compile(r'(급한|다급한|황급한)(중(?:에|에서|의))')
    for m in jung_adj_pattern.finditer(text):
        before = m.group(1)
        jung_suffix = m.group(2)
        full = m.group(0)
        if full in JUNG_NOSPLIT:
            continue
        add(full, f"{before} {jung_suffix}", "중")

    # 10. 앞 - 의존명사
    ap_dep_stems = ['하는', '한', '있는', '선', '나선', '앞장선']
    for stem in ap_dep_stems:
        for suffix in ['앞', '앞에', '앞으로', '앞에서', '앞의', '앞에도']:
            orig = stem + suffix
            if orig in AP_NOSPLIT:
                continue
            cnt = text.count(orig)
            if cnt > 0:
                add(orig, f"{stem} {suffix}", "앞")

    # 11. 뜻 - 의존명사
    ddut_dep_stems = ['하는', '한', '있는', '같은', '그', '이', '다른', '어떤', '깊은', '큰', '참', '본']
    for stem in ddut_dep_stems:
        for suffix in ['뜻', '뜻으로', '뜻이', '뜻을', '뜻은', '뜻이다']:
            orig = stem + suffix
            base = stem + '뜻'
            if orig in DDUT_NOSPLIT or base in DDUT_NOSPLIT:
                continue
            cnt = text.count(orig)
            if cnt > 0:
                add(orig, f"{stem} {suffix}", "뜻")

    # 12. 이상/이하 - 의존명사 (숫자+이상/이하)
    isang_pattern = re.compile(r'([0-9]+)(이상|이하)')
    for m in isang_pattern.finditer(text):
        num = m.group(1)
        dep = m.group(2)
        orig = m.group(0)
        if orig not in ISANG_NOSPLIT and orig not in IHA_NOSPLIT:
            add(orig, f"{num} {dep}", "이상/이하")

    # 13. 고하다 - 모두 단일어 (견고하다, 경고하다 등) → 교정 불필요
    # 문맥 확인 결과 "고하다" 패턴은 모두 단일어로 확인됨

    # 14. 모두 - 부사 (띄어쓰기 해당사항 없음)

    return changes


def process_file(label, src_path, log_fh):
    def log(msg):
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] {msg}"
        print(line, flush=True)
        if log_fh:
            try:
                log_fh.write(line + "\n")
                log_fh.flush()
            except Exception:
                pass

    log(f"\n{'=' * 70}")
    log(f"  [{label}파일] 의존명사/문맥 띄어쓰기 교정")
    log(f"{'=' * 70}")

    if not os.path.exists(src_path):
        log(f"  파일 없음: {src_path}")
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(OUT_DIR, f"{label}_context_corrected_{timestamp}.hwp")
    backup_path = os.path.join(BACKUP_DIR, f"{label}_backup_{timestamp}.hwp")
    shutil.copy2(src_path, backup_path)
    log(f"  백업: {backup_path}")

    text = extract_text(src_path)
    log(f"  텍스트: {len(text):,}자")

    rules = generate_context_rules(text)
    log(f"  교정 규칙: {len(rules)}개")

    cats = {}
    for src, dst, cat, cnt in rules:
        if cat not in cats:
            cats[cat] = 0
        cats[cat] += cnt
    for cat_name, total in sorted(cats.items(), key=lambda x: -x[1]):
        log(f"    {cat_name}: {total}건")

    if not rules:
        log(f"  수정 불필요")
        return None

    rules.sort(key=lambda r: len(r[0]), reverse=True)

    ole = olefile.OleFileIO(src_path, write_mode=False)
    all_stream_data = {}
    stream_list = ole.listdir()
    for sp in stream_list:
        sn = '/'.join(sp)
        all_stream_data[sn] = ole.openstream(sn).read()
    ole.close()

    total_changes = 0
    modified_streams = []
    change_log = []

    for sp in stream_list:
        sn = '/'.join(sp)
        if sp[0] != "BodyText":
            continue

        raw = all_stream_data[sn]
        try:
            dec = zlib.decompress(raw, -15)
        except zlib.error:
            continue

        records = parse_records(dec)
        stream_changes = 0
        modified_rec_count = 0

        for i, rec in enumerate(records):
            if rec["tag_id"] != 67:
                continue
            try:
                rec_text = rec["payload"].decode('utf-16-le', errors='replace')
            except Exception:
                continue

            new_text = rec_text
            rec_changes = 0

            for src_word, dst_word, cat, cnt in rules:
                actual_cnt = new_text.count(src_word)
                if actual_cnt > 0:
                    new_text = new_text.replace(src_word, dst_word)
                    rec_changes += actual_cnt
                    stream_changes += actual_cnt
                    total_changes += actual_cnt
                    change_log.append((src_word, dst_word, cat, actual_cnt))

            if rec_changes > 0:
                new_payload = new_text.encode('utf-16-le')
                records[i] = {
                    "tag_id": rec["tag_id"],
                    "level": rec["level"],
                    "size": len(new_payload),
                    "header_size": rec["header_size"],
                    "payload": new_payload,
                }
                modified_rec_count += 1

        if stream_changes > 0:
            new_dec = rebuild_stream(records)

            co = zlib.compressobj(level=6, method=zlib.DEFLATED, wbits=-15)
            new_compressed = co.compress(new_dec) + co.flush()
            original_size = len(raw)

            if len(new_compressed) <= original_size:
                all_stream_data[sn] = (new_compressed, original_size)
            else:
                co2 = zlib.compressobj(level=1, method=zlib.DEFLATED, wbits=-15)
                new_compressed2 = co2.compress(new_dec) + co2.flush()
                if len(new_compressed2) <= original_size:
                    all_stream_data[sn] = (new_compressed2, original_size)
                else:
                    log(f"  [오류] {sn}: 압축 크기 초과")
                    continue

            verify_dec = zlib.decompress(new_compressed if len(new_compressed) <= original_size else new_compressed2, -15)
            verify_records = parse_records(verify_dec)
            log(f"  {sn}: {modified_rec_count}개 레코드 수정, {stream_changes}건 교정, 검증 ✅")
            modified_streams.append(sn)

    if not modified_streams:
        log(f"  변경된 스트림 없음")
        return None

    log(f"\n  총 교정: {total_changes}건")

    import uuid
    out_tmp = out_path.replace('.hwp', f'_{uuid.uuid4().hex[:8]}.bin')
    shutil.copy2(src_path, out_tmp)
    os.chmod(out_tmp, stat.S_IWRITE | stat.S_IREAD)

    ole_info = olefile.OleFileIO(src_path, write_mode=False)
    sector_size = ole_info.sector_size

    for sn in modified_streams:
        compressed_data, original_stream_size = all_stream_data[sn]
        sp = sn.split('/')
        sid = ole_info._find(sp)
        entry = ole_info.direntries[sid]
        stream_size = entry.size
        start_sector = entry.isectStart

        fat = ole_info.fat
        chain = []
        current = start_sector
        while current >= 0 and current < len(fat):
            chain.append(current)
            current = fat[current]
            if len(chain) > 100000:
                break

        with open(out_tmp, 'r+b') as f:
            data_offset = 0
            for sect_idx, sect in enumerate(chain):
                offset = sector_size + sect * sector_size
                if data_offset >= len(compressed_data):
                    break
                chunk_end = min(data_offset + sector_size, len(compressed_data))
                chunk = compressed_data[data_offset:chunk_end]
                if len(chunk) < sector_size:
                    f.seek(offset)
                    existing = f.read(sector_size)
                    chunk = chunk + existing[len(chunk):]
                f.seek(offset)
                f.write(chunk)
                data_offset += sector_size

        if len(compressed_data) != stream_size:
            with open(out_tmp, 'r+b') as f:
                header = f.read(512)
                dir_start_sect = struct.unpack_from('<I', header, 48)[0]

                dir_chain = []
                cur_d = dir_start_sect
                while cur_d >= 0 and cur_d < len(fat):
                    dir_chain.append(cur_d)
                    cur_d = fat[cur_d]
                    if len(dir_chain) > 100:
                        break

                entries_per_sect = sector_size // 128
                sect_idx = sid // entries_per_sect
                entry_idx = sid % entries_per_sect

                if sect_idx < len(dir_chain):
                    dir_sect = dir_chain[sect_idx]
                    dir_entry_offset = sector_size + dir_sect * sector_size + entry_idx * 128

                    f.seek(dir_entry_offset + 120)
                    f.write(struct.pack('<I', len(compressed_data)))
                    f.seek(dir_entry_offset + 124)
                    f.write(struct.pack('<I', 0))

    ole_info.close()

    if os.path.exists(out_path):
        os.chmod(out_path, stat.S_IWRITE | stat.S_IREAD)
        os.remove(out_path)
    os.rename(out_tmp, out_path)
    log(f"  출력: {out_path}")

    text2 = extract_text(out_path)
    log(f"\n  교정 전: {len(text):,}자 → 교정 후: {len(text2):,}자")

    remaining = 0
    for src_word, dst_word, cat, cnt in rules:
        cnt2 = text2.count(src_word)
        if cnt2 > 0:
            remaining += cnt2
    if remaining == 0:
        log(f"  ✅ 모든 교정 완료!")
    else:
        log(f"  ⚠️ {remaining}건 잔여")

    cat_groups = {}
    for src_word, dst_word, cat, cnt in change_log:
        if cat not in cat_groups:
            cat_groups[cat] = []
        cat_groups[cat].append((src_word, dst_word, cnt))

    log(f"\n  [교정 상세]")
    for cat in sorted(cat_groups.keys()):
        items = cat_groups[cat]
        total_cat = sum(c for _, _, c in items)
        log(f"  [{cat}] {len(items)}개 항목, {total_cat}건")
        for src_word, dst_word, cnt in sorted(items, key=lambda x: -x[2])[:10]:
            log(f"    '{src_word}' → '{dst_word}' ({cnt}건)")

    return out_path


def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(LOG_DIR, f"context_correction_{timestamp}.txt")
    log_fh = open(log_path, "w", encoding="utf-8")

    log_fh.write(f"의존명사/문맥 띄어쓰기 교정\n")
    log_fh.write(f"시작: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    log_fh.write(f"대상: 것,수,데,뿐,바,적,상/하,두발,중,앞,뜻,이상/이하,고하다,모두\n\n")

    results = {}
    for label, fpath in FILES.items():
        if os.path.exists(fpath):
            result = process_file(label, fpath, log_fh)
            results[label] = result
        else:
            print(f"[{label}] 파일 없음: {fpath}")

    log_fh.write(f"\n완료: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    log_fh.close()
    print(f"\n로그: {log_path}")

    return results


if __name__ == "__main__":
    main()
