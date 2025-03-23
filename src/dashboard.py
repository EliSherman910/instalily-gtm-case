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
    Assume you previously reached out about DuPont Tedlar protective films for signage, and havent heard back.
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

    if not os.path.exists(DATA_PATH):
        st.error("No contact data found. Please generate contacts/messages first.")
        return

    df = pd.read_csv(DATA_PATH)

    # --- Sidebar: Company Selector ---
    companies = sorted(df["company"].unique())
    selected_company = st.sidebar.selectbox("🏢 Select a company to view its contacts", ["None", "All"] + companies)

    # --- Search and Filters ---
    st.sidebar.subheader("🔎 Search & Filters")
    search_term = st.sidebar.text_input("Search by name, title, or company")
    outreach_filter = st.sidebar.selectbox("Filter by Outreach Status", ["All", "Sent", "Not Sent"])
    followup_filter = st.sidebar.selectbox("Filter by Follow-Up Status", ["All", "Due", "Not Due"])

    
    if selected_company == "None":
        st.info("👈 Use the sidebar to select a company or search across all leads.")
        return
    company_df = df if selected_company == "All" else df[df["company"] == selected_company]
    filtered_df = company_df.copy()

    # Search filter
    if search_term:
        search_term = search_term.lower()
        filtered_df = filtered_df[
            filtered_df["name"].str.lower().str.contains(search_term) |
            filtered_df["title"].str.lower().str.contains(search_term) |
            filtered_df["company"].str.lower().str.contains(search_term)
        ]

    # Outreach status filter
    if outreach_filter != "All":
        updated_outreach = filtered_df["company"].copy()
        for idx, row in filtered_df.iterrows():
            sent_flag = f"sent_{idx}"
            if isinstance(st.session_state.get(sent_flag), dict):
                row["last_outreach_date"] = st.session_state[sent_flag]["last_outreach_date"]
        sent_mask = filtered_df["last_outreach_date"].notna() & (filtered_df["last_outreach_date"].astype(str).str.strip() != "")
        if outreach_filter == "Sent":
            filtered_df = filtered_df[sent_mask]
        elif outreach_filter == "Not Sent":
            filtered_df = filtered_df[~sent_mask]

    # Follow-up status filter
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
    sent_count = 0
    followups_due = 0

    # --- Charts ---
    with st.container():
        with st.spinner("Loading charts..."):
            st.subheader("📈 Outreach Analytics")

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
            outreach_sent = pd.notna(row.get("last_outreach_date")) and row.get("last_outreach_date") != ""

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
                # Add to activity log
                activity_entry = f"[{datetime.now()}] Marked {row['name']} ({row['title']}, {row['company']}) as contacted."
                st.session_state.get('activity_log', []).append(activity_entry)
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

                st.success("Marked as sent. Follow-up scheduled in 7 days.")
                outreach_sent = True
                just_marked_sent = True

                # Auto-save update to CSV
                df.to_csv(DATA_PATH, index=False)

        if outreach_sent:
            sent_count += 1

            try:
                next_followup = row.get("next_followup_date") or st.session_state.get(sent_flag, {}).get("next_followup_date")
                if isinstance(next_followup, str) and next_followup:
                    followup_date = datetime.fromisoformat(next_followup).date()
                    today = datetime.now().date()
                    followup_due = followup_date <= today
                    days_remaining = (followup_date - today).days
            except Exception as e:
                followup_due = False

            if followup_due:
                followups_due += 1

            if days_remaining is not None and days_remaining > 0:
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
                    st.success("Follow-up message generated!")

        followup_key = f"followup_text_{idx}"
        default_followup = str(row.get("followup_message", "")) if not pd.isna(row.get("followup_message", "")) else ""

        if default_followup.strip():
            followup_text = st.text_area(
                f"✍️ Edit Follow-Up Message ({row['name']})",
                key=followup_key,
                label_visibility="visible"
            )
            # Update DataFrame only, don't overwrite st.session_state again
            row["followup_message"] = followup_text
            df.loc[df_idx, "followup_message"] = followup_text
            df.loc[df_idx, "followup_message"] = followup_text

            if st.button(f"📋 Copy Follow-Up to Clipboard ({row['name']})", key=f"copy_followup_{idx}"):
                pyperclip.copy(followup_text)
                st.success("Follow-up message copied to clipboard!")

            if st.button(f"😴 Snooze 3 Days ({row['name']})", key=f"snooze_{idx}"):
                try:
                    new_date = datetime.now().date() + timedelta(days=3)
                    row["next_followup_date"] = new_date.isoformat()
                    df.loc[df_idx, "next_followup_date"] = row["next_followup_date"]
                    st.success(f"Snoozed. Next follow-up set for {new_date}.")
                except:
                    st.error("Error snoozing follow-up.")

    st.sidebar.metric("Total Leads", total_leads)
    st.sidebar.metric("Outreach Sent", sent_count)
    st.sidebar.metric("Follow-Ups Due", followups_due)

    # --- Activity Log ---
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

    if st.button("💾 Save All Updates"):
        for idx, row in company_df.iterrows():
            df_idx = row.name
            sent_flag = f"sent_{idx}"
            if isinstance(st.session_state.get(sent_flag), dict):
                df.loc[df_idx, "last_outreach_date"] = st.session_state[sent_flag]["last_outreach_date"]
                df.loc[df_idx, "next_followup_date"] = st.session_state[sent_flag]["next_followup_date"]
            followup_key = f"followup_text_{idx}"
            if followup_key in st.session_state:
                df.loc[df_idx, "followup_message"] = st.session_state[followup_key]

        df.to_csv(DATA_PATH, index=False)
        st.success("All updates saved!")

if __name__ == "__main__":
    main()

