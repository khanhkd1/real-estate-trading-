from function import crawl_apartment_links_of_a_page, crawl_apartment_info
from threading import Thread
import cloudscraper
import pandas as pd
import json


def crawl(start_page, end_page, thread_stt):
    print(f'Thead {thread_stt} - crawl apartment links')
    apartment_links = []
    for page in range(start_page, end_page + 1):
        apartment_links += crawl_apartment_links_of_a_page(f'{main_url}{page}', scraper, headers)

    apartment_jsons = []
    for i in range(len(apartment_links)):
        print(f'Thread {thread_stt} - crawl apartment info - {i}')
        apartment_jsons.append(crawl_apartment_info(apartment_links[i], scraper, headers))

    with open(f'data/data_thread_{thread_stt}.json', 'w', encoding='utf-8') as f_out:
        json.dump(apartment_jsons, f_out, ensure_ascii=False)

    apartment_df = pd.DataFrame(apartment_jsons)
    apartment_df.to_csv(f'data/data_thread_{thread_stt}.csv', index=False)


if __name__ == '__main__':
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'firefox',
            'platform': 'windows',
            'mobile': False
        }
    )

    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 '
                             'Firefox/3.0.7', }

    main_url = 'https://batdongsan.com.vn/ban-can-ho-chung-cu-ha-noi/p'
    end_page_thread_1 = 205
    end_page_thread_2 = 410
    end_page_thread_3 = 615
    end_page_thread_4 = 820
    
    t1 = Thread(target=crawl, args=(1, end_page_thread_1, 1))
    t2 = Thread(target=crawl, args=(end_page_thread_1 + 1, end_page_thread_2, 2))
    t3 = Thread(target=crawl, args=(end_page_thread_2 + 1, end_page_thread_3, 3))
    t4 = Thread(target=crawl, args=(end_page_thread_3 + 1, end_page_thread_4, 4))
    
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    
    t1.join()
    t2.join()
    t3.join()
    t4.join()
