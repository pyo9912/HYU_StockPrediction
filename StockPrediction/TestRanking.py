from konlpy.tag import Kkma, Okt

kkma = Kkma()
okt = Okt()

text = "대한항공 관련 뉴스 형태소 분석 테스트를 실시하겠습니다. 대한항공의 주가는 현재 유가급등과 국제유가의 영향을 받아 5% 하락했습니다."

print(kkma.nouns(text))
print(okt.morphs(text))
