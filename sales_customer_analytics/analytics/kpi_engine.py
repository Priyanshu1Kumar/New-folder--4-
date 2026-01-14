def compute_kpis(data, target_revenue):
    total_revenue = data["Revenue"].sum()
    total_orders = data["Order_ID"].nunique()
    total_customers = data["Customer_ID"].nunique()
    avg_order_value = round(total_revenue / total_orders, 2) if total_orders else 0

    health_score = min(100, int((total_revenue / target_revenue) * 100))

    status = "Good"
    if health_score < 50:
        status = "Critical"
    elif health_score < 80:
        status = "Warning"

    return {
        "revenue": total_revenue,
        "orders": total_orders,
        "customers": total_customers,
        "aov": avg_order_value,
        "score": health_score,
        "status": status
    }
