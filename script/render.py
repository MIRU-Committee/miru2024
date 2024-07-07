import pandas as pd
import argparse

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

    session_ids = [
        'IT',
        'DS',
        'IS1-A', 'IS1-B', 'IS2-A', 'IS2-B', 'IS3-A', 'IS3-B',
        'OS1-A', 'OS1-B', 'OS1-C', 'OS1-D', 'OS1-E',
        'OS2-A', 'OS2-B', 'OS2-C', 'OS2-D',
        'OS3-A'
    ]

    for session_id in session_ids:
        body = ""
        
        # e.g., select rows with SessionID == 'OS1-A'
        for _, row in df[df['SessionID'] == session_id].iterrows():
            poster_id = str(row['Poster ID'])
         
            # If English title is available and render-language is English, use English title.
            if type(row['英文タイトル | English title']) == str and args.lang == 'en':
                title = str(row['英文タイトル | English title'])
            else:
                title = str(row['Paper Title'])

            authors = str(row['著者リスト'])

            if session_id == 'IT':
                conf_name = str(row['会議・論文誌名の入力 | Enter the name of the conference/journal'])
                body += f'- {poster_id}: {authors}, **"{title}"**, [{conf_name}]\n'
            else:
                body += f'- {poster_id}: {authors}, **"{title}"**\n'

        # e.g., replace "{% OS1-A %}" with
        # """
        # - OS1-A-01: 本郷太郎（東大）, 駒場花子（京大）, **"強いTransformer"**
        # - OS1-A-02: Ziro Foo (Tokyo Tech.), Saburo Bar (Micro$oft), **"Deep Learning is Cool"**
        # """
        tmpl = tmpl.replace(f"{{% {session_id} %}}", body)
    
    with open(args.out, 'w') as f:
        f.write(tmpl)
