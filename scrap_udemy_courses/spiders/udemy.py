# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy_splash import SplashRequest


class UdemySpider(scrapy.Spider):
    name = 'udemy'
    udmey_url = 'https://www.udemy.com'
    headers = None
    search_keyword = ''
    script = '''
treat = require("treat")
function main(splash, args)

  local entries = treat.as_array({})
    splash:on_request(function(request)
        table.insert(entries, request.info)
    end)
  assert(splash:go{args.url,headers=splash.args.headers})
  assert(splash:wait(1))
  return {
    entries =entries,
  }
end
'''

    def start_requests(self):
        url = (f'{self.udmey_url}/courses/'
               f'search/?src=ukw&q={self.search_keyword}')
        yield SplashRequest(url,
                            callback=self.parse_headers,
                            endpoint='execute',
                            args={
                                'wait': 2,
                                'lua_source': self.script,
                            },
                            dont_filter=True)

    def parse_headers(self, response):
        search_request = None
        for entry in response.data['entries']:
            if 'api-2.0/search-courses/?fields' in entry['url']:
                search_request = entry
                break
        headers = {
            header['name']: header['value']
            for header in search_request['headers']
        }
        self.headers = headers
        yield scrapy.Request(url=search_request['url'],
                             callback=self.parse_courses,
                             headers=headers)

    def parse_courses(self, response):
        data = json.loads(response.body)
        for course in data['courses']:
            course_id = course['id']
            yield scrapy.Request(
                url=(f'{self.udmey_url}/api-2.0/course-landing-components/'
                     f'{course_id}/me/?components=curriculum'),
                callback=self.parse_course,
                headers=self.headers,
                meta={'course_name': course['title']})
        if 'next' in data['pagination']:
            next_page = data['pagination']['next']['url']
            yield scrapy.Request(url=f'{self.udmey_url}{next_page}',
                                 callback=self.parse_courses,
                                 headers=self.headers)

    def parse_course(self, response):
        data = json.loads(response.body)['curriculum']['data']
        yield {
            'course_name':
            response.meta['course_name'],
            'num_of_published_lectures':
            data['num_of_published_lectures'],
            'sections': [{
                'title':
                section['title'],
                'lecture_count':
                section['lecture_count'],
                'items': [{
                    'title': item['title'],
                    'content_summary': item['content_summary']
                } for item in section['items']]
            } for section in data['sections']]
        }
