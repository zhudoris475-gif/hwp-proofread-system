# -*- coding: utf-8 -*-
import sys, os, re, struct, zlib, hashlib, time, shutil, stat
from collections import Counter, defaultdict
from datetime import datetime

sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import olefile

from .constants import PROVINCE_ABBREV, SECTIONS

RULES_CHINA_PLACE = r"C:\AMD\AJ\hwp_proofreading_package\rules_china_place.txt"
RULES_DOCUMENTATION = r"C:\AMD\AJ\hwp_proofreading_package\rules_documentation.txt"
RULES_REGEX = r"C:\AMD\AJ\hwp_proofreading_package\rules_regex.txt"

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
    "진척이","진척을","진척의","진척도","련척","륙척","인척인","수척해보이자","수척해보이고","말리는척","자비스러운척",
    "없는척한다는","척추를","척추의","척추가","척수를","척수의","척수가","척도를","척도의","척도가",
    "진척하고","진척한","간척을","간척의","세척을","세척의","세척이","개척을","개척의","개척이","배척을","배척의","배척이","인척을","인척의","인척이",
    "배척당하고","계척","산세척","인척관계를","수척하다","수척한","수척해지다","지척에",
    "세척하다","세척액","세척법","세척제","개척하는","개척한","무척추동물의","무척추동물에","무척추동물지",
    "부패척결의","가치척도","협척혈","온도척도","화씨온도척도와","온도척도를","알카리세척제","알카리세척","알카리세척제를",
    "변기세척제","국부세척기","엉뎅이척추뼈","인기척에도","인기척이","기척도","뇌척수막","외척의","건설진척을",
    "척추동물의","지척거리는","공사진척이","공사진척",
}

ISANG_NOSPLIT = {"이상","이상의","이상으로","이상하다","이상하게","이상한","정상이상","비정상이상"}
MIT_NOSPLIT = {"밑","밑바닥","밑면","밑부분","밑천"}
AP_NOSPLIT = {"앞날","앞으로","앞서","앞뒤","앞문","앞길","앞장","앞니","앞발","앞다리","앞머리","앞바다","앞바람","앞뒤","앞쪽","앞부분","앞사람","앞뒤로","앞으로서","앞에서","앞에","앞의"}
GE_NOSPLIT = {"게다가","게으르다","게으름","게시판","게임","게으른","게을러","게을리","장게","게시","게재","게르만","게릴라","게이트","게르마늄","훈계게","총계게","통계게"}
DEUT_NOSPLIT = {"반듯","반듯이","빠듯","빠듯이","여느듯","그듯","가득듯","오직듯","마치듯","함듯","듯이","듯하다","듯싶다","인듯","듯이","만듯","같은듯","하는듯","있는듯","없는듯"}
CHARYE_NOSPLIT = {"차례차례","차례대로","이차례","삼차례","첫차례","다음차례","뒷차례","차례로","차례차례로"}

GAWUNDE_NOSPLIT = {"가운데","한가운데","가운데서","가운데로","가운데에","가운데의","가운데서부터"}
AN_NOSPLIT = {
    "집안","방안","안방","안쪽","안쪽으로","안으로","안에","안전","안정","안내","안녕","안부","안심","안주","안경","안개","안과","안기","안락","안마","안반","안벽","안색","안성","안약","안양","안입","안장","안중","안치","안태","안팎","안해","안흥","안으로서","안에서","안으로부터",
    "실내안","차안","내안","시안","평안","보안","건안","공안","치안","편안","불안","안과의사","안전하게","안전한","안정적","안정되다",
    "실내","안골","안마당","안뜰","안채",
    "안료","수안","편안하다","평안하다","불안하게","불안한","불안해","미안","미안하게","미안한","미안해",
    "위안","위안을","위안이","위안으로",
    "동안","동안에","동안의","한동안","오래동안","한참동안","시간동안","며칠동안",
    "해안","해안에","해안의","해안으로",
    "안도","답안","육안","문안","연안","장안","감안","제안","현안","의안","강안",
}
BAK_NOSPLIT = {
    "밖으로","밖에","밖의","밖에서","밖으로부터","바깥","바깥쪽","바깥으로","밖바람","역밖",
    "뜻밖","뜻밖에","뜻밖의","뜻밖이","예상밖","예상밖으로","예상밖의","예상밖에",
    "생각밖","생각밖이","생각밖으로","범위밖","규정밖","상식밖","기준밖","선밖",
    "수밖에","수밖에는",
}
DWI_NOSPLIT = {
    "뒤로","뒤에","뒤의","뒤에서","뒤로부터","뒷문","뒷마당","뒷산","뒷골목","뒷모습",
    "뒷바라지","뒷발","뒷방","뒷북","뒷일","뒷자리","뒷전","뒷편","뒷통증",
    "뒤늦","뒤바뀌다","뒤바뀌","뒤바뀐","뒤따르다","뒤따라","뒤돌아","뒷걸음",
    "뒷갈망","뒷다리","뒷말","뒷면","앞뒤",
    "여드레","사흘뒤","나흘뒤","이틀뒤","며칠뒤","한달뒤","일주일뒤",
}

GAUNDE_NOSPLIT = {
    "가운데","한가운데","그가운데","이가운데","저가운데",
    "사람가운데","학생가운데","것가운데","곳가운데","땅가운데",
    "집가운데","물가운데","산가운데","길가운데","또래가운데",
    "세계가운데","국민소득가운데","도시가운데","마을가운데",
    "숲가운데","바다가운데","방가운데","운동장가운데","광장가운데",
    "군중가운데","아이가운데","여성가운데","남성가운데","노인가운데",
    "청년가운데","학자가운데","직원가운데","시민가운데","국민가운데",
    "동료가운데","친구가운데","가족가운데","이웃가운데","형제가운데",
}

