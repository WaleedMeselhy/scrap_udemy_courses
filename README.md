# scrap_udemy_courses


* Using scrapy to scrap course info from udemy.com
* Using scrapy-splash to get request headers to be used in scrapy requests
## sample output
```json
[
    {
        "course_name": "Stepping into Python Web Services - Flask",
        "num_of_published_lectures": 11,
        "sections": [
            {
                "title": "Introduction",
                "lecture_count": 2,
                "items": [
                    {
                        "title": "Introduction",
                        "content_summary": "02:40"
                    },
                    {
                        "title": "How can you introduce yourself to the course community?",
                        "content_summary": "01:52"
                    }
                ]
            },
        ...
        ]
    }
]
```

## Run

```sh
$ cd scrap_udemy_courses
$ docker run -p 8050:8050 scrapinghub/splash
$ scrapy crawl udemy -a search_keyword="<search_keyword>" -o/output/courses.json
```

or run in docker-compose

```sh
$  docker-compose up --build
```
