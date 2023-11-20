import os
import modal
import pandas as pd
import random

LOCAL=True

if LOCAL == False:
   stub = modal.Stub("wine_daily")
   image = modal.Image.debian_slim().pip_install(["hopsworks"]) 

   @stub.function(image=image, schedule=modal.Period(days=1), secret=modal.Secret.from_name("jim-hopsworks-ai"))
   def f():
       g()


def generate_wine(quality : float, wine_fg):
    """
    Returns a single wine as a single row in a DataFrame
    """
    columns = ['volatile_acidity', 'residual_sugar', 'chlorides',
       'total_sulfur_dioxide', 'density', 'sulphates', 'alcohol']

    wine_dict = {'quality' : quality}
    for col in columns:
        col_df = wine_fg.select([col]).filter(wine_fg.quality == quality).read()
        # print(col_df[col].to_list())
        rand_val = [random.choice(col_df[col].to_list())]
        wine_dict[col] = rand_val
    # print(f"Selected value from col {col}: {rand_val}")

    print(wine_dict)
    sample_df = pd.DataFrame(wine_dict)

    # df = pd.DataFrame()
    return sample_df


def get_random_wine_sample(wine_fg):
    """
    Returns a DataFrame containing one random wine
    """
    import pandas as pd
    import random

    q = random.choice([3,4,5,6,7,8,9])
    wine_df = generate_wine(q, wine_fg)
    print(f"Generated wine of quality: {q}")

    return wine_df


def g():
    import hopsworks
    import pandas as pd

    project = hopsworks.login(api_key_value="RhZB20y7YUun5HUf.magj2ktWRWYpeAQ3Se3F1Dw13r2GLa14vi2huErtL8XZi9UuvpnRVXXQHgiGQX9d")
    fs = project.get_feature_store()
    wine_fg = fs.get_feature_group(name='wine', version = 1)
    wine_df = get_random_wine_sample(wine_fg)
    print(wine_df)

    wine_fg.insert(wine_df)

if __name__ == "__main__":
    if LOCAL == True :
        g()
    else:
        stub.deploy("wine_daily")
        with stub.run():
            f()
