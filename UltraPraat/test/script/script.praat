echo script
# Paul Boersma, 5 January 2009

asserterror Unknown variable:'newline$'« hg
hg

a = 1
asserterror Expected the end of the formula, but found a numeric variable:
a = 5a

printline OK