DEUNG_NOSPLIT = {
    "균등","고등","강등","상등","대등","초등","일등","발등",
    "갈등","평등","동등","항등","비등","불평등",
    "등등","등산","등록","등장","등급","등불","등대",
    "가로등","형광등","섬광등","전조등","경고등","경광등",
    "안전등","착륙등","착신등","진입등","탁상등","채색등",
    "책등","칼등","등뼈","등받이",
    "주민등록","기회균등","감수분렬부등",
    "신호등","손전등","전등","곱사등","호적등",
    "자원평등","교통신호등","립식전등","련결등",
    "풍력등","초불등","신용등","벌등",
    "렬등","귓등","뢰공등","랭음극형광등",
    "열등","산등","홍등","세등","중등","이등",
    "려객등","록색등","세움등","키큰등",
    "급등","등불","등기","등교","등반","등신",
    "휴대등","야간등","실내등","복도등","계단등",
    "비상등","유도등","출입등","통로등",
}

TTE_NOSPLIT = {"제때","한때","때때로","아무때","때때","명절때","점심때","저녁때","병때","본때"}
TTAE_MUN_NOSPLIT = {"때문","때문에","때문이다"}

BEON_NOSPLIT = {
    "이번","한번","두번","세번","네번","여러번","몇번","매번",
    "첫번","한꺼번","두리번","단번","백번","여섯번","일곱번",
    "여덟번","아홉번","두어번","빈번","농번","교번",
    "자동번","전화번","기계번","비밀번","일련번","부품번",
    "종자번","가축번","성장번","경찰번","천둥번","근친번",
    "금번","대번","해번","절번","홀수번",
    "순번","류번","원자번","발신번","당번","련속번",
    "천번","지난번","원소번","전번","자유번","추첨당첨번",
    "륜번","타번","리번","오즈번","번쩍번",
    "번번이","번쩍번쩍","번거롭다",
    "청소당번","야간당번","경비당번",
}

DE_NOSPLIT = {"가운데","한가운데","그가운데","포름알데","놀포름알데","메타알데","아쎄트알데","알데","데굴데","번데","한데","아데",
    "데려","데리고","데려가","데려오","데릴",
    "앙데","지데","놀이데","춤데",
    "수데","김데","빛데","밤데","길데","밭데",
    "어데","여데","제데","참데","집데",
    "껍데기","껍데","껍질데",
    "사람가운데","것가운데","곳가운데","땅가운데",
    "집가운데","물가운데","산가운데","길가운데",
    "또래가운데","세계가운데","국민소득가운데",
    "데구르르","데굴데굴","데미지","데시벨",
    "데탕트","데투라","데우다","데워",
    "본데","간데","하는데","한데","는데","은데","던데",
    "좋은데","많은데","적은데","높은데","편한데","큰데","작은데",
    "그런데","이런데","어떤데","없는데","있는데","된데",
}

DAERO_NOSPLIT = {"뜻대로","마음대로","그대로","이대로","저대로","자대로","제멋대로","맘대로","임의대로","자연대로",
    "이대로라도","그대로라도","있는대로","되는대로","하는대로",
    "본대로","들은대로","본대로","아는대로","가는대로",
    "절대로","제대로","대대로","영대로","선대로",
    "사실대로","순서대로","규정대로","요구대로","약속대로",
    "계획대로","예상대로","생각대로","소원대로","명령대로",
    "원래대로","그대로라도","있는그대로",
}

MANKEUM_NOSPLIT = {"그만큼","이만큼","저만큼","만큼"}

JUL_NOSPLIT = {"줄밖","줄",
    "힘줄","바줄","새끼줄","기계줄","청줄","산줄","드레박줄",
    "물줄","소줄","동줄","줄다","줄기","줄줄이",
    "생줄","명줄","목줄","핏줄","신줄","실줄",
    "어줄","당줄","줄줄","고줄","대줄","쇠줄",
    "전줄","연줄","줄당","줄자","줄녀석",
    "노끈줄","밧줄","끈줄","철줄","나일론줄",
    "고무줄","전깃줄","철사줄","끌줄","감줄",
    "매듭줄","낚시줄","안전줄","구명줄","전화줄",
    "올줄","굵은줄","가는줄","긴줄","짧은줄",
    "거미줄","덩굴줄","두레박줄","오라줄","계선줄",
    "다듬질줄","빨래줄","넋줄","밧줄","동아줄",
    "줄기차다","줄기","줄거리","줄임말","줄임",
    "줄알다","줄모르다","줄서다","줄잇다",
    "갈대줄","이야기줄","뾰족평줄","송곳줄","평줄",
    "줄발","줄당기다","줄조임","줄타기","줄임꼴",
    "줄간격","줄바꿈","줄세우기","줄거리","줄임표",
    "피줄","먹줄","당김줄","구린줄","어쩔줄",
    "묶음쇠줄","견인바줄","쇠바줄",
    "부끄러운줄","도와줄","붉은줄","검은줄",
    "련줄","알줄","볼줄","할줄","갈줄",
    "줄을","줄의","줄이","줄은","줄에",
    "피줄을","피줄의","먹줄을","먹줄의",
    "구리줄","나무줄","시계줄","버팀줄","포승줄",
    "닻줄","불줄","태줄","비줄","이음줄",
    "해줄","미역줄","낳은줄","싫은줄","않은줄",
}

