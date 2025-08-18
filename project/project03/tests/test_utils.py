# tests/test_utils.py
from src.utils import get_summary_stats, clean_column_names
import pandas as pd

# dummy DataFrame
df = pd.DataFrame({
    "Name": ["Alice", "Bob"],
    "Value Count": [10, 20]
})

# Test clean_column_names
cleaned_df = clean_column_names(df)
assert "name" in cleaned_df.columns, "Column 'name' should exist"
assert "value_count" in cleaned_df.columns, "Column 'value_count' should exist"

# Test get_summary_stats
summary = get_summary_stats(pd.DataFrame({"A": [1, 2, 3]}))
assert summary.loc["mean", "A"] == 2, "Mean should be 2"

print("All tests passed!")
