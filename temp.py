import pandas 
file = pandas.read_csv("output.csv")
print(file)
file=file.dropna(axis=1)
file.style.highlight_max(color="green")
print(type(file))
html_file=file.to_html("StockHistory.html")
# print(html_file)

# in each table row object from html_file add style="background-color:" " according to table value

