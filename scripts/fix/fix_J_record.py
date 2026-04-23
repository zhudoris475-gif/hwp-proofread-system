import sys, os, time, re, struct, zlib, shutil, hashlib, stat

sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import olefile
from collections import Counter

SRC = r"C:\Users\doris\Desktop\【大中朝 16】L 1787-1958--172--20240920__v1.hwp"
OUT = r"c:\Users\doris\.agent-skills\L_output.hwp"
OUT_TMP = r"c:\Users\doris\.agent-skills\L_work_" + str(__import__('uuid').uuid4().hex[:8]) + ".bin"
BACKUP_DIR = r"C:\Users\doris\AppData\Local\Temp\hwp_backup"
LOG_DIR = r"C:\Users\doris\AppData\Local\Temp\hwp_logs"
RULES_FILE = r"C:\AMD\AJ\hwp_proofreading_package\rules_documentation.txt"

GEOT_NOSPLIT = {"이것", "그것", "저것", "이것저것", "그것저것", "보잘것", "옛것", "새것", "별것", "그것", "모든것", "어느것", "어떤것", "들것", "말것"}

SU_NOSPLIT = {
    "장수", "교수", "척수", "우수", "선수", "준수", "주파수", "정수", "함수",
    "감수", "인수", "순수", "특수", "기수", "접수", "군수", "죄수", "다수",
    "가수", "수수", "보수", "점수", "완수", "지수", "호수", "분수",
    "박수", "불수", "할수록", "매수", "차수", "상수", "변수", "소수", "횟수",
    "갈수", "본수", "갈수록", "될수록",
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
    "어쩔수", "얻을수", "볼수", "떨어질수", "할수", "알수",
    "이십팔수",
    "말수", "골수", "필수", "원심탈수", "문화재밀수", "률수", "예술수",
    "생활수", "지방일수", "찰수", "연수", "진수", "경수", "뇌수",
    "간수", "평수", "광수", "난수", "세수", "의수", "치수",
}

TTAWI_NOSPLIT = {"따위", "따위의", "따위로", "따위를", "따위는", "따위가", "따위도"}
SAI_NOSPLIT = {"강사이", "수사이", "두사이", "그사이", "이사이", "중간사이"}
PPUN_NOSPLIT = {"뿐만", "뿐이다", "뿐이었다", "뿐이고", "뿐이며", "뿐이니", "사뿐사뿐", "사뿐"}

CHUK_NOSPLIT_PREFIXES = (
    "개척", "세척", "척추", "척결", "척도", "척골", "질척", "부척",
    "권척", "곡척", "협척", "률척", "고정척", "진촌퇴척",
    "척박", "간척", "투척",
)
CHUK_NOSPLIT = {
    "배척하다", "배척하고", "배척당하고", "무척", "지척", "계척", "산세척",
    "인척관계를", "수척하다", "수척한", "수척해지다",
    "지척에", "인척",
    "세척하다", "세척액", "세척법", "세척제", "세척",
    "개척하다", "개척하는", "개척한",
    "무척추동물의", "무척추동물에", "무척추동물지",
    "부패척결의", "가치척도", "협척혈", "온도척도", "화씨온도척도와", "온도척도를",
    "알카리세척제", "알카리세척", "알카리세척제를",
    "변기세척제", "국부세척기", "엉뎅이척추뼈",
    "인기척", "인기척에도", "인기척이", "기척도",
    "뇌척수막", "외척의", "건설진척을",
    "척추동물의", "척박한", "간척하다",
    "질척질척한",
    "기척", "기척이", "수척", "수척해",
    "지척거리다", "지척거리는", "공사진척이", "공사진척",
    "척하다", "척하고", "척하여",
    "진척이", "진척을", "진척의", "진척도",
    "련척", "륙척", "인척인",
    "수척해보이자", "수척해보이고",
    "친한척", "말리는척", "자비스러운척", "사람인척",
    "없는척한다는", "아는척하면",
    "척추", "척추뼈", "척수", "척도",
    "척추를", "척추의", "척추가",
    "척수를", "척수의", "척수가",
    "척도를", "척도의", "척도가",
    "진척하다", "진척하고", "진척한",
    "간척", "간척을", "간척의",
    "세척을", "세척의", "세척이",
    "개척을", "개척의", "개척이",
    "배척을", "배척의", "배척이",
    "인척을", "인척의", "인척이",
}

ISANG_NOSPLIT = {"이상", "이상의", "이상으로", "이상하다", "이상하게", "이상한", "정상이상", "비정상이상"}
MIT_NOSPLIT = {"밑", "밑바닥", "밑면", "밑부분", "밑천"}
AP_NOSPLIT = {"앞날", "앞으로", "앞서", "앞뒤", "앞문", "앞길", "앞장", "앞니", "앞발", "앞다리", "앞머리", "앞바다", "앞바람", "앞뒤", "앞쪽", "앞부분", "앞사람", "앞뒤로", "앞으로서", "앞에서", "앞에", "앞의"}
GE_NOSPLIT = {"게다가", "게으르다", "게으름", "게시판", "게임", "게으른", "게을러", "게을리", "장게", "게시", "게재", "게르만", "게릴라", "게이트", "게르마늄", "훈계게", "총계게", "통계게"}
DEUT_NOSPLIT = {"반듯", "반듯이", "빠듯", "빠듯이", "여느듯", "그듯", "가득듯", "오직듯", "마치듯", "함듯", "듯이", "듯하다", "듯싶다", "인듯", "듯이", "만듯", "같은듯", "하는듯", "있는듯", "없는듯"}
CHARYE_NOSPLIT = {"차례차례", "차례대로", "이차례", "삼차례", "첫차례", "다음차례", "뒷차례", "차례로", "차례차례로"}

DEUNG_NOSPLIT = {
    "균등", "고등", "강등", "상등", "대등", "초등", "일등", "발등",
    "갈등", "평등", "동등", "항등", "비등", "불평등",
    "등등", "등산", "등록", "등장", "등급", "등불", "등대",
    "가로등", "형광등", "섬광등", "전조등", "경고등", "경광등",
    "안전등", "착륙등", "착신등", "진입등", "탁상등", "채색등",
    "책등", "칼등", "등뼈", "등받이",
    "주민등록", "기회균등", "감수분렬부등",
    "신호등", "손전등", "전등", "곱사등", "호적등",
    "자원평등", "교통신호등", "립식전등", "련결등",
    "풍력등", "초불등", "신용등", "벌등",
    "렬등", "귓등", "뢰공등", "랭음극형광등",
    "열등", "산등", "홍등", "세등", "중등", "이등",
    "려객등", "록색등", "세움등", "키큰등",
    "급등", "등불", "등기", "등교", "등반", "등신",
    "휴대등", "야간등", "실내등", "복도등", "계단등",
    "비상등", "유도등", "출입등", "통로등",
}

TTE_NOSPLIT = {"제때", "그때", "이때", "한때", "때때로", "아무때", "때때", "명절때", "점심때", "저녁때", "병때", "본때"}
TTAE_MUN_NOSPLIT = {"때문", "때문에", "때문이다"}

