from datetime import timedelta
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel


class PlantBase(BaseModel):
    name: str


class PlantCreate(PlantBase):
    pass


class Plant(PlantBase):
    id: int

    class Config:
        from_attributes = True


class AssignedPlant(BaseModel):
    plant_name: str
    user_id: int


############################################################


class DepartmentBase(BaseModel):
    name: str


class AssignedDepartment(BaseModel):
    department_name: str
    user_id: int


class DepartmentCreate(DepartmentBase):
    pass


class Department(DepartmentBase):
    id: int

    class Config:
        from_attributes = True


############################################################
class UserEmail(BaseModel):
    email: str

    class Config:
        from_attributes = True


class TeamInUser(BaseModel):
    id: int
    name: str
    users: List[UserEmail]

    class Config:
        from_attributes = True

class RolesEnum(str, Enum):
    SUPERVISEUR = 'Superviseur'
    MANAGER = 'Manager'
    ZONE_LEADER = 'Zone leader'
    ADMIN = 'Admin'


class UserBase(BaseModel):
    username: str
    email: str
    role: RolesEnum
    account_status: Optional[bool] = False


class UserInDb(UserBase):
    hashed_password: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
    username: Optional[str] = None
    account_status: Optional[bool] = None
    password: Optional[str] = None


class UserDepartment(UserBase):
    departments: List[str]
    plants: List[str]
    password: str


class User(UserBase):
    id: int
    departments: List[Department]
    plants: List[Plant]
    teams: List[TeamInUser]

    class Config:
        from_attributes = True


class UserInDepartment(BaseModel):
    id: int
    username: str
    role: RolesEnum

    class Config:
        from_attributes = True


class UserPlantDepartment(BaseModel):
    plant: str
    departments: List[str]

class UserInTeam(BaseModel):
    username: str
    role: RolesEnum

    class Config:
        from_attributes = True

############################################################

class DepartmentUsers(DepartmentBase):
    id: int
    users: List[UserInDepartment]

    class Config:
        from_attributes = True


class RefreshToken(BaseModel):
    refresh_token: str
    token_type: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenCreationSettings(BaseModel):
    to_encode: any
    key: str
    expiry: timedelta
    algorithm: str

    class Config:
        arbitrary_types_allowed = True


class TokenVerificationSettings(BaseModel):
    token: str
    key: str
    algorithm: str


class LoginRequest(BaseModel):
    username: str
    password: str


class ForgetPasswordRequest(BaseModel):
    email: str


class ResetPasswordTokenVerificationRequest(BaseModel):
    token: str


class ResetPasswordRequest(BaseModel):
    email: str
    new_password: str
    confirm_password: str


############################################################

class TeamBase(BaseModel):
    name: str


class Team(BaseModel):
    id: int
    name: str
    users: List[UserInTeam]

    class Config:
        from_attributes = True


class TeamInDb(TeamBase):
    id: int
    created_at: Optional[str]
    updated_at: Optional[str]


class AppendToTeam(BaseModel):
    teams_id: List[int]
    users_id: List[int]

    class Config:
        from_attributes = True

class TeamUserDelete(BaseModel):
    team_id: int
    username: str