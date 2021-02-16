"""general utility functions for eia analysis
"""

def highlight_queens(s):
    is_queens = s == "Queens"
    return ["background-color: yellow" if v else "" for v in is_queens]

table_styles = [
    {"props": [("border-collapse", "separate"), ("border-spacing", "20px 0px")]}
]