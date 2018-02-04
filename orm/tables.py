from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Mouse(Base):
    __tablename__ = 'mice'

    id = Column(Integer, primary_key=True)
    genotype = Column(String(10))
    date_of_birth = Column(String(10))
    gender = Column(String(1))
    breeder = relationship('Breeder', back_populates='mouse')

    def __repr__(self):
        return '<Mouse(id={0}, genotype={1}, DOB={2}, gender={3})'.format(
        self.id, self.genotype, self.date_of_birth, self.gender
        )


class Breeder(Base):
    __tablename__ = 'breeders'

    id = Column(Integer, primary_key=True)
    mouse_id = Column(Integer, ForeignKey('mice.id'))
    cage = Column(String(5), nullable=False)

    mouse = relationship('Mouse', back_populates='breeder')
    child = relationship('ExperimentalMouse')

    def __repr__(self):
        return '<Breeder(id={0}, cage={1})'.format(
        self.id, self.cage
        )


class ExperimentalMouse(Base):
    __tablename__ = 'experimental_mice'

    id = Column(Integer, primary_key=True)
    genotype = Column(String)
    mother_id = Column(Integer, ForeignKey('breeders.id'))

    mother = relationship('Breeder', back_populates='child')

    def __repr__(self):
        return "<ExperimentalMouse(genotype={0}, mother={1}, father={2})".format(
        self.genotype, self.mother_id, self.father_id
        )
