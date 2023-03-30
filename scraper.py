from requests import get

#product_code = input("Please enter product code: ")
product_code="36991221"
#print(product_code)

url=f"https://www.ceneo.pl/{product_code}#tab=reviews"
response = get(url)
print(response.status_code)