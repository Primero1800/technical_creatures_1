from pydantic import ValidationError
from sqlalchemy import text
from src.data.init import Session, IntegrityError
from src.errors import Missing, Duplicate, Validation
from src.model.explorer import Explorer