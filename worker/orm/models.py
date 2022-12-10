from sqlalchemy import Boolean, CHAR, CheckConstraint, Column, DECIMAL, DateTime, ForeignKey, Index, Integer, String, Table, Text, func, case, or_
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from processor.utils import uuid_comb
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select
from orm import get_session
from decimal import Decimal
from dto_pack import TransferType

Base = declarative_base()
metadata = Base.metadata


class AuthGroup(Base):
    __tablename__ = 'auth_group'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)


class Bank(Base):
    __tablename__ = 'banks'

    uuid = Column(CHAR(32), primary_key=True, default=lambda: uuid_comb().hex)
    slug = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)


class BanksClient(Base):
    __tablename__ = 'banks_client'

    password = Column(String(128), nullable=False)
    last_login = Column(DateTime)
    is_superuser = Column(Boolean, nullable=False)
    username = Column(String(150), nullable=False)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(254), nullable=False)
    is_staff = Column(Boolean, nullable=False)
    is_active = Column(Boolean, nullable=False)
    date_joined = Column(DateTime, nullable=False)
    uuid = Column(CHAR(32), primary_key=True, default=lambda: uuid_comb().hex)

class DjangoContentType(Base):
    __tablename__ = 'django_content_type'
    __table_args__ = (
        Index('django_content_type_app_label_model_76bd3d3b_uniq', 'app_label', 'model', unique=True),
    )

    id = Column(Integer, primary_key=True)
    app_label = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)


class DjangoMigration(Base):
    __tablename__ = 'django_migrations'

    id = Column(Integer, primary_key=True)
    app = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    applied = Column(DateTime, nullable=False)


class DjangoSession(Base):
    __tablename__ = 'django_session'

    session_key = Column(String(40), primary_key=True)
    session_data = Column(Text, nullable=False)
    expire_date = Column(DateTime, nullable=False, index=True)


t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)


class AuthPermission(Base):
    __tablename__ = 'auth_permission'
    __table_args__ = (
        Index('auth_permission_content_type_id_codename_01ab375a_uniq', 'content_type_id', 'codename', unique=True),
    )

    id = Column(Integer, primary_key=True)
    content_type_id = Column(ForeignKey('django_content_type.id'), nullable=False, index=True)
    codename = Column(String(100), nullable=False)
    name = Column(String(255), nullable=False)

    content_type = relationship('DjangoContentType')


class BankAccount(Base):
    __tablename__ = 'bank_accounts'
    __table_args__ = (
        Index('bank_accounts_client_id_bank_id_iban_2a461612_uniq', 'client_id', 'bank_id', 'iban', unique=True),
    )

    uuid = Column(CHAR(32), primary_key=True, default=lambda: uuid_comb().hex)
    iban = Column(String(34), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    bank_id = Column(ForeignKey('banks.uuid'), nullable=False, index=True)
    client_id = Column(ForeignKey('banks_client.uuid'), nullable=False, index=True)

    bank = relationship('Bank')
    client = relationship('BanksClient')


class BanksClientGroup(Base):
    __tablename__ = 'banks_client_groups'
    __table_args__ = (
        Index('banks_client_groups_client_id_group_id_442c12d9_uniq', 'client_id', 'group_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    client_id = Column(ForeignKey('banks_client.uuid'), nullable=False, index=True)
    group_id = Column(ForeignKey('auth_group.id'), nullable=False, index=True)

    client = relationship('BanksClient')
    group = relationship('AuthGroup')


class DjangoAdminLog(Base):
    __tablename__ = 'django_admin_log'
    __table_args__ = (
        CheckConstraint('"action_flag" >= 0)'),
    )

    id = Column(Integer, primary_key=True)
    action_time = Column(DateTime, nullable=False)
    object_id = Column(Text)
    object_repr = Column(String(200), nullable=False)
    change_message = Column(Text, nullable=False)
    content_type_id = Column(ForeignKey('django_content_type.id'), index=True)
    user_id = Column(ForeignKey('banks_client.uuid'), nullable=False, index=True)
    action_flag = Column(Integer, nullable=False)

    content_type = relationship('DjangoContentType')
    user = relationship('BanksClient')


class Wallet(Base):
    __tablename__ = 'wallets'


    uuid = Column(CHAR(32), primary_key=True, default=lambda: uuid_comb().hex)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    client_id = Column(ForeignKey('banks_client.uuid'), nullable=False, index=True)

    client = relationship('BanksClient')


class AuthGroupPermission(Base):
    __tablename__ = 'auth_group_permissions'
    __table_args__ = (
        Index('auth_group_permissions_group_id_permission_id_0cd325b0_uniq', 'group_id', 'permission_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    group_id = Column(ForeignKey('auth_group.id'), nullable=False, index=True)
    permission_id = Column(ForeignKey('auth_permission.id'), nullable=False, index=True)

    group = relationship('AuthGroup')
    permission = relationship('AuthPermission')


class BanksClientUserPermission(Base):
    __tablename__ = 'banks_client_user_permissions'
    __table_args__ = (
        Index('banks_client_user_permissions_client_id_permission_id_f0d88acf_uniq', 'client_id', 'permission_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    client_id = Column(ForeignKey('banks_client.uuid'), nullable=False, index=True)
    permission_id = Column(ForeignKey('auth_permission.id'), nullable=False, index=True)

    client = relationship('BanksClient')
    permission = relationship('AuthPermission')


class Transaction(Base):
    __tablename__ = 'transactions'

    uuid = Column(CHAR(32), primary_key=True, default=lambda: uuid_comb().hex)
    amount = Column(DECIMAL, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    wallet_id = Column(ForeignKey('wallets.uuid'), nullable=False, index=True)

    wallet = relationship('Wallet')


class Transfer(Base):
    __tablename__ = 'transfers'

    uuid = Column(CHAR(32), primary_key=True, default=lambda: uuid_comb().hex)
    number = Column(String(25), nullable=False)
    status = Column(String(10), nullable=False)
    type = Column(String(10), nullable=False)
    amount = Column(DECIMAL, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    scheduled_at = Column(DateTime)

    schedule_id = Column(CHAR(32), nullable=True)
    finished_at = Column(DateTime)
    canceled_at = Column(DateTime)
    client_id = Column(ForeignKey('banks_client.uuid'), nullable=False, index=True)
    from_bank_account_id = Column(ForeignKey('bank_accounts.uuid'), index=True)
    to_bank_account_id = Column(ForeignKey('bank_accounts.uuid'), index=True)
    transaction_id = Column(ForeignKey('transactions.uuid'))

    client = relationship('BanksClient')
    from_bank_account = relationship('BankAccount', primaryjoin='Transfer.from_bank_account_id == BankAccount.uuid')
    to_bank_account = relationship('BankAccount', primaryjoin='Transfer.to_bank_account_id == BankAccount.uuid')
    transaction = relationship('Transaction')