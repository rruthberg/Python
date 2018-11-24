#Simple blockchain example

import hashlib as hasher
import datetime as date

#BLOCK - Main component which holds the data, timestamp and hashes (curr and previous)
class Block:
  def __init__(self, index, timestamp, data, previous_hash):
    self.index = index
    self.timestamp = timestamp
    self.data = data
    self.previous_hash = previous_hash
    self.hash = self.hash_block() #Hash function

  def hash_block(self):
    sha = hasher.sha256()
    hashString = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
    hashString = hashString.encode('utf-8')
    sha.update(hashString)
    return sha.hexdigest()


#GENESIS - creating an initial block
def create_genesis_block():
  #Initial block in the chain
  return Block(0, date.datetime.now(), "Init_Block", "0")

#NEXT - create next block referrring to last
def next_block(last_block):
  this_index = last_block.index + 1
  this_timestamp = date.datetime.now()
  this_data = "This block index: " + str(this_index)
  this_hash = last_block.hash
  return Block(this_index, this_timestamp, this_data, this_hash)

#RUN the chain
blockchain = [create_genesis_block()] #chain as a simple list
previous_block = blockchain[0] #set genesis block as previous block to the first real block
num_of_blocks_to_add = 15

# Add blocks to the chain
for i in range(0, num_of_blocks_to_add):
  previous_hash = previous_block.hash
  block_to_add = next_block(previous_block)
  blockchain.append(block_to_add)
  previous_block = block_to_add
  # Print chain
  outString1 = "Block #{} added to the blockchain".format(block_to_add.index)
  outString2 = " > Current hash: {}".format(block_to_add.hash)
  outString3 = " > Previous hash: {}\n".format(previous_hash)
  print(outString1)
  print(outString2)
  print(outString3)
