from bs4 import BeautifulSoup
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["web_crawler"]
pages_collection = db["pages"]
professors_collection = db["faculty"]

document = pages_collection.find_one({'url': 'https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml'})

if document:
    html_content = document['html']

    soup = BeautifulSoup(html_content, 'html.parser')

    faculty_divs = soup.find_all("div", class_="clearfix")

    for div in faculty_divs:

        name = div.find('h2').text.strip() if div.find('h2') else None

        details = div.find('p')

        if details:
            title = None
            office = None
            phone = None
            email = None
            web = None

            strong_tags = details.find_all('strong')

            for tag in strong_tags:
                field_name = tag.text.strip()
                if field_name == "Title:" or field_name == "Title":
                    title = tag.find_next_sibling(text=True).strip()
                elif field_name == "Office:" or field_name == "Office":
                    office = tag.find_next_sibling(text=True).strip()
                elif field_name == "Phone:" or field_name == "Phone":
                    phone = tag.find_next_sibling(text=True).strip()

        if details:
            email_link = details.find('a', href=lambda href: href and "mailto:" in href)
            email = email_link.get('href').replace('mailto:', '').strip() if email_link else None
            web_link = details.find('a', href=lambda href: href and "http" in href)
            web = web_link.get('href').strip() if web_link else None

            professor_document = {
                "name": name,
                "title": title,
                "office": office,
                "phone": phone,
                "email": email,
                "website": web
            }

            professors_collection.insert_one(professor_document)

    print("Faculty information has been stored in MongoDB.")
else:
    print("No document found with the specified URL.")
