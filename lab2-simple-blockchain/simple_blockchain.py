import hashlib
import json
from datetime import datetime


class Block:
    def __init__(self, index, certificate_data, previous_hash):
        self.index = index
        self.timestamp = str(datetime.now())
        self.certificate_data = certificate_data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_content = {
            "index": self.index,
            "timestamp": self.timestamp,
            "certificate_data": self.certificate_data,
            "previous_hash": self.previous_hash
        }

        block_string = json.dumps(block_content, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, certificate_data):
        previous_block = self.get_latest_block()
        new_block = Block(
            len(self.chain),
            certificate_data,
            previous_block.hash
        )
        self.chain.append(new_block)

    def display_chain(self):
        for block in self.chain:
            print("=" * 60)
            print("Block Index:", block.index)
            print("Timestamp:", block.timestamp)
            print("Certificate Data:", block.certificate_data)
            print("Previous Hash:", block.previous_hash)
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


# Create blockchain
certificate_blockchain = Blockchain()

# Add certificate records
certificate_blockchain.add_block({
    "certificate_id": "CERT-001",
    "student_name": "Dara Sok",
    "course": "Blockchain Technology",
    "status": "Completed"
})

certificate_blockchain.add_block({
    "certificate_id": "CERT-002",
    "student_name": "Sophea Chan",
    "course": "Blockchain Technology",
    "status": "Completed"
})

certificate_blockchain.add_block({
    "certificate_id": "CERT-003",
    "student_name": "Vicheka Kim",
    "course": "Blockchain Technology",
    "status": "Completed"
})

# Display blockchain
certificate_blockchain.display_chain()

# Check blockchain validity
print("=" * 60)
print("Is blockchain valid?", certificate_blockchain.is_chain_valid())


# Tampering test
print("\nNow we try to change old certificate data...")
certificate_blockchain.chain[1].certificate_data = {
    "certificate_id": "CERT-001",
    "student_name": "Fake Student",
    "course": "Blockchain Technology",
    "status": "Completed"
}

print("Is blockchain valid after changing data?", certificate_blockchain.is_chain_valid())
