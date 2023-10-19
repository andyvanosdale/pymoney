# Python Money Package

Based on [Google Cloud's Money](https://cloud.google.com/recommender/docs/reference/rest/Shared.Types/Money) type, this package will do basic calculations on a `Money` type.

> ***NOTE***: `Money` does not do any form of currency conversion.
Calculations on `Money` **must be** in the same currency.

## Examples

```python
from money import Money

monies = [Money('USD', 10, 0), Money('USD', 20, 0)]
quartermoney = sum(monies)/4
print(quartermoney)
print(quartermoney == Money('USD', 7, 500_000_000))
print(eval(repr(quartermoney)) == quartermoney)

# Output
# USD 7.500000000
# True
# True
```
