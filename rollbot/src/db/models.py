from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, JSON, DateTime, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Guild(Base):
    __tablename__ = "guilds"
    id = Column(BigInteger, primary_key=True)
    channels = relationship("Channel", back_populates="guild")


class Channel(Base):
    __tablename__ = "channels"
    id = Column(BigInteger, primary_key=True)
    guild_id = Column(BigInteger, ForeignKey("guilds.id"))

    prefix = Column(String)
    system = Column(String)

    channel_characters = relationship("ChannelCharacter", back_populates="channel")
    guild = relationship("Guild", back_populates="channels")

class Player(Base):
    __tablename__ = "players"
    id = Column(BigInteger, primary_key=True)
    characters = relationship("Character", back_populates="player")


class Character(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True)
    player_id = Column(BigInteger, ForeignKey("players.id"))

    name = Column(String)
    sheet_data = Column(JSON)

    player = relationship("Player", back_populates="characters")

    channel_links = relationship("ChannelCharacter", back_populates="character")
    variants = relationship("CharacterVariant", back_populates="character")


class CharacterVariant(Base):
    __tablename__ = "character_variants"
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey("characters.id"))
    diff_data = Column(JSON)

    character = relationship("Character", back_populates="variants")
    channel_links = relationship("ChannelCharacter", back_populates="variant")

class ChannelCharacter(Base):
    __tablename__ = "channel_characters"
    __table_args__ = (
        UniqueConstraint(
            "channel_id",
            "player_id",
            name="uq_channel_player"
        ),
    )
    id = Column(Integer, primary_key=True)
    channel_id = Column(BigInteger, ForeignKey("channels.id"))
    player_id = Column(BigInteger, ForeignKey("players.id"))
    character_id = Column(Integer, ForeignKey("characters.id"))
    variant_id = Column(Integer, ForeignKey("character_variants.id"))

    channel = relationship("Channel", back_populates="channel_characters")
    character = relationship("Character", back_populates="channel_links")
    player = relationship("Player")
    variant = relationship("CharacterVariant", back_populates="channel_links")

    joined_at = Column(DateTime)
