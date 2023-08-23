# Script fetches hunter.io data by API
# Creation date: 18 AUG 2023
# Last modification: 18 AUG 2023
# Made by: Kamil Smolag

import requests
import pandas as pd
import datetime as dt

def get_hunter_emails_from_domain(domain, api_key):
    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&type=personal&department=executive,it,management,operations&api_key={api_key}"
    response = requests.get(url)
    data = response.json()
    domain_emails = []
    if data.get("data", {}).get("emails"):
        domain_emails.extend(data['data']['emails'])
        return domain_emails
    else:
        return []

def get_uplead_emails_from_domain(domain, api_key):
    pass

def run_hunter_api():
    api_key_hunter = '3d113e7839b6c17a4b0aa48c4164f8c040c49f6b'
    filename = "websites_only_Legal_17-Aug-2023.csv"
    data = pd.read_csv(filename)
    
    all_emails_data = []
    for domain in data['Website']:
        hunter_emails = get_hunter_emails_from_domain(domain, api_key_hunter)
        # Hunter.io loop
        for email in hunter_emails:
            email_data = {
                'Platform': 'Hunter',
                'Domain': domain,
                'Email': email['value'],
                'First Name': email['first_name'],
                'Last Name': email['last_name'],
                'Phone number': email['phone_number'],
                'Position': email['position'],
                'Department': email['department'],
                'Twitter handle': email['twitter'],
                'LinkedIn URL': email['linkedin'],
                'Verification': email['verification']['status'],
            }
            all_emails_data.append(email_data)
    
    results_df = pd.DataFrame(all_emails_data)
    print(results_df)
    current_date = dt.datetime.now().strftime("%d-%b-%Y")
    results_df.to_excel(f"emails_{current_date}_Hunter.xlsx", index=False)
    
    print(f"Total {len(all_emails_data)} emails found.")

if __name__ == "__main__":
    run_hunter_api()