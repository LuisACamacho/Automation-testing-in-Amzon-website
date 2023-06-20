from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import json 

with open("data.json", "w") as f:
    json.dump([],f)

def write_json(new_data,filename='data.json'):
    with open(filename, 'r+') as file:
        #First we load existing data into a dictionary.
        file_data = json.load(file)
        #Join new_data with file_data inside emp_details 
        file_data.append(new_data)
        #sets files current postion at offset.
        file.seek(0)
        #convert back to json
        json.dump(file_data,file, indent = 4)
        

browser = webdriver.Chrome()
browser.get('https://www.amazon.com/s?k=keyboards+piano&i=mi&rh=n%3A11970031%2Cp_76%3A1249167011%2Cp_n_feature_three_browse-bin%3A24056669011%7C24056672011%2Cp_36%3A1253547011&dc&crid=3UEKRV979AAKQ&qid=1686798287&rnid=386685011&sprefix=keyboards%2Caps%2C955&ref=sr_nr_p_36_3&ds=v1%3AtWf4b7cJKh4IdheebbFtbx4GkKk1Bnq0S%2Fo2gpxvPu4')

isNextDisabled = False
page = 1

while not isNextDisabled:
    try: 
        
        element = WebDriverWait (browser,10).until(EC.presence_of_element_located(
            ( By.XPATH,'//div[@data-component-type="s-search-result"]')))
        #elem_list contains all the search results 
        elem_list = browser.find_element(
            By.CSS_SELECTOR,"div.s-main-slot.s-result-list.s-search-results.sg-row")  

        #items contains  all search results with the data-component-type field 
        items = elem_list.find_elements(
            By.XPATH,'//div[@data-component-type="s-search-result"]') 
        print("#ofItems:" + str(len(items)))
        #input("Press ENTER to exit\n") 
       

        for item in items:

            title = item.find_element(By.TAG_NAME, "h2").text
            price = "No Price Located"
            image = "No image Located"
            url = item.find_element(By.CSS_SELECTOR,".a-link-normal.s-no-outline").get_attribute("href")

            try:
                price = item.find_element(By.CSS_SELECTOR,".a-price").text.replace("\n",".") #found price and replace text of new line with . 
    
            except:
                pass  #no price found

            try:
                image = item.find_element(By.CSS_SELECTOR, ".s-image" ).get_attribute("src")
        
            except:
                pass #no image found
            
            print ("Page:" + str(page))
            print("Image:" + image)
            print("Title: " + title)
            print("Price:" + price)
            print("URL:" +url + "\n")
            
            write_json ({
                "page": str(page),
                "title": title,
                "price": price,
                "image": image,
                "link": url,
                
            })
   
        next_Button = WebDriverWait (browser,10).until(EC.presence_of_element_located(
            (By.CLASS_NAME,"s-pagination-next")))
        
        page += 1
        next_Class = next_Button.get_attribute('class')
        if 's-pagination-disabled' in next_Class:
            isNextDisabled = True
        else:
            #next button is click until pagination-disabled is true
            browser.find_element(
                By.CLASS_NAME, "s-pagination-next").click()
        
    except Exception as e:
        print(e, "Main error")
        isNextDisabled = True


    
input("Press ENTER to exit\n")
        

