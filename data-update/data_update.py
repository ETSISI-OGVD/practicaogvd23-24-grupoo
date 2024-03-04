import argparse
import pandas as pd
import numpy as np
import mlflow


def main():
    """Main function of the script."""

    # input and output arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-data", type=str, help="path to input data")
    parser.add_argument("--output-data", type=str, help="path to output data")

    args = parser.parse_args()

    # Start Logging
    mlflow.start_run()

    # enable autologging
    mlflow.sklearn.autolog()

    print(" ".join(f"{k}={v}" for k, v in vars(args).items()))
    print("input data:", args.data)

    df = pd.read_csv(
        args.input_data,
        dtype={"status": "category", "city": "category", "state": "category", "zip_code": "category", "bed": "Int32", "bath": "Int32"},
        parse_dates=["prev_sold_date"],
    )

    df[["house_size", "acre_lot"]] = df[["house_size", "acre_lot"]] / 10.764

    df.dropna(subset = ["price"], inplace=True)
    df.dropna(inplace=True)

    df = pd.concat([df, pd.get_dummies(df["status"], prefix="status").astype("float")], axis=1).drop(["status"], axis=1)

    df["city"] = df["city"].cat.remove_unused_categories()
    df["state"] = df["state"].cat.remove_unused_categories()
    df["zip_code"] = df["zip_code"].cat.remove_unused_categories()

    df["mean_city_price"] = df.groupby("city", observed=True)["price"].transform("mean")
    df["mean_state_price"] = df.groupby("state", observed=True)["price"].transform("mean")
    df["mean_zip_price"] = df.groupby("zip_code", observed=True)["price"].transform("mean")

    df.drop(["city", "state", "zip_code"], axis=1, inplace=True)

    df[['bed', 'bath', 'acre_lot', 'house_size', 'price']] = np.log(1. + df[['bed', 'bath', 'acre_lot', 'house_size', 'price']])

    df.to_csv(args.output_data, index=False)

    # Stop Logging
    mlflow.end_run()

if __name__ == "__main__":
    main()