TEO_NOSPLIT = {
    "콤퓨터","모니터","인터","인터넷","프린터","센터","터미널",
    "허터","필터","액터","팩터","벡터","렉터",
    "오래전부터","부터","로부터","에서부터","으로부터",
    "두터","흉터","엉터","엉터리","상처터",
    "량쪽으로부터","곁으로부터","밖으로부터","안으로부터",
    "터전","터밭","터끌","터럭","터진","터지다","터뜨리다",
    "터득","터득하다","터치","터치하다",
    "김터","밭터","집터","답터","터전",
    "모터","발전터","극터","온터",
    "포터","마스터","시터","지터",
    "렌터","카운터","아우터","이터",
    "파터","도터","비터","레터",
    "바터","페터","세터","게터",
    "부터","까지","까지도",
    "콤퓨터를","콤퓨터에","콤퓨터로","콤퓨터의","콤퓨터가","콤퓨터는",
    "모니터를","모니터에","모니터로","모니터의","모니터가","모니터는",
    "센터를","센터에","센터로","센터의","센터가","센터는",
    "프린터를","프린터에","프린터로","프린터의",
    "필터를","필터에","필터의",
    "예로부터","옛날부터","이전부터","싸움터","전쟁터","포스터","리히터",
    "흘리터","쎈치메터","립방메터","처음부터","예전부터","어릴적부터",
    "올해부터","언제부터","가죽부터","물러터","사회로부터","주형으로부터",
    "동지부터","이미전부터","세기말부터","휴대용콤퓨터","로인병치료센터",
    "발사로부터","눈물부터","뒤부터","립방쎈치메터","평방메터","쎈치리터",
    "릿터","리티움배터","겁부터","만메터","세제곱메터","립방데시메터",
    "립방미리메터","립방센치메터","아침부터","고체로부터","어디에서부터",
    "오래전부터","이때부터","고대로부터","인터페이스","인터럽트",
    "콤퓨터","컴퓨터","노트북","랩터","슬러터",
}

CHAE_NOSPLIT = {
    "색채","외채","공채","미지급채","납채","정채","국채","사채",
    "다문채","총채","끌채","가로채","낚아채","눈치채",
    "국가경제건설공채","건설공채","경제건설공채",
    "채권","채무","채석","채소","채집","채용","채택","채점",
    "채색","채널","채팅","채우다","채워","채운",
    "채소를","채소의","채소가","채소는",
    "채권을","채권의","채권이","채권은",
    "채용을","채용의","채용이","채용은",
    "채집을","채집의","채집이",
    "채택을","채택의","채택이",
    "공채를","공채의","공채가","공채는",
    "외채를","외채의","외채가","외채는",
    "사채를","사채의","사채가","사채는",
    "국채를","국채의","국채가","국채는",
    "납채를","납채의",
    "정채를","정채의",
    "색채를","색채의","색채가","색채는",
    "낚아채다","가로채다","눈치채다",
    "가로채서","가로채고","가로채면",
    "낚아채서","낚아채고","낚아채면",
    "눈치채서","눈치채고","눈치채면",
    "빚채","은채","금채","동채","철채",
    "파채","김채","밭채","채채",
    "대채","현채","단채","본채",
    "부채","보채","생채","랭채","벌채","다채",
    "류동부채","쓰레기채","가죽채","곰의말채",
    "부채를","부채의","부채가","부채는",
    "보채다","보채고","보채서",
    "송두리채","뻗은채","앉은채","누운채","서있는채",
    "사랑채","야채","유채","안채","풍채","전채",
    "통채","털채","꿀발부채","련대채","련쇄부채",
    "뿌리채","막힌채",
    "사랑채를","사랑채의","사랑채가",
    "야채를","야채의","야채가","야채는",
    "유채를","유채의","유채가","유채는",
    "안채를","안채의","안채가","안채는",
    "풍채를","풍채의","풍채가","풍채는",
    "전채를","전채의","전채가","전채는",
    "통채를","통채의","통채로",
    "털채를","털채의",
    "꿀발부채를","꿀발부채의",
    "련대채를","련대채의",
    "련쇄부채를","련쇄부채의",
    "뿌리채를","뿌리채의","뿌리채로",
    "막힌채로","막힌채를",
    "건너채","마루채","부엌채","광채","외양채",
    "곁채","별채","윗채","아랫채","웃채",
    "살림채","사랑채","행랑채","대청채",
    "야채를","야채와","야채에","야채로",
    "김치야채","신선야채","유기야채",
    "유채꽃","유채밭","유채기름",
    "풍채가","풍채를","풍채의",
    "전채식","전채요리",
}

JEOK_NOSPLIT = {
    "본적","간적","적성","적자","적중","적응","적극","적법","적당",
    "적색","적소","적임","적요","적의","적합","적활",
    "부적","부적절","부적당","부적합",
    "적극적","소극적","적극적으로","소극적으로",
    "적극성","적성검사","적자결산","적자운행",
    "근본적","기본적","일반적","구체적","객관적","주관적",
    "절대적","상대적","적극적","소극적","적대적",
    "특수적","일반적","개별적","전체적","국부적",
    "순간적","영구적","일시적","지속적","정치적",
    "경제적","사회적","문화적","역사적","과학적",
    "시간적","공간적","물리적","화학적","생물적",
    "원적","본적지","본적을","본적이","본적의",
    "시간적구간","공간적인","순간적으로","순간적인",
    "근본적으로","기본적으로","일반적으로","구체적으로",
}

JI_NOSPLIT = {
    "한지","간지","산지","할지","본지","갈지",
    "지구","지역","지방","지도","지시","지원","지식","지적",
    "지위","지점","지표","지평","지형","지질","지리",
    "인지","양지","음지","고지","본지","원지","외지",
    "한지","백지","장지","모지","절지","생지","건지",
    "간지도수","간지","산지를","산지의","산지가",
    "휴한지","휴경지","식량생산지",
    "지리하다","지루하다","지루하고",
}

