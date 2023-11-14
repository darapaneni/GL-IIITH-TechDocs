
pip install pyenchant



import enchant 
  
# Using 'en_US' dictionary 
d = enchant.Dict("en_US") 
  
# Taking input from user 
word = input("Enter word: ") 
  
d.check(word) 
  
# Will suggest similar words 
# form given dictionary 
print(d.suggest(word)) 
