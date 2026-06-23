SELECT
dt,
revenue
FROM daily_sales

from prophet import Prophet

df.columns=["ds","y"]

model=Prophet()

model.fit(df)

future=model.make_future_dataframe(
    periods=90
)

forecast=model.predict(
    future
)


px.line(
    forecast,
    x="ds",
    y="yhat"
)