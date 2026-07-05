import hashlib
import time


class Block:
    def __init__(self, index, data, previous_hash, difficulty):
        self.index = index
        self.timestamp = time.ctime()
        self.data = data
        self.previous_hash = previous_hash
        self.difficulty = difficulty
        self.nonce = 0
        self.hash = self.mine_block()

    def calculate_hash(self):
        block_text = (
            str(self.index)
            + self.timestamp
            + str(self.data)
            + self.previous_hash
            + str(self.nonce)
        )

        return hashlib.sha256(block_text.encode()).hexdigest()

    def mine_block(self):
        target = "0" * self.difficulty

        print("\nMining block", self.index)
        print("Target:", target)

        while True:
            block_hash = self.calculate_hash()

            if block_hash.startswith(target):
                print("Block mined successfully!")
                print("Nonce found:", self.nonce)
                print("Hash:", block_hash)
                return block_hash

            self.nonce += 1


class Blockchain:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0", self.difficulty)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        previous_block = self.get_latest_block()

        new_block = Block(
            len(self.chain),
            data,
            previous_block.hash,
            self.difficulty
        )

        self.chain.append(new_block)

    def display_chain(self):
        print("\n" + "=" * 70)
        print("BLOCKCHAIN DATA")
        print("=" * 70)

        for block in self.chain:
            print("\nBlock Index:", block.index)
            print("Timestamp:", block.timestamp)
            print("Data:", block.data)
            print("Previous Hash:", block.previous_hash)
            print("Nonce:", block.nonce)
            print("Current Hash:", block.hash)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True


# Main program
print("Mini Blockchain Proof of Work Lab")

difficulty = 4
my_blockchain = Blockchain(difficulty)

my_blockchain.add_block({
    "certificate_id": "CERT-001",
    "student_name": "Dara Sok",
    "course": "Blockchain Technology"
})

my_blockchain.add_block({
    "certificate_id": "CERT-002",
    "student_name": "Sophea Chan",
    "course": "Blockchain Technology"
})

my_blockchain.display_chain()

print("\nIs blockchain valid?", my_blockchain.is_chain_valid())
