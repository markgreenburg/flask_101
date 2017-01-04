"""
CRUD & related models for our wiki app
"""
from time import strftime
import pg
import config

class User(object):
    """
    User mapping for users in db
    """
    def __init__(self, user_id=0):
        if not isinstance(user_id, int):
            user_id = int(user_id)
        query = ("SELECT id, username, password FROM users WHERE id = %d" % user_id)
        result_set = Database.get_result(query)
        if result_set:
            self.user_id = user_id
            self.username = result_set[0].username
            self.password = result_set[0].password
        else:
            self.user_id = 0
            self.username = "Not Set"
            self.password = "Not Set"
        return

    @staticmethod
    def get_user(username):
        """
        finds user by username and returns that user's object.
        """
        query = ("SELECT id FROM users WHERE username = '%s'" % username)
        user_id_list = Database.get_result(query)
        user_id = user_id_list[0].id
        user = User(user_id)
        return user

class Page(object):
    """
    Object map for pages in the database
    """
    def __init__(self, page_id=0):
        if not isinstance(page_id, int):
            page_id = int(page_id)
        query = ("SELECT id, title, content, last_modified, modified_by,"
                 " deleted FROM page WHERE id = %d" % page_id)
        # Query our db to see if this page ID exists
        result_set = Database.get_result(query)
        # If page exists, set Page attributes to what's in the db
        if result_set:
            self.page_id = page_id
            self.title = result_set[0].title
            self.content = result_set[0].content
            self.last_modified = result_set[0].last_modified
            self.modified_by = result_set[0].modified_by
            self.deleted = result_set[0].deleted
        else:
            self.page_id = 0
            self.title = "Not Set"
            self.content = "Not Set"
            self.last_modified = "Not Set"
            self.modified_by = "Not Set"
            self.deleted = False
        return

    def insert(self):
        """
        Inserts new page into wiki. Should not be called directly - instead,
        use the Page.save() method.
        """
        self.last_modified = strftime("%Y-%m-%d %H:%M:%S")
        query = ("INSERT INTO page (title, content, last_modified, deleted,"
                 " modified_by) VALUES ('%s', '%s', '%s', %s, '%s')"
                 " RETURNING id" % \
                 (Database.escape(self.title), \
                  Database.escape(self.content), \
                  self.last_modified, \
                  self.deleted, \
                  Database.escape(self.modified_by)))
        result_list = Database.get_result(query)
        self.page_id = result_list[0].id
        print "PAGE ID IS: %s" % self.page_id
        return self.page_id

    def update(self):
        """
        Updates page in wiki. Should not be called directly - instead, use the
        Page.save() method.
        """
        query = ("UPDATE page SET title = '%s', content = '%s', last_modified"
                 " = '%s', modified_by = '%s' WHERE id = %d RETURNING id" % \
                (Database.escape(self.title),\
                 Database.escape(self.content),\
                 strftime("%Y-%m-%d %H:%M:%S"),\
                 Database.escape(self.modified_by),\
                 self.page_id))
        result_list = Database.get_result(query)
        return result_list[0].id

    def save(self):
        """
        Saves action to database by calling insert() or update() methods. If
        page already exists, will call update(), else will call insert().
        After insert or update, adds the last change to the revisions table.
        """
        if self.page_id:
            self.update()
        else:
            self.insert()
        revision = Revision()
        revision.page_id = self.page_id
        revision.title = self.title
        revision.content = self.content
        revision.last_modified = self.last_modified
        revision.modified_by = self.modified_by
        revision.deleted = self.deleted
        revision.save()
        return self.page_id

    def set_delete(self, deleted=True):
        """
        Sets a page's 'deleted' attribute to 1 by default (so it won't show in
        index) or 0 if passed in as an arg. Setting to 0 restores the page in
        the index.
        """
        query = "UPDATE page SET deleted = %s WHERE id = %d RETURNING id" \
                % (deleted, self.page_id)
        return Database.get_result(query)

    def get_revisions(self):
        """
        Fetches all undeleted pages from the database if no page_id entered. If
        page_id arg given, returns all historical revisions of that page_id
        from the revisions table. Returns all rows.
        """
        query = ("SELECT id, page_id, title, content, last_modified,"
                 "modified_by FROM revisions WHERE page_id = %d ORDER BY"
                 " last_modified DESC" % self.page_id)
        result_set = Database.get_result(query)
        revisions = []
        for revision in result_set:
            revision_id = int(revision[0])
            revisions.append(Revision(revision_id))
        return revisions

    @staticmethod
    def get_pages():
        """
        Fetches all undeleted pages from the database if no page_id entered. If
        page_id arg given, returns all historical revisions of that page_id
        from the revisions table. Returns all rows.
        """
        query = ("SELECT id, title, content, last_modified, modified_by"
                 " FROM page WHERE deleted = FALSE ORDER BY title ASC")
        result_set = Database.get_result(query)
        pages = []
        for page in result_set:
            page_id = int(page[0])
            pages.append(Page(page_id))
        return pages

    @staticmethod
    def find_pages(search_string):
        """
        Searches db with wildcard search on title and content.
        """
        search_string = Database.escape(search_string)
        query = ("SELECT id FROM page WHERE title LIKE '%s' OR content"
                 " LIKE '%s'" % ('%' + search_string + '%', \
                 '%' + search_string + '%'))
        result_set = Database.get_result(query)
        pages = []
        for page in result_set:
            page_id = int(page[0])
            pages.append(Page(page_id))
        return pages

