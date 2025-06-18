#!/usr/bin/env python
# coding: utf-8

# In[13]:


from bs4 import BeautifulSoup
import csv

def extract_tenders_from_file(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Get the first table in the document (should be the tender table)
    table = soup.find('table')
    if not table:
        print("❌ Could not find any table in the file.")
        return []

    tenders = []
    rows = table.find_all('tr')[1:]  # skip the header row

    for row in rows[:20]:  # limit to 20 tenders
        cols = row.find_all('td')
        if len(cols) < 10:
            continue

        nit = cols[1].get_text(strip=True)
        name_of_work = cols[2].get_text(strip=True)
        estimated_cost = cols[4].get_text(strip=True)
        emd_amount = cols[5].get_text(strip=True)
        bid_close = cols[6].get_text(strip=True)
        bid_open = cols[7].get_text(strip=True)

        tenders.append({
            "NIT/RFP NO": nit,
            "Name of Work": name_of_work,
            "Estimated Cost": estimated_cost,
            "Bid Submission Closing Date & Time": bid_close,
            "EMD Amount": emd_amount,
            "Bid Opening Date & Time": bid_open
        })

    return tenders

def save_to_csv(data, filename='tenders.csv'):
    if not data:
        print("⚠️ No data to save.")
        return

    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print(f"✅ Extracted {len(data)} tenders to {filename}")

if __name__ == "__main__":
    tenders = extract_tenders_from_file("tenders.html")
    save_to_csv(tenders)


# In[ ]:




