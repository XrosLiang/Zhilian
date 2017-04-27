import pymongo
import requests
from pyquery import PyQuery as pq
from multiprocessing import Pool
import time
import random


def get_page(url):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


def parse_index_page(html):
    doc = pq(html)
    job_urls = doc('#newlist_list_content_table').find('a').items()
    return [url.attr.href for url in job_urls if url.attr.href.startswith('http://jobs')]


def parse_detail_page(html):
    doc = pq(html)
    job = doc('.inner-left.fl h1').text()
    company = doc('.inner-left.fl h2').text()
    company_url = doc('.inner-left.fl h2 a').attr.href
    treatment = doc('.welfare-tab-box span').text()
    salary = doc('.terminalpage-left .terminal-ul.clearfix li:nth-child(1) strong').text().strip()
    date = doc('.terminal-ul.clearfix li strong #span4freshdate').text().strip()
    number = doc('.terminalpage-left .terminal-ul.clearfix li:nth-child(7) strong').text().strip()
    location = doc('.terminalpage-left .terminal-ul.clearfix li:nth-child(2) strong a').text().strip()
    education = doc('.terminalpage-left .terminal-ul.clearfix li:nth-child(6) strong').text().strip()
    catrgory = doc('.terminalpage-left .terminal-ul.clearfix li:nth-child(8) strong').text().strip()
    experience = doc('.terminalpage-left .terminal-ul.clearfix li:nth-child(5) strong').text().strip()
    property = doc('.terminalpage-left .terminal-ul.clearfix li:nth-child(4) strong').text().strip()
    address = doc('.tab-cont-box .tab-inner-cont h2').text().strip()
    demand = doc('.tab-inner-cont p').text()
    yield {
        "工作": job,
        "公司": company,
        "公司介绍": company_url,
        "待遇": treatment,
        "职位月薪": salary,
        "发布日期": date,
        "招聘人数": number,
        "工作性质": property,
        "地点": location,
        "工作经验": experience,
        "最低学历": education,
        "职位类别": catrgory,
        "职位描述": demand,
        "工作地点": address
    }


def save_to_mongo(content):
    client = pymongo.MongoClient()
    database = client['Job']
    collection = database['Zhilian']
    if collection.update({'职位描述': content['职位描述']}, {'$set': content}, True) and content['工作'] != "":
        print("Saved", content["工作"], content["职位月薪"])
    else:
        print("***************\nFailed! {}\n***************".format(content["公司"]))

def save_catrgory(content):
    with open("catrgory.txt", "a") as f:
        f.write(content)
        print("职位类别已录入...")

def save_education(content):
    with open("education.txt", 'a') as f:
        f.write(content)
        print("最低学历已录入...")

def save_experience(content):
    with open("experience.txt", 'a') as f:
        f.write(content)
        print("工作经验已录入...")

def save_demand(content):
    with open("demand.txt", 'a') as f:
        f.write(content)
        print("职位描述已录入...")


def save_location(content):
    with open("location.txt", "a") as f:
        f.write(content)
        print("地点已录入...")


def save_salary(content):
    with open("salary.txt", "a") as f:
        f.write(content)
        print("职位月薪已录入...")


def save_treatment(content):
    with open("treatment.txt", "a") as f:
        f.write(content)
        print("待遇已录入...")


def next_to_page(html):
    doc = pq(html)
    next_page = doc('.pagesDown-pos a').attr.href
    return next_page


def main(page):
    url = "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%85%A8%E5%9B%BD&kw=python&sm=0&p={}".format(page)
    html = get_page(url)
    docs = parse_index_page(html)
    print("休息后继续...")
    time.sleep(random.randint(1,5))
    for doc in docs:
        html = get_page(doc)
        job_infors = parse_detail_page(html)
        for job_infor in job_infors:
            save_to_mongo(job_infor)
            save_demand(job_infor['职位描述'])
            save_location(job_infor['地点'])
            save_salary(job_infor['职位月薪'])
            save_treatment(job_infor['待遇'])
            save_education(job_infor['最低学历'])
            save_catrgory(job_infor['职位类别'])
            save_experience(job_infor['工作经验'])
            print("休息...")
            time.sleep(random.randint(1,5))


if __name__ == '__main__':
    pool = Pool()
    try:
        pool.map(main, [page for page in range(1,200)])
        print("\n采集完成!")
    except:
        print("可能已经采集完毕。")