class Revision(object):
    """
    Subclass of Page. Over-rides some of the in-built functions to pull from
    the revisions table by ID instead of from the page table
    """
    def __init__(self, revision_id=0):
        if not isinstance(revision_id, int):
            revision_id = int(revision_id)
        query = ("SELECT id, page_id, title, content, last_modified,"
                 " modified_by, deleted FROM revisions WHERE id = %d" \
                 % revision_id)
        result_set = Database.get_result(query)
        if result_set:
            self.revision_id = revision_id
            self.page_id = result_set[0].page_id
            self.title = result_set[0].title
            self.content = result_set[0].content
            self.last_modified = result_set[0].last_modified
            self.modified_by = result_set[0].modified_by
            self.deleted = result_set[0].deleted
        else:
            self.revision_id = 0
            self.page_id = 0
            self.title = "not set"
            self.content = "not set"
            self.last_modified = "not set"
            self.modified_by = "not set"
            self.deleted = False

    def insert(self):
        """
        inserts each change to the page table as a new entry into the revisions
        table.
        """
        query = ("INSERT INTO revisions (page_id, title, content,"
                 " last_modified, modified_by, deleted) VALUES ("
                 " %d, '%s', '%s', '%s', '%s', %s) RETURNING id" % \
                 (self.page_id, self.title, self.content, \
                  self.last_modified, self.modified_by, \
                  self.deleted))
        result_list = Database.get_result(query)
        self.revision_id = result_list[0].id
        return self.revision_id

    def save(self):
        """
        Implemented for consistency with Page class methods. This method
        simply calls the insert() method for the Revision class.
        """
        self.insert()
        return self.revision_id

class Database(object):
    """
    Collection of static methods that setup our DB connection and create
    generalized methods for running queries / establish and release
    connections in mysql
    """
    @staticmethod
    def get_connection():
        """
        Sets up the postgreSQL connection. Uses settings from the config file.
        """
        return pg.DB(
            host=config.host,
            user=config.user_name,
            passwd=config.password,
            dbname=config.database
            )

    @staticmethod
    def escape(value):
        """
        Escapes apostrophes in SQL
        """
        return value.replace("'", "''")

    @staticmethod
    def get_result(query):
        """
        Opens a connection to the db, executes a query, fetches results, and
        then closes the connection.
        Args: query to execute, get_one (false by default, default is fetchall)
        Returns: the fetchOne or fetchAll of the query
        """
        conx = Database.get_connection()
        query = conx.query(query)
        result_list = query.namedresult()
        return result_list

    # @staticmethod
    # def do_query(query):
    #     """
    #     Takes care of opening and then closing our database connections. Also
    #     executes our SQL and auto-commits queries. Takes SQL query as arg and
    #     returns the lastrowid in case we need to insert it as foreign key
    #     elsewhere.
    #     """
    #     conx = Database.get_connection()
    #     cur = conx.cursor()
    #     cur.execute(query)
    #     conx.commit()
    #     last_id = cur.lastrowid
    #     cur.close()
    #     conx.close()
    #     return last_id
