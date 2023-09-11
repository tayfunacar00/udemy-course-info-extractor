import requests
from datetime import datetime

def get_udemy_course_info(course_url):
    # remove the trailing slash if the url has one (if left there it leads to unwanted behavior)
    if course_url.endswith('/'):
        course_url = course_url[:-1]
        
    # extract the course slug from the URL
    course_slug = course_url.split("/")[-1].strip()
    
    # firstly, the id is needed to retrieve course title and creation date
    id_api_url = f"https://www.udemy.com/api-2.0/courses/{course_slug}/"
    
    try:
        response = requests.get(id_api_url)
        if response.status_code == 200:
            course_data = response.json()
            course_id = course_data['id']
            
            # use the retrieved ip to get creation date
            details_api_url = f"https://www.udemy.com/api-2.0/courses/{course_id}/?fields[course]=created,title"
            details_response = requests.get(details_api_url)
            
            if details_response.status_code == 200:
                details_data = details_response.json()
                course_title = details_data['title']
                course_creation_date = details_data['created']
                formatted_date = format_date(course_creation_date)
                return course_title, formatted_date
            else:
                print(f"Failed to retrieve course details. Status code: {details_response.status_code}")
                return None, None
        else:
            print(f"Failed to retrieve course data. Status code: {response.status_code}")
            return None, None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None, None
        
def format_date(course_date):
    # the date returned from Udemy json is not formatted
    parsed_date = datetime.strptime(course_date, "%Y-%m-%dT%H:%M:%SZ")
    formatted_date = parsed_date.strftime("%m.%d.%Y")
    return formatted_date

# input the URL from user and log results
course_url = input("Enter the Udemy course URL: ")
course_title, course_creation_date = get_udemy_course_info(course_url)

if course_title and course_creation_date:
    print(f"{course_title} was created on {course_creation_date}")
else:
    print("Course information not found or an error occurred.")

