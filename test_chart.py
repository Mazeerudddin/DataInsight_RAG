from sql_agent import run_sql_analysis
from chart_agent import generate_chart

question = (
    "Compare average mileage "
    "across fuel types"
)

result = run_sql_analysis(
    question
)

print(result)

chart_result = generate_chart(
    result
)

print(chart_result)