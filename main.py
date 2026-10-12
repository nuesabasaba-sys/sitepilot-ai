import json

from analyzer import analyze_site


def main():
    url = input("URLを入力してください: ")
    analysis_result = analyze_site(url)

    print(analysis_result)
    print("SEOの問題点:", analysis_result.seo.issues)
    print("SEOの改善案:", analysis_result.seo.suggestions)
    print("title改善案:", analysis_result.title_suggestion)

    analysis_dict = analysis_result.model_dump()
    print(
        json.dumps(
            analysis_dict,
            ensure_ascii=False,
            indent=2
        )
    )


if __name__ == "__main__":
    main()
