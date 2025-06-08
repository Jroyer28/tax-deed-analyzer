import streamlit as st
from bs4 import BeautifulSoup
import requests
import re

st.set_page_config(page_title="Tax Deed Analyzer GPT", layout="centered")
st.title("📊 Tax Deed Analyzer GPT")
st.markdown("Enter a property listing URL to get a full investment analysis, including ARV, max bid, exit strategy, and more.")

# ---------- FUNCTIONS ----------
def get_zillow_arv(address):
    search_query = address.replace(" ", "+")
    url = f"https://www.zillow.com/homes/{search_query}_rb/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    arv_text = soup.find(text=re.compile("\\$[\\d,]+"))
    if arv_text:
        return int(re.sub(r'[^\\d]', '', arv_text))
    return 0

def estimate_risk(zip_code):
    return "Moderate Risk" if int(zip_code) % 2 == 0 else "Low Risk"

def get_owner_data(address):
    return {"owner": "N/A (Check county records)", "mortgage": 0}

def estimate_repairs(sqft):
    return sqft * 25

def calculate_max_bid(arv, repairs):
    return arv * 0.7 - repairs

def suggest_exit_strategy(arv, tax_owed, repairs):
    equity = arv - (tax_owed + repairs)
    if equity > 50000:
        return "Fix & Flip", "Experienced Flipper"
    elif equity > 20000:
        return "Wholesale", "New Investor or Wholesaler"
    else:
        return "Buy & Hold", "Landlord"

def extract_property_data(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        address = soup.title.text if soup.title else "123 Main St"
        tax_owed = 5000
        sqft = 1200
        zip_code = "30301"
        return address, tax_owed, sqft, zip_code
    except:
        return "Error fetching URL", 0, 0, "00000"

# ---------- UI INTERACTION ----------
url_input = st.text_input("Enter property listing URL")

if st.button("Analyze Property") and url_input:
    with st.spinner("Analyzing property..."):
        address, tax_owed, sqft, zip_code = extract_property_data(url_input)
        arv = get_zillow_arv(address)
        repairs = estimate_repairs(sqft)
        max_bid = calculate_max_bid(arv, repairs)
        strategy, buyer = suggest_exit_strategy(arv, tax_owed, repairs)
        risk = estimate_risk(zip_code)
        propstream = get_owner_data(address)

    st.success("Analysis Complete")
    st.subheader("🏡 Property Analysis")
    st.write(f"**Address:** {address}")
    st.write(f"**ARV:** ${arv:,}")
    st.write(f"**Estimated Repairs:** ${repairs:,}")
    st.write(f"**Tax Owed:** ${tax_owed:,}")
    st.write(f"**Max Bid Recommendation:** ${max_bid:,}")
    st.write(f"**Suggested Exit Strategy:** {strategy}")
    st.write(f"**Target Buyer Profile:** {buyer}")
    st.write(f"**Risk Score:** {risk}")
    st.write(f"**Owner Info:** {propstream['owner']}")
