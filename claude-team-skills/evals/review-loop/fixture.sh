#!/bin/bash
# A small Python project with one tested function, for the review loop to extend.
set -e
git init -q
git config user.email "eval@example.com"
git config user.name "Eval"
mkdir -p tests
cat > pricing.py <<'PY'
def total(items):
    """Sum (price, quantity) pairs."""
    return sum(price * quantity for price, quantity in items)
PY
cat > tests/test_pricing.py <<'PY'
import unittest

from pricing import total


class TotalTests(unittest.TestCase):
    def test_sums_price_times_quantity(self):
        self.assertEqual(total([(10.0, 2), (5.0, 1)]), 25.0)

    def test_empty_basket_is_zero(self):
        self.assertEqual(total([]), 0)


if __name__ == "__main__":
    unittest.main()
PY
touch tests/__init__.py
git add -A
git commit -q -m "feat: pricing total"
