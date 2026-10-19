# Executable spec: example/tests/test_features.py runs every row of the
# Examples table against shop.checkout.checkout(). Amounts are in cents.
Feature: Checkout totals
  As a shopper
  I want my receipt to apply discounts and shipping correctly
  So that I pay exactly what the shop's rules say

  The rules:
    - 10 or more items get 10% off the subtotal, rounded down to whole cents
    - The coupon WELCOME5 takes 500 cents off
    - Discounts never exceed the subtotal
    - Shipping costs 499 cents unless the discounted subtotal is at least 5000 cents

  Scenario Outline: Receipt for a single product line
    Given a cart with <quantity> units at <unit price> cents each
    And the coupon "<coupon>"
    When I check out
    Then the receipt shows subtotal <subtotal>, discount <discount>, shipping <shipping> and total <total>

    Examples:
      | quantity | unit price | coupon   | subtotal | discount | shipping | total |
      | 1        | 2000       | none     | 2000     | 0        | 499      | 2499  |
      | 9        | 1000       | none     | 9000     | 0        | 0        | 9000  |
      | 10       | 1000       | none     | 10000    | 1000     | 0        | 9000  |
      | 10       | 1000       | WELCOME5 | 10000    | 1500     | 0        | 8500  |
      | 1        | 5200       | WELCOME5 | 5200     | 500      | 499      | 5199  |
      | 1        | 5000       | none     | 5000     | 0        | 0        | 5000  |
      | 1        | 4999       | none     | 4999     | 0        | 499      | 5498  |
      | 1        | 300        | WELCOME5 | 300      | 300      | 499      | 499   |
