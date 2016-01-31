from collections import deque
import sys
DEBUG = 1
row = []

def greedy(board,player):
	if player=='1':
		board.update_pit()



def init_board(row):
	task = row[0]
	player = row[1]
	cf_depth = row[2]
	p2_state = row[3].split(' ')
	p1_state = row[4].split(' ')
	p2_score = row[5]
	p1_score = row[6]
	size = len(p1_state)
	board = Board(size,p1_score,p2_score)
	board.add_pit(Pit('A1',int(p2_score)))

	index = 2
	for elem in p1_state:
		name = 'B' + str(index)
		board.add_pit(Pit(name,int(elem)))
		index +=1
		if DEBUG:
			print 'Add '+name+' to board'
	name = 'B' + str(index)
	board.add_pit(Pit(name,int(p1_score)))
	if DEBUG:
			print 'Add '+name+' to board'

	p2_state.reverse()

	index -= 1

	for elem in p2_state:
		name = 'A' + str(index)
		board.add_pit(Pit(name,int(elem)))
		index -= 1
		if DEBUG:
			print 'Add '+name+' to board'

	board.print_board()


	
	symbol=''
	while(1):
		symbol = raw_input('choose pit: ')
		if 'q' in symbol :
			break
		if(board.update_pit(symbol)):
			board.print_board()
			break
		board.print_board()
		
	return


class Board():
	def __init__(self,size,p1_score,p2_score):
		self.size = size
		self.p1_score = p1_score
		self.p2_score = p2_score
		self.pit_array = []
	def add_pit(self, pit):
		self.pit_array.append(pit)
		if pit.get_position()== str(self.size+2):
			self.p1_mancala_idx = len(pit_array)-1
	def get_pit(self):
		for pit in self.pit_array:

			print pit
	def find_pit(self,position):
		index = 0
		for x in self.pit_array:
			index += 1
			if x == position:
				current = x			
				return current, index
	def if_end(self,player,enemy):
		empty_count = 0
		total_in_opposite_pit = 0
		for elem in self.pit_array:
			if player[0] in elem.get_position():
				if elem.get_position() != player:
					if elem.get_stone() == 0:
						empty_count += 1
			elif elem.get_position()!= enemy:
				total_in_opposite_pit += elem.get_stone()

		if empty_count == self.size:
			pit,tmp = self.find_pit(enemy)
			if DEBUG:
				print 'End time clean up' + str(total_in_opposite_pit)
			pit.update_stone(total_in_opposite_pit)
			for elem in self.pit_array:
				if enemy[0] in elem.get_position():
					if elem.get_position() != enemy:
						elem.clear_stone()

			return True
		else: 
			return False








	def update_pit(self,position):
		current,index = self.find_pit(position)
		if DEBUG:
			self.print_board()
			print 'Choose '+position
		step = current.get_stone()
		#abort illegal move
		if step==0:
			if DEBUG:
				print 'illegal move: pit have no stone'
			return

		
		current.clear_stone()


		if('A' in position):
			ignore_player_position = 'B' + str(self.size+2)
			player_position = 'A1'
		else:
			ignore_player_position = 'A1'
			player_position = 'B' + str(self.size+2)
		for n in range(1,step+1):
			idx = (index + n-1) % len(self.pit_array)	
			#skip the enemy mancala 
			if(self.pit_array[idx]== ignore_player_position):
				index += 1
			idx = (index + n-1) % len(self.pit_array)					
			#if last ends in player's own empty pit, then take away all the stones in opposite pit 
			if n ==step:
				
				if self.pit_array[idx].get_stone() == 0:
					if self.pit_array[idx].get_position() != player_position:
					
						if position[0] in self.pit_array[idx].get_position():
							
							opposite_idx = self.size*2 +2 - idx
							opposite_pit = self.pit_array[opposite_idx]
							stone =  opposite_pit.get_stone()
							opposite_pit.clear_stone()

							mancala,tmp = self.find_pit(player_position)
							mancala.update_stone(stone)
							if DEBUG:
								print self.pit_array[idx].get_position()+' is empty. ' +'reverse: take '+str(stone)+' stones from '+ opposite_pit.get_position()

					


			self.pit_array[idx].update_stone(1)
		
			if DEBUG:
				print str(n)+' :updating' + self.pit_array[idx].get_position() +'stone: '+ str(self.pit_array[idx].get_stone())
		return self.if_end(player_position,ignore_player_position)
			
	def get_p1_score(self):
		position = 'B' + str(self.size+2)
		current, idx = self.find_pit(position)
		return current.get_stone()
	def get_p2_score(self):
		position = 'A1'
		current, idx = self.find_pit(position)
		return current.get_stone()
	def print_board(self):
		p1_array =[]
		p2_array =[]
		for elem in self.pit_array:

			if elem.get_position() =='A1':
				continue
			if elem.get_position() == 'B'+str(self.size+2):
				continue
			
			if 'A' in elem.get_position():
				p2_array.append(elem.get_stone()) 
				continue
			if 'B' in elem.get_position():
				p1_array.append(elem.get_stone()) 
		p2_array.reverse()
		print '-----mancala board top-------'
		print self.get_p2_score()
		print p2_array
		print p1_array
		print self.get_p1_score()
		print '-----mancala board bottom-------'


class Pit():
	def __init__(self,position,stone):
		self.position = position
		self.stone = stone

	def get_stone(self):
		return self.stone

	def update_stone(self,num):
		self.stone +=num
	def clear_stone(self):
		self.stone = 0
	def get_position(self):
		return self.position


	def __repr__(self):
		return self.position

	def __cmp__(self,obj):
		return cmp(self.position,obj)



with open(sys.argv[1]) as f:
	for line in f:
		row.append(line.strip())
init_board(row)
#board.get_pit()



