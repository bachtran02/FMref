import streamlit as st

# Sample data: list of dicts
stats = [
    {"stat": "Non-Penalty Goals", "per90": 0.11, "percentile": 71},
    {"stat": "npxG: Non-Penalty xG", "per90": 0.07, "percentile": 51},
    {"stat": "Shots Total", "per90": 1.60, "percentile": 66},
    {"stat": "Assists", "per90": 0.22, "percentile": 93},
    {"stat": "xAG: Exp. Assisted Goals", "per90": 0.20, "percentile": 91},
    {"stat": "npxG + xAG", "per90": 0.27, "percentile": 84},
    {"stat": "Shot-Creating Actions", "per90": 3.43, "percentile": 85},
    {"stat": "Pass Completion %", "per90": "82.5%", "percentile": 40},
    {"stat": "Progressive Passes", "per90": 6.75, "percentile": 86},
    {"stat": "Aerials Won", "per90": 0.49, "percentile": 40},
    # Add more as needed
]

# Bar renderer
def render_bar(percentile):
    color = (
        "#4CAF50" if percentile >= 60 else
        "#9E9E9E" if percentile >= 40 else
        "#E57373"
    )
    return f'''
        <div style="background-color:#eee;width:100%;height:16px;border-radius:3px;">
            <div style="background-color:{color};width:{percentile}%;height:100%;border-radius:3px;"></div>
        </div>
    '''



def test_page():

    # Build HTML table
    table_html = """
    <style>
        table { width: 100%; border-collapse: collapse; font-size: 14px; }
        th, td { padding: 6px 8px; text-align: left; border-bottom: 1px solid #ddd; vertical-align: middle; }
        th { background-color: #f5f5f5; }
    </style>
    <table>
        <tr>
            <th>Statistic</th>
            <th>Per 90</th>
            <th>Percentile</th>
        </tr>
    """

    for row in stats:
        table_html += f"""
        <tr>
            <td>{row['stat']}</td>
            <td>{row['per90']}</td>
            <td>{render_bar(row['percentile'])}</td>
        </tr>
        """

    table_html += "</table>"

    # Render in Streamlit
    st.html("### vs. Midfielders")
    st.html(table_html)
