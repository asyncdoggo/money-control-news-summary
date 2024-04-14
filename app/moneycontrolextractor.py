import bs4
import re
import requests
from app.summarizer import Summarizer


summarizer = Summarizer()


class MoneyControlExtractor:
    def get_news_list(self, page):
        news_link = f"https://www.moneycontrol.com/news/business/economy/page-{page}"
        response = requests.get(news_link)
        html = response.text
        self.soup = bs4.BeautifulSoup(html, "html.parser")
        news = self.soup.find_all("li", {"id": re.compile("newslist-")})
        news_list = []
        for news_item in news:
            news_list.append({
                "title": news_item.find("a")["title"],
                "link": news_item.find("a")["href"]
            })
        return news_list
    
    def get_news_content(self, link):
        summarized_text = ""
        try:
            response = requests.get(link)
            html = response.text
            self.soup = bs4.BeautifulSoup(html, "html.parser")
            # If pro_artidesc class is present, it means the article is a premium article so skip it
            if self.soup.find("p", {"class": "pro_artidesc"}):
                return "Premium article"
            
            content = self.soup.find("div", {"id": "contentdata"})
            paras = content.find_all("p")
            text = " ".join([para.text for para in paras])     

            text = re.sub(r"\s+", " ", text) # Remove extra spaces
            text = re.sub(r"\n+", "\n", text) # Remove extra newlines
            text = text.replace("\n", " ") # Replace newlines with spaces
            text = re.sub(r"\s+([.,])", r"\1", text) # Remove spaces before punctuation
            text = re.sub(r"([.,])\s+", r"\1", text) # Remove spaces after punctuation



            if len(text) < 2048:
                return text
            
            summarized_text = summarizer.summarize(text, max_length=len(text) // 4)
            return summarized_text
        except:
            summarized_text = "Error fetching content"
            return summarized_text


if __name__ == "__main__":
    extractor = MoneyControlExtractor()
    x = extractor.get_news_list(1)

    for i in x:
        print(len(extractor.get_news_content(i["link"])))
        print("\n")




    