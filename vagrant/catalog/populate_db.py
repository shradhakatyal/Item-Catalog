from database_setup import Category, Item, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker()
DBSession.configure(bind=engine)
session = DBSession()

# Adding categories

category_1 = Category(name="Soccer")

session.add(category_1)
session.commit()

category_2 = Category(name="Tennis")

session.add(category_2)
session.commit()

category_3 = Category(name="Snowboarding")

session.add(category_3)
session.commit()


# Adding some items for the above categories
desc_1 = '''A football, soccer ball, or association football ball is the ball used in the sport of
association football. The ball's spherical shape, as well
as its size, weight, and material composition, are specified by Law 2 of the Laws
of the Game maintained by the International Football Association Board.
Additional, more stringent, standards are specified by FIFA and subordinate governing
bodies for the balls used in the competitions they sanction.'''

item_1 = Item(title="Soccer Ball", desc=desc_1, cat_id=1)

session.add(item_1)
session.commit()

desc_2 = '''Football boots, called cleats or soccer shoes in North America, are an item of footwear worn when playing football. Those designed for grass pitches have studs on the outsole to aid grip.'''

item_2 = Item(title="Football Shoes/Cleats", desc=desc_2, cat_id=1)

session.add(item_2)
session.commit()

desc_3 = '''A racket or racquet is a sports implement consisting of a handled frame with an open hoop across which a network of strings or catgut is stretched tightly. It is used for striking a ball or shuttlecock in games such as squash, tennis, racquetball, and badminton. Collectively, these games are known as racket sports'''
item_3 = Item(title="Racket", desc=desc_3, cat_id=2)

session.add(item_3)
session.commit()

desc_4 = '''A tennis ball is a ball designed for the sport of tennis. Tennis balls are fluorescent yellow at major sporting events, but in recreational play can be virtually any color. Tennis balls are covered in a fibrous felt which modifies their aerodynamic properties, and each has a white curvilinear oval covering it.'''
item_4 = Item(title="Tennis Ball", desc=desc_4, cat_id=2)

session.add(item_4)
session.commit()

desc_5 = '''Snowboards are boards where both feet are secured to the same board, which are wider than skis, with the ability to glide on snow. Snowboards widths are between 6 and 12 inches or 15 to 30 centimeters'''
item_5 = Item(title="Snowboard", desc=desc_5, cat_id=3)

session.add(item_5)
session.commit()

# Print message for user on terminal

print('Starter data added')