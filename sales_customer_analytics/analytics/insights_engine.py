def generate_insights(kpis, growth_rate):
    insights = []

    if kpis["score"] < 50:
        insights.append("Overall business health is critical.")

    if growth_rate < 0:
        insights.append("Sales trend shows decline.")

    if kpis["aov"] < 10000:
        insights.append("Average order value is low. Upselling recommended.")

    if not insights:
        insights.append("Business performance indicators are positive.")

    return insights
    