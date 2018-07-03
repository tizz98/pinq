import pytest
import random

from pinq import Pinq


class Product:
    def __init__(self, id, category, price):
        self.id = id
        self.category = category
        self.is_discounted = random.choice([True, False])
        self.price = price


class ProductDisplay:
    def __init__(self, product):
        self.product = product


@pytest.fixture(scope="class")
def products(request):
    request.cls.products = [Product(1, 2, 13.0), Product(2, 2, 99.99), Product(3, 4, 0.01)]


@pytest.mark.usefixtures("products")
class TestSelect:
    def test_values_returned_are_from_select_clause(self):
        p = Pinq(self.products)
        assert p.select(p.attr('id')).to_list() == [1, 2, 3]

    def test_multi_select(self):
        p = Pinq(self.products)
        assert p.select(p.attr('price')).select(str).to_list() == ["13.0", "99.99", "0.01"]


@pytest.mark.usefixtures("products")
class TestWhere:
    def test_filter_is_applied(self):
        p = Pinq(self.products)
        assert p.where(lambda p: p.category == 2).select(lambda p: p.id).to_list() == [1, 2]

    def test_multi_filter(self):
        p = Pinq(self.products)
        assert p.where(lambda p: p.category == 2).where(lambda p: p.price > 50).select(lambda p: p.id).to_list() == [2]


@pytest.mark.usefixtures("products")
class TestToSet:
    def test_returns_set_of_items(self):
        p = Pinq([1, 1, 2, 3, 5, 8, 13, 21, 34, 55])
        assert p.to_set() == {1, 2, 3, 5, 8, 13, 21, 34, 55}

    def test_returns_set_of_items_complex(self):
        p = Pinq(self.products)
        assert p.select(p.attr('category')).to_set() == {2, 4}


@pytest.mark.usefixtures("products")
class TestSum:
    def test_returns_sum(self):
        p = Pinq(range(100))
        assert p.sum() == 4950

    def test_returns_sum_complex(self):
        p = Pinq(self.products)
        assert p.select(p.attr('price')).sum() == 113


@pytest.mark.usefixtures("products")
class TestMin:
    def test_returns_min(self):
        p = Pinq([5, 90, -22, 42, 42])
        assert p.min() == -22

    def test_returns_min_complex(self):
        p = Pinq(self.products)
        assert p.select(p.attr('price')).min() == 0.01


@pytest.mark.usefixtures("products")
class TestMax:
    def test_returns_max(self):
        p = Pinq([5, 90, -22, 42, 42])
        assert p.max() == 90

    def test_returns_max_complex(self):
        p = Pinq(self.products)
        assert p.select(p.attr('price')).max() == 99.99


@pytest.mark.usefixtures("products")
class TestIterator:
    def test_can_iterate(self):
        p = Pinq(self.products)

        for product in p:
            # this is arbitrary, we're really checking we can iterate over p
            assert product.id > 0


class TestItem:
    def test_with_dictonary(self):
        products = [
            {'id': 1, 'price': 13, 'category': 2},
            {'id': 2, 'price': 99.99, 'category': 2},
            {'id': 3, 'price': 0.01, 'category': 4},
        ]

        p = Pinq(products)
        assert p.select(p.item('price')).max() == 99.99
        assert p.select(p.item('id')).to_list() == [1, 2, 3]