BA_NOSPLIT = {
    "바다","바람","바늘","바깥","바구니","바닥","바탕",
    "바위","바이러스","바이올린","바코드","바람직",
    "김바","밭바","산바","들바",
    "바꾸다","바꾸어","바꾸면",
    "바라다","바라고","바라면",
    "바로","바르다","바르게",
    "바치다","바치고","바치면",
    "바라","바래","바랍",
    "어바","가바","하바","자바",
    "우바","좌바","대바","명바",
    "바깥","바깥쪽","바깥으로",
    "거울바","문바","길바",
    "곧바로","똑바로","올바르다","옳바르다",
    "뒤바뀌다","뒤바뀌","뒤바뀐",
    "거꾸로바뀌다","서로바뀌다",
    "바삭바삭","들썩들썩","반짝반짝",
    "곧바","똑바","옳바","뒤바",
    "지르바","울바","낯바","밑바",
    "고무바","손바","가을바",
    "룸바","견인바","쇠바","골덴바",
    "회오리바","돌개바","류산바","장바","막바",
    "바탕","바람","바다","바느질",
}

IHA_NOSPLIT = {
    "가까이하다","가까이하고","가까이하여","가까이해서","가까이한",
    "가까이하","가까이해","가까이했",
    "기이하다","기이하고","기이한","기이하여",
    "기이하","기이해","기이했",
    "되풀이하다","되풀이하고","되풀이하여","되풀이한",
}

SANG_NOSPLIT = {
    "명실상","외관상","전설상","사실상","이론상","현실상","형식상","관념상",
    "법률상","도의상","원칙상","관례상","표면상","내용상","형편상",
    "성격상","성질상","기능상","구조상","형태상","위치상","조건상",
    "역사상","문화상","경제상","정치상","사회상","국제상",
    "인연상","운명상","숙명상","관계상","인과상",
    "합의상","계약상","규정상","법령상","규칙상",
    "이상","이상의","이상으로","이상하다","이상하게","이상한",
    "정상이상","비정상이상",
    "예상","예상의","예상으로","예상하다","예상하고","예상한",
    "하상","중상","상하","좌상","우상","전상","후상",
    "상식","상징","상태","상황","상관","상호","상반","상쇄","상승","상실","상존","상통","상응","상의","상조",
    "등상","대상","급상","최상","차상","하상","금상","은상","동상",
    "무역대상","문화대상","노벨상","아카데미상",
    "사불상","사마상","미곡상","어물상","약상","다과상","술상","밥상","반상",
    "민사상","형사상","외국상","분포상",
    "산하","강하","제강하다","제강하고","제강하여","생산하다","생산하고","생산하여","생산한",
    "청산하다","청산하고","청산하여","청산한","계산하다","계산하고","계산하여","계산한",
    "하강하다","하강하고","하강하여","강하다","강하고","강하여","강한",
    "산하의","산하를","산하가","산하는",
}

U_NOSPLIT = {"우두머리","우산","우주","우유","우편","우호","우연","우수","우월","우세","우려","우레","우습다","우울","우직"}
JUNG_NOSPLIT = {"소중","공중","대중","수중","신중","명중","집중","귀중","궁중","열중","과중","적중","집중적","대중적","공중전화","대중교통","중간","중계","중단","중독","중량","중립","중복","중심","중앙","중요","중지","중폭","중합","중화"}

GAT_NOSPLIT = {"똑같다","똑같이","똑같은","마찬가지로","같이","같은","같다"}

HA_NOSPLIT = {
    "비유하다","비유하고","비유하여","비유한",
    "속하다","속하고","속하여","속한",
    "형용하다","형용하고","형용하여","형용한",
    "못하다","못하고","못하여","못한",
    "말하다","말하고","말하여","말한",
    "청렴하다","청렴하고","청렴한",
    "사용하다","사용하고","사용하여","사용한",
    "일하다","일하고","일하여","일한",
    "처리하다","처리하고","처리하여","처리한",
    "로련하다","로련하고","로련한",
    "대하다","대하고","대하여","대한",
    "다하다","다하고","다하여","다한",
    "련결하다","련결하고","련결하여","련결한",
    "리용하다","리용하고","리용하여","리용한",
    "리해하다","리해하고","리해하여","리해한",
    "생각하다","생각하고","생각하여","생각한",
    "피로하다","피로하고","피로한",
    "랭담하다","랭담하고","랭담한",
    "좋아하다","좋아하고","좋아하여","좋아한",
    "그리워하다","그리워하고","그리워하여",
    "쌀쌀하다","쌀쌀하고","쌀쌀한",
    "정리하다","정리하고","정리하여","정리한",
    "어수선하다","어수선하고","어수선한",
    "비슷하다","비슷하고","비슷한",
    "시원하다","시원하고","시원한",
    "발생하다","발생하고","발생하여","발생한",
    "계속하다","계속하고","계속하여","계속한",
    "당하다","당하고","당하여","당한",
    "조심하다","조심하고","조심하여","조심한",
    "정직하다","정직하고","정직한",
    "민첩하다","민첩하고","민첩한",
    "란잡하다","란잡하고","란잡한",
    "깨끗하다","깨끗하고","깨끗한",
    "침착하다","침착하고","침착한",
    "안내하다","안내하고","안내하여","안내한",
    "이야기하다","이야기하고","이야기하여","이야기한",
    "진행하다","진행하고","진행하여","진행한",
    "실행하다","실행하고","실행하여","실행한",
    "싫어하다","싫어하고","싫어하여",
    "단정하다","단정하고","단정한",
    "하다","하고","하여","해서","하였다","한다","한","하세요","하기","함","할","했","하는",
    "산하","강하","제강하다","제강하고","제강하여",
    "생산하다","생산하고","생산하여","생산한",
    "청산하다","청산하고","청산하여","청산한",
    "계산하다","계산하고","계산하여","계산한",
    "하강하다","하강하고","하강하여",
    "강하다","강하고","강하여","강한",
    "산하의","산하를","산하가","산하는",
}

