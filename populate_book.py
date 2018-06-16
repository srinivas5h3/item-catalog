from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from db_setup import Users, Category, Base, BookDetails

engine = create_engine('sqlite:///bookstore.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()
# the main user details are added
User1 = Users(name="srinivas veeragommula", email="vsrinivasnaidu9@gmail.com",
              picture='https://bit.ly/2JW7QK5')
session.add(User1)
session.commit()

# first category is added
categories1 = Category(user_id=1, name="Poetry", description="Poetry is an art"
                       "form in which human language is used"
                       "for its aesthetic qualities in addition to, or instead"
                       "of,its notional and semantic content.")

session.add(categories1)
session.commit()

# the first category bookdetails
book = BookDetails(user_id=1, name="Where the Sidewalk Ends",
                   description="Children\'s poetry collection written and "
                   "illustrated by Shel Silverstein. Published by Harper and "
                   "Row Publishers.", type="eBook", price="Rs.120",
                   author="Shel Silverstein", categories=categories1)

session.add(book)
session.commit()


book1 = BookDetails(user_id=1, name="Leaves of Grass",
                    description="The seminal work of one of the most "
                    "influential writers of the nineteenth century.",
                    type="hardCopy", price="Rs.300", author="Walt Whitman",
                    categories=categories1)

session.add(book1)
session.commit()

book2 = BookDetails(user_id=1, name="Howl and Other Poems",
                    description="The single most influential poetic work of "
                    "the post-World War II era, with over 900,000 copies "
                    "now in print.", type="hardCopy", price="Rs.650",
                    author="Allen Ginsberg", categories=categories1)

session.add(book2)
session.commit()

book3 = BookDetails(user_id=1, name="Ariel", description="The beloved poet\'s "
                    "brilliant, provoking, and always moving poems, including "
                    "Ariel", type="eBook", price="Rs.670",
                    author="Sylvia Plath", categories=categories1)

session.add(book3)
session.commit()

book4 = BookDetails(user_id=1, name="Paradise Lost", description="One of the "
                    "greatest epic poems in the English language.",
                    type="hardCopy", price="Rs.900", author="John Milton",
                    categories=categories1)

session.add(book4)
session.commit()

book5 = BookDetails(user_id=1, name="The Odyssey", description="Literature\'s"
                    " grandest evocation of life's journey, and an individual"
                    " test of moral endurance", type="eBook", price="Rs.250",
                    author="Homer", categories=categories1)

session.add(book5)
session.commit()

book6 = BookDetails(user_id=1, name="The Iliad", description="One of the "
                    "greatest war stories of all time", type="hardCopy",
                    price="Rs.320", author="Homer", categories=categories1)

session.add(book6)
session.commit()


# Second category is added
categories2 = Category(user_id=1, name="Fantasy", description="Fantasy is a "
                       "categories of fiction set in a fictional universe, "
                       "often, but not always, without any locations, events,"
                       " or people referencing the real world.")

session.add(categories2)
session.commit()

# Second category bookdetails
book7 = BookDetails(user_id=1, name="The Chronicles of Narnia",
                    description="Journeys to the end of the world, fantastic "
                    "creatures, and epic battles between good and evil",
                    type="hardCopy", price="Rs.800", author="C.S. Lewis ",
                    categories=categories2)

session.add(book7)
session.commit()

book8 = BookDetails(user_id=1, name="The Final Empire", description="In a "
                    "world where ash falls from the sky, and mist dominates "
                    "the night, an evil cloaks the land and stifles all life.",
                    type="eBook", price="Rs.360", author="Brandon Sanderson",
                    categories=categories2)

session.add(book8)
session.commit()

book9 = BookDetails(user_id=1, name="A Game of Thrones", description="Summers "
                    "span decades. Winter can last a lifetime. And the "
                    "struggle for the Iron Throne has begun.", type="hardCopy",
                    price="Rs.740", author="George R.R. Martin",
                    categories=categories2)

session.add(book9)
session.commit()

book10 = BookDetails(user_id=1, name="Eragon", description="Eragon must "
                     "navigate the dangerous terrain and dark enemies of an "
                     "empire ruled by a king whose evil knows no bounds. ",
                     type="eBook", price="Rs.1250",
                     author="Christopher Paolini", categories=categories2)

session.add(book10)
session.commit()


# Third category is added
categories3 = Category(user_id=1, name="Horror", description="Horror is a "
                       "categories of fiction which is intended to, or has "
                       "the capacity to frighten, scare, disgust, or startle "
                       "its readers or viewers by inducing feelings of horror "
                       "and terror. ")

session.add(categories3)
session.commit()

# Third category bookdetails
book11 = BookDetails(user_id=1, name="Into the Drowning Deep",
                     description="Seven years ago, the Atargatis set off on a "
                     "voyage to the Mariana Trench to film a mockumentary "
                     "bringing to life ancient sea creatures of legend.",
                     type="hardCopy", price="Rs.550", author="Mira Grant",
                     categories=categories3)

session.add(book11)
session.commit()
book12 = BookDetails(user_id=1, name="Regression", description="Plagued by "
                     "ghastly waking nightmares, Adrian reluctantly agrees to "
                     "past life regression hypnotherapy. ", type="eBook",
                     price="Rs.800", author="Cullen Bunn",
                     categories=categories3)

session.add(book12)
session.commit()

book13 = BookDetails(user_id=1, name="Her Body and Other Parties",
                     description="Book demolishes the arbitrary borders "
                     "between psychological realism and science fiction, "
                     "comedy and horror, fantasy and fabulism. ",
                     type="hardCopy", price="Rs.680",
                     author="Carmen Maria Machado", categories=categories3)

session.add(book13)
session.commit()


# Fourth category is added
categories4 = Category(user_id=1, name="Children's", description="Children's "
                       "literature or juvenile literature includes stories,"
                       " books, magazines, and poems that are enjoyed "
                       "by children.")

session.add(categories4)
session.commit()

# Fourth category bookdetails
book14 = BookDetails(user_id=1, name="Where's the Unicorn?", description="A "
                     "Magical Search-and-Find Book ", type="hardCopy",
                     price="Rs.450", author="Paul Moran",
                     categories=categories4)

session.add(book14)
session.commit()

book15 = BookDetails(user_id=1, name="The Lost Words", description="Gorgeous "
                     "to look at and to read. Give it to a child to bring back"
                     " the magic of language - and its scope", type="eBook",
                     price="Rs.1550", author="Robert Macfarlane",
                     categories=categories4)

session.add(book15)
session.commit()


# Fifth category is added
categories5 = Category(user_id=1, name="History", description="Historical "
                       "fiction is a literary categories in which the plot "
                       "takes place in a setting located in the past. ")

session.add(categories5)
session.commit()

# Fifth category bookdetails
book16 = BookDetails(user_id=1, name="Sapiens: A Brief History of Humankind",
                     description="The Sunday Times number 1 bestseller",
                     type="eBook", price="Rs.1300",
                     author="Yuval Noah Harari", categories=categories5)

session.add(book16)

session.commit()
book17 = BookDetails(user_id=1, name="The Crusades: A History From Beginning "
                     "to End", description="Understanding the Crusades is key "
                     "in understanding the religious divides that still "
                     "threaten the order of the world. ", type="hardCopy",
                     price="Rs.250", author="Hourly History ",
                     categories=categories5)

session.add(book17)
session.commit()

# Sixth category is added
categories6 = Category(user_id=1, name="Comics", description="Comics is a "
                       "medium used to express ideas by images, often combined"
                       " with text or other visual information. Comics "
                       "frequently takes the form of juxtaposed sequences of "
                       "panels of images.")


session.add(categories6)
session.commit()

# Sixth category bookdetails
book18 = BookDetails(user_id=1, name="Comic Book Hero: Working with Britain's "
                     "Picture Strip Legends", description="Comic Book Hero "
                     "tells the inside story of how Barrie Tomlinson built up "
                     "a successful boys' publishing group at IPC Magazines",
                     type="eBook", price="Rs.2500", author="Barrie Tomlinson",
                     categories=categories6)

session.add(book18)
session.commit()

book19 = BookDetails(user_id=1, name="Super Graphic: A Visual Guide to the "
                     "Comic Book Universe", description="The comic book "
                     "universe is adventurous, mystifying and filled with "
                     "heroes,villains and ComicCon attendees.",
                     type="hardCopy", price="Rs.3000", author="Jonh Green",
                     categories=categories6)

session.add(book19)
session.commit()

book20 = BookDetails(user_id=1, name="Write and Draw Your Own Comics ",
                     description="An awesome activity book for budding comic "
                     "artists toimagine and draw their own comic strips. ",
                     type="hardCopy", price="Rs.4550", author="Louie Stowell",
                     categories=categories6)

session.add(book20)
session.commit()

print "books added"
