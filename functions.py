import os
import uuid
import tempfile
from database import session
from recognition.compare import compare_face
from datetime import timedelta, datetime, date
from recognition.functions import upload_profile
from models import Operator, Profile, Arrival, Departure


def save_temp_file(profile) -> str:
    """
    Saves a byte array as a temporary file and returns the file path.
    :param profile: The byte array of the profile image.
    :return: Path to the temporary file.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        temp_file.write(profile)
        return temp_file.name


def register(name: str, phone: str, email: str, password: str, post: str, profile) -> bool:
    """
    Registers a new operator.
    :param name: The name of the operator.
    :param phone: The phone number.
    :param email: The email address.
    :param password: The password.
    :param post: The post of the operator.
    :param profile: The picture of the operator (file path or byte array).
    :return: True if the operator was registered successfully.
    """
    operator_id = str(uuid.uuid4())  # Generate a unique user ID

    # Handle profile input (byte array or file path)
    if isinstance(profile, bytes):
        temp_image_path = save_temp_file(profile)
        path = upload_profile(operator_id, temp_image_path)
        os.remove(temp_image_path)  # Clean up temporary file
    else:
        path = upload_profile(operator_id, profile)

    # Create and save operator and profile records
    operator = Operator(id=operator_id, name=name, phone=phone, email=email, password=password, post=post)
    profile = Profile(operator_id=operator_id, profile_path=path["profile_path"], processed=True)
    session.add_all([operator, profile])
    session.commit()

    print(f"Created the operator {operator.to_dict()} and their profile {profile.to_dict()}")
    return True


def arrived(profile) -> None:
    """
    Registers the arrival of an operator if they have not been registered today.
    :param profile: The profile image of the operator (file path or byte array).
    """
    # Save temporary file if profile is in bytes
    if isinstance(profile, bytes):
        temp_image_path = save_temp_file(profile)
    else:
        temp_image_path = profile

    # Perform face comparison
    result = compare_face(temp_image_path)

    # Clean up temporary file if needed
    if isinstance(profile, bytes):
        os.remove(temp_image_path)

    # Check if the face comparison was successful
    if result[0]:
        operator_id = result[1]["operator_id"]

        # Check if the operator has already registered an arrival today
        today_start = datetime.combine(date.today(), datetime.min.time())
        existing_arrival = session.query(Arrival).filter(
            Arrival.operator_id == operator_id,
            Arrival.datestamp >= today_start
        ).first()

        if existing_arrival:
            print(f"Operator {operator_id} has already registered an arrival today.")
            return

        # Register arrival time
        arrival = Arrival(operator_id=operator_id, datestamp=datetime.now())
        session.add(arrival)
        session.commit()

        print(f"The operator {operator_id} arrived at {arrival.to_dict()}")
    else:
        print("Face not recognized. Who are you?")


def departed(profile) -> None:
    """
    Registers the departure of an operator if they have not been registered today.
    :param profile: The profile image of the operator (file path or byte array).
    """
    # Save temporary file if profile is in bytes
    if isinstance(profile, bytes):
        temp_image_path = save_temp_file(profile)
    else:
        temp_image_path = profile

    # Perform face comparison
    result = compare_face(temp_image_path)

    # Clean up temporary file if needed
    if isinstance(profile, bytes):
        os.remove(temp_image_path)

    # Check if the face comparison was successful
    if result[0]:
        operator_id = result[1]["operator_id"]

        # Check if the operator has already registered a departure today
        today_start = datetime.combine(date.today(), datetime.min.time())
        existing_departure = session.query(Departure).filter(
            Departure.operator_id == operator_id,
            Departure.datestamp >= today_start
        ).first()

        if existing_departure:
            print(f"Operator {operator_id} has already registered a departure today.")
            return

        # Register departure time
        departure = Departure(operator_id=operator_id, datestamp=datetime.now())
        session.add(departure)
        session.commit()

        print(f"The operator {operator_id} departed at {departure.to_dict()}")
    else:
        print("Face not recognized. Who are you?")


def assiduity(operator_id: str) -> dict:
    """
    Fetches all arrivals and departures for a specific operator.
    :param operator_id: The operator's ID.
    :return: Dictionary with arrivals and departures.
    """
    all_arrivals = session.query(Arrival).filter_by(operator_id=operator_id).all()
    all_departures = session.query(Departure).filter_by(operator_id=operator_id).all()

    return {
        "arrivals": [arrival.to_dict() for arrival in all_arrivals],
        "departures": [departure.to_dict() for departure in all_departures],
    }


def everyone() -> list:
    """
    Fetches all operators in the database.
    :return: A list of dictionaries representing all operators and their profiles.
    """
    operators = session.query(Operator).all()
    profiles = session.query(Profile).all()

    # Map profiles to operators
    profile_map = {profile.operator_id: profile.to_dict() for profile in profiles}
    all_data = [
        {
            "operator": operator.to_dict(),
            "profile": profile_map.get(operator.id, None),
        }
        for operator in operators
    ]

    return all_data


def someone(operator_id: str) -> dict:
    """
    Fetches a specific operator and their profile by operator ID.
    :param operator_id: The operator's ID.
    :return: A dictionary containing the operator and their profile.
    """
    operator = session.query(Operator).filter_by(id=operator_id).first()
    profile = session.query(Profile).filter_by(operator_id=operator_id).first()

    if not operator:
        raise ValueError(f"No operator found with ID {operator_id}")

    return {
        "operator": operator.to_dict(),
        "profile": profile.to_dict() if profile else None,
    }


def arrivals(operator_id: str, interval: int = 7) -> dict:
    """
    Fetches all arrivals for a specific operator.
    :param operator_id: The ID of the operator.
    :param interval: The interval of dates to fetch (in days).
    :return: A dictionary containing the operator and its arrivals.
    """
    # Fetch the operator
    operator = session.query(Operator).filter_by(id=operator_id).first()

    if not operator:
        raise ValueError(f"No operator found with ID {operator_id}")

    # Fetch arrivals for the operator within the specified interval
    time_threshold = datetime.now() - timedelta(days=interval)
    all_arrivals = session.query(Arrival).filter(
        Arrival.operator_id == operator_id,
        Arrival.datestamp > time_threshold
    ).all()

    # Convert arrivals to dictionary form
    arrivals_list = [arrival.to_dict() for arrival in all_arrivals]

    # Return the results
    return {
        "operator": operator.to_dict(),
        "arrivals": arrivals_list,
    }


def departures(operator_id: str, interval: int = 7) -> dict:
    """
    Fetches all arrivals for a specific operator.
    :param operator_id: The ID of the operator.
    :param interval: The interval of dates to fetch (in days).
    :return: A dictionary containing the operator and its arrivals.
    """
    # Fetch the operator
    operator = session.query(Operator).filter_by(id=operator_id).first()

    if not operator:
        raise ValueError(f"No operator found with ID {operator_id}")

    # Fetch arrivals for the operator within the specified interval
    time_threshold = datetime.now() - timedelta(days=interval)
    all_departures = session.query(Departure).filter(
        Departure.operator_id == operator_id,
        Departure.datestamp > time_threshold
    ).all()

    # Convert arrivals to dictionary form
    departures_list = [arrival.to_dict() for arrival in all_departures]

    # Return the results
    return {
        "operator": operator.to_dict(),
        "departures": departures_list,
    }

