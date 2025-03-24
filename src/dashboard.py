import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from openai import OpenAI
from dotenv import load_dotenv
import os
import pyperclip
import altair as alt

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DATA_PATH = "data/contacts_with_messages.csv"

def generate_followup_message(name, title, company):
    prompt = f"""
    Write a short and polite follow up message to {name}, the {title} at {company}.
    Assume you previously reached out about DuPont Tedlar protective films for signage, and haven't heard back.
    Make sure it is professional, polite and friendly, and include a soft invitation to connect. 
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating follow-up: {e}"

def main():
    st.title("Lead Outreach Dashboard")

    if 'activity_log' not in st.session_state:
        st.session_state['activity_log'] = []

    if not os.path.exists(DATA_PATH):
        st.error("No contact data found. Please generate contacts/messages first.")
        return

    df = pd.read_csv(DATA_PATH)
    df["last_outreach_date"] = pd.to_datetime(df["last_outreach_date"], errors="coerce")
    df["next_followup_date"] = pd.to_datetime(df["next_followup_date"], errors="coerce")

    if 'activity_log_initialized' not in st.session_state:
        st.session_state['activity_log'] = []
        for _, row in df.iterrows():
            if pd.notna(row["last_outreach_date"]):
                timestamp = row["last_outreach_date"].strftime("%Y-%m-%dT%H:%M:%S")
                log = f"[{timestamp}] Marked {row['name']} ({row['title']}, {row['company']}) as contacted."
                st.session_state['activity_log'].append(log)
        st.session_state['activity_log_initialized'] = True

    for idx in range(len(df)):
        sent_flag = f"sent_{idx}"
        if isinstance(st.session_state.get(sent_flag), dict):
            df.at[idx, "last_outreach_date"] = st.session_state[sent_flag]["last_outreach_date"]
            df.at[idx, "next_followup_date"] = st.session_state[sent_flag]["next_followup_date"]

    companies = sorted(df["company"].unique())
    selected_company = st.sidebar.selectbox("🏢 Select a company to view its contacts", ["None", "All"] + companies)

    st.sidebar.subheader("🔎 Search & Filters")
    search_term = st.sidebar.text_input("Search by name, title, or company")
    outreach_filter = st.sidebar.selectbox("Filter by Outreach Status", ["All", "Sent", "Not Sent"])
    followup_filter = st.sidebar.selectbox("Filter by Follow-Up Status", ["All", "Due", "Not Due"])

    if selected_company == "None":
        st.info("👈 Use the sidebar to select a company or search across all leads.")
        return

    company_df = df if selected_company == "All" else df[df["company"] == selected_company]
    filtered_df = company_df.copy()

    if search_term:
        search_term = search_term.lower()
        filtered_df = filtered_df[
            filtered_df["name"].str.lower().str.contains(search_term) |
            filtered_df["title"].str.lower().str.contains(search_term) |
            filtered_df["company"].str.lower().str.contains(search_term)
        ]

    if outreach_filter != "All":
        sent_mask = filtered_df["last_outreach_date"].notna()
        if outreach_filter == "Sent":
            filtered_df = filtered_df[sent_mask]
        elif outreach_filter == "Not Sent":
            filtered_df = filtered_df[~sent_mask]

    if followup_filter != "All":
        today = datetime.now().date()
        followup_dates = pd.to_datetime(filtered_df["next_followup_date"], errors="coerce")
        if followup_filter == "Due":
            filtered_df = filtered_df[followup_dates <= pd.to_datetime(today)]
        elif followup_filter == "Not Due":
            filtered_df = filtered_df[followup_dates > pd.to_datetime(today)]

    # --- Analytics ---
    st.sidebar.header("📊 Analytics")
    total_leads = len(company_df)
    sent_count = company_df["last_outreach_date"].notna().sum()
    followups_due = (company_df["next_followup_date"] <= pd.to_datetime(datetime.now().date())).sum()

    st.sidebar.metric("Total Leads", total_leads)
    st.sidebar.metric("Outreach Sent", sent_count)
    st.sidebar.metric("Follow-Ups Due", followups_due)

    st.sidebar.subheader("📖 Activity Log")
    with st.sidebar.expander("View Activity Log"):
        for log_entry in st.session_state.get('activity_log', []):
            try:
                log_date = log_entry.split(']')[0][1:]
                log_message = log_entry.split(']')[1].strip()
                log_date_parsed = datetime.fromisoformat(log_date)
                log_display = f"{log_date_parsed.strftime('%A, %B %d (%Y) %I:%M %p')}: {log_message}"
                st.markdown(f"- {log_display}")
            except:
                st.markdown(f"- {log_entry}")

    st.subheader("📈 Outreach Analytics")
    with st.container():
        chart_data = pd.DataFrame({
            "Status": ["Sent", "Not Sent"],
            "Count": [
                company_df["last_outreach_date"].notna().sum(),
                company_df["last_outreach_date"].isna().sum()
            ]
        })
        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X("Status", sort=None),
            y="Count",
            color="Status"
        ).properties(width=400, height=300)
        st.altair_chart(chart, use_container_width=True)

        today = datetime.now().date()
        followup_dates = pd.to_datetime(company_df["next_followup_date"], errors="coerce")
        due_count = (followup_dates <= pd.to_datetime(today)).sum()
        not_due_count = (followup_dates > pd.to_datetime(today)).sum()

        st.subheader("📬 Follow-Up Status")
        st.dataframe(pd.DataFrame({
            "Follow-Up": ["Due", "Not Due"],
            "Count": [due_count, not_due_count]
        }))

    for idx, row in filtered_df.iterrows():
        df_idx = row.name

        st.divider()
        st.subheader(f"{row['name']} – {row['title']} at {row['company']}")
        st.markdown(f"[LinkedIn Profile]({row['linkedin_url']})")

        sent_flag = f"sent_{idx}"
        sent_data = st.session_state.get(sent_flag, None)
        if isinstance(sent_data, dict):
            row["last_outreach_date"] = sent_data["last_outreach_date"]
            row["next_followup_date"] = sent_data["next_followup_date"]
            outreach_sent = True
        else:
            outreach_sent = pd.notna(row.get("last_outreach_date"))

        followup_due = False
        days_remaining = None
        just_marked_sent = False

        with st.expander("✉️ Initial Message"):
            initial_message = st.text_area(
                f"Edit Initial Outreach ({row['name']})",
                value=row.get("outreach_message", ""),
                key=f"initial_msg_{idx}"
            )
            row["outreach_message"] = initial_message
            df.loc[df_idx, "outreach_message"] = initial_message

            if st.button(f"📋 Copy Initial Message ({row['name']})", key=f"copy_initial_{idx}"):
                pyperclip.copy(initial_message)
                st.success("Initial outreach message copied to clipboard!")

        if not outreach_sent:
            if st.button(f"✅ Mark as Sent ({row['name']})", key=f"sent_btn_{idx}"):
                today = datetime.now().date()
                last_outreach = today.isoformat()
                next_followup = (today + timedelta(days=7)).isoformat()

                st.session_state[sent_flag] = {
                    "last_outreach_date": last_outreach,
                    "next_followup_date": next_followup
                }

                row["last_outreach_date"] = last_outreach
                row["next_followup_date"] = next_followup
                df.loc[df_idx, "last_outreach_date"] = last_outreach
                df.loc[df_idx, "next_followup_date"] = next_followup

                log_message = f"[{datetime.now()}] Marked {row['name']} ({row['title']}, {row['company']}) as contacted."
                st.session_state['activity_log'].append(log_message)

                df.to_csv(DATA_PATH, index=False)

                st.rerun()

        if outreach_sent:
            try:
                next_followup = row.get("next_followup_date") or st.session_state.get(sent_flag, {}).get("next_followup_date")
                if isinstance(next_followup, str):
                    followup_date = datetime.fromisoformat(next_followup).date()
                else:
                    followup_date = next_followup.date()
                today = datetime.now().date()
                followup_due = followup_date <= today
                days_remaining = (followup_date - today).days
            except:
                followup_due = False

            if days_remaining and days_remaining > 0:
                st.info(f"⏳ {days_remaining} days until follow-up.")
            if followup_due:
                st.warning("⏰ Time to follow up!")

            generate_key = f"generate_followup_{idx}"
            followup_key = f"followup_text_{idx}"

            if just_marked_sent or followup_due or not st.session_state.get(followup_key, '').strip():
                if st.button(f"🪄 Generate Follow-Up ({row['name']})", key=generate_key):
                    with st.spinner("Generating follow-up message..."):
                        followup = generate_followup_message(row['name'], row['title'], row['company'])
                        st.session_state[followup_key] = followup
                        row["followup_message"] = followup
                        df.loc[df_idx, "followup_message"] = followup
                        df.to_csv(DATA_PATH, index=False)
                    st.success("Follow-up message generated!")

        followup_msg = st.session_state.get(f"followup_text_{idx}", row.get("followup_message", ""))

        if isinstance(followup_msg, str) and followup_msg.strip():
            followup_key = f"followup_text_{idx}"

            if followup_key not in st.session_state:
                st.session_state[followup_key] = followup_msg

            followup_text = st.text_area(
                f"✍️ Edit Follow-Up Message ({row['name']})",
                key=followup_key
            )

            row["followup_message"] = followup_text
            df.loc[df_idx, "followup_message"] = followup_text

            if st.button(f"📋 Copy Follow-Up to Clipboard ({row['name']})", key=f"copy_followup_{idx}"):
                pyperclip.copy(followup_text)
                st.success("Follow-up message copied to clipboard!")

            if st.button(f"😴 Snooze 3 Days ({row['name']})", key=f"snooze_{idx}"):
                new_date = datetime.now().date() + timedelta(days=3)
                row["next_followup_date"] = new_date.isoformat()
                df.loc[df_idx, "next_followup_date"] = new_date
                st.success(f"Snoozed. Next follow-up set for {new_date}.")
                df.to_csv(DATA_PATH, index=False)

if __name__ == "__main__":
    main()

