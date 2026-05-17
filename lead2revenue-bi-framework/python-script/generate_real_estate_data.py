import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

# --------------------------
# CONFIG
# --------------------------
NUM_LEADS = 10000
NUM_BOOKINGS_TARGET = 600

sources = ["Google Ads", "Facebook", "99acres", "Housing", "Referral", "Channel Partner", "Walk-in"]
cities = ["Gurgaon", "Noida", "Mumbai", "Pune", "Bangalore", "Hyderabad"]
property_types = ["Apartment", "Villa", "Plot"]
projects = ["Sky Residency", "Elite Heights", "Green Valley", "Urban Square", "Palm Towers"]
sales_owners = ["Aman Sharma", "Ravi Mehta", "Priya Kapoor", "Neha Singh","Rohit Sharma","Viral Kohli","Sachin Tendulkar","Praveen Tambe","Shefali Mehta","Riya Kapoor"]

# --------------------------
# LEADS DATA
# --------------------------
leads = []

start_date = datetime(2024, 1, 1)

for i in range(1, NUM_LEADS + 1):
    source = random.choices(
        sources,
        weights=[30, 20, 15, 10, 10, 10, 5]
    )[0]

    city = random.choices(
        cities,
        weights=[25, 20, 15, 15, 15, 10]
    )[0]

    budget = random.randint(30, 200) * 100000  # 30L to 2Cr

    lead = {
        "LeadID": i,
        "LeadDate": start_date + timedelta(days=random.randint(0, 365)),
        "Source": source,
        "City": city,
        "Budget": budget,
        "PropertyType": random.choice(property_types),
        "Project": random.choice(projects),
        "SalesOwner": random.choice(sales_owners),
    }

    leads.append(lead)

leads_df = pd.DataFrame(leads)

# --------------------------
# FOLLOWUPS DATA
# --------------------------
followups = []

for _, row in leads_df.iterrows():
    num_followups = random.randint(1, 5)

    for j in range(num_followups):
        response_time = random.randint(1, 120)

        followups.append({
            "FollowUpID": f"{row['LeadID']}_{j}",
            "LeadID": row["LeadID"],
            "FollowUpDate": row["LeadDate"] + timedelta(days=j),
            "CallDuration": random.randint(1, 15),
            "ResponseTimeMins": response_time,
            "SiteVisit": random.choices(["Yes", "No"], weights=[30, 70])[0]
        })

followups_df = pd.DataFrame(followups)

# --------------------------
# BOOKINGS DATA (SMART LOGIC)
# --------------------------
bookings = []

for _, row in leads_df.iterrows():

    base_prob = 0.05

    # Source logic
    if row["Source"] == "Referral":
        base_prob += 0.15
    elif row["Source"] == "Facebook":
        base_prob += 0.08
    elif row["Source"] == "Google Ads":
        base_prob += 0.03

    # Budget logic
    if row["Budget"] > 10000000:
        base_prob += 0.05

    # Followup logic
    lead_followups = followups_df[followups_df["LeadID"] == row["LeadID"]]

    if len(lead_followups) >= 3:
        base_prob += 0.05

    if (lead_followups["ResponseTimeMins"] < 15).any():
        base_prob += 0.05

    # Final decision
    if random.random() < base_prob:

        bookings.append({
            "BookingID": f"B{row['LeadID']}",
            "LeadID": row["LeadID"],
            "BookingDate": row["LeadDate"] + timedelta(days=random.randint(5, 60)),
            "BookingAmount": row["Budget"] * random.uniform(0.9, 1.2),
            "PaymentStatus": random.choice(["Paid", "Partial", "Pending"])
        })

bookings_df = pd.DataFrame(bookings)

# --------------------------
# CAMPAIGN DATA
# --------------------------
campaigns = []

for i in range(1, 151):
    source = random.choice(sources)

    spend = random.randint(50000, 500000)

    leads_generated = random.randint(50, 300)

    campaigns.append({
        "CampaignID": i,
        "Source": source,
        "Month": random.randint(1, 12),
        "Spend": spend,
        "Clicks": random.randint(1000, 10000),
        "LeadsGenerated": leads_generated
    })

campaign_df = pd.DataFrame(campaigns)

# --------------------------
# EXPORT CSVs
# --------------------------
leads_df.to_csv("leads.csv", index=False)
followups_df.to_csv("followups.csv", index=False)
bookings_df.to_csv("bookings.csv", index=False)
campaign_df.to_csv("campaign_spend.csv", index=False)

print("✅ Data Generated Successfully!")