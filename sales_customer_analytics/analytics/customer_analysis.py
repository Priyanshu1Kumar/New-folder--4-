import pandas as pd

def rfm_analysis(data):
    snapshot_date = data["Order_Date"].max()

    rfm = data.groupby("Customer_Name").agg({
        "Order_Date": lambda x: (snapshot_date - x.max()).days,
        "Order_ID": "count",
        "Revenue": "sum"
    })

    rfm.columns = ["Recency", "Frequency", "Monetary"]

    rfm["Risk"] = pd.qcut(
        rfm["Recency"],
        q=3,
        labels=["Low Risk", "Medium Risk", "High Risk"]
    )

    return rfm.reset_index()