GO_NOSPLIT = {
    "고하다","고하고","고하여","고해서","고한",
    "고가다","고간다","고가고",
    "고있다","고있고","고있는","고있다",
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
    ("것같음", "것 같음"), ("것같고", "것 같고"),
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
    ("없는것", "없는 것"), ("있는것", "있는 것"),
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
    ("친구사이", "친구 사이"), ("부부사이", "부부 사이"),
    ("이웃사이", "이웃 사이"), ("형제사이", "형제 사이"),
    ("학생가운데", "학생 가운데"), ("사람가운데", "사람 가운데"),
    ("고하다", "고 하다"), ("고하였다", "고 하였다"), ("고합니다", "고 합니다"),
    ("고했다", "고 했다"), ("고하며", "고 하며"),
    ("잠간동안", "잠간 동안"), ("기간동안", "기간 동안"),
    ("오래동안", "오래 동안"), ("한참동안", "한참 동안"),
    ("시간동안", "시간 동안"), ("며칠동안", "며칠 동안"),
    ("볼게요", "볼 게요"), ("할게요", "할 게요"), ("될게요", "될 게요"),
    ("마음밖에", "마음 밖에"), ("문밖에", "문 밖에"), ("집밖에", "집 밖에"),
    ("마음안에", "마음 안에"), ("품안에", "품 안에"), ("가슴안에", "가슴 안에"),
    ("할수밖에", "할 수밖에"), ("될수밖에", "될 수밖에"),
]

CONTEXT_SPACING_RULES = [
    (r'(\w+)줄$', r'\1 줄'),
    (r'(\w+)줄(\s)', r'\1 줄\2'),
    (r'하려는대로', '하려는 대로'),
    (r'하는대로', '하는 대로'),
    (r'된대로', '된 대로'),
    (r'말한대로', '말한 대로'),
    (r'약속한대로', '약속한 대로'),
    (r'원한대로', '원한 대로'),
    (r'바란대로', '바란 대로'),
    (r'기대한대로', '기대한 대로'),
    (r'(\d+)(명|개|원|건|곳|군데|마리|권|부|장|포기|그루|송이|대|채|벌|켤레|줄|쪽|차례|번째)이상', r'\1\2 이상'),
    (r'(\d+)(명|개|원|건|곳|군데|마리|권|부|장|포기|그루|송이|대|채|벌|켤레|줄|쪽|차례|번째)이하', r'\1\2 이하'),
    (r'(\w+)가운데', r'\1 가운데'),
    (r'(\w+)밖에', r'\1 밖에'),
    (r'(\w+)밖으로', r'\1 밖으로'),
    (r'(\w+)밖은', r'\1 밖은'),
    (r'(\w+)밖도', r'\1 밖도'),
    (r'(\w+)등(?![산록급장불어심래])', r'\1 등'),
    (r'(\w+)뒤(?![로거에])', r'\1 뒤'),
    (r'(\w+)뒤로', r'\1 뒤로'),
    (r'(\w+)뒤에', r'\1 뒤에'),
    (r'(\w+)앞(?![날로서길장문])', r'\1 앞'),
    (r'(\w+)앞으로', r'\1 앞으로'),
    (r'(\w+)앞에', r'\1 앞에'),
    (r'(\w+)안에', r'\1 안에'),
    (r'(\w+)안으로', r'\1 안으로'),
    (r'(\w+)사이에', r'\1 사이에'),
    (r'(\w+)사이의', r'\1 사이의'),
    (r'(\w+)사이에서', r'\1 사이에서'),
    (r'(\w+)때에', r'\1 때에'),
    (r'(\w+)때부터', r'\1 때부터'),
    (r'(\w+)때까지', r'\1 때까지'),
    (r'그때', '그 때'),
    (r'이때', '이 때'),
    (r'그때부터', '그 때부터'),
    (r'그때까지', '그 때까지'),
    (r'그때에', '그 때에'),
    (r'이때에', '이 때에'),
]

QUOTE_RULES = [
    ("\u201c", "\u2018"),
    ("\u201d", "\u2019"),
    ("\u300c", "\u2018"),
    ("\u300d", "\u2019"),
    ("\u300e", "\u2018"),
    ("\u300f", "\u2019"),
]

BOTH_FORMS_DEP_NOUNS = {"줄","대로","상","가운데","밖","안","등","뒤"}

CHUK_NOSPLIT_PREFIXES = (
    "개척", "세척", "척추", "척결", "척도", "척골", "질척", "부척",
    "권척", "곡척", "협척", "률척", "고정척", "진촌퇴척",
    "척박", "간척", "투척",
)

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
}

DDUT_NOSPLIT = {
    "뜻하지", "뜻밖에", "뜻밖의", "뜻밖",
    "본뜻", "원뜻", "참뜻", "속뜻", "첫뜻",
    "큰뜻", "작은뜻", "깊은뜻",
}

MODU_NOSPLIT = {
    "모두", "모두가", "모두를", "모두의", "모두는", "모두도",
}

CHEOK_NOSPLIT = {
    "수척하다", "수척하고", "수척한",
    "간척하다", "간척하고", "간척한",
    "배척하다", "배척하고", "배척한",
    "개척하다", "개척하고", "개척한",
    "질척질척", "질척질척한",
    "부척", "인척", "혈척",
}