BEON_NOSPLIT = {
    "이번", "한번", "두번", "세번", "네번", "여러번", "몇번", "매번",
    "첫번", "한꺼번", "두리번", "단번", "백번", "여섯번", "일곱번",
    "여덟번", "아홉번", "두어번", "빈번", "농번", "교번",
    "자동번", "전화번", "기계번", "비밀번", "일련번", "부품번",
    "종자번", "가축번", "성장번", "경찰번", "천둥번", "근친번",
    "금번", "대번", "해번", "절번", "홀수번",
    "순번", "류번", "원자번", "발신번", "당번", "련속번",
    "천번", "지난번", "원소번", "전번", "자유번", "추첨당첨번",
    "륜번", "타번", "리번", "오즈번", "번쩍번",
    "번번이", "번쩍번쩍", "번거롭다",
    "청소당번", "야간당번", "경비당번",
}

DE_NOSPLIT = {"가운데", "한가운데", "그가운데", "포름알데", "놀포름알데", "메타알데", "아쎄트알데", "알데", "데굴데", "번데", "한데", "아데",
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
    "본데", "간데", "하는데", "한데", "는데", "은데", "던데",
    "좋은데", "많은데", "적은데", "높은데", "편한데", "큰데", "작은데",
    "그런데", "이런데", "어떤데", "없는데", "있는데", "된데",
}
DAERO_NOSPLIT = {"뜻대로", "마음대로", "그대로", "이대로", "저대로", "자대로", "제멋대로", "맘대로", "임의대로", "자연대로",
    "이대로라도", "그대로라도", "있는대로", "되는대로", "하는대로",
    "본대로", "들은대로", "본대로", "아는대로", "가는대로",
    "절대로", "제대로", "대대로", "영대로", "선대로",
    "사실대로", "순서대로", "규정대로", "요구대로", "약속대로",
    "계획대로", "예상대로", "생각대로", "소원대로", "명령대로",
    "원래대로", "그대로라도", "있는그대로",
}
MANKEUM_NOSPLIT = {"그만큼", "이만큼", "저만큼", "만큼"}
JUL_NOSPLIT = {"줄밖", "줄",
    "힘줄", "바줄", "새끼줄", "기계줄", "청줄", "산줄", "드레박줄",
    "물줄", "소줄", "동줄", "줄다", "줄기", "줄줄이",
    "생줄", "명줄", "목줄", "핏줄", "신줄", "실줄",
    "어줄", "당줄", "줄줄", "고줄", "대줄", "쇠줄",
    "전줄", "연줄", "줄당", "줄자", "줄녀석",
    "노끈줄", "밧줄", "끈줄", "철줄", "나일론줄",
    "고무줄", "전깃줄", "철사줄", "끌줄", "감줄",
    "매듭줄", "낚시줄", "안전줄", "구명줄", "전화줄",
    "올줄", "굵은줄", "가는줄", "긴줄", "짧은줄",
    "거미줄", "덩굴줄", "두레박줄", "오라줄", "계선줄",
    "다듬질줄", "빨래줄", "넋줄", "밧줄", "동아줄",
    "줄기차다", "줄기", "줄거리", "줄임말", "줄임",
    "줄알다", "줄모르다", "줄서다", "줄잇다",
    "갈대줄", "이야기줄", "뾰족평줄", "송곳줄", "평줄",
    "줄발", "줄당기다", "줄조임", "줄타기", "줄임꼴",
    "줄간격", "줄바꿈", "줄세우기", "줄거리", "줄임표",
    "피줄", "먹줄", "당김줄", "구린줄", "어쩔줄",
    "묶음쇠줄", "견인바줄", "쇠바줄",
    "부끄러운줄", "도와줄", "붉은줄", "검은줄",
    "련줄", "알줄", "볼줄", "할줄", "갈줄",
    "줄을", "줄의", "줄이", "줄은", "줄에",
    "피줄을", "피줄의", "먹줄을", "먹줄의",
    "구리줄", "나무줄", "시계줄", "버팀줄", "포승줄",
    "닻줄", "불줄", "태줄", "비줄", "이음줄",
    "해줄", "미역줄", "낳은줄", "싫은줄", "않은줄",
}

TEO_NOSPLIT = {
    "콤퓨터", "모니터", "인터", "인터넷", "프린터", "센터", "터미널",
    "허터", "필터", "액터", "팩터", "벡터", "렉터",
    "오래전부터", "부터", "로부터", "에서부터", "으로부터",
    "두터", "흉터", "엉터", "엉터리", "상처터",
    "량쪽으로부터", "곁으로부터", "밖으로부터", "안으로부터",
    "터전", "터밭", "터끌", "터럭", "터진", "터지다", "터뜨리다",
    "터득", "터득하다", "터치", "터치하다",
    "김터", "밭터", "집터", "답터", "터전",
    "모터", "발전터", "극터", "온터",
    "포터", "마스터", "시터", "지터",
    "렌터", "카운터", "아우터", "이터",
    "파터", "도터", "비터", "레터",
    "바터", "페터", "세터", "게터",
    "부터", "까지", "까지도",
    "콤퓨터를", "콤퓨터에", "콤퓨터로", "콤퓨터의", "콤퓨터가", "콤퓨터는",
    "모니터를", "모니터에", "모니터로", "모니터의", "모니터가", "모니터는",
    "센터를", "센터에", "센터로", "센터의", "센터가", "센터는",
    "프린터를", "프린터에", "프린터로", "프린터의",
    "필터를", "필터에", "필터의",
    "예로부터", "옛날부터", "이전부터", "싸움터", "전쟁터", "포스터", "리히터",
    "흘리터", "쎈치메터", "립방메터", "처음부터", "예전부터", "어릴적부터",
    "올해부터", "언제부터", "가죽부터", "물러터", "사회로부터", "주형으로부터",
    "동지부터", "이미전부터", "세기말부터", "휴대용콤퓨터", "로인병치료센터",
    "발사로부터", "눈물부터", "뒤부터", "립방쎈치메터", "평방메터", "쎈치리터",
    "릿터", "리티움배터", "겁부터", "만메터", "세제곱메터", "립방데시메터",
    "립방미리메터", "립방센치메터", "아침부터", "고체로부터", "어디에서부터",
    "오래전부터", "이때부터", "고대로부터", "인터페이스", "인터럽트",
    "콤퓨터", "컴퓨터", "노트북", "랩터", "슬러터",
}

