import pandas as pd
import argparse



def render_body(row, lang):
    """
    Render the body of a paper based on the given row and language.

    Args:
        row (pandas.Series): The row containing the data for the paper.
        lang (str): The language to be used for rendering.

    Returns:
        str: The rendered body of the paper.
    """
    assert lang in ['jp', 'en'], f"Unknown language: {lang}"

    # Convert the pandas-row to a usual python dict. Empty cell will be an empty string.
    row = row.fillna('').to_dict()

    poster_id = row['Poster ID']

    title = row['Paper Title']

    # If English title is available and render-language is English, add English title.
    # e.g., "強いトランスフォーマー (Strong Transformer)"
    if row['英文タイトル | English title'] and lang == 'en' and row['英文タイトル | English title'] != row['Paper Title']:
        title += " (" + row['英文タイトル | English title'] + ")"

    # If English name is available (meaning that English title is available) and rendering mode is English, use it for the author list
    if row['CMT著者名'] and lang == 'en':
        authors = row['CMT著者名']
    else:
        authors = row['著者リスト']

    if row['SessionID'] == 'ES':
        # If the paper is in the sponser session, don't show authors. Don't use `"` for title.
        return f'- {poster_id}: **{title}**'
    elif row['SessionID'] == 'IT':
        # If the paper is in the top-conference session, add the conference/journal name.
        conf_name = row['会議・論文誌名の入力 | Enter the name of the conference/journal']
        return f'- {poster_id}: {authors}, **"{title}"**, [{conf_name}]'
    else:
        return f'- {poster_id}: {authors}, **"{title}"**'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', default='timetable.csv', help='Path to the filtered master csv file')
    parser.add_argument('--template', default='template_jp.md', help='Path to the template of the markdown.')
    parser.add_argument('--out', default='output_jp.md', help='Path to the output markdown file')
    parser.add_argument('--lang', default='jp', choices=['jp', 'en'], help='If en, render the English paper title if possible')
    args = parser.parse_args()

    df = pd.read_csv(args.src)

    with open(args.template, 'r') as f:
        tmpl = f.read()

    # Not interactive session
    session_ids = [
        'IT',
        'OS-1A', 'OS-1B', 'OS-1C', 'OS-1D', 'OS-1E',
        'OS-2A', 'OS-2B', 'OS-2C', 'OS-2D',
        'OS-3A'
    ]

    # Interactive session (Prefix)
    # IS-A means; All three days. A-session.
    # IS-2B means: Second-day. B-session.
    interactive_session_ids = [
        'IS-A', 'IS-B',
        'IS-1A', 'IS-1B', 'IS-2A', 'IS-2B', 'IS-3A', 'IS-3B',
    ]

    # For each session (w/o interactive sessions), render the body of the papers and replace the placeholder.
    for session_id in session_ids:
        body = ""
        
        # e.g., select rows with SessionID == 'OS-1A'
        for _, row in df[df['SessionID'] == session_id].iterrows():
            body += render_body(row, args.lang) + '\n'

        # e.g., replace "{% OS-1A %}" with
        # """
        # - OS-1A-01: 本郷太郎（東大）, 駒場花子（京大）, **"強いTransformer"**
        # - OS-1A-02: Ziro Foo (Tokyo Tech.), Saburo Bar (Micro$oft), **"Deep Learning is Cool"**
        # """
        tmpl = tmpl.replace(f"{{% {session_id} %}}", body)


    # Do the similar things for interactive sessions.
    # For each interactive session, render the body of the papers and replace the placeholder.
    for interactive_session_id in interactive_session_ids:
        body = ""
        for _, row in df[df['IS-session'].str.startswith(interactive_session_id)].iterrows():
            body += render_body(row, args.lang) + '\n'
        tmpl = tmpl.replace(f"{{% {interactive_session_id} %}}", body)

    with open(args.out, 'w') as f:
        f.write(tmpl)
