import pytest
from supplier_price import get_args, get_supplier_id

def test_get_supplier_id():
    # Test the get_supplier_id function with a sample supplier name
    args = get_args()
    args.name = 'Acme Coffee'
    supplier_id = get_supplier_id(args)

    # Check that the supplier ID is correct
    assert supplier_id == 1