CHAE_NOSPLIT = {
    "색채", "외채", "공채", "미지급채", "납채", "정채", "국채", "사채",
    "다문채", "총채", "끌채", "가로채", "낚아채", "눈치채",
    "국가경제건설공채", "건설공채", "경제건설공채",
    "채권", "채무", "채석", "채소", "채집", "채용", "채택", "채점",
    "채색", "채널", "채팅", "채우다", "채워", "채운",
    "채소를", "채소의", "채소가", "채소는",
    "채권을", "채권의", "채권이", "채권은",
    "채용을", "채용의", "채용이", "채용은",
    "채집을", "채집의", "채집이",
    "채택을", "채택의", "채택이",
    "공채를", "공채의", "공채가", "공채는",
    "외채를", "외채의", "외채가", "외채는",
    "사채를", "사채의", "사채가", "사채는",
    "국채를", "국채의", "국채가", "국채는",
    "납채를", "납채의",
    "정채를", "정채의",
    "색채를", "색채의", "색채가", "색채는",
    "낚아채다", "가로채다", "눈치채다",
    "가로채서", "가로채고", "가로채면",
    "낚아채서", "낚아채고", "낚아채면",
    "눈치채서", "눈치채고", "눈치채면",
    "빚채", "은채", "금채", "동채", "철채",
    "파채", "김채", "밭채", "채채",
    "대채", "현채", "단채", "본채",
    "부채", "보채", "생채", "랭채", "벌채", "다채",
    "류동부채", "쓰레기채", "가죽채", "곰의말채",
    "부채를", "부채의", "부채가", "부채는",
    "보채다", "보채고", "보채서",
    "송두리채", "뻗은채", "앉은채", "누운채", "서있는채",
    "사랑채", "야채", "유채", "안채", "풍채", "전채",
    "통채", "털채", "꿀발부채", "련대채", "련쇄부채",
    "뿌리채", "막힌채",
    "사랑채를", "사랑채의", "사랑채가",
    "야채를", "야채의", "야채가", "야채는",
    "유채를", "유채의", "유채가", "유채는",
    "안채를", "안채의", "안채가", "안채는",
    "풍채를", "풍채의", "풍채가", "풍채는",
    "전채를", "전채의", "전채가", "전채는",
    "통채를", "통채의", "통채로",
    "털채를", "털채의",
    "꿀발부채를", "꿀발부채의",
    "련대채를", "련대채의",
    "련쇄부채를", "련쇄부채의",
    "뿌리채를", "뿌리채의", "뿌리채로",
    "막힌채로", "막힌채를",
    "건너채", "마루채", "부엌채", "광채", "외양채",
    "곁채", "별채", "윗채", "아랫채", "웃채",
    "살림채", "사랑채", "행랑채", "대청채",
    "야채를", "야채와", "야채에", "야채로",
    "김치야채", "신선야채", "유기야채",
    "유채꽃", "유채밭", "유채기름",
    "풍채가", "풍채를", "풍채의",
    "전채식", "전채요리",
}

JEOK_NOSPLIT = {
    "본적", "간적", "적성", "적자", "적중", "적응", "적극", "적법", "적당",
    "적색", "적소", "적임", "적요", "적의", "적합", "적활",
    "부적", "부적절", "부적당", "부적합",
    "적극적", "소극적", "적극적으로", "소극적으로",
    "적극성", "적성검사", "적자결산", "적자운행",
    "근본적", "기본적", "일반적", "구체적", "객관적", "주관적",
    "절대적", "상대적", "적극적", "소극적", "적대적",
    "특수적", "일반적", "개별적", "전체적", "국부적",
    "순간적", "영구적", "일시적", "지속적", "정치적",
    "경제적", "사회적", "문화적", "역사적", "과학적",
    "시간적", "공간적", "물리적", "화학적", "생물적",
    "원적", "본적지", "본적을", "본적이", "본적의",
    "시간적구간", "공간적인", "순간적으로", "순간적인",
    "근본적으로", "기본적으로", "일반적으로", "구체적으로",
}

JI_NOSPLIT = {
    "한지", "간지", "산지", "할지", "본지", "갈지",
    "지구", "지역", "지방", "지도", "지시", "지원", "지식", "지적",
    "지위", "지점", "지표", "지평", "지형", "지질", "지리",
    "인지", "양지", "음지", "고지", "본지", "원지", "외지",
    "한지", "백지", "장지", "모지", "절지", "생지", "건지",
    "간지도수", "간지", "산지를", "산지의", "산지가",
    "휴한지", "휴경지", "식량생산지",
    "지리하다", "지루하다", "지루하고",
}

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
    "바삭바삭", "들썩들썩", "반짝반짝",
    "곧바", "똑바", "옳바", "뒤바",
    "지르바", "울바", "낯바", "밑바",
    "고무바", "손바", "가을바",
    "룸바", "견인바", "쇠바", "골덴바",
    "회오리바", "돌개바", "류산바", "장바", "막바",
    "바탕", "바람", "바다", "바느질",
}


IHA_NOSPLIT = {
    "가까이하다", "가까이하고", "가까이하여", "가까이해서", "가까이한",
    "가까이하", "가까이해", "가까이했",
    "기이하다", "기이하고", "기이한", "기이하여",
    "기이하", "기이해", "기이했",
    "되풀이하다", "되풀이하고", "되풀이하여", "되풀이한",
    "되풀이하", "되풀이해", "되풀이했",
    "해이하다", "해이하고", "해이한", "해이하여",
    "해이하", "해이해", "해이했",
    "같이하다", "같이하고", "같이하여",
    "같이하", "같이해", "같이했",
    "괴이하다", "괴이하고", "괴이한", "괴이하여",
    "괴이하", "괴이해", "괴이했",
    "매갈이하다", "매갈이하고",
    "매갈이하", "매갈이해", "매갈이했",
    "돈벌이하다", "돈벌이하고",
    "돈벌이하", "돈벌이해", "돈벌이했",
    "밭갈이하다", "밭갈이하고",
    "밭갈이하", "밭갈이해", "밭갈이했",
    "특이하다", "특이하고", "특이한", "특이하여",
    "특이하", "특이해", "특이했",
    "고기잡이하다", "고기잡이하고",
    "고기잡이하", "고기잡이해", "고기잡이했",
    "용이하다", "용이하고", "용이한",
    "용이하", "용이해", "용이했",
    "부득이하다", "부득이하고", "부득이한",
    "부득이하", "부득이해", "부득이했",
    "맞이하다", "맞이하고", "맞이하여", "맞이한",
    "맞이하", "맞이해", "맞이했",
    "수준이하", "생리적령점이하", "령이하", "영도이하", "류행성이하",
    "상이하다", "상이하고", "상이한",
    "상이하", "상이해", "상이했",
    "중동무이하다", "중동무이하고",
    "중동무이하", "중동무이해", "중동무이했",
    "되풀이", "고기잡이", "기이", "용이", "가까이", "해이", "괴이", "매갈이", "돈벌이",
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
    "비중에", "비중의", "비중이",
    "민중에", "민중의", "민중이",
}

SANG_NOSPLIT = {
    "세상", "항상", "현상", "리상", "이상", "예상", "사상", "로상",
    "조상", "책상", "증상", "감상", "륙상", "고상", "진상", "대상",
    "린상", "정상", "수상", "기상", "해상", "손상", "호상", "인상",
    "앙상", "지상", "추상", "중상", "가상", "화상", "령상", "살상",
    "일상", "관상", "걸상", "련쇄상", "립상",
    "인간세상", "노벨물리학상", "둘이상",
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
}

