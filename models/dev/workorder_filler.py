import logging
from faker import Faker
from models import Workorder, WorkorderItem, Designer, Sidemark, Inventory  # replace with actual import paths
from db.database import DatabaseSession
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Faker for generating dummy data
fake = Faker()

# Predefined lists for generating varied furniture names
colors = ["Red", "Blue", "Green", "Yellow", "Black", "White", "Brown", "Gray", "Purple"]
materials = ["Wooden", "Metal", "Plastic", "Glass", "Leather", "Fabric", "Marble"]
furniture_types = ["Chair", "Table", "Sofa", "Bed", "Cabinet", "Desk", "Shelf", "Bench"]


# Function to generate a unique furniture name
def generate_furniture_name(existing_names):
    while True:
        color = random.choice(colors)
        material = random.choice(materials)
        furniture_type = random.choice(furniture_types)
        name = f"{color} {material} {furniture_type}"
        if name not in existing_names:  # Ensure the name is unique
            existing_names.add(name)
            return name


def generate_sku():
    # Generate a readable SKU in the format 'ABC12-34567'
    return (f"{fake.random_uppercase_letter()}{fake.random_uppercase_letter()}{fake.random_uppercase_letter()}"
            f"{random.randint(10, 99)}-{random.randint(10000, 99999)}")


def generate_size():
    # Return a random size from "S", "M", or "L"
    return random.choice(["S", "M", "L"])


def generate_workorder_id():
    # Generate a readable workorder ID in the format 'WO-ABCDE-12345'
    return (f"WO-{fake.random_uppercase_letter()}{fake.random_uppercase_letter()}{fake.random_uppercase_letter()}"
            f"{fake.random_uppercase_letter()}{fake.random_uppercase_letter()}-{random.randint(10000, 99999)}")


# Generate fake data for Inventory linked to Designers
def create_inventory(session, designers, n=100):
    inventories = []
    existing_names = set()  # Set to track unique inventory names
    for _ in range(n):
        inventory = Inventory(
            item_name=generate_furniture_name(existing_names),  # Generate unique name
            sku=generate_sku(),
            manufacture=fake.company(),
            quantity=random.randint(1, 100),
            description=fake.text(),
            designer_id=fake.random_element(designers).id,  # Link to a designer
            length=random.randint(10, 200),
            width=random.randint(10, 200),
            height=random.randint(10, 200),
            active=fake.boolean(),
            cubic_sq_inches=random.uniform(100.0, 1000.0),
            cubic_sq_footage=random.uniform(1.0, 10.0),
            in_storage=fake.boolean(),
            days_in_storage=random.randint(0, 365),
            size=generate_size(),
            weight=random.randint(5, 100),
            received_by_admin=fake.boolean(),
            ground_receive=random.randint(0, 1),
            freight_receive=random.randint(0, 1),
            assembled=random.randint(0, 1),
            unpacked=random.randint(0, 1),
            assembly_time=random.randint(0, 120)
        )
        logging.info(f"Generated Inventory: {inventory.item_name}, SKU: {inventory.sku}")
        inventories.append(inventory)
        session.add(inventory)
    session.commit()  # Commit the inventories to ensure IDs are assigned
    logging.info("Committed all inventory items to the database")
    return inventories


# Generate a random number of Workorders (between 2 and 13) for each Sidemark
def create_workorders(session, sidemarks):
    workorders = []
    for sidemark in sidemarks:
        # Generate a random number of workorders for each sidemark
        num_workorders = random.randint(2, 13)
        for _ in range(num_workorders):
            workorder = Workorder(
                workorder_id=generate_workorder_id(),  # Unique identifier for workorder
                designer_id=sidemark.designer_id,  # Link to the designer of the sidemark
                sidemark_id=sidemark.id,  # Link to the current sidemark
                status=fake.random_element(['pending', 'processing', 'completed'])  # Random status
            )
            logging.info(
                f"Generated Workorder: {workorder.workorder_id}, Status: {workorder.status}, Sidemark ID: {workorder.sidemark_id}")
            workorders.append(workorder)
            session.add(workorder)
    session.commit()  # Commit the workorders to ensure IDs are assigned
    logging.info("Committed all workorders to the database")
    return workorders


# Generate a random number of WorkorderItems (between 3 and 15) for each Workorder
def create_workorder_items(session, workorders, inventories):
    workorder_items = []
    for workorder in workorders:
        # Generate a random number of workorder items for each workorder
        num_items = random.randint(3, 15)
        for _ in range(num_items):
            workorder_item = WorkorderItem(
                workorder_id=workorder.id,  # Link to the current workorder
                inventory_id=fake.random_element(inventories).id,  # Use existing inventory IDs
                quantity=random.randint(1, 10),  # Random quantity
                assembly_time=random.randint(0, 120),  # Random assembly time
                unpacked=random.randint(0, 1),  # Unpacked status
                assembled=random.randint(0, 1),  # Assembled status
                total_fee=random.uniform(100.0, 5000.0)  # Random fee
            )
            logging.info(
                f"Generated WorkorderItem: Workorder ID: {workorder_item.workorder_id}, Inventory ID: {workorder_item.inventory_id}, Quantity: {workorder_item.quantity}")
            workorder_items.append(workorder_item)
            session.add(workorder_item)
    session.commit()  # Commit the workorder items to ensure IDs are assigned
    logging.info("Committed all workorder items to the database")
    return workorder_items


# Main function to generate all the data
def main():
    with DatabaseSession() as session:
        # Fetch all existing designers and sidemarks from the database
        designers = session.query(Designer).all()
        sidemarks = session.query(Sidemark).all()

        # Ensure there are designers and sidemarks to create workorders and items
        if not designers or not sidemarks:
            raise ValueError("Not enough designers or sidemarks available to create workorders.")

        logging.info("Starting data generation")

        # Step 1: Generate Inventory
        inventories = create_inventory(session, designers, 100)  # Generate 100 inventory items

        # Step 2: Generate Workorders for each Sidemark (2 to 13 per sidemark)
        workorders = create_workorders(session, sidemarks)

        # Step 3: Generate WorkorderItems for each Workorder (3 to 15 per workorder)
        create_workorder_items(session, workorders, inventories)

        logging.info("Data generation completed successfully")


if __name__ == "__main__":
    main()
