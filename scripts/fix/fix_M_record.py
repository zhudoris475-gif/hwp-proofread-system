import sys, os, time, re, struct, zlib, shutil, hashlib, stat
sys.path.insert(0, r"C:\AMD\AJ\hwp_proofreading_package")
import olefile
from collections import Counter

SRC = r"C:\Users\doris\Desktop\【大中朝 17】M 1959-2093--135--20240920.hwp"
OUT = r"c:\Users\doris\.agent-skills\M_output.hwp"
OUT_TMP = r"c:\Users\doris\.agent-skills\M_work_" + str(__import__('uuid').uuid4().hex[:8]) + ".bin"
BACKUP_DIR = r"C:\Users\doris\AppData\Local\Temp\hwp_backup"
LOG_DIR = r"C:\Users\doris\AppData\Local\Temp\hwp_logs"
RULES_FILE = r"C:\AMD\AJ\hwp_proofreading_package\rules_documentation.txt"
REGEX_RULES_FILE = r"C:\AMD\AJ\hwp_proofreading_package\rules_regex.txt"

GEOT_NOSPLIT = {"이것", "그것", "저것", "이것저것", "그것저것"}
SU_NOSPLIT = {"장수","교수","척수","우수","선수","준수","주파수","정수","함수","감수","인수","순수","특수","기수","접수","군수","죄수","다수","가수","수수","보수","점수","완수","지수","호수","분수","박수","불수","할수록","매수","차수","상수","변수","소수","횟수","역수","약수","공수","출수","생수","화수","해수","강수","풍수","수술","수도","수원","수산","수입","수출","수면","수련","수렵","수호","수비","수색","수송","수확","수집","수여","수행","수반","수습","수용","수치","수필","수분","수명","수단","수리","치수","속임수","복수","흡수","급수","한수","운수","어수","계수","도수","액수","건수","명수","회수","층수","권수","징수","산수","홀수","단수","밀수","검수","입수","포수","묘수","암수","추수","낙수","유수","조수","배수","누수","탈수","양수","음수","총수","평균수","최대수","최소수","합계수","누계수","증감수","옥수수","기본주파수","교통운수","머리수","파수","고수","목수","방수","부수","금수","취수","거수","무수","근수","독수","대수","압수","몰수","담수","혼수","홍수","전수","령수","철수","국수","적수","야수","엄수","차단주파수","실수","침수","헛수","간수","충수","저수","락수","랭수","어쩔수","얻을수","볼수","떨어질수","할수","알수","이십팔수","말수","골수","필수","원심탈수","문화재밀수","률수","예술수","생활수","지방일수","찰수","연수","진수","경수","뇌수","평수","광수","난수","세수","의수"}
TTAWI_NOSPLIT = {"따위","따위의","따위로","따위를","따위는","따위가","따위도"}
SAI_NOSPLIT = {"강사이","수사이","두사이","그사이","이사이","중간사이"}
PPUN_NOSPLIT = {"뿐만","뿐이다","뿐이었다","뿐이고","뿐이며","뿐이니","사뿐사뿐","사뿐"}
CHUK_NOSPLIT_PREFIXES = ("개척","세척","척추","척결","척도","척골","질척","부척","권척","곡척","협척","률척","고정척","진촌퇴척","척박","간척","투척")
CHUK_NOSPLIT = {"배척하다","배척하고","무척","지척","인척","세척","개척하다","인기척","척하다","척하고","척추","척수","척도","진척하다","간척","수척","기척","친한척","사람인척","아는척하면"}
ISANG_NOSPLIT = {"이상","이상의","이상으로","이상하다","이상하게","이상한","정상이상","비정상이상"}
MIT_NOSPLIT = {"밑","밑바닥","밑면","밑부분","밑천"}
DEUNG_NOSPLIT = {"균등","고등","강등","상등","대등","초등","일등","발등","갈등","평등","동등","항등","비등","불평등","등등","등산","등록","등장","등급","등불","등대","가로등","형광등","섬광등","전조등","경고등","경광등","안전등","착륙등","착신등","진입등","탁상등","채색등","책등","칼등","등뼈","등받이","주민등록","기회균등","감수분렬부등","신호등","손전등","전등","곱사등","호적등","자원평등","교통신호등","립식전등","련결등","풍력등","초불등","신용등","벌등","렬등","귓등","뢰공등","랭음극형광등","열등","산등","홍등","세등","중등","이등","려객등","록색등","세움등","키큰등","급등","등불","등기","등교","등반","등신","휴대등","야간등","실내등","복도등","계단등","비상등","유도등","출입등","통로등"}
TTE_NOSPLIT = {"제때","그때","이때","한때","때때로","아무때","때때","명절때","점심때","저녁때","병때","본때"}
TTAE_MUN_NOSPLIT = {"때문","때문에","때문이다"}
BEON_NOSPLIT = {"이번","한번","두번","세번","네번","여러번","몇번","매번","첫번","한꺼번","두리번","단번","백번","여섯번","일곱번","여덟번","아홉번","두어번","빈번","농번","교번","자동번","전화번","기계번","비밀번","일련번","부품번","종자번","가축번","성장번","경찰번","천둥번","근친번","금번","대번","해번","절번","홀수번","순번","류번","원자번","발신번","당번","련속번","천번","지난번","원소번","전번","자유번","추첨당첨번","륜번","타번","리번","오즈번","번쩍번","번번이","번쩍번쩍","번거롭다","청소당번","야간당번","경비당번"}
DE_NOSPLIT = {"가운데","한가운데","그가운데","포름알데","놀포름알데","메타알데","아쎄트알데","알데","데굴데","번데","한데","아데","데려","데리고","데려가","데려오","데릴","앙데","지데","놀이데","춤데","수데","김데","빛데","밤데","길데","밭데","어데","여데","제데","참데","집데","껍데기","껍데","껍질데","사람가운데","것가운데","곳가운데","땅가운데","집가운데","물가운데","산가운데","길가운데","또래가운데","세계가운데","국민소득가운데","데구르르","데굴데굴","데미지","데시벨","데탕트","데투라","데우다","데워","몰리브데","몰리브덴","데면데","데면데기","솔데","콜데","필데","질데","빌데","날데","만데","탈데","걸데","올데","굴데","불데","쏠데","쉴데","툴데","홀데","꿀데","둘데","썰데","알데","찰데","필데","헐데"}
DAERO_NOSPLIT = {"뜻대로","마음대로","그대로","이대로","저대로","자대로","제멋대로","맘대로","임의대로","자연대로","이대로라도","그대로라도","있는대로","되는대로","하는대로","본대로","들은대로","아는대로","가는대로","절대로","제대로","대대로","영대로","선대로","사실대로","순서대로","규정대로","요구대로","약속대로","계획대로","예상대로","생각대로","소원대로","명령대로","원래대로","그대로라도","있는그대로"}
MANKEUM_NOSPLIT = {"그만큼","이만큼","저만큼","만큼"}
JUL_NOSPLIT = {"줄밖","줄","힘줄","바줄","새끼줄","기계줄","청줄","산줄","드레박줄","물줄","소줄","동줄","줄다","줄기","줄줄이","생줄","명줄","목줄","핏줄","신줄","실줄","어줄","당줄","줄줄","고줄","대줄","쇠줄","전줄","연줄","줄당","줄자","줄녀석","노끈줄","밧줄","끈줄","철줄","나일론줄","고무줄","전깃줄","철사줄","끌줄","감줄","매듭줄","낚시줄","안전줄","구명줄","전화줄","올줄","굵은줄","가는줄","긴줄","짧은줄","거미줄","덩굴줄","두레박줄","오라줄","계선줄","다듬질줄","빨래줄","넋줄","밧줄","동아줄","줄기차다","줄기","줄거리","줄임말","줄임","줄알다","줄모르다","줄서다","줄잇다","갈대줄","이야기줄","뾰족평줄","송곳줄","평줄","줄발","줄당기다","줄조임","줄타기","줄임꼴","줄간격","줄바꿈","줄세우기","줄거리","줄임표","피줄","먹줄","당김줄","구린줄","어쩔줄","묶음쇠줄","견인바줄","쇠바줄","부끄러운줄","도와줄","붉은줄","검은줄","련줄","알줄","볼줄","할줄","갈줄","줄을","줄의","줄이","줄은","줄에","피줄을","피줄의","먹줄을","먹줄의","구리줄","나무줄","시계줄","버팀줄","포승줄","닻줄","불줄","태줄","비줄","이음줄","해줄","미역줄","낳은줄","싫은줄","않은줄"}
TEO_NOSPLIT = {"콤퓨터","모니터","인터","인터넷","프린터","센터","터미널","허터","필터","액터","팩터","벡터","렉터","오래전부터","부터","로부터","에서부터","으로부터","두터","흉터","엉터","엉터리","상처터","터전","터밭","터끌","터럭","터진","터지다","터뜨리다","터득","터득하다","터치","터치하다","까지","까지도","예로부터","옛날부터","이전부터","싸움터","전쟁터","포스터","처음부터","예전부터","어릴적부터","올해부터","언제부터","인터페이스","인터럽트","마스터","미스터","시스터","레스터","오스터","윈스터","로스터","부스터","체스터","글로스터","레스터","워스터","체스터필드","오체스터","멘터","센터","도터","벤처","런처","캐처","워처","리처","피처","크리처","프리처","스케처","스케쳐","스위처","위처","피쳐","레쳐","프로쳐","피쳐","런쳐","캐쳐","멘쳐","도쳐","벤쳐","일부터","후부터","첫날부터","어려서부터","이로부터","내일부터","오늘부터","저녁부터","아침부터","작년부터","올해부터","내년부터","작때부터","그때부터","지금부터","언제부터","여기부터","거기부터","어디부터","어디서부터","머리로부터","발부터","손부터","눈부터","입부터"}
CHAE_NOSPLIT = {"색채","외채","공채","미지급채","납채","정채","국채","사채","다문채","총채","끌채","가로채","낚아채","눈치채","국가경제건설공채","건설공채","경제건설공채","채권","채무","채석","채소","채집","채용","채택","채점","채색","채널","채팅","채우다","채워","채운","낚아채다","가로채다","눈치채다","송두리채","뻗은채","앉은채","누운채","서있는채","사랑채","야채","유채","안채","풍채","전채","통채","털채","부채","보채다","뿌리채","막힌채"}
BA_NOSPLIT = {"바다","바람","바늘","바깥","바구니","바닥","바탕","바위","바이러스","바이올린","바코드","바람직","바로","바르다","바꾸다","바라다","바치다","곧바로","똑바로","올바르다","옳바르다"}
IHA_NOSPLIT = {"가까이하다","기이하다","되풀이하다","해이하다","같이하다","괴이하다","특이하다","용이하다","부득이하다","맞이하다","수준이하","영도이하","상이하다","되풀이","고기잡이","기이","용이","가까이","해이","괴이"}
JUNG_NOSPLIT = {"신중","대중","이중","관중","귀중","공중","랑중","집중","소중","존중","도중","진중","정중","엄중","명중","적중","궁중","하중","시중","군중","장중","출중","과중","기중","일반대중","한밤중","그중","나중","산중","밤중","중간","중심","중앙","중요","중복","중단","중지","중계","중량","중소","중순","중세","중기","중류","중합","중화","중독","중상","중년","중국","중부","중층","중형","비중","민중","수중","우중","둔중"}
SANG_NOSPLIT = {"세상","항상","현상","리상","이상","예상","사상","로상","조상","책상","증상","감상","륙상","고상","진상","대상","린상","정상","수상","기상","해상","손상","호상","인상","앙상","지상","추상","중상","가상","화상","령상","살상","일상","관상","상하","상대","상황","상태","상식","상류","상처","상실","상인","상업","상점","상품","상공","무역대상","노벨물리학상","노벨화학상","노벨문학상","노벨평화상","노벨경제학상","노벨생리의학상","미곡상","포목상","철물상","잡화상","약상","식료품상","건재상","곡물상","목재상","연탄상","석탄상","어물상","과일상","야채상","고기상","가구상","도자기상","의류상","직물상","사상","사불상","인간세상","명실상","전설상","외관상","장부상","모친상","유명상","민사상","국가지상","벌사상","형사상","행정상","법률상","실질상","형식상","이론상","실제상","관념상","개념상","사실상","원칙상","격식상","문법상","논리상","도덕상","윤리상","예의상","체면상","겉보기상","겉모양상","외모상","외형상","내용상","내면상","내심상","본심상","진심상","표면상","이면상","당면상","공간상","시간상","지역상","지방상","국가상","국제상","세계상","지구상","우주상","자연상","환경상","생태상","경제상","산업상","농업상","공업상","상업상","무역상","금융상","재정상","사회상","문화상","정치상","군사상","역사상","지리상","기후상","날씨상","계절상","심리상","정신상","신체상","건강상","영양상","의학상","병리상","생리상","해부상","조직상","구조상","기능상","성능상","품질상","규격상","크기상","모양상","색상","색채상","음향상","소리상","온도상","습도상","압력상","속도상","무게상","농도상","밀도상","강도상","경도상","점도상","산도상","비중상","비율상","비례상","균형상","대칭상","조화상","통일상","일치상","대조상","비교상","차이상","차별상","구별상","분류상","배열상","배치상","순서상","순위상","등급상","수준상","정도상","분량상","수량상","규모상","범위상","영역상","면적상","넓이상","길이상","높이상","깊이상","거리상","위치상","방향상","각도상","방위상","경도상","위도상","고도상","표고상","해발상","해면상","지형상","지세상","지물상","지질상","토질상","토양상","수질상","공기상","대기상","기상상","천기상","천문상","우주상","항성상","행성상","위성상","별자리상","은하상","성운상","성단상","태양상","달상","지구상","지상","천상","해상","공상","우주상","사마상","범상","비상","초상","급상","승상","재상","각상","공상","명상","영상","조상","진상","친상","향상","인상","결상","과상","규상","기상","단상","도상","독상","만상","방상","복상","부상","분상","빈상","사상","산상","선상","성상","소상","숙상","승상","시상","신상","실상","역상","연상","영상","오상","운상","원상","위상","유상","은상","의상","이상","인상","임상","자상","장상","재상","정상","종상","중상","진상","차상","참상","천상","총상","추상","칙상","태상","통상","판상","평상","풍상","학상","향상","회상","효상","황사현상","흙비황사현상","석회상","성장상","우회상","특정상","판매상","인지상","엽맥상","시맥상","만원상","암흑상","분포상","명의상","외국상","력사상","주의적정치사상","현상학","현상관","현상론","사상사","사상가","사상적","석회상","성장상","우회상","특정상","판매상","인지상","엽맥상","시맥상","만원상","암흑상","분포상","명의상","외국상","력사상","주의적정치사상","백상","대리상","영업상","경영상","재무상","회계상","세무상","법률상","노동상","고용상","임금상","복지상","안전상","보건상","위생상","환경상","공해상","오염상","생태상","자연상","기후상","날씨상","기상상","지진상","화산상","해일상","태풍상","홍수상","가뭄상","폭우상","폭설상","폭풍상","낙뢰상","우박상","안개상","서리상","이슬상","습기상","건조상","습윤상","한랭상","온난상","열대상","냉대상","온대상","아열대상","한대상","건조상","반건조상","다습상","고온상","저온상","상온상","극지상","적도상","적도상","고위도상","저위도상","중위도상","극권상","아극권상","온대권상","아열대권상","열대권상","적도권상"}
U_NOSPLIT = {"매우","경우","좌우","겨우","폭우","강우","전우","대우","아우","새우","무우","배우","태우","채우","키우","싸우","세우","피우","뉘우","도우","메우","씌우","우리","우주","우수","우월","우연","우편","우호","우량","우세","우습다","어려우","쉬우","폭풍우","아름다우","우의","우에","우로","우에서","명배우","보리새우","닭새우","쑤저우","항저우","광저우","해치우","내세우","걷어치우","덮어씌우","체면세우","일반우","아래우","막역지우","마천우","성벽우","두루마기우","먼터거우","마티우","우산","우비","우체국","우표","우승","우물","우두머리","우레","우람하다","우직하다","우악스럽다","우쭐하다","우쭐대다","우매하다","우둔하다","우직스럽다","우아하다","우수하다","우월하다","우량하다","우호적","우연하다","우연히","우발","우발적","우발사건","우뚝하다","우두커니","우쩍","우뚝","우습게","우스꽝스럽다","우스운","우매","우둔","우악","우직","우람","우아","우발적으로","풍우","만성풍우","무대우","참새우","젓새우","영화배우","구이저우","마오저우","치켜세우","시새우","가벼우","아이브라우","형아우","실겨우","창문우","디딤돌우","갈우","말우","받우","벌우","살우","솔우","씨우","양우","열우","종우","주우","철우","큰우","황우","흑우","백우","적우","청우","녹우","남우","여우","노우","소우","고우","명우","인우","선우","의우","우수리","다우","라우","바우","사우","아우","자우","카우","타우","파우","하우","허우","후우","그루우","나루우","마루우","부루우","수우","시우","아우우","오우","우우","조우","주우","참우","해우","화우","희우"}
HA_NOSPLIT = {"비유하다","속하다","형용하다","못하다","말하다","청렴하다","사용하다","일하다","처리하다","대하다","다하다","련결하다","리용하다","리해하다","생각하다","좋아하다","그리워하다","정리하다","발생하다","계속하다","당하다","조심하다","진행하다","실행하다","하다","하고","하여","해서","하였다","한다","한","하기","함","할","했","하는"}
GAT_NOSPLIT = {"똑같다","똑같이","똑같은","마찬가지로","같이","같은","같다"}
GO_NOSPLIT = {"고하다","고하고","고하여","고해서","고한","고가다","고간다","고가고","고있다","고있고","고있는"}


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
        records.append({"tag_id": tag_id, "level": level, "size": size, "header_size": header_size, "payload": payload})
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


