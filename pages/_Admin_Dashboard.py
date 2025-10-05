# admin_app.py
import streamlit as st
import requests

st.set_page_config(page_title="Admin Dashboard", layout="wide")
st.title("🛠️ Admin Dashboard")

PROCEDURES = "https://8000-dep-01k6sj99nxkqpr1m5srkmwgyk8-d.cloudspaces.litng.ai/procedure"
SERVICES = "https://8000-dep-01k6sj99nxkqpr1m5srkmwgyk8-d.cloudspaces.litng.ai/service"
PRODUCTS = "https://8000-dep-01k6sj99nxkqpr1m5srkmwgyk8-d.cloudspaces.litng.ai/product"

st.header("Procedures Management")

try:
    resp = requests.get(PROCEDURES+"/all")
    procedures = resp.json()
except:
    procedures = []
    st.warning("Could not fetch procedures from backend.")

for proc in procedures:
    with st.expander(f"{proc['title']} (ID: {proc['id']})"):
        st.write(proc["description"])
        for step in proc.get("steps", []):
            st.markdown(f"- Step {step['step_number']}: {step['title']}")
        if st.button(f"Delete Procedure {proc['id']}"):
            requests.delete(f"{PROCEDURES}/delete/{proc['id']}")
            st.success(f"Deleted procedure {proc['id']}")
            st.rerun()


st.subheader("Add New Procedure")
with st.form("add_proc"):
    title = st.text_input("Procedure Title")
    description = st.text_area("Procedure Description")
    steps_raw = st.text_area("Steps (format: step_number|title|description per line)")
    submitted = st.form_submit_button("Add Procedure")
    if submitted:
        steps = []
        for line in steps_raw.strip().split("\n"):
            try:
                step_number, step_title, step_desc = line.split("|")
                steps.append({
                    "step_number": int(step_number),
                    "title": step_title.strip(),
                    "description": step_desc.strip()
                })
            except:
                st.error(f"Invalid step line: {line}")
        data = {"title": title, "description": description, "steps": steps}
        r = requests.post(PROCEDURES+"/add", json=data)
        if r.status_code == 201:
            st.success("Procedure added successfully!")
            st.rerun()
        else:
            st.error(f"Error adding procedure: {r.text}")

st.header("Services Management")

try:
    resp = requests.get(SERVICES+'/all')
    Services = resp.json()
except:
    Services = []
    st.warning("Could not fetch Services from backend.")

for sub in Services:
    st.markdown(f"- **{sub['service_name']}** | Category: {sub['category']} | Price: ${sub['service_price']}")
    if st.button(f"Delete Service {sub['service_name']}"):
        requests.delete(f"{SERVICES}/delete/{sub['service_id']}")
        st.success(f"Deleted Service {sub['service_name']}")
        st.rerun()

st.subheader("Add New Service")
with st.form("add_sub"):
    name = st.text_input("Service Name")
    price = st.number_input("Price", min_value=0.0, format="%.2f")
    category = st.text_input("Category")
    submitted_sub = st.form_submit_button("Add Service")
    if submitted_sub:
        data = {"name": name, "price": price, "category": category}
        r = requests.post(SERVICES+"/add", json=data)
        if r.status_code == 201:
            st.success("Service added successfully!")
            st.rerun()
        else:
            st.error(f"Error adding Service: {r.text}")

st.header("Products Management")

try:
    resp = requests.get(PRODUCTS+"/all")
    products = resp.json()
except:
    products = []
    st.warning("Could not fetch products from backend.")

for prod in products:
    st.markdown(f"- **{prod['title']}** | Price: ${prod['price']}")
    if st.button(f"Delete Product {prod['title']}"):
        requests.delete(f"{PRODUCTS}/delete/{prod['id']}")
        st.success(f"Deleted product {prod['title']}")
        st.rerun()

st.subheader("Add New Product")
with st.form("add_prod"):
    title = st.text_input("Product Title")
    price = st.number_input("Price", min_value=0.0, format="%.2f")
    category = st.text_input("Product Category")
    submitted_prod = st.form_submit_button("Add Product")
    if submitted_prod:
        data = {"title": title, "price": price,"category": category}
        r = requests.post(PRODUCTS+"/add", json=data)
        if r.status_code == 201:
            st.success("Product added successfully!")
            st.rerun()
        else:
            st.error(f"Error adding product: {r.text}")

st.title("🧠 Embedding Creator")

if st.button("Create Embeddings"):
    if "token" not in st.session_state:
        st.warning("⚠️ Please sign in first.")
    else:
        with st.spinner("Creating embeddings..."):
            try:
                response = requests.get(
                    "https://8000-dep-01k6sj99nxkqpr1m5srkmwgyk8-d.cloudspaces.litng.ai/create-embedding/",
                    timeout=120
                )
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"✅ {data.get('count', 0)} embeddings created successfully!")
                else:
                    st.error(f"⚠️ Server error: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("⚠️ Could not connect to backend.")
            except Exception as e:
                st.error(f"⚠️ Unexpected error: {e}")