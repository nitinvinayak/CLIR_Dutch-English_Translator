from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float,PrimaryKeyConstraint
from collections import defaultdict

def createTable():

	engine = create_engine('sqlite:///college.db', echo = True)
	meta = MetaData()

	students = Table(
	   'tProb', meta, 
	   Column('english', String), 
	   Column('dutch', String), 
	   Column('t(e|f)', Float),
	   PrimaryKeyConstraint('english', 'dutch', name='tProb')
	)
	meta.create_all(engine)

