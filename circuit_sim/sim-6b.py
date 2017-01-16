#!/usr/bin/python

import sys, getopt


def help():
   print('sim-6b.py -i <inputfile> -s <initial_state>')
   sys.exit()

# To specify a 6b circuit to the program you should do:
# 
# gate_number; <truth_table>
# The k bits truth_table format being:
# <input 1 >:<output 1>, ..., <input 2^k>:<output 2^k>
#
# In 6 bits circuits k is 1 for gates 1 and 7 and 2 for others
# For k=2 gates the convention is Up Down -> Up Down

def parse_6b_circuit(filename):
   raw_data = open(filename, "r").read()
   raw_data = list(filter(lambda x: not(x == '' or x[0] == '%'),raw_data.split("\n")))
   circuit = {1:{},2:{},3:{},4:{},5:{},6:{},7:{}}
   for row in raw_data:
      row_data = row.split(';')
      row_number = int(row_data[0])
      if not row_number in circuit or circuit[row_number] != {}:
         print('Error while parsing '+filename+': rows should be numbered from 1 to 7 and specified exactly once.')
         sys.exit()
      truth_table = row_data[1].replace(" ", "").split(',')
      for entry in truth_table:
         parsed_entry = entry.split(':')
         circuit[row_number][parsed_entry[0]] = parsed_entry[1]

   return circuit

# f is the 6b function computed
# from the circuit
def f(circuit,x):
   input_2_1 = circuit[1][x[0]]
   input_2_2 = circuit[3][x[1]+x[2]][0]
   
   input_4_1 = circuit[3][x[1]+x[2]][1]
   input_4_2 = circuit[6][x[3]+x[4]][0]

   input_6_1 = circuit[6][x[3]+x[4]][1]
   input_6_2 = circuit[7][x[5]]

   return circuit[2][input_2_1+input_2_2]+circuit[4][input_4_1+input_4_2]+circuit[6][input_6_1+input_6_2]





def main(argv):
   if len(argv) < 5:
      help()

   if argv[1] != '-i':
      help()

   inputfile = argv[2]

   if argv[3] != '-s':
      help()

   init_state = argv[4]
   if len(init_state) != 6:
      print("Initial state should be coded on 6bits")
      sys.exit()

   print('Input file is "', inputfile)
   print('Initial state is "', init_state)
   circuit = parse_6b_circuit(inputfile)


   curr_state = init_state
   k = 0
   seen = {}
   while not curr_state in seen:
      print("s"+str(k)+" "+curr_state)
      seen[curr_state] = k
      curr_state = f(circuit,curr_state)
      k+=1
   print("s"+str(k+1)+" "+curr_state+" (cf s"+str(seen[curr_state])+")")

if __name__ == "__main__":
   main(sys.argv)