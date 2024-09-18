from faker import Faker
from models import Designer, Sidemark  # replace with actual import paths
from db.database import DatabaseSession
import random

# Initialize Faker for generating dummy data
fake = Faker()


# Generate fake data for Designer if necessary
def create_designers(session, n=100):
    # Check if there are existing designers
    existing_designers = session.query(Designer).all()
    designers = existing_designers if existing_designers else []

    # Only create new designers if less than n exist
    if len(existing_designers) < n:
        for _ in range(n - len(existing_designers)):
            designer = Designer(
                company=fake.company(),
                abbreviation=fake.lexify(text='???'),
                designer_name=fake.name(),
                email=fake.email(),
                secondary_email=fake.email(),
                phone=fake.phone_number()
            )
            designers.append(designer)
            session.add(designer)
        session.commit()  # Commit the designers so they get IDs

    return designers


# Generate random number of Sidemarks (3 to 11) for each Designer
def create_sidemarks_for_designers(session, designers):
    sidemarks = []
    for designer in designers:
        # Generate a random number of sidemarks (between 3 and 11) for each designer
        num_sidemarks = random.randint(3, 11)
        for _ in range(num_sidemarks):
            sidemark = Sidemark(
                name=fake.name(),
                designer_id=designer.id  # Link to the current designer
            )
            sidemarks.append(sidemark)
            session.add(sidemark)
    session.commit()  # Commit all sidemarks to the database
    return sidemarks


# Main function to generate the data
def main():
    with DatabaseSession() as session:
        designers = create_designers(session, 100)  # Generate or use existing designers up to 100
        create_sidemarks_for_designers(session, designers)  # Create between 3 and 11 sidemarks for each designer


if __name__ == "__main__":
    main()