def file_hash(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def parse_records(data):
    records = []
    i = 0
    while i < len(data):
        if i + 4 > len(data):
            break
        tag_id = struct.unpack_from('<H', data, i)[0]
        level = struct.unpack_from('<H', data, i + 2)[0]
        if i + 8 > len(data):
            break
        size = struct.unpack_from('<I', data, i + 4)[0]
        header_size = 8
        if size == 0xFFFFFFFF:
            if i + 12 > len(data):
                break
            size = struct.unpack_from('<I', data, i + 8)[0]
            header_size = 12
        payload_start = i + header_size
        payload_end = payload_start + size
        if payload_end > len(data):
            payload = data[payload_start:]
            records.append({"tag_id": tag_id, "level": level, "size": size, "header_size": header_size, "payload": payload})
            break
        payload = data[payload_start:payload_end]
        records.append({"tag_id": tag_id, "level": level, "size": size, "header_size": header_size, "payload": payload})
        i = payload_end
    return records

def rebuild_stream(records):
    buf = bytearray()
    for rec in records:
        buf += struct.pack('<HH', rec["tag_id"], rec["level"])
        if rec["header_size"] == 12:
            buf += struct.pack('<I', 0xFFFFFFFF)
            buf += struct.pack('<I', len(rec["payload"]))
        else:
            buf += struct.pack('<I', len(rec["payload"]))
        buf += rec["payload"]
    return bytes(buf)

def extract_text_from_records(records):
    parts = []
    for rec in records:
        if rec["tag_id"] == 67:
            try:
                t = rec["payload"].decode('utf-16-le', errors='replace')
                parts.append(t)
            except Exception:
                pass
    return ''.join(parts)

def load_china_place_rules():
    rules = []
    if not os.path.exists(RULES_CHINA_PLACE):
        return rules
    with open(RULES_CHINA_PLACE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('→')
            if len(parts) == 2:
                rules.append((parts[0].strip(), parts[1].strip()))
            else:
                parts2 = line.split(' -> ')
                if len(parts2) == 2:
                    rules.append((parts2[0].strip(), parts2[1].strip()))
    return rules

def parse_txt_rules(path):
    rules = []
    if not os.path.exists(path):
        return rules
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('→')
            if len(parts) == 2:
                rules.append((parts[0].strip(), parts[1].strip()))
            else:
                parts2 = line.split(' -> ')
                if len(parts2) == 2:
                    rules.append((parts2[0].strip(), parts2[1].strip()))
    return rules

def parse_regex_rules(path):
    simple = []
    patterns = []
    if not os.path.exists(path):
        return simple, patterns
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('→')
            if len(parts) == 2:
                src = parts[0].strip()
                dst = parts[1].strip()
                try:
                    pat = re.compile(src)
                    if pat.groups > 0:
                        patterns.append((pat, dst, f"regex-group"))
                    else:
                        simple.append((src, dst, "regex-simple"))
                except re.error:
                    simple.append((src, dst, "regex-plain"))
            else:
                parts2 = line.split(' -> ')
                if len(parts2) == 2:
                    simple.append((parts2[0].strip(), parts2[1].strip(), "regex-plain"))
    return simple, patterns

def generate_dynamic_nara_rules(text):
    rules = []
    nara_names = [
        ("당唐","당(唐)"),("송宋","송(宋)"),("명明","명(明)"),("청淸","청(淸)"),
        ("원元","원(元)"),("수隋","수(隋)"),("진秦","진(秦)"),("한漢","한(漢)"),
        ("위魏","위(魏)"),("촉蜀","촉(蜀)"),("오吴","오(吴)"),("진晉","진(晉)"),
        ("동진東晉","동진(東晉)"),("서진西晉","서진(西晉)"),
        ("남송南宋","남송(南宋)"),("북송北宋","북송(北宋)"),
        ("서하西夏","서하(西夏)"),("요遼","요(遼)"),("금金","금(金)"),
    ]
    for cn, kr in nara_names:
        if cn in text:
            cnt = text.count(cn)
            rules.append((cn, kr, "1단계-나라", cnt))
    return rules

def _has_modifier_ending(word, suffix_len):
    stem = word[:-suffix_len]
    if len(stem) < 1:
        return False
    last = stem[-1]
    code = ord(last)
    if 0xAC00 <= code <= 0xD7A3:
        jongseong = (code - 0xAC00) % 28
        if jongseong in (1, 3, 4, 7, 8, 16, 17, 19, 21, 22, 23, 24, 25, 26, 27):
            return True
    if last in ('는','은','을','던','할','한','될','된','갈','볼','알','올','셀','낼','뺄','뗄','뜰','팔','펼','쉴','깔','걸'):
        return True
    return False

def apply_dependent_noun_inspection(text):
    results = {}
    dep_noun_patterns = {
        "것": (r'([가-힣]+것)', GEOT_NOSPLIT, 1, None),
        "수": (r'([가-힣]+수)', SU_NOSPLIT, 1, "modifier_check"),
        "등": (r'([가-힣]{2,6}등)', DEUNG_NOSPLIT, 1, None),
        "번": (r'([가-힣]{2,6}번)', BEON_NOSPLIT, 1, None),
        "때문": (r'([가-힣]{2,6}때문)', TTAE_MUN_NOSPLIT, 2, None),
        "대로": (r'([가-힣]{2,6}대로)', DAERO_NOSPLIT, 2, None),
        "만큼": (r'([가-힣]{2,6}만큼)', MANKEUM_NOSPLIT, 2, None),
        "중": (r'([가-힣]{2,6}중)', JUNG_NOSPLIT, 1, None),
        "이상": (r'([가-힣]{1,6}이상)', ISANG_NOSPLIT, 2, None),
        "이하": (r'([가-힣]{1,6}이하)', IHA_NOSPLIT, 2, None),
        "척": (r'([가-힣]{2,6}척)', CHUK_NOSPLIT, 1, None),
        "상": (r'([가-힣]{2,6}상)', SANG_NOSPLIT, 1, "exclude_isang_iha"),
        "우": (r'([가-힣]{2,6}우)', U_NOSPLIT, 1, None),
        "줄": (r'([가-힣]{2,6}줄)', JUL_NOSPLIT, 1, "modifier_check"),
        "바": (r'([가-힣]{2,6}바)', BA_NOSPLIT, 1, "modifier_check"),
        "터": (r'([가-힣]{2,6}터)', TEO_NOSPLIT, 1, None),
        "채": (r'([가-힣]{2,6}채)', CHAE_NOSPLIT, 1, None),
        "데": (r'([가-힣]{2,6}데)', DE_NOSPLIT, 1, "exclude_gaunde"),
        "뿐": (r'([가-힣]{2,6}뿐)', PPUN_NOSPLIT, 1, None),
        "따위": (r'([가-힣]{2,6}따위)', TTAWI_NOSPLIT, 2, None),
        "사이": (r'([가-힣]{2,6}사이)', SAI_NOSPLIT, 2, None),
        "가운데": (r'([가-힣]{2,6}가운데)', GAUNDE_NOSPLIT, 3, None),
        "밖": (r'([가-힣]{1,6}밖)', BAK_NOSPLIT, 1, None),
        "안": (r'([가-힣]{1,6}안)', AN_NOSPLIT, 1, None),
        "뒤": (r'([가-힣]{1,6}뒤)', DWI_NOSPLIT, 1, None),
    }
    both_forms_results = {}
    for noun, (pat, nosplit, slen, check) in dep_noun_patterns.items():
        pattern = re.compile(pat)
        found = Counter(pattern.findall(text)).most_common(100)
        attached = []
        for word, cnt in found:
            if word == noun:
                continue
            if check == "modifier_check" and not _has_modifier_ending(word, slen):
                continue
            if check == "exclude_isang_iha" and (word.endswith("이상") or word.endswith("이하")):
                continue
            if check == "exclude_gaunde" and word.endswith("가운데"):
                continue
            is_nosplit = nosplit and word in nosplit
            spaced_ver = word[:-slen] + " " + word[-slen:]
            if noun in BOTH_FORMS_DEP_NOUNS:
                attached.append((word, spaced_ver, cnt, is_nosplit))
            else:
                if not is_nosplit:
                    attached.append((word, spaced_ver, cnt))
        if noun in BOTH_FORMS_DEP_NOUNS:
            both_forms_results[noun] = attached
        else:
            results[noun] = attached
    return results, both_forms_results

def apply_text_corrections(text):
    changes = []
    dep_results, both_forms_results = apply_dependent_noun_inspection(text)
    for noun, items in dep_results.items():
        for item in items:
            if len(item) == 3:
                word, spaced, cnt = item
            else:
                word, spaced, cnt, is_ns = item
                if is_ns:
                    continue
            changes.append((word, spaced, f"의존명사-{noun}", cnt))
    for noun, items in both_forms_results.items():
        for item in items:
            if len(item) == 4:
                word, spaced, cnt, is_ns = item
                if is_ns:
                    continue
                changes.append((word, spaced, f"의존명사-{noun}", cnt))
    return changes

def build_all_rules(text, use_regex=True):
    china_rules = load_china_place_rules()
    txt_rules = parse_txt_rules(RULES_DOCUMENTATION)
    text_changes = apply_text_corrections(text)
    dynamic_nara_rules = generate_dynamic_nara_rules(text)

    step1_rules = []
    for orig, repl in china_rules:
        if orig in text:
            cnt = text.count(orig)
            step1_rules.append((orig, repl, "1단계-중한", cnt))

    step2_rules = []
    for src, dst in txt_rules:
        if src not in text:
            continue
        cnt = text.count(src)
        step2_rules.append((src, dst, "2단계-TXT", cnt))

    step_regex = []
    if use_regex:
        regex_simple, regex_patterns = parse_regex_rules(RULES_REGEX)
        for src, dst, comment in regex_simple:
            if src in text:
                cnt = text.count(src)
                step_regex.append((src, dst, f"3단계-REGEX({comment})", cnt))
        for pat, dst, comment in regex_patterns:
            matches = pat.findall(text)
            if matches:
                for m in set(matches):
                    cnt = text.count(m)
                    if cnt > 0:
                        step_regex.append((m, dst.replace('\\1', m) if '\\1' in dst else dst, f"3단계-REGEX-P({comment})", cnt))

    all_rules = step1_rules + dynamic_nara_rules + step2_rules + step_regex + text_changes
    all_rules.sort(key=lambda r: len(r[0]), reverse=True)
    return all_rules, {
        "china": len(step1_rules),
        "dynamic_nara": len(dynamic_nara_rules),
        "txt": len(step2_rules),
        "regex": len(step_regex),
        "dep_noun": len(text_changes),
        "total": len(all_rules),
    }

def process_hwp_binary(src_path, out_path, all_rules, log_fn=None):
    if log_fn is None:
        def log_fn(msg):
            print(msg, flush=True)

    BACKUP_DIR = r"C:\Users\doris\AppData\Local\Temp\hwp_backup"
    os.makedirs(BACKUP_DIR, exist_ok=True)
    backup_name = os.path.basename(src_path).replace('.hwp', f'_bak_{time.strftime("%H%M%S")}.hwp')
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    shutil.copy2(src_path, backup_path)
    log_fn(f"  백업: {backup_path}")

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
            log_fn(f"  [경고] {sn}: 압축해제 실패 - 건너뜀")
            continue

        records = parse_records(dec)
        log_fn(f"\n  {sn}: {len(records)}개 레코드, 압축={len(raw):,}, 해제={len(dec):,}")

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

        log_fn(f"  텍스트 레코드: {text_rec_count}개, 수정: {modified_rec_count}개, 교정: {stream_changes}건")

        if stream_changes > 0:
            new_dec = rebuild_stream(records)
            log_fn(f"  스트림 재구성: {len(dec):,} -> {len(new_dec):,} bytes (+{len(new_dec)-len(dec):,})")

            compressed_ok = False
            for level in [6, 5, 4, 3, 2, 1]:
                co = zlib.compressobj(level=level, method=zlib.DEFLATED, wbits=-15)
                nc = co.compress(new_dec) + co.flush()
                if len(nc) <= len(raw):
                    all_stream_data[sn] = (nc, len(raw))
                    log_fn(f"  압축(level={level}): {len(nc):,} / {len(raw):,} (여유: {len(raw) - len(nc):,})")
                    compressed_ok = True
                    break
                else:
                    log_fn(f"  압축(level={level}): {len(nc):,} > {len(raw):,} (초과, 다음 레벨 시도)")

            if not compressed_ok:
                log_fn(f"  [오류] 압축 불가! 파일이 너무 커짐")
                return None, change_log, total_changes

            verify_data = all_stream_data[sn][0]
            verify_dec = zlib.decompress(verify_data, -15)
            verify_records = parse_records(verify_dec)
            verify_text = extract_text_from_records(verify_records)
            log_fn(f"  검증: OK 압축해제 일치 (레코드={len(verify_records)}, 텍스트={len(verify_text):,}자)")
            modified_streams.append(sn)
        else:
            log_fn(f"  변경 없음")

    if not modified_streams:
        log_fn(f"\n  변경된 스트림 없음")
        return out_path, change_log, 0

    OUT_TMP = out_path.replace('.hwp', f'_work_{time.strftime("%H%M%S")}_{os.getpid()}.bin')
    shutil.copy2(src_path, OUT_TMP)
    os.chmod(OUT_TMP, stat.S_IWRITE | stat.S_IREAD)
    log_fn(f"  작업본 복사 완료: {OUT_TMP}")

    ole_info = olefile.OleFileIO(src_path, write_mode=False)
    sector_size = ole_info.sector_size

    for sn in modified_streams:
        compressed_data, original_stream_size = all_stream_data[sn]
        sp = sn.split('/')
        sid = ole_info._find(sp)
        entry = ole_info.direntries[sid]
        stream_size = entry.size
        start_sector = entry.isectStart

        log_fn(f"  스트림: {sn}, size={stream_size:,}, start_sector={start_sector}")

        with open(OUT_TMP, 'r+b') as f:
            header = f.read(512)
            num_fat_sectors = struct.unpack_from('<I', header, 44)[0]
            first_dir_sect = struct.unpack_from('<I', header, 48)[0]

            difat = []
            for i in range(109):
                s = struct.unpack_from('<I', header, 76 + i * 4)[0]
                if s != 0xFFFFFFFE and s != 0xFFFFFFFF:
                    difat.append(s)

            fat = []
            for fs in difat[:num_fat_sectors]:
                f.seek(512 + fs * sector_size)
                for _ in range(sector_size // 4):
                    fat.append(struct.unpack('<I', f.read(4))[0])

            chain = []
            cur = start_sector
            while cur != 0xFFFFFFFE and cur != 0xFFFFFFFF and cur < len(fat):
                chain.append(cur)
                cur = fat[cur]
                if len(chain) > 10000:
                    break

            data_to_write = compressed_data
            for idx, sect in enumerate(chain):
                offset = 512 + sect * sector_size
                f.seek(offset)
                chunk_size = min(sector_size, len(data_to_write) - idx * sector_size)
                if chunk_size <= 0:
                    break
                chunk = data_to_write[idx * sector_size:idx * sector_size + chunk_size]
                if len(chunk) < sector_size:
                    existing = f.read(sector_size)
                    f.seek(offset)
                    chunk = chunk + existing[len(chunk):]
                f.seek(offset)
                f.write(chunk)

            if len(compressed_data) != stream_size:
                dir_start_sect = first_dir_sect
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
                    dir_entry_offset = 512 + dir_sect * sector_size + entry_idx * 128

                    f.seek(dir_entry_offset + 120)
                    old_size_bytes = f.read(4)
                    old_size = struct.unpack('<I', old_size_bytes)[0]

                    f.seek(dir_entry_offset + 120)
                    f.write(struct.pack('<I', len(compressed_data)))
                    f.seek(dir_entry_offset + 124)
                    f.write(struct.pack('<I', 0))

                    log_fn(f"  디렉토리 엔트리 size 업데이트: {old_size:,} -> {len(compressed_data):,}")

    ole_info.close()

    if os.path.exists(out_path):
        os.chmod(out_path, stat.S_IWRITE | stat.S_IREAD)
        os.remove(out_path)
    os.rename(OUT_TMP, out_path)
    log_fn(f"\n  출력 파일: {out_path}")
    log_fn(f"  출력 크기: {os.path.getsize(out_path):,} bytes")
    log_fn(f"  총 교정: {total_changes}건")

    return out_path, change_log, total_changes


class SpacingCorrector:
    def __init__(self):
        self.changelog = []
        self._both_forms = BOTH_FORMS_DEP_NOUNS

    def _log(self, heading, before, after, rule, reason):
        self.changelog.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'heading': heading,
            'before': before,
            'after': after,
            'rule': rule,
            'reason': reason,
        })

    def correct_spacing(self, text, heading=''):
        result = text
        dep_results, both_forms = apply_dependent_noun_inspection(text)
        offset = 0
        for noun, items in dep_results.items():
            for item in items:
                if len(item) == 3:
                    word, spaced, cnt = item
                elif len(item) == 4:
                    word, spaced, cnt, is_ns = item
                    if is_ns:
                        continue
                else:
                    continue
                if word in result:
                    before = word
                    after = spaced
                    result = result.replace(before, after)
                    cnt_actual = text.count(before)
                    if cnt_actual > 0:
                        self._log(heading, before, after, f'dep_noun_{noun}',
                                  f'의존명사 "{noun}"는 앞말에서 띄어 씀')
        for noun, items in both_forms.items():
            for item in items:
                if len(item) == 4:
                    word, spaced, cnt, is_ns = item
                    if is_ns:
                        continue
                else:
                    continue
                if word in result:
                    before = word
                    after = spaced
                    result = result.replace(before, after)
                    cnt_actual = text.count(before)
                    if cnt_actual > 0:
                        self._log(heading, before, after, f'dep_noun_{noun}',
                                  f'의존명사 "{noun}"는 앞말에서 띄어 씀')
        return result

    def get_changelog(self):
        return self.changelog

    def get_stats(self):
        by_rule = {}
        total = 0
        for entry in self.changelog:
            rule = entry['rule']
            by_rule[rule] = by_rule.get(rule, 0) + 1
            total += 1
        return {'total_changes': total, 'by_rule': by_rule}
