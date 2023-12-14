import wikipedia, csv, re
from datetime import datetime

#store a list of items, to no repeat it when it searches new context
item_list=[]
csv_item=[]
#eu
wikipedia.set_lang(prefix='eu')
csv_list = []
csv_dict = {"Index":'',
            "Title":'',
            "Content":'',
            "URL":''
            }


def convert_to_one_liner(input_text):
    # Replace line breaks and extra spaces with a single space
    one_liner_text = ' '.join(input_text.split())
    #remove titles '=='
    one_liner_text = one_liner_text.replace("==", "")
    #remove non alphanumeric
    one_liner_text = re.sub(r'[^\w\s]', '', one_liner_text)
    return one_liner_text

def to_check(check_item):
    global item_list
    new_item= check_item
    if not new_item in item_list:
        item_list.append(new_item)
        with open('items_list.txt','a') as f:
            f.write(new_item + '\n')
        return True


for i in range(1,5):
    try:
            print('Downdloading: ', i)
            random_page= wikipedia.random(pages=1)
            page_obj = wikipedia.page(title=random_page)
            page_content = page_obj.content
            if to_check(random_page):
                text = convert_to_one_liner(page_content)
                item_list.append(random_page)
                #Create Dictionary:
                csv_dict={"Index":i,
                        "Title":random_page,
                        "Content":text,
                        "URL": page_obj.url}

                csv_list.append(csv_dict)



    except wikipedia.exceptions.DisambiguationError as e:
        print(f"DisambiguationError: {e}")
    except wikipedia.exceptions.HTTPTimeoutError as e:
        print(f"HTTPTimeoutError: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


#Exportation
current_date = datetime.now().strftime("%Y-%m-%d")
csv_filename = f"{current_date}_wikipedia_data.csv"

# Write data to CSV using the list of dictionaries
with open(csv_filename, mode='w', encoding='utf-8', newline='') as f:
    csv_writer = csv.DictWriter(f, fieldnames=["Index", "Title", "Content","URL"])
    csv_writer.writeheader()
    csv_writer.writerows(csv_list)

print(f"Data saved to {csv_filename}")