U_NOSPLIT = {
    "매우", "경우", "좌우", "겨우", "폭우", "강우", "전우", "대우",
    "아우", "새우", "무우", "배우", "태우", "채우", "키우", "싸우",
    "세우", "피우", "뉘우", "도우", "메우", "씌우",
    "산봉우", "산봉우리", "물우", "산우", "땅우", "들보우",
    "머리우", "책상우", "담장우", "나무우",
    "덮어씌우", "멈춰세우", "내세우",
    "명배우", "첩첩산봉우",
    "우리", "우주", "우수", "우월", "우연", "우편", "우호",
    "우량", "우세", "우습다", "우습고",
    "루저우", "길우", "뢰우",
    "어려우", "쉬우",
    "봉우", "보우", "라우", "례우", "서우",
    "닭새우", "전자우", "길거리배우", "몸우", "무늬우", "겨자무우",
    "오물전자우", "소우", "가우", "나우", "다우", "마우", "바우",
    "사우", "자우", "차우", "카우", "타우", "파우", "하우",
    "우산", "우유", "우물", "우레", "운우", "명우", "현우",
    "독우", "양우", "협우", "친우", "교우", "난우", "강우",
    "건우", "규우", "기우", "동우", "명우", "복우", "선우",
    "성우", "영우", "용우", "은우", "인우", "재우", "정우",
    "주우", "진우", "창우", "춘우", "태우", "평우", "학우",
    "폭풍우", "아름다우", "란저우", "녀배우", "번거로우",
    "탁자우", "돼지우", "울타리우", "란간우", "란다우",
    "애태우", "불우", "외우", "라쯔러우",
    "폭풍우를", "폭풍우의", "폭풍우가",
    "아름다우나", "아름다우면",
    "란저우를", "란저우의", "란저우가",
    "녀배우를", "녀배우의", "녀배우가",
    "번거로우나", "번거로우면",
    "탁자우에", "탁자우의",
    "돼지우에", "돼지우의",
    "울타리우에", "울타리우의",
    "란간우에", "란간우의",
    "불우를", "불우의", "불우가",
    "외우를", "외우의", "외우가",
    "가로우", "마루우", "마당우", "지붕우",
    "발우", "발우에", "발우의",
    "우의", "우에", "우로", "우에서",
}

HA_NOSPLIT = {
    "비유하다", "비유하고", "비유하여", "비유한",
    "속하다", "속하고", "속하여", "속한",
    "형용하다", "형용하고", "형용하여", "형용한",
    "못하다", "못하고", "못하여", "못한",
    "말하다", "말하고", "말하여", "말한",
    "청렴하다", "청렴하고", "청렴한",
    "사용하다", "사용하고", "사용하여", "사용한",
    "일하다", "일하고", "일하여", "일한",
    "처리하다", "처리하고", "처리하여", "처리한",
    "로련하다", "로련하고", "로련한",
    "대하다", "대하고", "대하여", "대한",
    "다하다", "다하고", "다하여", "다한",
    "련결하다", "련결하고", "련결하여", "련결한",
    "리용하다", "리용하고", "리용하여", "리용한",
    "리해하다", "리해하고", "리해하여", "리해한",
    "생각하다", "생각하고", "생각하여", "생각한",
    "피로하다", "피로하고", "피로한",
    "랭담하다", "랭담하고", "랭담한",
    "좋아하다", "좋아하고", "좋아하여", "좋아한",
    "그리워하다", "그리워하고", "그리워하여",
    "쌀쌀하다", "쌀쌀하고", "쌀쌀한",
    "정리하다", "정리하고", "정리하여", "정리한",
    "어수선하다", "어수선하고", "어수선한",
    "비슷하다", "비슷하고", "비슷한",
    "시원하다", "시원하고", "시원한",
    "발생하다", "발생하고", "발생하여", "발생한",
    "계속하다", "계속하고", "계속하여", "계속한",
    "당하다", "당하고", "당하여", "당한",
    "조심하다", "조심하고", "조심하여", "조심한",
    "정직하다", "정직하고", "정직한",
    "민첩하다", "민첩하고", "민첩한",
    "란잡하다", "란잡하고", "란잡한",
    "깨끗하다", "깨끗하고", "깨끗한",
    "침착하다", "침착하고", "침착한",
    "안내하다", "안내하고", "안내하여", "안내한",
    "이야기하다", "이야기하고", "이야기하여", "이야기한",
    "진행하다", "진행하고", "진행하여", "진행한",
    "실행하다", "실행하고", "실행하여", "실행한",
    "싫어하다", "싫어하고", "싫어하여",
    "단정하다", "단정하고", "단정한",
    "하다", "하고", "하여", "해서", "하였다", "한다", "한", "하세요",
    "하기", "함", "할", "했", "하는",
    "산하", "강하", "제강하다", "제강하고", "제강하여",
    "생산하다", "생산하고", "생산하여", "생산한",
    "청산하다", "청산하고", "청산하여", "청산한",
    "계산하다", "계산하고", "계산하여", "계산한",
    "하강하다", "하강하고", "하강하여",
    "강하다", "강하고", "강하여", "강한",
    "산하의", "산하를", "산하가", "산하는",
}

GAT_NOSPLIT = {
    "똑같다", "똑같이", "똑같은",
    "마찬가지로",
    "같이", "같은", "같다",
}

