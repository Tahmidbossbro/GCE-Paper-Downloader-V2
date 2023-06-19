import requests
from bs4 import BeautifulSoup
import os

gce_guide_url = 'https://gceguide.com/past-papers/'


def get_url_data(url):
    response = requests.get(url)
    html_content = response.content
    return BeautifulSoup(html_content, 'html.parser')


course_list = get_url_data(gce_guide_url).find('div', {'id': 'pg-9-1'})

courses = course_list.find_all('div', {'class': 'panel-grid-cell'})

for _ in range(1, 4):
    print(f"For {courses[_ - 1].find('h3').text} press {_}")

# For The Course
selected_course = courses[int(input("Which Course do you want?: ")) - 1]
selected_course_name = selected_course.find('h3').text
selected_course_url = f"https:{selected_course.find('a').get('href')}"
selected_course_data = get_url_data(selected_course_url)
selected_course_subject_list = selected_course_data.find('ul', {'class': 'paperslist'}).find_all('li', {'class', 'dir'})
subject_code_list = []

for _ in selected_course_subject_list:
    subject_code = _.find('a').get('href').split(" ")[-1]
    for __ in '()':
        subject_code = subject_code.replace(__, "")
    subject_code_list.append(subject_code)
# For The Subject
selected_subject_index = input(f"\nPlease Input the Code of your {selected_course_name} subject: ")
selected_subject = selected_course_subject_list[subject_code_list.index(selected_subject_index)]
selected_subject_name = selected_subject.find('a').get('href')
selected_subject_url = f"{selected_course_url}/{selected_subject.find('a').get('href').replace(' ', '%20') + '/'}"
selected_subject_data = get_url_data(selected_subject_url)
print("-------------------------------------------------------------------------------------")
print(f"You have selected {selected_subject_name}")
print("-------------------------------------------------------------------------------------\n")

selected_subject_year_list = selected_subject_data.find('ul', {'class': 'paperslist'}).find_all('li', {'class': 'dir'})

year_list = []
for year in selected_subject_year_list:
    year_list.append(year.text)

# Only Year
year_start_index = year_list.index(input("Paper Start Year: "))
year_end_index = year_list.index(input("Paper End Year: "))
year_range_list = year_list[int(year_start_index): int(year_end_index) + 1]  # Final Year Range

print(f"Downloading {selected_subject_name}")
print("-------------------------------------------------------------------------------------")
for year in year_range_list:
    paper_by_year_url = f"{selected_subject_url}{year}"
    selected_year_data = get_url_data(paper_by_year_url)
    full_data_list = list(selected_year_data.find('ul', {'class': 'paperslist'}))
    ads_list = selected_year_data.find('ul', {'class': 'paperslist'}).find_all('div')

    # Ads Remover
    for ads in ads_list:
        full_data_list.remove(ads)

    # Saving File Zone
    current_directory = ""
    top_directory = f"C:/Users/Tahmid Newaz/Downloads/{selected_subject_name}/{year}"
    for data in full_data_list[1:-1]:
        if data.name == 'p':
            current_directory = data.text
            os.makedirs(f"{top_directory}/{current_directory}")
        else:
            download_url = f"{paper_by_year_url}/{data.text}"
            with open(f"{top_directory}/{current_directory}/{download_url.split('/')[-1]}", 'wb') as f:
                f.write(requests.get(download_url).content)

print("Download Complete")
