import os
import uuid
import tempfile

from database import session
from tkinter import messagebox
from recognition.compare import compare_face
from datetime import timedelta, datetime, date
from recognition.functions import upload_profile
from models import Operator, Profile, Arrival, Departure


def save_temp_file(profile) -> str:
    """
    Saves a byte array as a temporary file and returns the file path.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        temp_file.write(profile)
        return temp_file.name


def register(name: str, phone: str, email: str, password: str, post: str, profile) -> bool:
    operator_id = str(uuid.uuid4())

    if isinstance(profile, bytes):
        temp_image_path = save_temp_file(profile)
        path = upload_profile(operator_id, temp_image_path)
        os.remove(temp_image_path)
    else:
        path = upload_profile(operator_id, profile)

    operator = Operator(id=operator_id, name=name, phone=phone, email=email, password=password, post=post)
    profile = Profile(operator_id=operator_id, profile_path=path["profile_path"], processed=True)
    session.add_all([operator, profile])
    session.commit()

    messagebox.showinfo("Info", f"Created the operator {operator.to_dict()} and their profile {profile.to_dict()}")
    return True


def update(operator_id: str, name: str, phone: str, email: str, password: str, post: str, profile) -> bool:
    operator = session.query(Operator).filter_by(id=operator_id).first()
    if not operator:
        raise ValueError(f"No operator found with ID {operator_id}")

    operator.name = name
    operator.phone = phone
    operator.email = email
    operator.password = password
    operator.post = post

    if isinstance(profile, bytes):
        temp_image_path = save_temp_file(profile)
        path = upload_profile(operator_id, temp_image_path)
        os.remove(temp_image_path)
    else:
        path = upload_profile(operator_id, profile)

    profile_record = session.query(Profile).filter_by(operator_id=operator_id).first()
    if profile_record:
        profile_record.profile_path = path["profile_path"]
    else:
        profile_record = Profile(operator_id=operator_id, profile_path=path["profile_path"], processed=True)
        session.add(profile_record)

    session.commit()
    return True


def arrived(profile) -> None:
    if isinstance(profile, bytes):
        temp_image_path = save_temp_file(profile)
    else:
        temp_image_path = profile

    result = compare_face(temp_image_path)
    if isinstance(profile, bytes):
        os.remove(temp_image_path)

    if result[0]:
        operator_id = result[1]["operator_id"]
        today_start = datetime.combine(date.today(), datetime.min.time())
        existing_arrival = session.query(Arrival).filter(
            Arrival.operator_id == operator_id,
            Arrival.datestamp >= today_start
        ).first()

        if existing_arrival:
            messagebox.showinfo("Info", f"Operator {operator_id} has already registered an arrival today.")
            return

        arrival = Arrival(operator_id=operator_id, datestamp=datetime.now())
        session.add(arrival)
        session.commit()
        messagebox.showinfo("Info", f"The operator {operator_id} arrived at {arrival.datestamp}")
    else:
        messagebox.showinfo("Info", "Face not recognized. Who are you?")


def departed(profile) -> None:
    if isinstance(profile, bytes):
        temp_image_path = save_temp_file(profile)
    else:
        temp_image_path = profile

    result = compare_face(temp_image_path)
    if isinstance(profile, bytes):
        os.remove(temp_image_path)

    if result[0]:
        operator_id = result[1]["operator_id"]
        today_start = datetime.combine(date.today(), datetime.min.time())
        existing_departure = session.query(Departure).filter(
            Departure.operator_id == operator_id,
            Departure.datestamp >= today_start
        ).first()

        if existing_departure:
            messagebox.showinfo("Info", f"Operator {operator_id} has already registered a departure today.")
            return

        departure = Departure(operator_id=operator_id, datestamp=datetime.now())
        session.add(departure)
        session.commit()
        messagebox.showinfo("Info", f"The operator {operator_id} departed at {departure.datestamp}")
    else:
        messagebox.showinfo("Info", "Face not recognized. Who are you?")


def assiduity(operator_id: str) -> dict:
    all_arrivals = session.query(Arrival).filter_by(operator_id=operator_id).all()
    all_departures = session.query(Departure).filter_by(operator_id=operator_id).all()
    return {
        "arrivals": [arrival.to_dict() for arrival in all_arrivals],
        "departures": [departure.to_dict() for departure in all_departures],
    }


def everyone() -> list:
    operators = session.query(Operator).all()
    profiles = session.query(Profile).all()
    profile_map = {profile.operator_id: profile.to_dict() for profile in profiles}
    return [{"operator": op.to_dict(), "profile": profile_map.get(op.id)} for op in operators]


def someone(operator_id: str) -> dict:
    operator = session.query(Operator).filter_by(id=operator_id).first()
    if not operator:
        raise ValueError(f"No operator found with ID {operator_id}")
    profile = session.query(Profile).filter_by(operator_id=operator_id).first()
    return {"operator": operator.to_dict(), "profile": profile.to_dict() if profile else None}


def arrivals(operator_id: str, interval: int = 7) -> dict:
    operator = session.query(Operator).filter_by(id=operator_id).first()
    if not operator:
        raise ValueError(f"No operator found with ID {operator_id}")
    time_threshold = datetime.now() - timedelta(days=interval)
    all_arrivals = session.query(Arrival).filter(
        Arrival.operator_id == operator_id, Arrival.datestamp > time_threshold).all()
    return {"operator": operator.to_dict(), "arrivals": [arrival.to_dict() for arrival in all_arrivals]}


def departures(operator_id: str, interval: int = 7) -> dict:
    operator = session.query(Operator).filter_by(id=operator_id).first()
    if not operator:
        raise ValueError(f"No operator found with ID {operator_id}")
    time_threshold = datetime.now() - timedelta(days=interval)
    all_departures = session.query(Departure).filter(
        Departure.operator_id == operator_id, Departure.datestamp > time_threshold).all()
    return {"operator": operator.to_dict(), "departures": [dep.to_dict() for dep in all_departures]}
