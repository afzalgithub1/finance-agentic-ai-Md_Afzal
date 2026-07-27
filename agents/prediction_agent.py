from langchain.tools import tool

from ml.predictor import predict_next_close


@tool
def prediction_tool(company_name: str) -> str:
    """
    Predict the next trading day's closing price for an Indian stock.

    Input:
        Company name

    Example:
        HDFC_BANK
        RELIANCE
        TCS
        INFOSYS
    """

    try:
        result = predict_next_close(company_name)

        response = (
            f"Prediction for {result['company']}\n\n"
            f"Last Closing Price : ₹{result['last_close']:.2f}\n"
            f"Predicted Next Close : ₹{result['predicted_close']:.2f}\n"
            f"Prediction Date : {result['prediction_date']}"
        )

        return response

    except Exception as ex:
        return f"Prediction failed: {str(ex)}"