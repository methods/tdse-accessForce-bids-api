"""
This file contains tests for the helper functions in helpers.py
"""
import pytest
from helpers.helpers import (
    prepend_host_to_links,
    validate_pagination,
    validate_sort,
)


# Case 1: Host is prepended to values in links object
def test_prepend_host():
    resource = {
        "_id": "9f688442-b535-4683-ae1a-a64c1a3b8616",
        "alias": "ONS",
        "bid_date": "2023-06-23",
        "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "client": "Office for National Statistics",
        "last_updated": "2023-07-19T11:15:25.743340",
        "links": {
            "questions": "/api/bids/9f688442-b535-4683-ae1a-a64c1a3b8616/questions",
            "self": "/api/bids/9f688442-b535-4683-ae1a-a64c1a3b8616",
        },
        "status": "in_progress",
        "tender": "Business Intelligence and Data Warehousing",
        "was_successful": False,
    }
    hostname = "localhost:8080"

    result = prepend_host_to_links(resource, hostname)

    assert result["links"] == {
        "questions": "http://localhost:8080/api/bids/9f688442-b535-4683-ae1a-a64c1a3b8616/questions",
        "self": "http://localhost:8080/api/bids/9f688442-b535-4683-ae1a-a64c1a3b8616",
    }


# Case 2: pagination values are validated correctly
def test_validate_pagination(default_limit, max_limit, default_offset, max_offset):
    valid_limit = 10
    valid_offset = 20
    nan_limit = "five"
    nan_offset = "ten"
    negative_limit = -5
    negative_offset = -10

    assert validate_pagination(valid_limit, valid_offset) == (valid_limit, valid_offset)
    assert validate_pagination(None, valid_offset) == (int(default_limit), valid_offset)
    assert validate_pagination(valid_limit, None) == (valid_limit, int(default_offset))
    with pytest.raises(
        ValueError, match=f"Limit value must be a number between 0 and {max_limit}"
    ):
        validate_pagination(nan_limit, valid_offset)
    with pytest.raises(
        ValueError, match=f"Limit value must be a number between 0 and {max_limit}"
    ):
        validate_pagination(negative_limit, valid_offset)
    with pytest.raises(
        ValueError, match=f"Offset value must be a number between 0 and {max_offset}"
    ):
        validate_pagination(valid_limit, nan_offset)
    with pytest.raises(
        ValueError, match=f"Offset value must be a number between 0 and {max_offset}"
    ):
        validate_pagination(valid_limit, negative_offset)


# Case 3: sort value is validated correctly
def test_validate_sort(default_sort_bids, default_sort_questions):
    valid_field_asc = "last_updated"
    valid_field_desc = "-last_updated"
    invalid_field = "invalid"

    assert validate_sort(valid_field_asc, "bids") == (valid_field_asc, 1)
    assert validate_sort(valid_field_asc, "questions") == (valid_field_asc, 1)
    assert validate_sort(valid_field_desc, "bids") == (valid_field_desc[1:], -1)
    assert validate_sort(valid_field_desc, "questions") == (valid_field_desc[1:], -1)
    assert validate_sort(None, "bids") == (default_sort_bids, 1)
    assert validate_sort(None, "questions") == (default_sort_questions, 1)
    with pytest.raises(ValueError, match="Invalid sort criteria"):
        validate_sort(invalid_field, "bids")
    with pytest.raises(ValueError, match="Invalid sort criteria"):
        validate_sort(invalid_field, "questions")
