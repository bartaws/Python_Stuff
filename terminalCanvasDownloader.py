import requests
from lxml import html
from clint.textui import progress #progressbar

USERNAME = "<your_email>" # <--- Change!
PASSWORD = "<your_password>" # <--- Change!

LOGIN_URL = "https://canvas.academy.se/login/canvas" 
URL = "https://canvas.academy.se/courses/111/modules" 

def main():

    # This section is for user authentication and login

    print("\nThis is a terminal version of Canvas\n")
    print("First time use: Edit username and password inside this .py file with a text editor of your choise \n")
    week = input("Enter an int value of the corresponding week you wish to examine. (eg. 3) or Enter 666 to dowload every file: ")

    session_requests = requests.session()

    # Get login csrf token
    result = session_requests.get(LOGIN_URL)
    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='authenticity_token']/@value")))[0]

    # Create payload
    payload = {
        "pseudonym_session[unique_id]": USERNAME, 
        "pseudonym_session[password]": PASSWORD, 
        "authenticity_token": authenticity_token
    }

    # Perform login
    result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))

    # Scrape url
    result = session_requests.get(URL)
    doc = html.fromstring(result.content) # Attaching the HTML content to doc variable
    
    # This list contains each HTML element (<div>-wrapper) for corresbonding week.
    # Could have been done more elegantly.. for-loop perhaps?
    weeks = ["placeholder",
                '//*[@id="context_module_1089"]', #1
                '//*[@id="context_module_1090"]', #2
                '//*[@id="context_module_1091"]', #3
                '//*[@id="context_module_1092"]', #4
                '//*[@id="context_module_1093"]', #5
                '//*[@id="context_module_1094"]', #6
                '//*[@id="context_module_1095"]', #7
                '//*[@id="context_module_1096"]', #8
                '//*[@id="context_module_1097"]', #9
                '//*[@id="context_module_1098"]', #10
                '//*[@id="context_module_1099"]', #11
                '//*[@id="context_module_1100"]'] #12

    # Definition of the download function.
    def downloadFunction(x, week_context_module_item, week_container):
        # week_context_module contains a list of each name(str) of an item in the week section.
        filename = week_context_module_item[x].strip() # getting rid of exces whitespace
        usersAction = ".//*[@aria-label=\"" + filename + "\"]" # creating xpath for link to another link to download file
        download_link = "https://canvas.academy.se" + week_container.xpath(usersAction)[0].get("href") # creating xpath to the actual download link
        download_html = session_requests.get(download_link) # attaching the link to a variable
        download_doc = html.fromstring(download_html.content) # attaching the HTML of the link to a variable
        file_url = "https://canvas.academy.se" + download_doc.xpath('//*[@id="content"]/div[1]/span/a')[0].get("href") # creating the actual download URL
        result = session_requests.get(file_url, stream = True) # attaching the actual download link to a variable
        
        # Downloadin file in chunks
        with open(filename,"wb") as f:
            total_length =  int(result.headers.get('content-length')) # Initializing progress bar
            for chunk in progress.bar(result.iter_content(chunk_size=1024),  expected_size=(total_length/1024) + 1): 
                # writing one chunk at a time to pdf file 
                if chunk: 
                    f.write(chunk)
                    f.flush() 
        print(filename + " downloaded!")

    if (week == 666): # If user wants to download every file 
        for j in range(1,12): # Loops every week. 12 total
            week_container = doc.xpath(weeks[j])[0]
            week_context_module_item = week_container.xpath('.//*[@tabindex="-1"]/text()')
            i=0
            for x in week_context_module_item: # Loops every item in the week
                i+=1
                try:
                    downloadFunction(i, week_context_module_item, week_container)
                  #  print(i)
                except IndexError: # In case one of the elements contain no file to download eg. "Materiaaleja"
                    pass
        print("Download complete")

    else: # In case user wants to download only one week content or just examine them.
        week_container = doc.xpath(weeks[week])[0]
        week_context_module_item = week_container.xpath('.//*[@tabindex="-1"]/text()')

        # Prints every item of the week choisen.
        i = 1
        for x in week_context_module_item:
            print(str(i) + ". " + x.strip())
            i += 1
        

        #Download a file in the week section:
        while True:
            action = input("\nEnter a number to download the file you want or enter 666 to download every file in the list: ") - 1
            if (action == 665):
                i=0
                for x in week_context_module_item:
                    i+=1
                    try:
                        downloadFunction(i, week_context_module_item, week_container)
                      #  print(i)
                    except IndexError:
                        pass
            else:
                try: # In case user chooses an item with no file to download
                    downloadFunction(action, week_context_module_item, week_container)
                except IndexError:
                    print("\nNo file to download!\n")
                    continue

if __name__ == '__main__':
    main()

 