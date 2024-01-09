import os
import requests
from bs4 import BeautifulSoup
import nltk as nk
from tqdm import tqdm

# to save the file contaning the content and title of the article in the specified folder
def save_to_text_file(title, content, folder_path='articles'):
    """ 
    save all the content in the given output file and 
    save it in a folder 
    --->  default is in the articles folder
    """

    # Create the output folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Use the title as the filename (replace spaces with underscores)
    filename = os.path.join(folder_path, f"{title.replace(' ', '_')}.txt")

    with open(filename, 'w', encoding='utf-8') as file:
        # file.write(f"{title}\n\n")
        file.write(f"{content}")

    # print(f"Data saved to {filename}")


def data_extracter(data,folder_path='articles'):
    """
    This Function takes whole dataframe as the input and returns a datframe which contains content about all the aricle present in 
    all the given URL_IDs 
    -- dataframe should only contain 2 columns URL and URL_ID

    it also creates a specified folder and insert all the content in file and save this file to this newly created folder
    --> default name of the folder articles  

    it is specific to this particular data provided for the assignment
    """

    datadata = data.copy()
    URL = data.URL.values
    URL_ID = data.URL_ID.values
    article_content = list()
    for i in tqdm(range(data.shape[0])):
        assign = int(data.URL_ID.values[i][-4:])
        filename = URL_ID[i]
        htmltxt = requests.get(URL[i]).text
        soup = BeautifulSoup(htmltxt,'lxml')
        if assign not in [36,49]: # These URL_ID doesnt have data in them 
            if assign in [14,20,29,43,83,84,92,99,100]: # this URL_ID contain data in div but with different class name 
                title = soup.find('h1',class_="tdb-title-text").text
                content = soup.find('div',class_="tdb-block-inner td-fix-index").text.replace("\n"," ")
            else:
                title = soup.find('h1',class_='entry-title').text
                content = soup.find('div',class_="td-post-content tagdiv-type").text.replace("\n"," ")
            var = title+" "+content
            article_content.append(var)
            # print(i)/
            save_to_text_file(filename,var,folder_path)
        else:
            print('Error')
            article_content.append("Error data not found")

    datadata["content"] = article_content

    return datadata

def read_custom_stopwords(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        stopwords_list = [line.strip() for line in file.readlines()]
    return set(stopwords_list)


if __name__ == '__main__':
    pass