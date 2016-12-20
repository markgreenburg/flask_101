"""
CRUD models for our wiki app
"""
import mysql.connector
import config
import time

class Page(object):
    """
    Object map for pages in the database
    """
    def __init__(self, page_id=0):
        if not isinstance(page_id, int):
            page_id = int(page_id)
        query = ("SELECT page_id, title, content, last_modified, modified_by"
                 " FROM page WHERE page_id = %d" % page_id)
        # Query our db to see if this page ID exists
        result_set = Database.get_result(query, True)
        # If page exists, set Page attributes to what's in the db
        if result_set:
            self.page_id = page_id
            self.title = result_set[1]
            self.content = result_set[2]
            self.last_modified = result_set[3]
            self.modified_by = result_set[4]
        else:
            self.page_id = 0
            self.title = "Not Set"
            self.content = "Not Set"
            self.last_modified = "Not Set"
            self.modified_by = "Not Set"
        return

    def insert(self):
        """
        Inserts new page into wiki. Should not be called directly - instead,
        use the Page.save() method.
        """
        query = ("INSERT INTO page (title, content, last_modified,"
                 " modified_by) VALUES (\"%s\", \"%s\", \"%s\", \"%s\")" % \
                 (Database.escape(self.title), \
                  Database.escape(self.content),\
                  time.time(), \
                  Database.escape(self.modified_by)))
        return Database.do_query(query)

    def update(self):
        """
        Updates page in wiki. Should not be called directly - instead, use the
        Page.save() method.
        """
        query = ("UPDATE page set title = '%s', content = '%s', last_modified"
                 " = '%s', modified_by = '%s' WHERE page_id = %d" % \
                (Database.escape(self.title),\
                 Database.escape(self.content),\
                 time.time(),\
                 Database.escape(self.modified_by),\
                 self.page_id))
        return Database.do_query(query)

    def save(self):
        """
        Saves action to database by calling insert() or update() methods. If
        page already exists, will call update(), else will call insert().
        Returns the respective method calls.
        """
        if self.page_id:
            return self.update()
        else:
            return self.insert()

    def set_delete(self, deleted=1):
        """
        Sets a page's 'deleted' attribute to 1 by default (so it won't show in
        index) or 0 if passed in as an arg. Setting to 0 restores the page in
        the index.
        """
        query = "UPDATE page SET deleted = %d WHERE page_id = %d" \
                % (deleted, self.page_id)
        return Database.do_query(query)

    @staticmethod
    def get_pages():
        """
        Fetches all undeleted pages from the database. Returns all rows.
        """
        query = ("SELECT page_id, title, content, last_modified, modified_by FROM"
                 " page WHERE deleted = 0")
        result_set = Database.get_result(query)
        pages = []
        for page in result_set:
            page_id = int(page[0])
            pages.append(Page(page_id))
        return pages

class Database(object):
    """
    Collection of static methods that setup our DB connection and create
    generalized methods for running queries / establish and release
    connections in mysql
    """
    @staticmethod
    def get_connection():
        """
        Sets up the mysql connection. Uses settings from the config file.
        """
        return mysql.connector.connect(
            user=config.user_name,
            password=config.password,
            host=config.host,
            database=config.database
        )

    @staticmethod
    def escape(value):
        """
        Escapes apostrophes in SQL
        """
        return value.replace("'", "''")

    @staticmethod
    def get_result(query, get_one=False):
        """
        Opens a connection to the db, executes a query, fetches results, and
        then closes the connection.
        Args: query to execute, get_one (false by default, default is fetchall)
        Returns: the fetchOne or fetchAll of the query
        """
        conx = Database.get_connection()
        cur = conx.cursor()
        cur.execute(query)
        if get_one:
            result_set = cur.fetchone()
        else:
            result_set = cur.fetchall()
        cur.close()
        conx.close()
        return result_set

    @staticmethod
    def do_query(query):
        """
        Takes care of opening and then closing our database connections. Also
        executes our SQL and auto-commits queries. Takes SQL query as arg and
        returns the lastrowid in case we need to insert it as foreign key
        elsewhere.
        """
        conx = Database.get_connection()
        cur = conx.cursor()
        cur.execute(query)
        conx.commit()
        last_id = cur.lastrowid
        cur.close()
        conx.close()
        return last_id
