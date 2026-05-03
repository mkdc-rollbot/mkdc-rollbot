from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, JSON, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Guild(Base):
    __tablename__ = "guilds"
    id = Column(BigInteger, primary_key=True)


class Channel(Base):
    __tablename__ = "channels"
    id = Column(BigInteger, primary_key=True)
    guild_id = Column(BigInteger, ForeignKey("guilds.id"))
    prefix = Column(String)
    system = Column(String)

    channel_characters = relationship("ChannelCharacter", back_populates="channel")


class Player(Base):
    __tablename__ = "players"
    id = Column(BigInteger, primary_key=True)


class Character(Base):
    __tablename__ "characters"
    id = Column(Integer, primary_key=True)
    player_id = Column(BigInteger, ForeignKey("players.id"))

    name = Column(String)
    sheet_data = Column(JSON)

    channel_links = relationship("ChannelCharacter", backpopulates="character")


class ChannelCharacter(Base):
    __tablename__ = "channel_characters"
    id = Column(Integer, primary_key=True)
    channel_id = Column(BigInteger, ForeignKey("channels.id"))
    player_id = Column(BigInteger, ForeignKey("players.id"))
    character_id = Column(BigInteger, ForeignKey("characters.id"))

    channel = relationship("Channel", back_populates="channel_characters")
    character = relationship("Character", back_populates="channel_links")
    player = relationship("Player")

    joined_at = Column(DateTime)
