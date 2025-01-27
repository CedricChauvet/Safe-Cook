import pandas as pd

# manipulation du csv
def make_df():

    df = pd.read_csv('./archive/variety_classification.csv')

    # on grade "for_cropping"  j'ai enlevé amout de drop
    df.drop(['layout_id', 'for_cropping', 'packed', 'uniform_background', 'spoiled', 'weight', 'cam', 'city', 'crowd', 'date', 'simp_amount', 'shop'], axis=1, inplace=True)
    train_df = df[df['subset'] == 'train']
    train_df.loc[:, 'variety_image_path'] = train_df['variety_image_path'].str.replace(
        'varieties_classification_dataset/train/', '', regex=False)


    test_df = df[df['subset'] == 'test']
    test_df.loc[:, 'variety_image_path'] = test_df['variety_image_path'].str.replace(
        'varieties_classification_dataset/test/', '', regex=False)


    labels = df['species'].unique()

    # Création d'un dictionnaire pour convertir les labels en entiers
    label_to_int = {label: idx for idx, label in enumerate(labels)}

    #print(label_to_int)
    df.loc[:, 'variety_image_path'] = df['variety_image_path'].str.replace(
        'varieties_classification_dataset/train/', '', regex=False)
    print(df.head(100))
    
    return train_df, test_df, label_to_int

if __name__ == '__main__':
    make_df()