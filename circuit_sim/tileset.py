#!/usr/bin/python

import sys, getopt

class Color:

  def __init__(self, side, color, tile, mode = ""):
     self.mode = mode
     self.color = color
     self.tile = tile
     self.side = side
     self.voisin = set()
     
  def __str__(self):
     return self.getName()
     
  def getName(self):
     return self.mode + "#" + str(self.color) + "#" + str(self.tile) + "#" + str(self.side)
     
  def link(self, color):
     if self.mode != "" and color.mode != "" and color.mode == self.mode:
        return None
     if(not( color in self.voisin)):
        self.voisin.add(color)
        color.voisin.add(self)

  def split(self):
     color_down = Color(self.side, self.color, self.tile, "d")
     color_up = Color(self.side, self.color, self.tile, "u")
     for color in self.voisin:
        color.voisin.remove(self)
        color.link(color_down)
        color.link(color_up)
     return color_down, color_up
     

class Tile:
   def __init__(self):
      self.colors = {}
      
   def addColor(self, color, pos):
      self.colors[pos] = color
      
   def getSide(self, side):
      return self.colors[side]
   

def parse_6b_circuit(filename):
   raw_data = open(filename, "r").read()
   raw_data = list(filter(lambda x: not(x == '' or x[0] == '%'),raw_data.split("\n")))
   circuit = {1:{},2:{},3:{},4:{},5:{},6:{},7:{}}

   for (i,row) in enumerate(raw_data):
      if i == 0 or i == 6:
         circuit[i+1]['0'] = row[0]
         circuit[i+1]['1'] = row[1]
      else:
         circuit[i+1]['00'] = row[0]+row[1]
         circuit[i+1]['01'] = row[2]+row[3]
         circuit[i+1]['10'] = row[4]+row[5]
         circuit[i+1]['11'] = row[6]+row[7]
   print(circuit)
   return circuit
   
def makeProofReading(tiles): #May need hard debuging.
   NewColors = set()
   proofTiles = set()
   
   for tile in tiles[0]:
      tile1 = Tile()
      tile2 = Tile()
      tile3 = Tile()
      tile4 = Tile()
      
      
      proofTiles.add(tile1)
      proofTiles.add(tile2)         
      proofTiles.add(tile3)         
      proofTiles.add(tile4)
        
   
   for i in range(1, len(tiles) - 1):
      unique = 0
      for tile in tiles[i]:
         tile1 = Tile()
         tile2 = Tile()
         tile3 = Tile()
         tile4 = Tile()
         
         #intern colors
         c0 = Color(-1, unique, i, "i") #color of 1
         c1 = Color( 2, unique, i, "i")
         tile1.addColor(c0,-1)
         tile1.addColor(c1, 2)
         
         c2 = Color(-2, unique, i, "i") #color of 2
         c3 = Color( 1, unique, i, "i")
         tile2.addColor(c2,-2)
         tile2.addColor(c3, 1)
         
         c4 = Color(-1, unique, i, "i") #color of 3
         c5 = Color(-2, unique, i, "i")
         tile3.addColor(c4,-1)
         tile3.addColor(c5,-2)
         
         c6 = Color( 2, unique, i, "i") #color of 4
         c7 = Color( 1, unique, i, "i")
         tile4.addColor(c6, 2)
         tile4.addColor(c7, 2)
         
         c0.link(c7)
         c2.link(c1)
         c4.link(c3)
         c6.link(c5)
         NewColors.add(c0)
         NewColors.add(c1)
         NewColors.add(c2)
         NewColors.add(c3)
         NewColors.add(c4)
         NewColors.add(c5)
         NewColors.add(c6)
         NewColors.add(c7)
         unique = unique + 1
         
         
         
         
         #extern colors
         color_down, color_up = tile.colors[-1].split()
         NewColors.add(color_down)
         NewColors.add(color_up)
         tile2.addColor(color_up, -1)
         tile1.addColor(color_down, -1)
         
         color_down, color_up = tile.colors[2].split()
         NewColors.add(color_down)
         NewColors.add(color_up)
         tile2.addColor(color_up, 2)
         tile3.addColor(color_down, 2)

         color_down, color_up = tile.colors[1].split()
         NewColors.add(color_down)
         NewColors.add(color_up)
         tile3.addColor(color_up, 1)
         tile4.addColor(color_down, 1)

         color_down, color_up = tile.colors[-2].split()
         NewColors.add(color_down)
         NewColors.add(color_up)
         tile1.addColor(color_up, -2)
         tile4.addColor(color_down, -2)
         
         proofTiles.add(tile1)
         proofTiles.add(tile2)         
         proofTiles.add(tile3)         
         proofTiles.add(tile4)
         
   return proofTiles, NewColors
         
         
         
                  
def help():
   print('tileset.py -i <inputfile>')
   sys.exit()

def main(argv):

   if len(argv) < 3:
      help()

   if argv[1] != '-i':
      help()
      
   inputfile = argv[2]
   circuit = parse_6b_circuit(inputfile)

   colors = {}
   sides = []
   tiles = []
   
   for t in range(len(circuit)): #construct tiles.
      if t == 0:
         sides = [[-2], [1]]
      elif t == 6:
         sides = [[-1], [2]]
      else:
         sides = [[-1, -2], [1, 2]]
         
      tiles.append([])
      print("start circuit " + str(t+1) + " " + str(circuit[t+1].keys()))
      for key in circuit[t+1].keys():
         string = key + circuit[t+1][key]
         tile = Tile()
         for i in range(len(sides[0])):
            color_in = Color(sides[0][i], string[i], t+1)
            color_out = Color(sides[1][i], string[i + len(string)/2], t+1)        
            tile.addColor(color_in, sides[0][i])
            tile.addColor(color_out, sides[1][i])
            
            colors[color_in.getName()] = color_in
            colors[color_out.getName()] = color_out
         tiles[t].append(tile)
      print(len(tiles))
   
   print(len(colors))
   
   for color_name in colors.keys(): #link colors
      color = colors[color_name]
      tile_id = color.tile
      side = color.side
      if(side == -1 or side == 2):
        tile_link = (tile_id - 1)
      else:
        tile_link = (tile_id + 1)
        
      if(tile_link < 1 or tile_link > 7):
         continue
      for tile in tiles[tile_link-1]:
         if(tile.getSide(-side).color == color.color):
            tile.getSide(-side).link(color)
   
   tiles, colors = makeProofReading(tiles)
   print(len(tiles))
   print(len(colors))

   
if __name__ == "__main__":
   main(sys.argv)
