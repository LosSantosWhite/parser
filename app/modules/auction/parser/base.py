import asyncio
import datetime
import locale
from typing import Generator
from urllib import parse
import re

from bs4 import BeautifulSoup
import httpx

from app.utils.decorators import my_logger


class ParserBase:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.1.762 Yowser/2.5 Safari/537.36"
    }
    timeout = 10
    pattern = r"\d{2} \w+ \d{4}"

    def __init__(self, url: str):
        self.url = url
        # необходимо для конвертации строки даты на русском в объект datetime.date
        locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

    @staticmethod
    def __convert_str_to_date(s: str) -> datetime.date:
        result = datetime.datetime.strptime(s, "%d %B %Y").date()
        return result

    @property
    def base_url(self) -> str:
        url_parser = parse.urlparse(self.url)
        return f"{url_parser.scheme}://{url_parser.netloc}"

    @my_logger()
    async def last_page_number(self) -> int:
        """Номер последней страницы"""
        async with httpx.AsyncClient(headers=self.headers, timeout=10) as session:
            response = await session.get(self.url)
            soup = BeautifulSoup(response.text, "lxml")
            last_page = soup.find_all(
                "a",
                class_="safeparam u-pagination-v1__item u-pagination-v1-4 g-rounded-50 g-pa-7-16",
            )[-1]["href"]
            return int(last_page.split("=")[-1])

    async def get_info_from_html_detail(self, html: str) -> dict:
        """Получить данные из детального отображения аукциона
        результат функции
        {
            "deadline": None или "число месяц год",
            "fee": None или число,
            "organizer": None или организатор
        }
        """
        soup = BeautifulSoup(html, "lxml")
        table = soup.find(
            "div",
            class_="col-lg-9 g-mb-50 g-mb-0--lg",
        )
        try:
            deadline = (
                table.find("dt", string="Срок подачи заявок").parent()[-1].text.strip()
            )
            deadline = re.search(self.patter, deadline)
            if deadline:
                deadline = deadline.group(0)
            deadline = self.__convert_str_to_date(deadline)
        except AttributeError:
            deadline = None
        try:
            fee = (
                table.find("dt", string="Стартовый платеж (руб)")
                .parent()[-1]
                .text.strip()
            )
            fee = int("".join(re.findall("\d+", fee)))
        except AttributeError:
            fee = None
        try:
            organizer = table.find("dt", string="Организатор").parent()[-1].text.strip()
        except AttributeError:
            organizer = None

        return dict(deadline=deadline, fee=fee, organizer=organizer)

    def _get_html_list_items(self, html) -> Generator:
        """Получить данные из html-таблицы аукционов
        генератор для каждой строки таблицы tbody
        результат
        {
            "date": число месяц год,
            "url": ссылка на детальное отображение аукциона,
            "location": локация,
            "region": регион,
            "status": статус аукциона
        }
        """
        soup = BeautifulSoup(html, "lxml")
        table = soup.find("tbody", class_="g-color-black-opacity-0_6").find_all("tr")
        for row in table:
            row = row.find_all("td")
            date = row[0].text.strip()
            date = self.__convert_str_to_date(date)
            url = row[0].find("a")["href"]
            location = row[1].text.strip()
            region = row[2].text.strip()
            status = row[3].text.strip()

            yield dict(
                date=date, url=url, location=location, region=region, status=status
            )

    async def _html_to_dict(self) -> list[dict]:
        pages_list = await self.collect_pages()
        htmls = await self.requests_list_items(pages_list)
        result = []
        for html in htmls:
            for item in self._get_html_list_items(html):
                result.append(item)
        return result

    async def collect_pages(self) -> list[str, str | dict[str | int]]:
        """Генерация списка страниц, на которые необходимо сделать запросы"""
        last_mage_number = await self.last_page_number()
        pages_list = [dict(url=self.url, params={"ap": ap}) for ap in range(1, 1 + 1)]
        return pages_list

    async def fetch_html(
        self, session: httpx.AsyncClient, url: str, params: dict = {}
    ) -> str:
        response = await session.get(url, params=params)
        if response.status_code == 200:
            return response.text
        raise Exception(f"{response.status_code} --- {response.url}")

    @my_logger()
    async def requests_list_items(self, urls: dict[str, str]) -> list[str]:
        """Запрос на получение html кода страниц"""
        async with httpx.AsyncClient(
            headers=self.headers, timeout=self.timeout
        ) as session:
            requests = [
                self.fetch_html(session, param["url"], param.get("params"))
                for param in urls
            ]
            result = await asyncio.gather(*requests)
            return result

    async def request_detail_item(self, param: dict) -> dict[str, str | int]:
        async with httpx.AsyncClient(
            headers=self.headers,
            timeout=self.timeout,
        ) as session:
            url = parse.urljoin(self.base_url, param["url"])
            html = await self.fetch_html(session, url)
            param = param | await self.get_info_from_html_detail(html)
            # obj=2daff8ecf59464b8d45e50117317b0c4
            id_ = param["url"].split("obj=")[-1]
            param["obj_id"] = id_
            param.pop("url")
            return param

    async def parse_info(self) -> list[dict[str, str | int]]:
        items = await self._html_to_dict()
        result = [self.request_detail_item(item) for item in items]
        result = await asyncio.gather(*result)
        return result
