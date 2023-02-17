#TESTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import glob
import datetime as dt

# --Functions--
def get_users_count(comment):
    splits = [" , ", " by "] # Possible separators in "comment"
    for s in splits: # Loop to get users count 
        if s in comment:
            users_count = comment.split(s)[1] # Taking only " X anonymous"
            return int(re.search(r'\d+', users_count).group()) # Taking only number
        elif any(char.isdigit() for char in comment): # if digit/number in string
            users_count = int(re.search(r'\d+', comment).group()) # Taking only number
        else:
            users_count = None
    return users_count

def get_watchguard_info(company):
    watchguard_links = []
    watchguard_visitors = 0
    try:
        watchguards = company.find_all('span', {"style": "font-size:10.0pt;color:#001F32"})
        for w in watchguards:
            w = w.text.replace("\r","").replace("  ","").replace("\n"," ")
            if "watchguard" in w:
                watchguard_links.append(w.split(",")[0])
                watchguard_visitors += int(re.search(r'\d+', w.split(",")[1]).group())
    except Exception as e:
        print(e)
        pass
    return watchguard_visitors, watchguard_links

def scrap_email(url):
    soup = BeautifulSoup(open(url, 'rb').read())
    sense_table = soup.find('table', {"style": re.compile(r"^max-width:565.5pt;border-collapse:collapse;mso-yfti-tbllook:1184")}) # Fetching 6sense email table
    company_table = sense_table.find_all('table', {"style": re.compile(r"^width:100.0%;mso-cellspacing:0in;background:white;")})
    activities_dates = sense_table.find_all("p", {"class": "MsoNormal"}) # Difficult to define correct p - checking every
    activities_date = ""
    for p in activities_dates:
        if "Activities from" in p.text: # Looking for p wich contains "Activites from"
            activities_date = p.text.split("Activities from : ")[1] # Taking only Date period
            if " - " in activities_date:
                activities_date = p.text.split(" - ")[1] # Taking the last day
            break
        elif "Activities on : " in p.text:
            activities_date = p.text.split("Activities on : ")[1]
            break
    for company in company_table:
        activities_date_list.append(activities_date) # Each company has to have this
        name = company.find('span', {"style": "font-size:13.5pt"}).text.replace("\r","").replace("  ","").replace("\n"," ") # Extracting and normalizizng text
        names_list.append(name)
        website = company.find('span', {"style": "color:#0082D4;text-decoration:none;text-underline:none"})
        website_and_location = website.find_previous("p").text.replace("\r","").replace("  ","").replace("\n"," ").split(",") #spliting "p" as it has 2 vars
        website = website_and_location[0] # re-saving "website" to not create another variable
        websites_list.append(website)
        location = website_and_location[1]
        locations_list.append(location)
        comment = company.find('span', {"style": "font-size:11.5pt;color:#001F32"}).text.replace("\r","").replace("  ","").replace("\n"," ")
        comments_list.append(comment)
        users_count_list.append(get_users_count(comment))
        print(name)
        # add this
        get_watchguard_info(company)
        # ---


        for item in company.find_all('span', {"style": "font-size:11.5pt;color:black"}): # Scrapping stage, fit, reach - they all have the same style 
            item = item.text.replace("\r","").replace("  ","").replace("\n"," ")
            if "buying stage:" in item.lower():
                buying_stage_list.append(item.replace("Buying Stage: ",""))
            elif "profile fit:" in item.lower():
                profile_fit_list.append(item.replace("Profile Fit: ",""))
            elif "account reach:" in item.lower():
                account_reach_list.append(item.replace("Account Reach: ",""))
        keywords = company.find_all('span', {"style": re.compile(r"^font-size:10.5pt;color:#505C62;")})
        if not keywords:
            keyword1_list.append("")
            keyword2_list.append("")
            keyword3_list.append("")
            keyword4_list.append("")
            keyword5_list.append("")
        else:
            for count, keyword in enumerate(keywords): # There are usually 3 keywords - loop needed
                keyword = keyword.text.replace("\r","").replace("  ","").replace("\n"," ").split(" (")[0]
                if len(keywords) >= 5:
                    if count == 0:
                        keyword1_list.append(keyword)
                    elif count == 1:
                        keyword2_list.append(keyword)
                    elif count == 2:
                        keyword3_list.append(keyword)
                    elif count == 3:
                        keyword4_list.append(keyword)
                    elif count == 4:
                        keyword5_list.append(keyword)
                if len(keywords) == 4:
                    if count == 0:
                        keyword1_list.append(keyword)
                    elif count == 1:
                        keyword2_list.append(keyword)
                    elif count == 2:
                        keyword3_list.append(keyword)
                    elif count == 3:
                        keyword4_list.append(keyword)
                        keyword5_list.append("")
                if len(keywords) == 3:
                    if count == 0:
                        keyword1_list.append(keyword)
                    elif count == 1:
                        keyword2_list.append(keyword)
                    elif count == 2:
                        keyword3_list.append(keyword)
                        keyword4_list.append("")
                        keyword5_list.append("")
                elif len(keywords) == 2: 
                    if count == 0:
                        keyword1_list.append(keyword)
                    elif count == 1:
                        keyword2_list.append(keyword)
                        keyword3_list.append("")
                        keyword4_list.append("")
                        keyword5_list.append("")
                elif len(keywords) == 1:
                    keyword1_list.append(keyword)
                    keyword2_list.append("")
                    keyword3_list.append("")
                    keyword4_list.append("")
                    keyword5_list.append("")

# --Vars--
date_list = []
activities_date_list = []
names_list = []
websites_list = []
locations_list = []
buying_stage_list = []
profile_fit_list = []
account_reach_list = []
keyword1_list = []
keyword2_list = []
keyword3_list = []
keyword4_list = []
keyword5_list = []
comments_list = []
users_count_list = []


# --Main-code--
if __name__ == "__main__":
    path = os.getcwd()
    # html_files = glob.glob(os.path.join(path, "*.html"))
    # html_files += glob.glob(os.path.join(path, "*.htm"))
    html_files = [r"C:\eMazzanti\6sense\FW 6sense Hot Accounts USCAN - NE eMazz ARMA NE List 2    January 9zxc__.html"]
    print("Found", len(html_files), "HTML files")

    for url in html_files:
        # print(url)
        scrap_email(url)

    for name in names_list:
        date_list.append(dt.datetime.today().strftime("%d-%b-%Y"))

    dict = {
        "Date added": date_list,
        "Activity date": activities_date_list,
        "Name": names_list,
        "Website": websites_list,
        "Location": locations_list,
        "Buying stage": buying_stage_list,
        "Profile fit": profile_fit_list,
        "Account reach": account_reach_list,
        "Keyword1": keyword1_list,
        "Keyword2": keyword2_list,
        "Keyword3": keyword3_list,
        "Keyword4": keyword4_list,
        "Keyword5": keyword5_list,
        "Comment": comments_list,
        "Users": users_count_list,
    }

    df_data = pd.DataFrame(dict).sort_values(by="Users")
# df_data

# 2:
# implement watchguard.com 
# 1 column Watchgouard visitors; 1 coulmn list of watchguard visitors