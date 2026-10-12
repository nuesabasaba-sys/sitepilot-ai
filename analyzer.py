import json
import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from pydantic import BaseModel


class AnalysisSection(BaseModel):
    issues: list[str]
    suggestions: list[str]


class SiteAnalysis(BaseModel):
    seo: AnalysisSection
    copywriting: AnalysisSection
    cta: AnalysisSection
    readability: AnalysisSection

    target_audience: str
    overall_issues: list[str]

    title_suggestion: str
    meta_description_suggestion: str
    h1_suggestion: str


load_dotenv()

client = OpenAI()
MODEL_NAME = "gpt-6-luna"


def analyze_site(url: str) -> SiteAnalysis:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        

    except requests.Timeout:
        raise TimeoutError("Webサイトへの接続がタイムアウトしました")
    
    except requests.RequestException:
        raise ConnectionError("Webサイトを取得できませんでした")
    
    soup = BeautifulSoup(response.text, "html.parser")

    print(response.status_code)
    if soup.title is not None:
        title = soup.title.text
    else:
        title = ""
    print("title:", title)

    if soup.h1 is not None:
        h1 = soup.h1.get_text(" ", strip=True)
    else:
        h1 = ""
    print("h1:", h1)

    h2_list = soup.find_all("h2")
    h2_text_list = []
    for h2 in h2_list:
        h2_text_list.append(h2.get_text(" ", strip=True))
    print("h2:", h2_text_list)
    print("h2の数:", len(h2_list))

    if len(h2_list) == 0:
        print("h2なし")

    for h2 in h2_list:
        print(h2.text)

    description_tag = soup.find("meta", attrs={"name": "description"})
    if description_tag is not None:
        description = description_tag["content"]
    else:
        description = ""
    print("description:", description)

    body = soup.body
    body_text = body.get_text(" ", strip=True)
    print(body_text)
    page_data = {
        "url": url,
        "title": title,
        "description": description,
        "h1": h1,
        "h2": h2_text_list,
        "body": body_text
    }
    print(page_data)

    page_data_json = json.dumps(
        page_data,
        ensure_ascii=False
    )

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("APIキーを読み込めました")
    else:
        print("APIキーを読み込めませんでした")

    analysis_prompt = f"""
以下はWebページから抽出した情報です。

{page_data_json}

このWebページを以下の観点から分析してください。

1. SEO
2. コピーライティング
3. CTA
4. 読みやすさ
5. 想定ターゲット
6. Webサイト全体の問題点
7. titleの改善案
8. meta descriptionの改善案
9. h1の改善案

各項目について、問題点と具体的な改善案を日本語で説明してください。
"""

    try:
        response_ai = client.responses.parse(
            model=MODEL_NAME,
            input=analysis_prompt,
            text_format=SiteAnalysis
        )

    except OpenAIError:
        raise RuntimeError("AI分析に失敗しました")

    analysis_result = response_ai.output_parsed

    if not isinstance(analysis_result, SiteAnalysis):
        raise RuntimeError("AI分析結果を取得できませんでした")

    return analysis_result