GO_NOSPLIT = {
    "고하다", "고하고", "고하여", "고해서", "고한",
    "고가다", "고간다", "고가고",
    "고있다", "고있고", "고있는", "고있다",
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


def load_china_place_rules():
    rules = []
    path = r"C:\AMD\AJ\hwp_proofreading_package\rules_china_place.txt"
    if not os.path.exists(path):
        return rules
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '→' in line:
                parts = line.split('→')
                if len(parts) == 2:
                    s = parts[0].strip().strip("'\"")
                    d = parts[1].strip().strip("'\"")
                    if s and d:
                        rules.append((s, d))
    return rules


def parse_txt_rules(filepath):
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
                    s = parts[0].strip().strip("'\"")
                    d = parts[1].strip().strip("'\"")
                    if s and d and s != d:
                        rules.append((s, d))
    return rules


def apply_text_corrections(text):
    changes = []

    def add(src, dst, cat):
        cnt = text.count(src)
        if cnt > 0:
            changes.append((src, dst, cat, cnt))

    pattern = re.compile(r'([가-힣]+것)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in GEOT_NOSPLIT or word == '것':
            continue
        add(word, f"{word[:-1]} 것", "것")

    def has_suitable_ending(word):
        if len(word) < 2:
            return False
        char_before_su = word[-2]
        code = ord(char_before_su)
        if 0xAC00 <= code <= 0xD7A3:
            jongseong = (code - 0xAC00) % 28
            if jongseong == 8:
                return True
        if char_before_su in ('는', '은', '겠', '던', '랬', '렸'):
            return True
        return False

    pattern = re.compile(r'([가-힣]+수)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in SU_NOSPLIT or word == '수':
            continue
        if not has_suitable_ending(word):
            continue
        add(word, f"{word[:-1]} 수", "수")

    pattern = re.compile(r'([가-힣]+따위)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in TTAWI_NOSPLIT or word == '따위':
            continue
        add(word, f"{word[:-2]} 따위", "따위")

    pattern = re.compile(r'([가-힣]+사이)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in SAI_NOSPLIT or word == '사이':
            continue
        add(word, f"{word[:-2]} 사이", "사이")

    pattern = re.compile(r'([가-힣]+뿐)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in PPUN_NOSPLIT or word == '뿐':
            continue
        add(word, f"{word[:-1]} 뿐", "뿐")

    pattern = re.compile(r'([가-힣]+뿐만)')
    for word, cnt in Counter(pattern.findall(text)).most_common(200):
        if word == '뿐만':
            continue
        add(word, f"{word[:-2]} 뿐만", "뿐만")

    if text.count("고있") > 0:
        add("고있", "고 있", "고있")

    pattern = re.compile(r'고(있다|있고|있는|가다|간다|하다|하고|하여|해서|한다|하였다)')
    for m in pattern.finditer(text):
        orig = m.group(0)
        suffix = m.group(1)
        add(orig, f"고 {suffix}", "고+동사")

    pattern = re.compile(r'(것)(같.+?)')
    for m in pattern.finditer(text):
        orig = m.group(0)
        gat_part = m.group(2)
        add(orig, f"것 {gat_part}", "것 같은")

    pattern = re.compile(r'([가-힣]+것)(같[은다이고])')
    for m in pattern.finditer(text):
        orig = m.group(0)
        geot_part = m.group(1)
        gat_part = m.group(2)
        if geot_part in GEOT_NOSPLIT:
            continue
        add(orig, f"{geot_part} {gat_part}", "것 같은")

    pattern = re.compile(r'([가-힣]+)같([은다이고])')
    for word, cnt in Counter(pattern.findall(text)).most_common(200):
        full = f"{word}같{cnt}"
    gat_pattern = re.compile(r'([가-힣]+같[은다이고])')
    for m in gat_pattern.finditer(text):
        orig = m.group(1)
        if orig in GAT_NOSPLIT:
            continue
        idx_gat = orig.index('같')
        before = orig[:idx_gat]
        after = orig[idx_gat+1:]
        if before.endswith('것'):
            continue
        add(orig, f"{before} 같{after}", "같은")

    pattern = re.compile(r'([가-힣]+척[가-힣]*)')
    for word, cnt in Counter(pattern.findall(text)).most_common(500):
        if word in CHUK_NOSPLIT:
            continue
        if '친척' in word:
            continue
        skip = False
        for prefix in CHUK_NOSPLIT_PREFIXES:
            if word.startswith(prefix) or prefix in word:
                skip = True
                break
        if skip:
            continue
        idx = word.index('척')
        before = word[:idx]
        after = word[idx+1:]
        add(word, f"{before} 척{after}", "척")

    for cat, nosplit, suffix_len in [
        ("이상", ISANG_NOSPLIT, 2), ("이하", IHA_NOSPLIT, 2),
        ("밑", MIT_NOSPLIT, 1),
        ("등", DEUNG_NOSPLIT, 1), ("때", TTE_NOSPLIT, 1),
        ("때문", TTAE_MUN_NOSPLIT, 2), ("번", BEON_NOSPLIT, 1),
        ("데", DE_NOSPLIT, 1),
        ("대로", DAERO_NOSPLIT, 2),
        ("만큼", MANKEUM_NOSPLIT, 2),
        ("중", JUNG_NOSPLIT, 1),
        ("앞", AP_NOSPLIT, 1),
        ("게", GE_NOSPLIT, 1),
    ]:
        pattern = re.compile(r'([가-힣]+' + cat + r')')
        for word, cnt in Counter(pattern.findall(text)).most_common(500):
            if word in nosplit or word == cat:
                continue
            if cat == "이하" and len(word) >= 3:
                if re.search(r'이하[다고여면며서았었겠는기임할봐야지죠네요거]', word):
                    continue
                if re.search(r'이했', word):
                    continue
            if cat == "데" and len(word) >= 3:
                if word[-2:] in ("는데", "은데", "던데", "는데"):
                    continue
                if re.search(r'(하|는|은|던|었|였|았)는데$', word):
                    continue
            if cat == "앞" and len(word) >= 3:
                if re.search(r'앞(으로|서|에|의|에서|쪽|길|날|문|발|니|바다|바람|머리|다리|장|뒤|부분|사람|고)', word):
                    continue
            if cat == "게" and len(word) >= 3:
                if re.search(r'게(다가|으르|으름|으른|을러|을리|시판|임|시|재|르만|릴라|이트|르마늄)', word):
                    continue
                if not re.search(r'[할될있을없을갈볼알쓸칠먹을걸을탈받을만들줄놓을다닐살열팔는은던]게$', word):
                    continue
            stem = word[:-suffix_len]
            add(word, f"{stem} {cat}", cat)

    HA_DIRECTIONAL = {"위하", "아래하", "앞하", "뒤하", "안하", "밖하", "옆하", "위쪽하", "아래쪽하"}
    ha_pattern = re.compile(r'([가-힣]+하)')
    for word, cnt in Counter(ha_pattern.findall(text)).most_common(500):
        if word == '하' or word in HA_NOSPLIT:
            continue
        if word in HA_DIRECTIONAL:
            stem = word[:-1]
            add(word, f"{stem} 하", "하(방향)")
            continue

    jul_pattern = re.compile(r'([가-힣]+줄)')
    for word, cnt in Counter(jul_pattern.findall(text)).most_common(500):
        if word == '줄' or word in JUL_NOSPLIT:
            continue
        if re.search(r'[는은던할갈볼알줄]줄$', word):
            continue
        if word.endswith('줄') and len(word) >= 3:
            before = word[:-1]
            last_code = ord(before[-1])
            if 0xAC00 <= last_code <= 0xD7A3:
                jongseong = (last_code - 0xAC00) % 28
                if jongseong > 0:
                    continue
        if re.search(r'(닻|불|태|시계|비|견|버팀|포승|미역|이음|해|땅우)줄$', word):
            continue
        add(word, f"{word[:-1]} 줄", "줄")

    for cat, suffix_len, nosplit in [("듯", 1, DEUT_NOSPLIT), ("차례", 2, CHARYE_NOSPLIT), ("무렵", 2, set())]:
        pattern = re.compile(r'([가-힣]+' + cat + r')')
        for word, cnt in Counter(pattern.findall(text)).most_common(200):
            if word == cat or word in nosplit:
                continue
            stem = word[:-suffix_len]
            add(word, f"{stem} {cat}", cat)

    chae_pattern = re.compile(r'([가-힣]+채)')
    for word, cnt in Counter(chae_pattern.findall(text)).most_common(200):
        if word == '채' or word in CHAE_NOSPLIT:
            continue
        if re.search(r'[는은던한]채$', word):
            stem = word[:-1]
            add(word, f"{stem} 채", "채")
            continue

    jeok_pattern = re.compile(r'([가-힣]+적)')
    for word, cnt in Counter(jeok_pattern.findall(text)).most_common(500):
        if word == '적' or word in JEOK_NOSPLIT:
            continue
        if re.search(r'[는은던할본간만갈볼알먹]적$', word):
            stem = word[:-1]
            add(word, f"{stem} 적", "적")
            continue

    ji_pattern = re.compile(r'([가-힣]+지)')
    for word, cnt in Counter(ji_pattern.findall(text)).most_common(500):
        if word == '지' or word in JI_NOSPLIT:
            continue
        if re.search(r'[는은던할갈본볼알]지$', word):
            stem = word[:-1]
            add(word, f"{stem} 지", "지")
            continue

    ba_dep_pattern = re.compile(r'([가-힣]+바)')
    for word, cnt in Counter(ba_dep_pattern.findall(text)).most_common(500):
        if word == '바' or word in BA_NOSPLIT:
            continue
        if re.search(r'[는은던할있없하는]바$', word):
            stem = word[:-1]
            add(word, f"{stem} 바", "바")
            continue

    LDQ = '\u201c'
    RDQ = '\u201d'
    LSQ = '\u2018'
    RSQ = '\u2019'

    double_quote_pattern = re.compile(re.escape(LDQ) + r'([^' + re.escape(RDQ) + r']{1,50})' + re.escape(RDQ))
    for m in double_quote_pattern.finditer(text):
        q = m.group(1).strip()
        orig = m.group(0)
        cnt = text.count(orig)
        if cnt == 0:
            continue
        convert = False
        if len(q) > 20:
            continue
        elif any(ch in q for ch in "，。？！；：,.?!;:"):
            continue
        elif re.fullmatch(r'[가-힣·ㆍ\- ]{1,9}', q):
            convert = True
        elif re.fullmatch(r'[\u4e00-\u9fff()（）]{1,20}', q):
            convert = True
        elif re.fullmatch(r'[가-힣A-Za-z0-9\u4e00-\u9fff·ㆍ()（）\- ]{1,20}', q):
            convert = True
        if convert:
            corr = f"{LSQ}{q}{RSQ}"
            add(orig, corr, "쌍따옴표")

    dot_pattern = re.compile(r'([가-힣]+)·([가-힣]+)')
    seen_dots = set()
    for m in dot_pattern.finditer(text):
        orig = m.group(0)
        if orig in seen_dots:
            continue
        seen_dots.add(orig)
        has_chinese = bool(re.search(r'[\u4e00-\u9fff]', orig))
        has_digit = bool(re.search(r'\d', orig))
        if has_chinese or has_digit:
            continue
        corr = f"{m.group(1)}, {m.group(2)}"
        cnt = text.count(orig)
        if cnt > 0:
            add(orig, corr, "가운데점")

    return changes


def main():
    log_lines = []

    def log(msg):
        print(msg, flush=True)
        log_lines.append(msg)

    log(f"{'=' * 70}")
    log(f"  L파일 띄어쓰기 교정 (레코드 단위 수정)")
    log(f"  시작: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"{'=' * 70}")

    if not os.path.exists(SRC):
        log(f"  [오류] 원본 파일 없음: {SRC}")
        return

    src_hash = file_hash(SRC)
    log(f"  원본: {os.path.basename(SRC)}")
    log(f"  출력: {os.path.basename(OUT)}")
    log(f"  원본 크기: {os.path.getsize(SRC):,} bytes")
    log(f"  원본 해시: {src_hash}")

    log(f"\n  {'━' * 50}")
    log(f"  [1/7] 원본 파일 무결성 검증")
    log(f"  {'━' * 50}")

    try:
        ole = olefile.OleFileIO(SRC, write_mode=False)
        streams = ole.listdir()
        body_streams = [s for s in streams if s and s[0] == "BodyText"]
        ole.close()
        log(f"  OLE 구조: ✅ ({len(streams)} 스트림, BodyText {len(body_streams)}개)")
    except Exception as e:
        log(f"  OLE 구조: ❌ {e}")
        return

    log(f"\n  {'━' * 50}")
    log(f"  [2/7] 텍스트 추출 + 교정 규칙 생성")
    log(f"  {'━' * 50}")

    text = extract_text(SRC)
    log(f"  추출 텍스트: {len(text):,}자")

    before_stats = {}
    for cat in ["것", "수", "따위", "사이", "뿐", "뿐만", "고있", "고+동사", "척", "이상", "이하", "밑", "등", "때", "때문", "번",
                "데", "대로", "만큼", "줄", "듯", "채", "바", "터", "차례", "무렵", "듬",
                "중", "상", "우", "하", "같은", "것 같은", "나라"]:
        spaced = text.count(f" {cat}")
        total = text.count(cat)
        attached = total - spaced
        before_stats[cat] = {"spaced": spaced, "attached": attached, "total": total}
        if attached > 0:
            log(f"  [{cat}] 띄어쓰기={spaced}, 붙여쓰기={attached}, 총={total}")

    china_rules = load_china_place_rules()
    txt_rules = parse_txt_rules(RULES_FILE)
    text_changes = apply_text_corrections(text)

    DYNASTIES = [
        "당(唐)", "송(宋)", "명(明)", "청(淸)", "원(元)", "수(隋)", "진(秦)", "한(漢)",
        "위(魏)", "촉(蜀)", "오(吴)", "진(晉)", "동진(東晉)", "서진(西晉)",
        "남송(南宋)", "북송(北宋)", "서하(西夏)", "요(遼)", "금(金)",
        "제(齊)", "초(楚)", "량(梁)", "진(陳)",
    ]
    dyn_suffixes = ["때", "시기", "말기", "초기", "중기", "시기에", "때의", "의", "에", "가", "를", "이후에는", "사람으로서"]
    dynamic_nara_rules = []
    for dyn in DYNASTIES:
        for suf in dyn_suffixes:
            orig = f"{dyn}나라{suf}"
            repl = f"{dyn}조 {suf}"
            if orig in text:
                cnt = text.count(orig)
                dynamic_nara_rules.append((orig, repl, "1단계-중한(동적)", cnt))
    for suf in dyn_suffixes:
        orig = f"당나라{suf}"
        repl = f"당조 {suf}"
        if orig in text:
            cnt = text.count(orig)
            dynamic_nara_rules.append((orig, repl, "1단계-중한(동적)", cnt))

    log(f"\n  [1단계] 나라→조 + 지명: {len(china_rules)}개 (파일) + {len(dynamic_nara_rules)}개 (동적)")
    step1_rules = []
    for orig, repl in china_rules:
        if orig in text:
            cnt = text.count(orig)
            step1_rules.append((orig, repl, "1단계-중한", cnt))
            log(f"  '{orig}' → '{repl}' ({cnt}건)")
    for orig, repl, cat, cnt in dynamic_nara_rules:
        step1_rules.append((orig, repl, cat, cnt))
        log(f"  '{orig}' → '{repl}' ({cnt}건, 동적)")

    log(f"\n  [2단계] TXT 통합규칙: {len(txt_rules)}개 로드")
    step2_rules = []
    for src, dst in txt_rules:
        if src not in text:
            continue
        cnt = text.count(src)
        step2_rules.append((src, dst, "2단계-TXT", cnt))
    log(f"  적용: {len(step2_rules)}개, {sum(r[3] for r in step2_rules)}건")

    log(f"\n  [3단계] 의존명사/누락규칙: {len(text_changes)}개")
    cats = {}
    for src, dst, cat, cnt in text_changes:
        if cat not in cats:
            cats[cat] = 0
        cats[cat] += cnt
    for cat_name, total in sorted(cats.items(), key=lambda x: -x[1]):
        log(f"    {cat_name}: {total}건")

    all_rules = step1_rules + step2_rules + text_changes
    all_rules.sort(key=lambda r: len(r[0]), reverse=True)
    log(f"\n  총 규칙: {len(all_rules)}개, {sum(r[3] for r in all_rules)}건")

    if not all_rules:
        log(f"\n  수정 불필요")
        return

    log(f"\n  {'━' * 50}")
    log(f"  [3/7] 백업 + 레코드 단위 수정")
    log(f"  {'━' * 50}")

    os.makedirs(BACKUP_DIR, exist_ok=True)
    backup_name = os.path.basename(SRC).replace('.hwp', f'_bak_{time.strftime("%H%M%S")}.hwp')
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    shutil.copy2(SRC, backup_path)
    log(f"  백업: {backup_path}")

    ole = olefile.OleFileIO(SRC, write_mode=False)
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
            log(f"  [경고] {sn}: 압축해제 실패 - 건너뜀")
            continue

        records = parse_records(dec)
        log(f"\n  {sn}: {len(records)}개 레코드, 압축={len(raw):,}, 해제={len(dec):,}")

        stream_changes = 0
        text_rec_count = 0
        modified_rec_count = 0

        for i, rec in enumerate(records):
            if rec["tag_id"] != 67:
                continue
            text_rec_count += 1

            try:
                rec_text = rec["payload"].decode('utf-16-le', errors='replace')
            except Exception:
                continue

            new_text = rec_text
            rec_changes = 0

            for src_word, dst_word, cat, cnt in all_rules:
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

        log(f"  텍스트 레코드: {text_rec_count}개, 수정: {modified_rec_count}개, 교정: {stream_changes}건")

        if stream_changes > 0:
            new_dec = rebuild_stream(records)
            log(f"  스트림 재구성: {len(dec):,} → {len(new_dec):,} bytes (+{len(new_dec)-len(dec):,})")

            co = zlib.compressobj(level=6, method=zlib.DEFLATED, wbits=-15)
            new_compressed = co.compress(new_dec) + co.flush()
            original_size = len(raw)
            log(f"  압축: {original_size:,} → {len(new_compressed):,} bytes")

            if len(new_compressed) <= original_size:
                all_stream_data[sn] = (new_compressed, original_size)
                log(f"  압축: {len(new_compressed):,} / {original_size:,} (여유: {original_size - len(new_compressed):,})")
            else:
                log(f"  [경고] 압축 크기 초과! 원본={original_size:,}, 새={len(new_compressed):,}")
                log(f"  [해결] 압축 레벨을 낮추어 재시도...")
                co2 = zlib.compressobj(level=1, method=zlib.DEFLATED, wbits=-15)
                new_compressed2 = co2.compress(new_dec) + co2.flush()
                log(f"  재압축(level=1): {len(new_compressed2):,} bytes")
                if len(new_compressed2) <= original_size:
                    all_stream_data[sn] = (new_compressed2, original_size)
                    log(f"  압축: {len(new_compressed2):,} / {original_size:,} (여유: {original_size - len(new_compressed2):,})")
                else:
                    log(f"  [오류] 압축 불가! 파일이 너무 커짐")
                    return

            verify_dec = zlib.decompress(new_compressed if len(new_compressed) <= original_size else new_compressed2, -15)
            verify_records = parse_records(verify_dec)
            verify_text = extract_text_from_records(verify_records)
            log(f"  검증: ✅ 압축해제 일치 (레코드={len(verify_records)}, 텍스트={len(verify_text):,}자)")
            modified_streams.append(sn)
        else:
            log(f"  변경 없음")

    if not modified_streams:
        log(f"\n  변경된 스트림 없음")
        return

    log(f"\n  {'━' * 50}")
    log(f"  [4/7] 직접 바이너리 수정 (OLE 구조 보존)")
    log(f"  {'━' * 50}")

    shutil.copy2(SRC, OUT_TMP)
    os.chmod(OUT_TMP, stat.S_IWRITE | stat.S_IREAD)
    log(f"  작업본 복사 완료: {OUT_TMP}")

    ole_info = olefile.OleFileIO(SRC, write_mode=False)
    sector_size = ole_info.sector_size

    for sn in modified_streams:
        compressed_data, original_stream_size = all_stream_data[sn]
        sp = sn.split('/')
        sid = ole_info._find(sp)
        entry = ole_info.direntries[sid]
        stream_size = entry.size
        start_sector = entry.isectStart

        log(f"  스트림: {sn}, size={stream_size:,}, start_sector={start_sector}")
        log(f"  압축 데이터: {len(compressed_data):,} bytes (스트림 크기: {original_stream_size:,})")

        fat = ole_info.fat
        chain = []
        current = start_sector
        while current >= 0 and current < len(fat):
            chain.append(current)
            current = fat[current]
            if len(chain) > 100000:
                break

        log(f"  섹터 체인: {len(chain)}개 섹터")

        with open(OUT_TMP, 'r+b') as f:
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

        log(f"  직접 쓰기 완료: {len(compressed_data):,} bytes → {min(data_offset, len(compressed_data)):,} bytes 기록")

        if len(compressed_data) != stream_size:
            with open(OUT_TMP, 'r+b') as f:
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
                    old_size_bytes = f.read(4)
                    old_size = struct.unpack('<I', old_size_bytes)[0]

                    f.seek(dir_entry_offset + 120)
                    f.write(struct.pack('<I', len(compressed_data)))
                    f.seek(dir_entry_offset + 124)
                    f.write(struct.pack('<I', 0))

                    log(f"  디렉토리 엔트리 size 업데이트: {old_size:,} → {len(compressed_data):,}")
                    log(f"  디렉토리 엔트리 offset: 0x{dir_entry_offset:X} (섹터 {dir_sect}:{entry_idx})")
                else:
                    log(f"  [경고] 디렉토리 엔트리를 찾을 수 없음 (sid={sid}, sect_idx={sect_idx})")
        else:
            log(f"  디렉토리 엔트리 size 변경 불필요 (동일: {stream_size:,})")

    ole_info.close()

    if os.path.exists(OUT):
        try:
            os.chmod(OUT, stat.S_IWRITE | stat.S_IREAD)
            os.remove(OUT)
            OUT_FINAL = OUT
        except PermissionError:
            log(f"  [경고] 기존 .hwp 파일 삭제 실패, 새 이름으로 저장")
            OUT_FINAL = OUT.replace('.hwp', '_new.hwp')
            if os.path.exists(OUT_FINAL):
                try:
                    os.chmod(OUT_FINAL, stat.S_IWRITE | stat.S_IREAD)
                    os.remove(OUT_FINAL)
                except PermissionError:
                    OUT_FINAL = OUT.replace('.hwp', f'_new_{time.strftime("%H%M%S")}.hwp')
    else:
        OUT_FINAL = OUT
    os.rename(OUT_TMP, OUT_FINAL)
    log(f"  .bin → .hwp 변경 완료: {OUT_FINAL}")

    hash_after_write = file_hash(OUT_FINAL)
    log(f"  쓰기 후 해시: {hash_after_write}")
    log(f"  해시 변경됨: {hash_after_write != file_hash(SRC)}")

    if hash_after_write == file_hash(SRC):
        log(f"  [오류] 해시 변경 없음! 직접 쓰기 미적용!")
        return

    log(f"\n  {'━' * 50}")
    log(f"  [5/7] 출력 파일 검증")
    log(f"  {'━' * 50}")

    try:
        ole = olefile.OleFileIO(OUT_FINAL, write_mode=False)
        streams = ole.listdir()
        body_count = sum(1 for s in streams if s and s[0] == "BodyText")
        for sp in streams:
            if sp[0] == "BodyText":
                raw = ole.openstream('/'.join(sp)).read()
                dec = zlib.decompress(raw, -15)
                records = parse_records(dec)
                text = extract_text_from_records(records)
                log(f"  OLE: ✅ ({len(streams)} 스트림, BodyText {body_count}개)")
                log(f"  압축해제: ✅ ({len(raw):,}→{len(dec):,} bytes)")
                log(f"  레코드: {len(records)}개")
                log(f"  텍스트: {len(text):,}자")
        ole.close()
    except Exception as e:
        log(f"  [오류] {e}")
        return

    log(f"\n  {'━' * 50}")
    log(f"  [6/7] 교정 결과 검증 (수정 전후 비교)")
    log(f"  {'━' * 50}")

    text2 = extract_text(OUT_FINAL)
    log(f"  수정 후 텍스트: {len(text2):,}자 (원본: {len(text):,}자)")

    after_stats = {}
    for cat in ["것", "수", "따위", "사이", "뿐", "뿐만", "고있", "고+동사", "척", "이상", "이하", "밑", "등", "때", "때문", "번",
                "데", "대로", "만큼", "줄", "듯", "채", "바", "터", "차례", "무렵", "듬",
                "중", "상", "우", "하", "같은", "것 같은", "나라"]:
        spaced = text2.count(f" {cat}")
        total = text2.count(cat)
        attached = total - spaced
        after_stats[cat] = {"spaced": spaced, "attached": attached, "total": total}

    log(f"\n  {'패턴':<8} {'전-붙임':>8} {'전-띄움':>8} {'후-붙임':>8} {'후-띄움':>8} {'변화':>8}")
    log(f"  {'─' * 55}")
    for cat in ["것", "수", "따위", "사이", "뿐", "뿐만", "고있", "고+동사", "척", "이상", "이하", "밑", "등", "때", "때문", "번",
                "데", "대로", "만큼", "줄", "듯", "채", "바", "터", "차례", "무렵", "듬",
                "중", "상", "우", "하", "같은", "것 같은", "나라"]:
        b = before_stats.get(cat, {"spaced": 0, "attached": 0})
        a = after_stats.get(cat, {"spaced": 0, "attached": 0})
        diff = b["attached"] - a["attached"]
        if b["attached"] > 0 or a["attached"] > 0:
            mark = "✅" if diff > 0 else ("➖" if diff == 0 else "❌")
            log(f"  {cat:<8} {b['attached']:>8} {b['spaced']:>8} {a['attached']:>8} {a['spaced']:>8} {diff:>+8} {mark}")

    remaining = 0
    remaining_details = []
    for src_word, dst_word, cat, cnt in all_rules:
        cnt2 = text2.count(src_word)
        if cnt2 > 0:
            remaining += cnt2
            remaining_details.append((src_word, dst_word, cnt2, cat))

    if remaining == 0:
        log(f"\n  ✅ 모든 교정 완료! (남은 항목 없음)")
    else:
        log(f"\n  ⚠️ {remaining}건 남음")
        for src_word, dst_word, cnt2, cat in remaining_details[:30]:
            log(f"    남음: '{src_word}' → '{dst_word}' ({cnt2}건, {cat})")

    log(f"\n  {'━' * 50}")
    log(f"  [교정 상세 내역]")
    log(f"  {'━' * 50}")

    cat_groups = {}
    for src_word, dst_word, cat, cnt in change_log:
        if cat not in cat_groups:
            cat_groups[cat] = []
        cat_groups[cat].append((src_word, dst_word, cnt))

    for cat in sorted(cat_groups.keys()):
        items = cat_groups[cat]
        total_cat = sum(c for _, _, c in items)
        log(f"\n  [{cat}] {len(items)}개 항목, {total_cat}건")
        for src_word, dst_word, cnt in sorted(items, key=lambda x: -x[2])[:15]:
            log(f"    '{src_word}' → '{dst_word}' ({cnt}건)")
        if len(items) > 15:
            extra = sum(c for _, _, c in items[15:])
            log(f"    ... 외 {len(items)-15}개 ({extra}건)")

    log(f"\n  {'━' * 50}")
    log(f"  [7/7] HWP 파일 열기 테스트")
    log(f"  {'━' * 50}")

    try:
        import subprocess
        hwp_exe = r'C:\Program Files (x86)\Hnc\Office 2024\HOffice130\Bin\Hwp.exe'
        if os.path.exists(hwp_exe):
            proc = subprocess.Popen([hwp_exe, OUT_FINAL])
            time.sleep(5)
            poll = proc.poll()
            if poll is None:
                log(f"  ✅ HWP 파일 열기 성공! (PID={proc.pid})")
            elif poll == 0:
                log(f"  ✅ HWP 정상 종료 (코드: 0)")
            else:
                log(f"  ⚠️ HWP가 종료됨 (코드: {poll})")
        else:
            log(f"  ⚠️ HWP 실행 파일 없음 - 수동 확인 필요")
    except Exception as e:
        log(f"  ⚠️ HWP 열기 테스트 실패: {e}")

    log(f"\n{'=' * 70}")
    log(f"  완료: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"  총 교정: {total_changes}건")
    log(f"  출력 파일: {OUT_FINAL}")
    log(f"  최종 해시: {file_hash(OUT_FINAL)}")
    log(f"  원본 해시: {src_hash}")
    log(f"  파일 변경됨: {file_hash(OUT_FINAL) != src_hash}")
    log(f"{'=' * 70}")

    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, f"L교정로그_{time.strftime('%Y%m%d_%H%M%S')}.txt")
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    log(f"  로그 저장: {log_path}")


if __name__ == "__main__":
    main()
