from sqlmodel import create_engine

sqlite_file_name = "blog.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
my_engine = create_engine(sqlite_url, connect_args=connect_args)