def parse_regex_rules(filepath):
    simple_rules = []
    pattern_rules = []
    if not os.path.exists(filepath):
        return simple_rules, pattern_rules
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '->' not in line:
                continue
            parts = line.split('->')
            if len(parts) != 2:
                continue
            src = parts[0].strip().strip("'\"")
            dst = parts[1].strip().split('#')[0].strip().strip("'\"")
            comment = ''
            if '#' in parts[1]:
                comment = parts[1].split('#', 1)[1].strip()
            if not src or not dst:
                continue
            if re.search(r'[\\^$.*+?{}()|[\]]', src):
                try:
                    pat = re.compile(src)
                    pattern_rules.append((pat, dst, comment))
                except re.error:
                    continue
            else:
                simple_rules.append((src, dst, comment))
    return simple_rules, pattern_rules


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

    for cat, nosplit, slen in [("따위", TTAWI_NOSPLIT, 2), ("사이", SAI_NOSPLIT, 2), ("뿐", PPUN_NOSPLIT, 1)]:
        pattern = re.compile(r'([가-힣]+' + cat + r')')
        for word, cnt in Counter(pattern.findall(text)).most_common(500):
            if word in nosplit or word == cat:
                continue
            add(word, f"{word[:-slen]} {cat}", cat)

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
        ("이상", ISANG_NOSPLIT, 2), ("이하", IHA_NOSPLIT, 2), ("밑", MIT_NOSPLIT, 1),
        ("등", DEUNG_NOSPLIT, 1), ("때", TTE_NOSPLIT, 1), ("때문", TTAE_MUN_NOSPLIT, 2),
        ("번", BEON_NOSPLIT, 1), ("데", DE_NOSPLIT, 1), ("대로", DAERO_NOSPLIT, 2),
        ("만큼", MANKEUM_NOSPLIT, 2), ("중", JUNG_NOSPLIT, 1),
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

    DEUT_NOSPLIT = {"반듯", "반듯이", "빠듯", "빠듯이", "여느듯", "그듯", "가득듯"}
    CHARYE_NOSPLIT = {"차례차례", "차례대로", "이차례", "삼차례", "첫차례"}
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


