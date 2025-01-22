from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base

# Create the Base class
Base = declarative_base()

# Base mixin class for utility methods
# This class provides reusable functionality to all models
class BaseMixin:
    def to_dict(self):
        """
        Converts the model instance into a dictionary representation.
        Returns all column names and their corresponding values as a dictionary.
        """
        if hasattr(self, "__table__"):
            return {column.name: getattr(self, column.name) for column in self.__table__.columns}
        raise AttributeError(f"'{self.__class__.__name__}' does not have a '__table__' attribute.")

    def __repr__(self):
        """
        Provides a string representation of the model instance for debugging purposes.
        """
        try:
            columns = self.to_dict()
            column_strings = [f"{key}={repr(value)}" for key, value in columns.items()]
            return f"<{self.__class__.__name__}({', '.join(column_strings)})>"
        except AttributeError:
            return f"<{self.__class__.__name__}(Not a SQLAlchemy Model)>"

# Operator's model
# Premises: The operator "id" with name "name", phone number "phone", email "email",
# and password "password" with post "post".
class Operator(Base, BaseMixin):
    __tablename__ = 'operators'

    id = Column(String, primary_key=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    post = Column(String)

# Profile's model
# The profile "id" of the operator "operator_id" with storage path "profile_path"
# with procession confirmation "processed".
class Profile(Base, BaseMixin):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    operator_id = Column(String, ForeignKey('operators.id'))
    profile_path = Column(String)
    processed = Column(Boolean)

# Arrival's model
# The arrival model defined by the operator "operator_id" who arrived at "datestamp".
class Arrival(Base, BaseMixin):
    __tablename__ = 'arrivals'

    id = Column(Integer, primary_key=True, autoincrement=True)
    operator_id = Column(Integer, ForeignKey('operators.id'))
    datestamp = Column(DateTime)

# Departure's model
# The departure model defined by the operator "operator_id" who departed at "datestamp".
class Departure(Base, BaseMixin):
    __tablename__ = 'departures'

    id = Column(Integer, primary_key=True, autoincrement=True)
    operator_id = Column(Integer, ForeignKey('operators.id'))
    datestamp = Column(DateTime)
