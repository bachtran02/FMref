from utils import percentile_to_color

def render_summary_table(mp, min, gls, ast, xg, npxg, xa):
    return f'''
        <colgroup>
            <col style="width: 60px;">
            <col style="width: 60px;">
            <col style="width: 60px;">
            <col style="width: 60px;">
            <col style="width: 60px;">
            <col style="width: 60px;">
            <col style="width: 60px;">
        </colgroup>
        <thead>
            <tr>
                <th>MP</th>
                <th>Min</th>
                <th>Gls</th>
                <th>Ast</th>
                <th>xG</th>
                <th>npxG</th>
                <th>xA</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>{mp}</td>
                <td>{min}</td>
                <td>{gls}</td>
                <td>{ast}</td>
                <td>{xg}</td>
                <td>{npxg}</td>
                <td>{xa}</td>
            </tr>
        </tbody>
    '''

def render_percentile_bar(perc):
    """ Render horizontal bar for the percentile value. """
    return f'''
        <div style="display: flex; align-items: center;">
            <div align="center" style="min-width: 22px; display: inline-block;">{perc}</div>
            <div style="width: 200px; height: 15px;">
                <div style="width: {perc}%; height: 100%; background-color: {percentile_to_color(perc)};"></div>
            </div>
        </div>
    '''

def percentile_table_thead(category_name):
    """ Render thead for percentile table """
    return f'''
        <thead>
            <tr>
                <th colspan="3">{category_name}</th>
            </tr>
            </tr>
            <tr>
                <th>Statistic</th>
                <th>Per 90</th>
                <th>Percentile</th>
            </tr>
        </thead>
    '''

def similar_table_thead():
    return '''
        <thead>
            <tr>
                <th>Rk</th>
                <th>Player</th>
                <th>Nation</th>
                <th>Squad</th>
            </tr>
        </thead>
    '''