def apply_dependent_noun_inspection(text):
    results = {}

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
        if last in ('는', '은', '을', '던', '할', '한', '될', '된', '갈', '볼', '알', '올', '셀', '낼', '뺄', '뗄', '뜰', '팔', '펼', '쉴', '깔', '걸', '술', '물', '둘', '셋', '넷', '몇', '얼', '얻', '짓', '잃', '닿', '옳', '옰', '얇', '밟', '넓', '외', '둘', '셋', '이', '그', '저', '어', '무', '어느', '아무', '어떤'):
            return True
        return False

    def _is_verb_stem_ending(word, suffix_len):
        stem = word[:-suffix_len]
        if len(stem) < 1:
            return False
        last = stem[-1]
        code = ord(last)
        if 0xAC00 <= code <= 0xD7A3:
            jongseong = (code - 0xAC00) % 28
            if jongseong == 0:
                return True
        return False

    JI_NOSPLIT_EXTRA = {"아버지","어머니","두루마기","바가지","나무가지","여러가지","두가지","세가지","네가지","오가지","판타지","허둥지","리사지","막역지","사각지","가지","가지각색","가지런히","가지다","가지러","가지런","가지치기","가지관","가지점","허우적","허우적대다","허우적거리다","주춤지","주춤하다","머뭇지","머뭇거리다","우물쭈물지","우물쭈물하다","사라지","사라지다","사라져","사라진","사라질","사라짐","사라져서","사라졌","보이지","보이지다","보이지않","보이지않다","가리지","가리지다","가리지않","가리지않다","없어지","없어지다","없어져","없어진","없어질","없어짐","이루지","이루지다","이루지않","이루지못","이어지","이어지다","이어져","이어진","이어질","분명하지","분명하지않","분명하지못","말하지","말하지않","말하지못","느끼지","느끼지않","느끼지못","빨개지","빨개지다","빨개져","밝아지","밝아지다","밝아져","무서워하지","무서워하지않","생각지","생각지않","생각지못","깨닫지","깨닫지못","깨닫지않","알지","알지못","알지않","보지","보지못","보지않","듣지","듣지못","듣지않","하지","하지않","하지못","가지","가지않","가지못","오지","오지않","오지못","되지","되지않","되지못","있지","있지않","있지못","없지","없지않","없지못","죽지","죽지않","죽지못","살지","살지않","살지못","달리지","달리지않","달리지못","움직이지","움직이지않","움직이지못","변하지","변하지않","변하지못","떠나지","떠나지않","떠나지못","버리지","버리지않","버리지못","잊지","잊지않","잊지못","포기하지","포기하지않","포기하지못","늦지","늦지않","늦지않다","적지","적지않","적지않다","크지","크지않","크지않다","작지","작지않","작지않다","많지","많지않","많지않다","좋지","좋지않","좋지않다","나쁘지","나쁘지않","나쁘지않다","어렵지","어렵지않","어렵지않다","쉽지","쉽지않","쉽지않다","길지","길지않","길지않다","짧지","짧지않","짧지않다","높지","높지않","높지않다","낮지","낮지않","낮지않다","넓지","넓지않","넓지않다","좁지","좁지않","좁지않다","강하지","강하지않","강하지않다","약하지","약하지않","약하지않다","빠르지","빠르지않","빠르지않다","느리지","느리지않","느리지않다","덥지","덥지않","덥지않다","춥지","춥지않","춥지않다","맑지","맑지않","맑지않다","흐리지","흐리지않","흐리지않다","새롭지","새롭지않","새롭지않다","오래지","오래지않","오래지않다","일찍지","일찍지않","일찍지않다","늦지","늦지않","늦지않다","다르지","다르지않","다르지않다","같지","같지않","같지않다","틀리지","틀리지않","틀리지않다","부족하지","부족하지않","부족하지않다","필요하지","필요하지않","필요하지않다","중요하지","중요하지않","중요하지않다","가능하지","가능하지않","가능하지않다","충분하지","충분하지않","충분하지않다","적당하지","적당하지않","적당하지않다","적절하지","적절하지않","적절하지않다","정확하지","정확하지않","정확하지않다","분명하지","분명하지않","분명하지않다","명확하지","명확하지않","명확하지않다","확실하지","확실하지않","확실하지않다","안전하지","안전하지않","안전하지않다","위험하지","위험하지않","위험하지않다","복잡하지","복잡하지않","복잡하지않다","단순하지","단순하지않","단순하지않다","쉽지","쉽지않","쉽지않다","어렵지","어렵지않","어렵지않다","편하지","편하지않","편하지않다","불편하지","불편하지않","불편하지않다","행복하지","행복하지않","행복하지않다","슬프지","슬프지않","슬프지않다","기쁘지","기쁘지않","기쁘지않다","우습지","우습지않","우습지않다","아프지","아프지않","아프지않다","맵지","맵지않","맵지않다","달지","달지않","달지않다","짜지","짜지않","짜지않다","시지","시지않","시지않다","쓰지","쓰지않","쓰지않다","익지","익지않","익지않다","생지","생지않","생지않다","국가지","산가지","오래가지","닻가지","밑가지","윗가지","앞가지","뒷가지","옆가지","굵은가지","가는가지","긴가지","짧은가지","마른가지","푸른가지","꽃가지","열매가지","잎가지","뿌리가지","줄기가지","돌가지","모래가지","흙가지","물가지","불가지","바람가지","구름가지","비가지","눈가지","얼음가지","안개가지","이슬가지","서리가지","우박가지","번개가지","천둥가지","햇빛가지","달빛가지","별빛가지","그림자가지","무지개가지","아침가지","저녁가지","낮가지","밤가지","봄가지","여름가지","가을가지","겨울가지","목적지","관광지","거주지","출생지","산지","원산지","생산지","발상지","발상지","근거지","주거지","요충지","전략지","분지","평야지","해안지","내륙지","고산지","산간지","농촌지","도시지","공업지","상업지","주택지","상업지","공업지","관광지","휴양지","위락지","유적지","사적지","유적지","명승지","절터지","널판지","합판지","골판지","양철지","은박지","주석지","도화지","백지","장미지","도화지","색도화지","골판지","양면지","흑백지","칼라지","인쇄지","신문지","잡지","간행지","출판지","기관지","당기관지","학교기관지","어루만지","어루만지다","어루만져","어루만진","어루만질","어루만짐","반지","금반지","은반지","다이아반지","보석반지","결혼반지","약혼반지","가락지","돌가락지","은가락지","쇠가락지","기준지","기준치","표준지","표준치","평균지","평균치","중간지","중간치","한계지","한계치","임계지","임계치","최대지","최대치","최소지","최소치","최고지","최고치","최저지","최저치","상한지","상한치","하한지","하한치","적정지","적정치","적합지","적합치","부적합지","부적합치","허용지","허용치","규정지","규정치","지정지","지정치","설정지","설정치","측정지","측정치","관측지","관측치","예상지","예상치","예측지","예측치","실적지","실적치","성과지","성과치","실적지","실적치","지표지","지수치","비율지","비율치","비중지","비중치","비례지","비례치","비율지","비율치","백분율지","백분율치","천분율지","천분율치","만분율지","만분율치","지질","지층","지대","지맥","지형","지세","지리","지도","지하","지상","지표","지면","지점","지역","지구","지방","지대","지위","지지","지식","지능","지혜","지령","지시","지배","지도","지향","지침","지연","지속","지진","지평","지평선","지구력","지도자","지배력","지적","지리적","지역적","지방적","지구적","지속적","지연적","지향적","지배적","지도적","지침적"}

    CONNECTIVE_DE = re.compile(r'[가-힣]+(는데|은데|던데|ㄴ데|는 데|은 데|던 데)$')
    CONNECTIVE_JI = re.compile(r'[가-힣]+(는지|은지|던지|ㄴ지|려지|려는지|려는지라도|려나|는지라도|을지|ㄹ지)$')
    PARTICLE_TEO = re.compile(r'[가-힣]+부터$')

    def _is_connective_ending_de(word):
        if CONNECTIVE_DE.match(word):
            return True
        stem = word[:-1]
        if len(stem) >= 1:
            last = stem[-1]
            code = ord(last)
            if 0xAC00 <= code <= 0xD7A3:
                jongseong = (code - 0xAC00) % 28
                if jongseong == 0 and word.endswith("데"):
                    return True
        return False

    def _is_connective_ending_ji(word):
        if CONNECTIVE_JI.match(word):
            return True
        return False

    def _is_particle_teo(word):
        if PARTICLE_TEO.match(word):
            return True
        return False

    dep_noun_patterns = {
        "것": (r'([가-힣]+것)', GEOT_NOSPLIT, 1, None),
        "수": (r'([가-힣]+수)', SU_NOSPLIT, 1, "modifier_check"),
        "지": (r'([가-힣]{2,6}지)', JI_NOSPLIT_EXTRA, 1, "modifier_check"),
        "듯": (r'([가-힣]{2,6}듯)', {"반듯", "반듯이", "빠듯", "빠듯이", "여느듯", "그듯", "가득듯"}, 1, None),
        "데": (r'([가-힣]{2,6}데)', DE_NOSPLIT, 1, None),
        "바": (r'([가-힣]{2,6}바)', BA_NOSPLIT, 1, "modifier_check"),
        "줄": (r'([가-힣]{2,6}줄)', JUL_NOSPLIT, 1, "modifier_check"),
        "터": (r'([가-힣]{2,6}터)', TEO_NOSPLIT, 1, None),
        "채": (r'([가-힣]{2,6}채)', CHAE_NOSPLIT, 1, None),
        "뿐": (r'([가-힣]{2,6}뿐)', PPUN_NOSPLIT, 1, None),
        "때문": (r'([가-힣]{2,6}때문)', TTAE_MUN_NOSPLIT, 2, None),
        "대로": (r'([가-힣]{2,6}대로)', DAERO_NOSPLIT, 2, None),
        "만큼": (r'([가-힣]{2,6}만큼)', MANKEUM_NOSPLIT, 2, None),
        "차례": (r'([가-힣]{2,6}차례)', {"차례차례", "차례대로"}, 2, None),
        "무렵": (r'([가-힣]{2,6}무렵)', None, 2, None),
        "사이": (r'([가-힣]{2,6}사이)', SAI_NOSPLIT, 2, None),
        "따위": (r'([가-힣]{2,6}따위)', TTAWI_NOSPLIT, 2, None),
        "등": (r'([가-힣]{2,6}등)', DEUNG_NOSPLIT, 1, None),
        "번": (r'([가-힣]{2,6}번)', BEON_NOSPLIT, 1, None),
        "중": (r'([가-힣]{2,6}중)', JUNG_NOSPLIT, 1, None),
        "이상": (r'([가-힣]{2,6}이상)', ISANG_NOSPLIT, 2, None),
        "이하": (r'([가-힣]{2,6}이하)', IHA_NOSPLIT, 2, None),
        "척": (r'([가-힣]{2,6}척)', CHUK_NOSPLIT, 1, None),
        "상": (r'([가-힣]{2,6}상)', SANG_NOSPLIT, 1, None),
        "우": (r'([가-힣]{2,6}우)', U_NOSPLIT, 1, None),
    }

    for noun, (pat, nosplit, slen, check) in dep_noun_patterns.items():
        pattern = re.compile(pat)
        found = Counter(pattern.findall(text)).most_common(100)
        attached = []
        for word, cnt in found:
            if nosplit and word in nosplit:
                continue
            if word == noun:
                continue
            if check == "modifier_check" and not _has_modifier_ending(word, slen):
                continue
            if noun == "지" and (_is_verb_stem_ending(word, slen) or _is_connective_ending_ji(word)):
                continue
            if noun == "데" and _is_connective_ending_de(word):
                continue
            if noun == "터" and _is_particle_teo(word):
                continue
            spaced_ver = word[:-slen] + " " + word[-slen:]
            attached.append((word, spaced_ver, cnt))
        results[noun] = attached
    return results


