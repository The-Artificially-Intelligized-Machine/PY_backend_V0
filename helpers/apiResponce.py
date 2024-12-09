from fastapi import HTTPException
from typing import Any, Dict, Optional

def success_response(message: str,status_code: int = 200, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Create a standardized success response for API endpoints.

    Args:
        message (str): A message describing the success of the operation.
        data (Optional[Dict[str, Any]]): Additional data to include in the response. Default is None.

    Returns:
        Dict[str, Any]: A standardized JSON response structure with status "success".
    """
    response = {
        "status_code": status_code,
        "status": "success",
        "message": message,
    }
    if data is not None:
        response["data"] = data
    return response


def error_response(message: str, status_code: int = 400) -> None:
    """
    Create and raise a standardized error response for API endpoints.

    Args:
        message (str): A message describing the error.
        status_code (int): HTTP status code for the error. Default is 400.

    Raises:
        HTTPException: A FastAPI HTTPException with a standardized error structure.
    """
    raise HTTPException(
        status_code=status_code,
        detail={
            "status": "Error",
            "message": message,
        },
    )
