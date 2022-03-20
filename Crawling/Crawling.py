import requests
from bs4 import BeautifulSoup
import urllib
# 구글 뉴스 페이지
base_url = "https://news.google.com"


# 예제 010을 참조하여 구글 뉴스 클리핑 함수 정의
def google_news_clipping_keyword(keyword_input, limit=20):
    
    keyword = urllib.parse.quote(keyword_input)
    
    search_url = base_url + "/search?q=" + keyword + "&hl=ko&gl=KR&ceid=KR%3Ako"
    
    google_response = requests.get(search_url)
    google_html_src = google_response.text
    google_soup = BeautifulSoup(google_html_src, 'html.parser')
    
    news_items = google_soup.select('div[class="xrnccd"]')
    
    for item in news_items[:limit]:

        link = item.find('a', attrs={'class':'VDXfz'}).get('href')
        
        # 뉴스 redirect 링크 
        news_url = base_url + link[1:]
        #print(news_url)

        news_response = requests.get(news_url)
        news_html_src = news_response.text
        news_soup = BeautifulSoup(news_html_src, 'html.parser')

        # 뉴스 원본 링크 
        ## 뉴스 원본 링크를 찾지 못하는 경우도 있음
        ### 원인은??
        #### news_link = news_soup.find('link', {'rel': 'canonical'})['href']
        ### 수정 완료
        #### news_link = news_soup.find('link', rel = 'canonical')
        try:
            news_link = news_soup.find('link', rel = 'canonical')
            print("find news link\t")
        except:
            print("Cannot find news link\t")
            continue
        

        # 뉴스 제목 
        news_title = item.find('a', attrs={'class':'DY5T1d'}).getText()
        print(news_title)

        # 신문사
        news_agency = item.find('a', attrs={'class':'wEwyrc AVN2gc uQIVzc Sksgp'}).text
        print(news_agency)
        
        news_reporting = item.find('time', attrs={'class':'WW6dff uQIVzc Sksgp'})
        news_reporting_datetime = news_reporting.get('datetime').split('T')
        news_reporting_date = news_reporting_datetime[0]
        news_reporting_time = news_reporting_datetime[1][:-1]
        print(news_reporting_date)
        print(news_reporting_time)

        news_text = news_soup.text.split("\n")
        #print(news_text)
        # news_content = []
        # prev_empty = 0
        # next_empty = 0
        # was_text = False
        # temp_text = []
        # for text in news_text:
        #     if text == '' or text == ' ':
        #         if next_empty == 0 and was_text == False:
        #             prev_empty += 1
        #         if prev_empty != 0 and was_text == True:
        #             next_empty +=1

        #     else:
        #         if prev_empty != 0 and next_empty == 0:
        #                 temp_text.append(text)

        #         elif prev_empty != 0 and next_empty != 0:
                        
        #             if temp_text:
        #                 if (next_empty == 1) or (prev_empty == 1):
        #                     check_length = [x for x in temp_text if len(x) < 20 or '|' in x]
        #                     last_text = temp_text[-1]
                            
        #                     if not check_length:
        #                         if len(last_text) > 150:
        #                             if last_text[-1] == '.' or last_text[-1] == ' ':
        #                                 print(temp_text)

                    
        #             prev_empty = next_empty
        #             next_empty = 0
        #             temp_text.clear()
        #             temp_text.append(text)


        #         was_text = True




        

                
    # result = {'link':links, 'title':titles, 'contents':contents, 'agency':agencies, \
    #          'date':reporting_dates, 'time':reporting_times}
    
    return news_items

# 함수를 실행하여 뉴스 목록 정리

news = google_news_clipping_keyword("대한항공", 5)