def main():
    log_lines = []

    def log(msg):
        print(msg, flush=True)
        log_lines.append(msg)

    log(f"{'=' * 70}")
    log(f"  M파일 띄어쓰기 교정 (레코드 단위 수정 + 의존명사 별도 검사)")
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
    log(f"  [1/8] 원본 파일 무결성 검증")
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
    log(f"  [2/8] 텍스트 추출 + 규칙 로드")
    log(f"  {'━' * 50}")

    text = extract_text(SRC)
    log(f"  추출 텍스트: {len(text):,}자")

    before_stats = {}
    for cat in ["것", "수", "따위", "사이", "뿐", "뿐만", "고있", "고+동사", "척", "이상", "이하", "밑", "등", "때", "때문", "번",
                "데", "대로", "만큼", "줄", "듯", "채", "바", "터", "차례", "무렵", "적", "지",
                "중", "상", "우", "하", "같은", "것 같은", "나라"]:
        spaced = text.count(f" {cat}")
        total = text.count(cat)
        attached = total - spaced
        before_stats[cat] = {"spaced": spaced, "attached": attached, "total": total}
        if attached > 0:
            log(f"  [{cat}] 띄어쓰기={spaced}, 붙여쓰기={attached}, 총={total}")

    china_rules = load_china_place_rules()
    txt_rules = parse_txt_rules(RULES_FILE)
    regex_simple, regex_patterns = parse_regex_rules(REGEX_RULES_FILE)

    log(f"\n  {'━' * 50}")
    log(f"  [3/8] 다단계 규칙 생성 (중요 규칙 우선)")
    log(f"  {'━' * 50}")

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

    log(f"\n  [1단계] 중국 지명 + 나라→조: {len(china_rules)}개 (파일) + {len(dynamic_nara_rules)}개 (동적)")
    step1_rules = []
    for orig, repl in china_rules:
        if orig in text:
            cnt = text.count(orig)
            step1_rules.append((orig, repl, "1단계-중한", cnt))
            log(f"  '{orig}' → '{repl}' ({cnt}건)")
    for orig, repl, cat, cnt in dynamic_nara_rules:
        step1_rules.append((orig, repl, cat, cnt))
        log(f"  '{orig}' → '{repl}' ({cnt}건, 동적)")

    log(f"\n  [2단계] TXT 통합규칙 (rules_documentation.txt): {len(txt_rules)}개 로드")
    step2_rules = []
    for src, dst in txt_rules:
        if src not in text:
            continue
        cnt = text.count(src)
        step2_rules.append((src, dst, "2단계-TXT", cnt))
    log(f"  적용: {len(step2_rules)}개, {sum(r[3] for r in step2_rules)}건")

    log(f"\n  [3단계] 정규식 단순 치환 (rules_regex.txt): {len(regex_simple)}개 로드")
    step3_rules = []
    for src, dst, comment in regex_simple:
        if src not in text:
            continue
        cnt = text.count(src)
        step3_rules.append((src, dst, f"3단계-정규식단순({comment})", cnt))
    log(f"  적용: {len(step3_rules)}개, {sum(r[3] for r in step3_rules)}건")

    REGEX_NOSPLIT = {
        "적": {"민주적","공개적","사회적","정치적","경제적","문화적","역사적","자연적","물리적","화학적","생물적","수학적","논리적","철학적","과학적","기술적","의학적","법적","도덕적","윤리적","예술적","체육적","교육적","종교적","군사적","외교적","국제적","민족적","국가적","지역적","세계적","전통적","현대적","고전적","원시적","봉건적","자본적","사회주의적","공산적","혁명적","반동적","진보적","보수적","급진적","온건적","적극적","소극적","능동적","수동적","주동적","주체적","객관적","주관적","구체적","추상적","현실적","이상적","실질적","형식적","외형적","내면적","심리적","정신적","물질적","유기적","무기적","전체적","부분적","국부적","전반적","일반적","특수적","개별적","집단적","대중적","개인적","공동적","협동적","단독적","복합적","단일적","다원적","다양적","종합적","분석적","체계적","조직적","자발적","강제적","인위적","자연적","선천적","후천적","본능적","습관적","규칙적","불규칙적","정상적","비정상적","합법적","불법적","공식적","비공식적","공개적","비공개적","내밀적","비밀적","공공적","사적","공적","사영적","국영적","집체적","개인적","기본적","근본적","필수적","임의적","선택적","필연적","우연적","절대적","상대적","보편적","특정적","고유적","독자적","독립적","종속적","자립적","의존적","상호적","쌍방적","일방적","다방적","다각적","입체적","평면적","선형적","점적","면적","체적","공간적","시간적","영구적","일시적","순간적","지속적","단속적","연속적","병행적","동시적","순차적","점진적","급진적","급속적","완만적","점진적","순환적","반복적","규칙적","주기적","계절적","연례적","월례적","일례적","정기적","부정기적","정상적","비정상적","건강적","병적","생리적","병리적","치료적","예방적","보건적","위생적","안전적","위험적","보호적","방어적","공격적","저항적","항쟁적","투쟁적","경쟁적","협력적","협조적","지원적","원조적","구호적","구제적","복지적","후생적","문화적","문명적","야만적","미개적","선진적","후진적","개발적","발전적","성장적","확대적","축소적","증가적","감소적","생산적","소비적","유통적","분배적","교환적","거래적","무역적","상업적","공업적","농업적","수산적","임업적","축산적","광업적","건설적","토목적","건축적","조경적","도시적","농촌적","어촌적","산촌적","도시적","근교적","원교적","중심적","주변적","외곽적","내륙적","해안적","국경적","변경적","내지적","외지적","고유적","토착적","이국적","외래적","수입적","수출적","국산적","외제적","전통적","현대적","신식적","구식적","구형적","신형적","신품적","중고적","신품적","일품적","대량적","소량적","다량적","소수적","다수적","전원적","일부적","전체적","국가적","당적","정치적","조직적","제도적","법적","규범적","원칙적","예외적","일반적","특별적","특수적","정상적","비상적","긴급적","돌발적","예측적","불예측적","가능적","불가능적","현실적","가상적","실제적","이론적","실천적","실행적","운동적","활동적","행동적","정적","동적","정태적","동태적","안정적","불안정적","균형적","불균형적","조화적","불조화적","통일적","분열적","결합적","분리적","통합적","해체적","집중적","분산적","흡수적","방출적","팽창적","수축적","확장적","축소적","개방적","폐쇄적","자유적","구속적","해방적","억압적","진보적","퇴보적","발전적","정체적","쇠퇴적","부흥적","부흥적","재생적","소생적","부활적","신생적","창조적","모방적","독창적","전래적","유래적","기원적","발원적","시발적","종말적","최종적","초기적","중기적","말기적","전기적","후기적","전반적","후반적","초반적","중반적","시작적","완료적","완성적","미완성적","완결적","미완결적","성공적","실패적","유효적","무효적","적법적","위법적","정당적","부당적","합리적","비합리적","논리적","비논리적","과학적","비과학적","체계적","비체계적","조직적","비조직적","질서적","무질서적","규율적","무규율적","규칙적","불규칙적"},
        "지": {"판타지","목적지","관광지","거주지","출생지","산지","원산지","생산지","근거지","주거지","요충지","전략지","분지","해안지","내륙지","고산지","산간지","농촌지","도시지","공업지","상업지","주택지","휴양지","위락지","유적지","사적지","명승지","널판지","합판지","골판지","양철지","은박지","주석지","도화지","백지","신문지","잡지","간행지","출판지","기관지","반지","가락지","지질","지층","지대","지맥","지형","지세","지리","지도","지하","지상","지표","지면","지점","지역","지구","지방","지위","지지","지식","지능","지혜","지령","지시","지배","지향","지침","지연","지속","지진","지평","지평선","지구력","지도자","지배력","지적","지리적","지역적","지방적","지구적","지속적","지연적","지향적","지배적","지도적"},
    }

    log(f"\n  [4단계] 정규식 패턴 매칭 (rules_regex.txt): {len(regex_patterns)}개 로드")
    step4_rules = []
    for pat, dst, comment in regex_patterns:
        for m in pat.finditer(text):
            orig = m.group(0)
            try:
                repl = m.expand(dst)
            except re.error:
                repl = dst
            skip = False
            for suffix, nosplit_set in REGEX_NOSPLIT.items():
                if orig.endswith(suffix) and orig in nosplit_set:
                    skip = True
                    break
            if skip:
                continue
            cnt = text.count(orig)
            if cnt > 0:
                step4_rules.append((orig, repl, f"4단계-정규식패턴({comment})", cnt))
    step4_dedup = {}
    for src, dst, cat, cnt in step4_rules:
        if src not in step4_dedup:
            step4_dedup[src] = (src, dst, cat, cnt)
    step4_rules = list(step4_dedup.values())
    log(f"  적용: {len(step4_rules)}개, {sum(r[3] for r in step4_rules)}건")

    log(f"\n  [5단계] 의존명사/누락규칙 (apply_text_corrections)")
    text_changes = apply_text_corrections(text)
    cats = {}
    for src, dst, cat, cnt in text_changes:
        if cat not in cats:
            cats[cat] = 0
        cats[cat] += cnt
    for cat_name, total in sorted(cats.items(), key=lambda x: -x[1]):
        log(f"    {cat_name}: {total}건")

    log(f"\n  [6단계] 의존명사 별도 검사 (apply_dependent_noun_inspection)")
    dep_noun_results = apply_dependent_noun_inspection(text)
    step6_rules = []
    dep_total = 0
    for noun, items in dep_noun_results.items():
        if items:
            log(f"    [{noun}] 붙여쓰기 {len(items)}개 항목")
            for word, spaced_ver, cnt in items[:10]:
                log(f"      '{word}' → '{spaced_ver}' ({cnt}건)")
                step6_rules.append((word, spaced_ver, f"6단계-의존명사({noun})", cnt))
                dep_total += cnt
            if len(items) > 10:
                extra = sum(c for _, _, c in items[10:])
                log(f"      ... 외 {len(items)-10}개 ({extra}건)")
                for word, spaced_ver, cnt in items[10:]:
                    step6_rules.append((word, spaced_ver, f"6단계-의존명사({noun})", cnt))
                    dep_total += cnt
    log(f"  의존명사 별도 검사: {len(step6_rules)}개 항목, {dep_total}건")

    all_rules = step1_rules + step2_rules + step3_rules + step4_rules + text_changes + step6_rules
    seen_src = set()
    deduped_rules = []
    for r in all_rules:
        if r[0] not in seen_src:
            seen_src.add(r[0])
            deduped_rules.append(r)
    all_rules = deduped_rules
    all_rules.sort(key=lambda r: len(r[0]), reverse=True)
    log(f"\n  총 규칙 (중복제거): {len(all_rules)}개, {sum(r[3] for r in all_rules)}건")

    if not all_rules:
        log(f"\n  수정 불필요")
        return

    log(f"\n  {'━' * 50}")
    log(f"  [4/8] 백업 + 레코드 단위 수정")
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

            compressed_ok = False
            for level in [6, 5, 4, 3, 2, 1]:
                co = zlib.compressobj(level=level, method=zlib.DEFLATED, wbits=-15)
                new_compressed = co.compress(new_dec) + co.flush()
                if len(new_compressed) <= len(raw):
                    all_stream_data[sn] = (new_compressed, len(raw))
                    log(f"  압축(level={level}): {len(new_compressed):,} / {len(raw):,} (여유: {len(raw) - len(new_compressed):,})")
                    compressed_ok = True
                    break
                else:
                    log(f"  압축(level={level}): {len(new_compressed):,} > {len(raw):,} (초과, 다음 레벨 시도)")

            if not compressed_ok:
                log(f"  [오류] 압축 불가! 파일이 너무 커짐")
                return

            verify_data = all_stream_data[sn][0]
            verify_dec = zlib.decompress(verify_data, -15)
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
    log(f"  [5/8] 직접 바이너리 수정 (OLE 구조 보존)")
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

    OUT_FINAL = OUT
    if os.path.exists(OUT):
        try:
            os.remove(OUT)
        except PermissionError:
            OUT_FINAL = OUT.replace('.hwp', f'_new_{time.strftime("%H%M%S")}.hwp')
            if os.path.exists(OUT_FINAL):
                try:
                    os.remove(OUT_FINAL)
                except PermissionError:
                    OUT_FINAL = OUT.replace('.hwp', f'_v2_{time.strftime("%H%M%S")}.hwp')
    os.rename(OUT_TMP, OUT_FINAL)
    log(f"  .bin → .hwp 변경 완료: {OUT_FINAL}")

    hash_after_write = file_hash(OUT_FINAL)
    log(f"  쓰기 후 해시: {hash_after_write}")
    log(f"  해시 변경됨: {hash_after_write != file_hash(SRC)}")

    if hash_after_write == file_hash(SRC):
        log(f"  [오류] 해시 변경 없음! 직접 쓰기 미적용!")
        return

    log(f"\n  {'━' * 50}")
    log(f"  [6/8] 출력 파일 검증")
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
                vtext = extract_text_from_records(records)
                log(f"  OLE: ✅ ({len(streams)} 스트림, BodyText {body_count}개)")
                log(f"  압축해제: ✅ ({len(raw):,}→{len(dec):,} bytes)")
                log(f"  레코드: {len(records)}개")
                log(f"  텍스트: {len(vtext):,}자")
        ole.close()
    except Exception as e:
        log(f"  [오류] {e}")
        return

    log(f"\n  {'━' * 50}")
    log(f"  [7/8] 교정 결과 검증 (수정 전후 비교)")
    log(f"  {'━' * 50}")

    text2 = extract_text(OUT_FINAL)
    log(f"  수정 후 텍스트: {len(text2):,}자 (원본: {len(text):,}자)")

    after_stats = {}
    for cat in ["것", "수", "따위", "사이", "뿐", "뿐만", "고있", "고+동사", "척", "이상", "이하", "밑", "등", "때", "때문", "번",
                "데", "대로", "만큼", "줄", "듯", "채", "바", "터", "차례", "무렵", "적", "지",
                "중", "상", "우", "하", "같은", "것 같은", "나라"]:
        spaced = text2.count(f" {cat}")
        total = text2.count(cat)
        attached = total - spaced
        after_stats[cat] = {"spaced": spaced, "attached": attached, "total": total}

    log(f"\n  {'패턴':<8} {'전-붙임':>8} {'전-띄움':>8} {'후-붙임':>8} {'후-띄움':>8} {'변화':>8}")
    log(f"  {'─' * 55}")
    for cat in ["것", "수", "따위", "사이", "뿐", "뿐만", "고있", "고+동사", "척", "이상", "이하", "밑", "등", "때", "때문", "번",
                "데", "대로", "만큼", "줄", "듯", "채", "바", "터", "차례", "무렵", "적", "지",
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
    log(f"  [의존명사 별도 검사 결과 (수정 후 재검토)]")
    log(f"  {'━' * 50}")

    dep_noun_after = apply_dependent_noun_inspection(text2)
    for noun, items in dep_noun_after.items():
        if items:
            log(f"  [{noun}] 여전히 붙여쓰기 {len(items)}개:")
            for word, spaced_ver, cnt in items[:5]:
                log(f"    '{word}' → '{spaced_ver}' ({cnt}건)")
            if len(items) > 5:
                log(f"    ... 외 {len(items)-5}개")

    log(f"\n  {'━' * 50}")
    log(f"  [8/8] HWP 파일 열기 테스트")
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
    log_path = os.path.join(LOG_DIR, f"M교정로그_{time.strftime('%Y%m%d_%H%M%S')}.txt")
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    log(f"  로그 저장: {log_path}")


if __name__ == "__main__":
    main()
