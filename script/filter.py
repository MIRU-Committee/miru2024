import argparse
import pandas as pd



def abbriviate(name):
    """
    Convert the name of a conference/journal to its abbreviation, e.g.,
    - 'Computer Vision and Pattern Recognition' -> 'CVPR'    <- The long original name is shortened.
    - 'ICCV 2024' -> 'ICCV'     <- Sometimes, the original name is already shortened. Format it (in this case, remove the year)
    """
    if not isinstance(name, str):
        return name

    if 'Computer Vision and Pattern Recognition' in name:
        return 'CVPR'
    elif 'CVPR' in name:
        return 'CVPR'
    elif 'International Conference on Computer Vision' in name:
        return 'ICCV'
    elif 'ICCV' in name:
        return 'ICCV'
    elif 'Pattern Analysis' in name:
        return 'TPAMI'
    elif 'SIGGRAPH' in name:
        return 'SIGGRAPH'
    elif 'ICLR' in name:
        return 'ICLR'
    elif 'International Journal' in name:
        return 'IJCV'
    elif 'ICRA' in name:
        return 'ICRA'
    elif 'NeurIPS' in name:
        return 'NeurIPS'
    else:
        assert 0, f"Unknown conference/journal name: {name}"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', default="timetable0.csv", help='path to the master CSV file')
    parser.add_argument('--out', default="timetable.csv", help='path to the output filtered CSV file')
    args = parser.parse_args()

    session_ids = [
        'IT',
        'DS',
        'IS1', 'IS2', 'IS3',
        'OS1-A', 'OS1-B', 'OS1-C', 'OS1-D', 'OS1-E',
        'OS2-A', 'OS2-B', 'OS2-C', 'OS2-D',
        'OS3-A'
    ]

    df = pd.read_csv(args.src)

    # Filter out the rows that are not in the session_ids, such as withdrawals
    df_filtered = df[df['SessionID'].isin(session_ids)]

    # Select only the columns we need.
    # The columns are:
    # - SessionID
    #     - Seission ID, e.g., 'IT', 'DS', 'IS1', 'OS1-A'
    # - IS-session
    #     - Interactive session ID (Poster session ID), e.g., 'IS1-A', 'IS1-B', 'IS2-A', 'IS2-B', 'DS'
    #     - For IS papers: e.g, "IS1" papers are divided into "IS1-A" and "IS1-B", and so on.
    #     - For DS papers: "DS".
    #     - For other papers: Poster session ID is assigned. E.g., "IS1-A" is assigned to "OS1-B"
    # - Poster ID
    #     - Unique ID. e.g., IS3-096
    # - Paper Title
    #     - Japanese title
    # - 著者リスト
    #     - Authors
    # - 英文タイトル | English title
    #     - English title (optional)
    # - 会議・論文誌名の入力 | Enter the name of the conference/journal
    #     - Only used for top-conference sission (IT). Confereence/journal name such as 'Computer Vision and Pattern Recognition'
    df_filtered = df_filtered[['SessionID', 'IS-session', 'Poster ID', 'Paper Title',
                               '著者リスト', '英文タイトル | English title', '会議・論文誌名の入力 | Enter the name of the conference/journal']]

    # For IT session (top-conference session), abbreviate the conference/journal names, e.g., 'Computer Vision and Pattern Recognition' -> 'CVPR'    
    df_filtered['会議・論文誌名の入力 | Enter the name of the conference/journal'] = df_filtered['会議・論文誌名の入力 | Enter the name of the conference/journal'].apply(abbriviate)


    df_filtered.to_csv(args.out, index=False)
