import pywikibot

def search_commons_titles(keywords):
    site = pywikibot.Site('commons', 'commons')
    search_results = []

    for keyword in keywords:
        search_page = pywikibot.Page(site, 'Special:Search')
        search_generator = site.search(keyword, total=50)  # Adjust 'total' to get more results

        for page in search_generator:
            if any(k in page.title() for k in keywords):
                search_results.append(page.title())

    return search_results

if __name__ == "__main__":
    keywords = ["KMS1"]
    results = search_commons_titles(keywords)

    for title in results:
        print(title)
    