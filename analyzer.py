from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt

def analyze() :
    df = pd.read_csv("products.csv")

    df = df.dropna(
        subset=["price_number"]
    )

    X = df[["price_number"]]
    y = df["likes"]

    model = LinearRegression()
    model.fit(X, y)

    print(model.coef_)
    print(model.score(X, y))

    plt.scatter(
        df["price_number"],
        df["likes"]
    )

    plt.xlabel("Price")
    plt.ylabel("Likes")

    plt.show()