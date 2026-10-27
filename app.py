
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="ProfitGuard AI",
    page_icon="🛡️",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("customer_analytics.csv")

df = load_data()

st.title("🛡️ ProfitGuard AI")
st.subheader("Margin-Aware B2B Customer Retention")
st.caption(
    "Decision-support prototype | Synthetic demonstration data | "
    "Rule-based risk scores"
)

# Portfolio KPIs
total_customers = len(df)
high_risk = (df["risk_category"] == "High").sum()
total_revenue = df["annual_revenue"].sum()
total_margin = df["estimated_contribution_margin"].sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Accounts", f"{total_customers:,}")
c2.metric("High-Risk Accounts", f"{high_risk:,}")
c3.metric("Annual Revenue", f"₹{total_revenue:,.0f}")
c4.metric("Estimated Contribution", f"₹{total_margin:,.0f}")

st.divider()

# Risk distribution
left, right = st.columns(2)

with left:
    st.subheader("Customer Risk Distribution")
    risk_counts = (
        df["risk_category"]
        .value_counts()
        .reindex(["High", "Medium", "Low"], fill_value=0)
        .rename_axis("Risk Category")
        .reset_index(name="Customers")
    )

    fig = px.bar(
        risk_counts,
        x="Risk Category",
        y="Customers",
        title="Accounts by Risk Level",
        color="Risk Category",
        color_discrete_map={
            "High": "#D9534F",
            "Medium": "#F0AD4E",
            "Low": "#5CB85C"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Revenue by Industry")
    industry_revenue = (
        df.groupby("industry", as_index=False)["annual_revenue"]
        .sum()
    )

    fig2 = px.pie(
        industry_revenue,
        names="industry",
        values="annual_revenue",
        title="Revenue Contribution by Industry"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Account explorer
st.subheader("Customer Account Explorer")

risk_filter = st.multiselect(
    "Filter by risk category",
    ["High", "Medium", "Low"],
    default=["High", "Medium", "Low"]
)

filtered = df[df["risk_category"].isin(risk_filter)]

st.dataframe(
    filtered[
        [
            "customer_id",
            "company_name",
            "industry",
            "days_since_last_order",
            "churn_risk_score",
            "risk_category",
            "annual_revenue",
            "estimated_contribution_margin"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

st.divider()

# Individual account review
st.subheader("Account Retention Review")

if not filtered.empty:
    selected_id = st.selectbox(
        "Select an account",
        filtered["customer_id"].tolist()
    )

    customer = df[df["customer_id"] == selected_id].iloc[0]

    a, b, c = st.columns(3)
    a.metric("Churn Risk Score", f"{customer['churn_risk_score']}/100")
    b.metric("Risk Category", customer["risk_category"])
    c.metric(
        "Estimated Annual Contribution",
        f"₹{customer['estimated_contribution_margin']:,.0f}"
    )

    
    reasons = []
    score_breakdown = []

    days = int(customer["days_since_last_order"])
    complaints = int(customer["complaints_last_year"])
    satisfaction = int(customer["satisfaction_score"])
    orders = int(customer["orders_last_year"])

    # Match the original churn-scoring rules exactly
    recency_points = (
        40 if days > 90 else
        25 if days > 60 else 0
    )

    complaint_points = (
        25 if complaints >= 5 else
        15 if complaints >= 3 else 0
    )

    satisfaction_points = (
        25 if satisfaction <= 2 else
        10 if satisfaction == 3 else 0
    )

    order_points = 10 if orders <= 5 else 0

    factors = [
        ("Days since last order", days, recency_points,
         "More than 90 days" if days > 90 else
         "More than 60 days" if days > 60 else "Within threshold"),
        ("Complaints last year", complaints, complaint_points,
         "5 or more complaints" if complaints >= 5 else
         "3–4 complaints" if complaints >= 3 else "Within threshold"),
        ("Satisfaction score", satisfaction, satisfaction_points,
         "Low satisfaction" if satisfaction <= 2 else
         "Moderate satisfaction" if satisfaction == 3 else "Within threshold"),
        ("Orders last year", orders, order_points,
         "Low order frequency" if orders <= 5 else "Within threshold")
    ]

    for factor, value, points, explanation in factors:
        score_breakdown.append({
            "Risk Factor": factor,
            "Customer Value": value,
            "Points Added": points,
            "Explanation": explanation
        })

    st.write("**Why this customer received this score**")
    st.dataframe(
        pd.DataFrame(score_breakdown),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "The score is the sum of rule-based points, capped at 100. "
        "These rules are illustrative and have not been statistically "
        "validated against actual churn outcomes."
    )

st.caption(
    "Prototype limitation: Risk scores and contribution margins are "
    "illustrative rules and assumptions, not validated predictions. "
    "Recommendations require human review."
)

# ProfitGuard AI: Retention Action Decision Engine

st.divider()
st.header("💰 Retention Action Decision Engine")
st.write(
    "Compare possible interventions and select the option "
    "with the highest estimated incremental profit."
)

if not filtered.empty:
    st.caption(
        "Illustrative assumptions for demonstration only. "
        "Retention uplift and intervention costs are not "
        "validated using historical business data."
    )

    action_options = {
        "No action": {"uplift": 0.00, "cost": 0},
        "Account manager call": {"uplift": 0.05, "cost": 500},
        "Service recovery": {"uplift": 0.10, "cost": 1500},
        "Personalized discount offer": {"uplift": 0.08, "cost": 2000}
    }

    margin = float(customer["estimated_contribution_margin"])

    # Compare all actions using illustrative retention-uplift assumptions
    comparison = []

    for name, details in action_options.items():
        benefit = details["uplift"] * margin
        cost = details["cost"]
        profit = benefit - cost

        comparison.append({
            "Retention Action": name,
            "Assumed Retention Uplift": f"{details['uplift']:.0%}",
            "Estimated Benefit (₹)": round(benefit, 2),
            "Intervention Cost (₹)": cost,
            "Estimated Incremental Profit (₹)": round(profit, 2)
        })

    comparison_df = pd.DataFrame(comparison)
    ranked = comparison_df.sort_values(
        "Estimated Incremental Profit (₹)",
        ascending=False
    )

    # Automatically identify the best positive-profit action
    best = ranked.iloc[0]
    best_action = best["Retention Action"]
    best_profit = best["Estimated Incremental Profit (₹)"]

    st.subheader("Action Comparison")
    st.dataframe(ranked, use_container_width=True, hide_index=True)

    if best_profit > 0:
        st.success(
            f"Recommended action: {best_action} | "
            f"Estimated incremental profit: ₹{best_profit:,.2f}"
        )
    else:
        best_action = "No action"
        st.warning(
            "No intervention has positive estimated incremental "
            "profit under the current assumptions. Review the account "
            "before spending on retention."
        )

    st.caption(
        "The uplift percentages are hypothetical assumptions, not "
        "validated predictions. This ranking is a scenario analysis, "
        "not proof that an intervention will cause retention."
    )

    st.subheader("Selected Action")

    selected_action = st.selectbox(
        "Choose an action for review",
        list(action_options.keys()),
        index=list(action_options.keys()).index(best_action)
    )

    action = action_options[selected_action]
    expected_profit = action["uplift"] * margin - action["cost"]

    col1, col2, col3 = st.columns(3)

    col1.metric("Estimated Contribution", f"₹{margin:,.2f}")
    col2.metric("Intervention Cost", f"₹{action['cost']:,.2f}")
    col3.metric("Estimated Incremental Profit", f"₹{expected_profit:,.2f}")

    if selected_action == best_action and best_profit > 0:
        st.info("You have selected the automatically recommended action.")
    elif expected_profit <= 0 and selected_action != "No action":
        st.warning("This action has no positive estimated incremental profit.")
    else:
        st.info("Review this alternative against the recommended action.")

    
    st.write("### Human Approval")

    approved = st.checkbox(
        "I approve creating a simulated follow-up task.",
        key=f"approval_{selected_id}_{selected_action}"
    )

    if "task_log" not in st.session_state:
        st.session_state["task_log"] = []

    if st.button("Create Simulated CRM Task"):
        if not approved:
            st.warning("Please approve the action first.")
        else:
            existing_pending = any(
                task["Customer ID"] == selected_id
                and task["Action"] == selected_action
                and task["Status"] == "Pending"
                for task in st.session_state["task_log"]
            )

            if existing_pending:
                st.warning(
                    "A pending task already exists for this "
                    "customer and action."
                )
            else:
                task = {
                    "Customer ID": selected_id,
                    "Customer": customer["company_name"],
                    "Action": selected_action,
                    "Estimated Incremental Profit (₹)": round(
                        expected_profit, 2
                    ),
                    "Status": "Pending"
                }

                st.session_state["task_log"].append(task)

                st.success("Simulated follow-up task created!")

    st.divider()
    st.subheader("Simulated CRM Task Log")

    task_log = st.session_state["task_log"]

    if task_log:
        task_df = pd.DataFrame(task_log)

        st.dataframe(
            task_df.drop(columns=["Customer ID"]),
            use_container_width=True,
            hide_index=True
        )

        pending_tasks = [
            task for task in task_log
            if task["Status"] == "Pending"
        ]

        if pending_tasks:
            st.write("### Update Task Status")

            task_labels = [
                f"{i + 1}. {task['Customer']} — {task['Action']}"
                for i, task in enumerate(task_log)
                if task["Status"] == "Pending"
            ]

            selected_label = st.selectbox(
                "Choose a pending task",
                task_labels
            )

            if st.button("Mark Task as Completed"):
                pending_index = [
                    i for i, task in enumerate(task_log)
                    if task["Status"] == "Pending"
                ][task_labels.index(selected_label)]

                st.session_state["task_log"][pending_index]["Status"] = (
                    "Completed"
                )

                st.success("Task marked as completed.")
                st.rerun()
        else:
            st.info("All simulated follow-up tasks are completed.")

    else:
        st.info("No follow-up tasks have been created yet.")

    st.caption(
        "Tasks are stored in the current Streamlit session. "
        "They are simulated and are not sent to a real CRM system."
    )

    st.divider()
    st.header("📊 Business Impact Dashboard")

    tasks = st.session_state.get("task_log", [])
    impact_df = pd.DataFrame(tasks)

    if not impact_df.empty:
        total_tasks = len(impact_df)
        completed_tasks = (
            impact_df["Status"] == "Completed"
        ).sum()
        pending_tasks = (
            impact_df["Status"] == "Pending"
        ).sum()

        completion_rate = (
            completed_tasks / total_tasks * 100
            if total_tasks else 0
        )

        estimated_profit = impact_df[
            "Estimated Incremental Profit (₹)"
        ].sum()

        k1, k2, k3, k4 = st.columns(4)

        k1.metric("Tasks Created", total_tasks)
        k2.metric("Tasks Completed", int(completed_tasks))
        k3.metric("Tasks Pending", int(pending_tasks))
        k4.metric("Task Completion Rate", f"{completion_rate:.1f}%")

        st.subheader("Tasks by Retention Action")

        action_counts = (
            impact_df["Action"]
            .value_counts()
            .rename_axis("Action")
            .reset_index(name="Number of Tasks")
        )

        fig_tasks = px.bar(
            action_counts,
            x="Action",
            y="Number of Tasks",
            title="Simulated Follow-up Activity"
        )

        st.plotly_chart(
            fig_tasks,
            use_container_width=True
        )

        st.subheader("Estimated Financial Impact")

        st.metric(
            "Sum of Estimated Incremental Profit",
            f"₹{estimated_profit:,.2f}"
        )

        st.caption(
            "This is the sum of scenario estimates attached to "
            "created tasks, not realized profit or proven savings. "
            "Completed tasks do not necessarily mean customers were "
            "retained. Real impact requires outcome and cost data."
        )

    else:
        st.info(
            "Create a simulated follow-up task to begin tracking "
            "workflow metrics."
        )
